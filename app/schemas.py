from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator, computed_field

class EvaluationRequest(BaseModel):
    user_query: str
    bot_response: str
    reference_context: Optional[str] = Field(default=None)

class EvaluationResult(BaseModel):
    accuracy_score: int = Field(ge = 1, le = 5, description = 'Оценка точности ответа бота от 1 до 5')
    tone_score: int = Field(ge = 1, le = 5, description = 'Оценка следлванию Tone of Voice ботом от 1 до 5')
    errors: list[str] = Field(default = [])
    verdict: Literal["PASS", "FAIL"] = "PASS"
    average_score: float

    @field_validator("verdict", mode="before")
    @classmethod
    def check_verdict(cls, value):
        value = value.replace(' ', '').upper()
        if value != "PASS" and value != "FAIL":
            raise ValueError(f'verdict должен быть "PASS" или "FAIL", получено: {value!r}')
        return value

    @computed_field
    @property
    def average(self) -> float:
        return (self.accuracy_score + self.tone_score) / 2
