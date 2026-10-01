from services.gemini_client import generate_text


def summarize_text(text: str, max_words: int = 120) -> str:
    prompt = f"""
Summarize the following educational text in no more than {max_words} words.

Keep:
- the main idea
- important facts
- key terms
- relationships between ideas

Write in simple English suitable for revision. Do not add facts that are not present.

Text:
{text}
"""
    return generate_text(prompt, temperature=0.2)
