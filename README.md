# QA Judge

Инструмент для автоматической оценки качества ответов бота с использованием LLM от OpenAI. 

## Стек
* Python
* FastAPI
* Playwright
* Pydantic
* SQL

## Структура проекта
* `app` - исходный код:
  * `main.py` 
  * `evaluator.py` - логика оценки и взаимодействия с LLM
  * `schemas.py` - Pydantic-схемы запросов и ответов
  * `database.py` - настройка БД
* `qa_judge.py` - скрипт запуска