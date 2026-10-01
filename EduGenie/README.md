# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational web application based on the supplied project documentation. It provides:

- Question answering
- Simplified topic explanations
- MCQ quiz generation
- Educational text summarization
- Personalized learning paths

The backend uses FastAPI and the frontend uses plain HTML/CSS/JavaScript, matching the architecture described in the project document.

## Important model update

The original document names **Gemini 1.5 Pro**. Gemini model availability changes over time, so this implementation does not hard-code that retired/legacy choice. The model is configurable through `GEMINI_MODEL`; the default is a current Gemini Flash model shown in Google's documentation.

The project uses Google's current `google-genai` Python SDK and `client.models.generate_content(...)`.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── services/
│   ├── __init__.py
│   └── gemini_client.py
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
├── tests/
│   ├── test_api.py
│   └── test_quiz_module.py
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-local.txt
├── requirements-dev.txt
└── README.md
```

## 1. Prerequisites

Install:

- Python 3.10 or newer
- VS Code
- A Gemini API key

Python 3.12 is a good choice for this project.

## 2. Open the project in VS Code

Extract/open the `EduGenie` folder in VS Code.

Open the integrated terminal:

**Terminal → New Terminal**

Create a virtual environment:

### Windows

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

If `py` is unavailable:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Do not install the local model dependencies unless you actually want local LaMini inference.

Optional:

```bash
pip install -r requirements-local.txt
```

The local model can be several hundred MB and may take time to download the first time.

## 4. Configure the Gemini API key

Copy:

```text
.env.example
```

to:

```text
.env
```

Then put your key in:

```env
GEMINI_API_KEY=your_real_key_here
```

Keep `.env` private. It is already included in `.gitignore`.

Google's current Gemini documentation recommends the `GEMINI_API_KEY` environment variable and the `google-genai` SDK.

## 5. Choose the model

The default is:

```env
GEMINI_MODEL=gemini-3.8-flash
```

You can change it without changing Python files:

```env
GEMINI_MODEL=your_available_model_name
```

If your Google AI Studio account does not have access to the configured model, choose a model available to your account.

## 6. Run the application

From the project root:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI API documentation is also available at:

```text
http://127.0.0.1:8000/docs
```

## 7. Test the application

### Browser test

Try each task:

1. Ask a Question
   - `What is the largest ocean?`

2. Explain a Topic
   - `Pythagoras theorem`

3. Generate Quiz
   - Paste a short lesson about photosynthesis.
   - Choose 3 questions.
   - Answer the displayed MCQs.

4. Summarize Text
   - Paste a paragraph from your notes.

5. Learning Path
   - Enter `SQL`
   - Choose `college`
   - Choose `4 weeks`

### Health check

Open:

```text
http://127.0.0.1:8000/health
```

You should see JSON similar to:

```json
{
  "status": "ok",
  "app": "EduGenie",
  "gemini_configured": true,
  "model": "gemini-3.8-flash",
  "explanation_provider": "gemini"
}
```

## 8. Run automated tests

With the virtual environment activated:

```bash
pytest -q
```

These tests do not call Gemini. They test the application page, health endpoint, request validation, and quiz data validation.

## 9. API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is cloud computing?\"}"
```

### Explanation

```bash
curl -X POST http://127.0.0.1:8000/explain ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\":\"Pythagoras theorem\",\"level\":\"beginner\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Photosynthesis is the process by which green plants convert light energy into chemical energy.\",\"count\":3}"
```

For Linux/macOS, replace `^` with `\` for multiline curl commands.

## 10. Optional local explanation model

The project document specifies LaMini-Flan-T5-783M for concept explanation. This implementation supports that model through:

```env
EXPLANATION_PROVIDER=local
```

and:

```env
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

Install:

```bash
pip install -r requirements-local.txt
```

The first local request downloads the model. If local inference fails, EduGenie falls back to Gemini so the application remains usable.

## 11. Docker

Create `.env` first, then:

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000
```

Stop:

```bash
docker compose down
```

## 12. Troubleshooting

### "Gemini API key is not configured"

Check `.env`:

```env
GEMINI_API_KEY=...
```

Then stop and restart Uvicorn.

### 401/403 from Gemini

Check that the API key is correct and that the configured model is available to your account.

### Model not found

Change `GEMINI_MODEL` in `.env` to a currently available Gemini model.

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

### PowerShell blocks activation

Use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate
```

### Local LaMini model is slow

Use:

```env
EXPLANATION_PROVIDER=gemini
```

This keeps the explanation feature cloud-based and avoids downloading the local model.

## Architecture

```text
Browser
   |
   | POST JSON
   v
FastAPI (main.py)
   |
   +--> /qa ------------------> qna.py
   |
   +--> /explain --------------> explanation_module.py
   |                              |
   |                              +--> LaMini optional
   |                              +--> Gemini fallback
   |
   +--> /quiz -----------------> quiz_module.py
   |
   +--> /summarize ------------> summary_module.py
   |
   +--> /learn/recommendations -> learning_path.py
                                  |
                                  v
                           Gemini Client
                                  |
                                  v
                           Google Gemini API
```

## Security notes

- Never put the Gemini API key in HTML or JavaScript.
- Keep the key in `.env`.
- Do not commit `.env` to Git.
- For production, add authentication, rate limiting, logging, HTTPS, and stricter CORS settings.
- AI-generated educational answers should still be checked against reliable course material for high-stakes academic work.
