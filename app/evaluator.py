from __future__ import annotations
import os
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas import EvaluationRequest, EvaluationResult

load_dotenv()

SYSTEM_PROMPT = """
Ты — старший QA-инспектор службы поддержки.
Твоя задача — проверить соответствие ответа бота вопросу клиента.
Если ответ содержит фактические ошибки, неполную информацию или грубость — ставь вердикт FAIL.
"""

def run_evaluation(data: EvaluationRequest) -> EvaluationResult:
    # Инициализация клиента внутри функции защищает сервер от падения при старте
    api_key = os.getenv("OPENAI_API_KEY") or "dummy-key-placeholder"
    client = OpenAI(api_key=api_key)

    content = f"Вопрос клиента:\n{data.user_query}\n\nОтвет бота:\n{data.bot_response}"
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
        ],
        response_format=EvaluationResult
    )
    return response.choices[0].message.parsed