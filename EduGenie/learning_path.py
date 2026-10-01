from services.gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    timeline: str = "4 weeks",
) -> str:
    prompt = f"""
Create a personalized learning path for "{topic}".

Learner level: {level}
Available timeline: {timeline}

Organize the response as:
1. Goal
2. Prerequisites
3. Week-by-week or stage-by-stage plan from beginner to advanced
4. For each stage: concepts to learn, a small practice activity, and a checkpoint
5. Recommended resource types (videos, official documentation, books, practice sites)
6. Final project idea
7. Next steps after completing the plan

Keep the plan realistic and concise. Do not invent specific URLs.
"""
    return generate_text(prompt, temperature=0.45)
