from pydantic import BaseModel, Field, field_validator, property, computed_field

class EvalutionRequest(BaseModel):
    user_query: str
    bot_response: str
    reference_context: str = Field(default = None)

class EvalutionResult(BaseModel):
    accuracy_score: int = Field(ge = 1, le = 5, description = 'Оценка точности ответа бота от 1 до 5')
    tone_score: int = Field(ge = 1, le = 5, description = 'Оценка следлванию Tone of Voice ботом от 1 до 5')
    errors: list[str] = Field(default = [])
    verdict: str = "PASS" or "FAIL"
    average_score = float

    @field_validator("verdict")
    def check_verdict(cls, value):
        value = value.replace(' ','').upper()
        if value != "PASS" and value != "FAIL":
            raise ValueError
        return value

    @property
    @computed_field
    def average(self)  -> float:
        return (self.accuracy_score + self.tone_score)/2
