from services.gemini_client import generate_text


def answer_question(question: str, context: str | None = None) -> str:
    context_block = (
        f"\nUse the following learner-provided context when relevant:\n{context}\n"
        if context
        else ""
    )
    prompt = f"""
Answer this educational question:

{question}
{context_block}

Give the direct answer first, then a short explanation.
If the question is ambiguous, state the assumption you are making.
If the learner's provided context conflicts with established facts, point that out politely.
"""
    return generate_text(prompt, temperature=0.2)
