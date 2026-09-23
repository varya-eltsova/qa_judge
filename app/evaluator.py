from __future__ import annotations
import os
import json
import re
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from app.schemas import EvaluationRequest, EvaluationResult

load_dotenv(find_dotenv())

SYSTEM_PROMPT = """
Ты — оценщик QA ответов бота.
Проверь соответствие ответа бота вопросу клиента.
Если передан эталонный контекст — сверяй ответ бота с ним и учитывай это при оценке accuracy_score.

Верни ответ СТРОГО в формате JSON без markdown-разметки (без ```json) со следующей структурой:
{
  "accuracy_score": 5,
  "tone_score": 5,
  "errors": [],
  "verdict": "PASS",
  "average_score": 5.0
}

Правила:
- accuracy_score: целое число от 1 до 5
- tone_score: целое число от 1 до 5
- errors: массив строк с описанием ошибок (например, [])
- verdict: строка "PASS" или "FAIL"
- average_score: дробное число (float)
"""

def run_evaluation(data: EvaluationRequest) -> EvaluationResult:
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return EvaluationResult(
            accuracy_score=1,
            tone_score=1,
            errors=["API key missing: Переменная OPENAI_API_KEY не найдена в .env"],
            verdict="FAIL",
            average_score=1.0
        )

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        content = f"Вопрос клиента:\n{data.user_query}\n\nОтвет бота:\n{data.bot_response}"
        if data.reference_context:
            content += f"\n\nБаза знаний для проверки:\n{data.reference_context}"
        
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ],
            temperature=0.1,
            timeout=30.0 
        )
        
        raw_text = response.choices[0].message.content.strip()

        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            raw_text = match.group(0)
            
        parsed_json = json.loads(raw_text)
        return EvaluationResult(**parsed_json)

    except Exception as e:

        return EvaluationResult(
            accuracy_score=1,
            tone_score=1,
            errors=[f"Ошибка исполнения: {str(e)}"],
            verdict="FAIL",
            average_score=1.0
        )