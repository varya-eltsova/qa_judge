# QA Judge Bot

Микросервис на FastAPI для оценки ответа бота, сравнивая вопрос клиента и ответ бота по нескольким критериям, и отдает оценку с вердиктом PASS или FAIL. 

Оценивает ответ бота LLM. Используется стандартный `openai` SDK, настроенный на `base_url`. Результат проверки сохраняется в SQLite. 

## Используемый стек

- Python
- FastAPI + Uvicorn - REST API и веб-сервер
- OpenAI Python SDK - интеграция с LLM (через OpenRouter)
- Pydantic - валидация запросов и ответов
- SQLAlchemy - ORM для работы с SQLite
- SQLite - локальная БД
- python-dotenv - управление конфигурацией

## Структура проекта

```text
qa_judge/
│
├── app/
│   ├── __init__.py
│   ├── main.py         
│   ├── evaluator.py   
│   ├── schemas.py     
│   └── database.py      
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Развернуть локально 


### Клонировать репозиторий

```
git clone <URL_этого_репозитория>
cd qa_judge
```

### Настроить  виртуальное окружение

```
python -m venv env
env\Scripts\Activate
```

### Установить зависимости

```
pip install -r requirements.txt
```

### Подготовить .env файл с ключом OpenRouter

Сервис обращается к LLM через OpenRouter (`base_url = https://openrouter.ai/api/v1`),
поэтому нужен ключ именно с [openrouter.ai/keys](https://openrouter.ai/keys), а не с platform.openai.com.

Скопируйте `.env.example` в `.env` и впишите свой ключ:

```
cp .env.example .env
```

```
OPENAI_API_KEY=ваш_ключ_openrouter
```


### Запустить сервер

```
uvicorn app.main:app --reload
```

После запуска (Swagger UI) будет  доступна по адресу: http://127.0.0.1:8000/docs


##  Пример использования

````
POST /evaluate

Отправить запрос можно через встроенный Swagger UI (`http://127.0.0.1:8000/docs`), Postman или прямо из терминала с помощью утилиты `curl`:

**Пример запроса (cURL):**
```
curl -X 'POST' \
  '[http://127.0.0.1:8000/evaluate](http://127.0.0.1:8000/evaluate)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_query": "Как восстановить пароль?",
  "bot_response": "Нажмите кнопку «Забыли пароль» на экране входа.",
  "reference_context": "Восстановление пароля происходит через форму авторизации."
}'
````
**Успешный ответ (HTTP 200 OK):**

```
{
  "accuracy_score": 5,
  "tone_score": 5,
  "errors": [],
  "verdict": "PASS",
  "average_score": 5.0
}
```
