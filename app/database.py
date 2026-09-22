import sqlite3
import json
from app.schemas import EvaluationRequest, EvaluationResult

DB_FILE = "evaluations.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_query TEXT,
                bot_response TEXT,
                accuracy INTEGER,
                tone INTEGER,
                verdict TEXT,
                errors TEXT,
                recommendation TEXT
            )
        """)

def save_result(req: EvaluationRequest, res: EvaluationResult):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO logs (user_query, bot_response, accuracy, tone, verdict, errors, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            req.user_query, req.bot_response,
            res.accuracy_score, res.tone_score,
            res.verdict, json.dumps(res.errors, ensure_ascii=False),
            res.recommendation
        ))