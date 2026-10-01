from pydantic import BaseModel, Field, field_validator

from config import settings


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=settings.max_input_chars)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty.")
        return value


class QARequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=settings.max_input_chars)
    context: str | None = Field(default=None, max_length=settings.max_input_chars)

    @field_validator("question")
    @classmethod
    def clean_question(cls, value: str) -> str:
        return value.strip()


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=500)
    level: str = Field(default="beginner", max_length=50)

    @field_validator("topic", "level")
    @classmethod
    def clean_fields(cls, value: str) -> str:
        return value.strip()


class QuizRequest(TextRequest):
    count: int = Field(default=3, ge=1, le=10)


class SummaryRequest(TextRequest):
    max_words: int = Field(default=120, ge=30, le=500)


class LearnRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=300)
    level: str = Field(default="beginner", max_length=50)
    timeline: str = Field(default="4 weeks", max_length=100)

    @field_validator("topic", "level", "timeline")
    @classmethod
    def clean_fields(cls, value: str) -> str:
        return value.strip()


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
