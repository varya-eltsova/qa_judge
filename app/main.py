from __future__ import annotations
from fastapi import FastAPI
from dotenv import load_dotenv
from app.schemas import EvaluationRequest, EvaluationResult
from app.evaluator import run_evaluation
from app.database import init_db, save_result

load_dotenv()
init_db()

app = FastAPI(title="QA Judge Service")

@app.post("/evaluate", response_model=EvaluationResult)
def evaluate_endpoint(request: EvaluationRequest):
    result = run_evaluation(request)
    save_result(request, result)
    return result