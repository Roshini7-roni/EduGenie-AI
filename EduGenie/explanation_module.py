from config import settings
from services.gemini_client import generate_text


def _local_explanation(topic: str, level: str) -> str:
    try:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires the optional local-model dependencies. "
            "Run: pip install -r requirements-local.txt"
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(settings.local_explanation_model)
    model = AutoModelForSeq2SeqLM.from_pretrained(settings.local_explanation_model)
    generator = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    prompt = (
        f"Explain {topic} to a {level} learner in simple English. "
        "Use a short definition, 3 key points, and one basic example."
    )
    result = generator(prompt, max_new_tokens=220, do_sample=False)[0]["generated_text"]
    return result.strip()


def explain_topic(topic: str, level: str = "beginner") -> str:
    if settings.explanation_provider == "local":
        try:
            return _local_explanation(topic, level)
        except Exception:
            # Local inference is optional; fall back to Gemini so the web app remains usable.
            pass

    prompt = f"""
Explain the topic "{topic}" for a {level} learner.

Use this exact teaching structure:
1. Simple definition
2. How it works
3. Three important points
4. One easy real-world or academic example
5. One-line recap

Use simple English and avoid unnecessary jargon.
"""
    return generate_text(prompt, temperature=0.3)
