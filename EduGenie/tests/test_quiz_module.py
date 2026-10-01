from quiz_module import clean_json_block
from schemas import QuizResponse


def test_clean_json_block():
    raw = '```json\n{"questions":[]}\n```'
    assert clean_json_block(raw) == '{"questions":[]}'


def test_quiz_schema():
    payload = {
        "questions": [{
            "question": "What is Python?",
            "options": ["A language", "A database", "An OS", "A browser"],
            "answer": "A language",
            "explanation": "Python is a programming language."
        }]
    }
    result = QuizResponse.model_validate(payload)
    assert len(result.questions) == 1
