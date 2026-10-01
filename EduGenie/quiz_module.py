import json

from schemas import QuizResponse
from services.gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def _fallback_parse(text: str) -> QuizResponse:
    cleaned = clean_json_block(text)
    data = json.loads(cleaned)
    return QuizResponse.model_validate(data)


def generate_quiz(text: str, count: int = 3) -> dict:
    prompt = f"""
Create exactly {count} multiple-choice questions from the educational passage below.

Requirements:
- Each question must have exactly 4 options.
- The answer must exactly match one option.
- Include a short explanation for the correct answer.
- Avoid trick questions and duplicate questions.
- Return ONLY JSON matching this shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "answer": "one of the four options",
      "explanation": "short explanation"
    }}
  ]
}}

Passage:
{text}
"""

    try:
        raw = generate_text(
            prompt,
            temperature=0.35,
            response_schema=QuizResponse.model_json_schema(),
            response_mime_type="application/json",
        )
        quiz = _fallback_parse(raw)
    except Exception:
        # A second attempt without schema handling makes the module tolerant of
        # provider/model configuration differences.
        raw = generate_text(prompt, temperature=0.2)
        quiz = _fallback_parse(raw)

    if len(quiz.questions) != count:
        raise ValueError(f"Model returned {len(quiz.questions)} questions; expected {count}.")

    return quiz.model_dump()
