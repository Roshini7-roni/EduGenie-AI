from functools import lru_cache

from fastapi import HTTPException

from config import settings


@lru_cache(maxsize=1)
def get_client():
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured.",
        )

    try:
        from google import genai
        return genai.Client(api_key=settings.gemini_api_key)
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="google-genai is not installed.",
        ) from exc


def demo_response(prompt: str, response_mime_type=None) -> str:
    """Offline responses for demo mode."""

    p = prompt.lower()

    # Quiz
    if response_mime_type == "application/json" or "multiple-choice questions" in p:
        return """
{
  "questions": [
    {
      "question": "What is the main purpose of an operating system?",
      "options": [
        "To manage computer hardware and software",
        "To create only websites",
        "To replace the CPU",
        "To increase internet speed"
      ],
      "answer": "To manage computer hardware and software",
      "explanation": "An operating system manages hardware resources and provides services for applications."
    },
    {
      "question": "Which component performs most calculations in a computer?",
      "options": [
        "CPU",
        "Keyboard",
        "Monitor",
        "Printer"
      ],
      "answer": "CPU",
      "explanation": "The CPU executes instructions and performs calculations required by programs."
    },
    {
      "question": "What does RAM provide to a computer?",
      "options": [
        "Temporary working memory",
        "Permanent file storage",
        "Internet connection",
        "Power supply"
      ],
      "answer": "Temporary working memory",
      "explanation": "RAM temporarily stores data and instructions that the CPU is actively using."
    }
  ]
}
""".strip()

    # Learning path
    if "learning path" in p or "personalized learning path" in p:
        return """
1. Goal
Build a strong understanding of the topic from fundamentals to practical application.

2. Prerequisites
Basic computer knowledge and familiarity with the main terminology.

3. Learning Plan

Week 1 — Fundamentals
- Learn the basic concepts and terminology.
- Practice with simple examples.
- Checkpoint: explain the main concepts in your own words.

Week 2 — Core Concepts
- Study how the major components work together.
- Complete small exercises.
- Checkpoint: solve beginner-level problems independently.

Week 3 — Practical Application
- Build a small practical example.
- Review mistakes and improve the solution.
- Checkpoint: complete a small project.

Week 4 — Review and Project
- Review important concepts.
- Complete a final mini-project.
- Checkpoint: explain your project and the concepts behind it.

4. Recommended Resource Types
Videos, official documentation, textbooks, coding exercises, and practice projects.

5. Final Project
Create a small application that demonstrates the concepts learned.

6. Next Steps
Continue with more advanced projects and real-world practice.
""".strip()

    # Explanation — School
    if "explain the topic" in p and "school" in p:
        return """
1. Simple definition

An operating system (OS) is the main software that helps a computer work.

2. How it works

It helps the computer control things like the keyboard, mouse, screen, memory, and files.

3. Three important points

- It manages computer hardware.
- It helps programs run.
- It helps users interact with the computer.

4. Easy example

Windows is an operating system used on many computers.

5. One-line recap

An operating system helps the computer and its programs work together.
""".strip()

    # Explanation — College
    if "explain the topic" in p and "college" in p:
        return """
1. Simple definition

An operating system (OS) is system software that manages computer hardware and provides services for application programs.

2. How it works

The OS manages CPU scheduling, memory, storage, files, input/output devices, and processes.

3. Three important points

- Process and CPU management
- Memory and storage management
- File and device management

4. Academic example

Linux provides process management, virtual memory, file systems, device drivers, and system calls that allow applications to interact with hardware.

5. One-line recap

An operating system acts as an interface between applications, users, and computer hardware.
""".strip()

    # Explanation — Advanced
    if "explain the topic" in p and "advanced" in p:
        return """
1. Simple definition

An operating system is a resource-management and abstraction layer that coordinates hardware execution and provides controlled services to user-space programs.

2. How it works

The OS manages processes and threads through scheduling, isolates address spaces using virtual memory, controls I/O through device drivers, and provides persistent storage through file-system abstractions.

3. Three important points

- CPU scheduling and concurrency control
- Virtual memory, protection, and address-space isolation
- System calls, I/O subsystems, and file-system management

4. Technical example

When an application requests a file read, it can issue a system call. The kernel validates the request and coordinates the I/O operation.

5. One-line recap

An operating system provides protected abstractions over hardware while managing computation, memory, I/O, and persistent resources.
""".strip()

    # Explanation — Beginner
    if "explain the topic" in p:
        return """
1. Simple definition

An operating system (OS) is the main software that manages a computer and helps other programs run.

2. How it works

It manages the CPU, memory, files, storage, and connected devices.

3. Three important points

- Manages hardware
- Runs applications
- Manages files and memory

4. Example

Windows, Linux, macOS, Android, and iOS are operating systems.

5. One-line recap

An operating system helps hardware, software, and users work together.
""".strip()

    # Summary
    if "summarize" in p:
        return """
An operating system is essential software that manages computer hardware and software resources. It controls components such as the CPU, memory, storage, and input/output devices. It also provides services that allow applications to run and users to interact with the computer. Common examples include Windows, macOS, Linux, Android, and iOS.
""".strip()

    # General question
    return """
An operating system (OS) is system software that manages a computer's hardware and software resources.

It acts as a bridge between the user, applications, and hardware. It manages resources such as the CPU, memory, storage, and connected devices.

Examples include Windows, macOS, Linux, Android, and iOS.

In simple terms: the operating system helps the computer's hardware and software work together.
""".strip()


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4,
    response_schema=None,
    response_mime_type: str | None = None,
) -> str:

    # Demo mode does not call Gemini.
    if settings.demo_mode:
        return demo_response(prompt, response_mime_type)

    client = get_client()

    config = {
        "temperature": temperature,
        "system_instruction": (
            "You are EduGenie, a helpful educational assistant. "
            "Be accurate, clear, age-appropriate, and concise. "
            "Teach rather than overwhelm. Do not invent citations or sources."
        ),
    }

    if response_schema is not None:
        config["response_schema"] = response_schema

    if response_mime_type:
        config["response_mime_type"] = response_mime_type

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=config,
        )

        text = getattr(response, "text", None)

        if not text:
            raise ValueError("Gemini returned an empty response.")

        return text.strip()

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                f"Gemini request failed: {type(exc).__name__}. "
                "Check your API key, model, and quota."
            ),
        ) from exc