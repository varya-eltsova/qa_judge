import json
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.schemas import EvaluationRequest, EvaluationResult
from app.evaluator import run_evaluation
from app.database import engine, Base, get_db, Log

Base.metadata.create_all(bind=engine)

app = FastAPI(title="QA Judge")

@app.post("/evaluate", response_model=EvaluationResult)
def evaluate_endpoint(
    request: EvaluationRequest, 
    db: Session = Depends(get_db)
):
    result = run_evaluation(request)
    
    try:
        db_log = Log(
            user_query=request.user_query,
            bot_response=request.bot_response,
            accuracy=result.accuracy_score,
            tone=result.tone_score,
            verdict=result.verdict,
            errors=json.dumps(result.errors, ensure_ascii=False),
            average_score=result.average_score
        )
        
        db.add(db_log)
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"Не удалось сохранить результат в БД: {e}")

    return result