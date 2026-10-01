from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from schemas import (
    ExplainRequest, LearnRequest, QARequest, QuizRequest, SummaryRequest
)
from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="Educational assistant for Q&A, explanations, quizzes, summaries and learning paths.",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name, "model": settings.gemini_model},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
        "explanation_provider": settings.explanation_provider,
    }


@app.post("/qa")
async def qa(payload: QARequest):
    return {"answer": answer_question(payload.question, payload.context)}


@app.post("/explain")
async def explain(payload: ExplainRequest):
    return {"explanation": explain_topic(payload.topic, payload.level)}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    return {"quiz": generate_quiz(payload.text, payload.count)}


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    return {"summary": summarize_text(payload.text, payload.max_words)}


@app.post("/learn/recommendations")
async def learn(payload: LearnRequest):
    return {
        "learning_path": get_learning_recommendations(
            payload.topic, payload.level, payload.timeline
        )
    }
