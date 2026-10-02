\# 5. Project Development



\## Development Overview



EduGenie is developed as a modular AI-powered educational web application using Python and FastAPI.



The application separates its major educational functions into individual modules so that each feature can be developed and maintained independently.



\## Technology Stack



\### Backend



\- Python

\- FastAPI

\- Uvicorn



\### Frontend



\- HTML

\- CSS

\- JavaScript



\### Artificial Intelligence



\- Google Gemini API



\### Development Tools



\- Visual Studio Code

\- Git

\- GitHub



\## Main Application Components



\### main.py



The main application file initializes the FastAPI application and handles the application's routes and requests.



\### explanation\_module.py



This module handles AI-powered topic explanations.



The learner can provide a topic and receive an explanation appropriate to the requested learning level.



\### qna.py



This module handles question-and-answer functionality.



It accepts a learner's question and generates a relevant educational response.



\### summary\_module.py



This module provides text summarization functionality.



It converts longer educational content into a shorter summary while retaining the important information.



\### quiz\_module.py



This module generates quiz questions for learner self-assessment.



\### learning\_path.py



This module provides personalized learning recommendations and learning paths.



\### services/gemini\_client.py



This module handles communication with the Google Gemini API.



The API key is loaded through environment configuration rather than being stored directly in the source code.



\## Frontend Development



The frontend is implemented using:



\- HTML for page structure

\- CSS for styling

\- JavaScript for interaction with the backend



The frontend communicates with the FastAPI backend and displays the generated educational results.



\## Environment Configuration



Sensitive configuration values such as the Gemini API key are stored in a local `.env` file.



The `.env` file is excluded from Git using `.gitignore`.



An `.env.example` file is provided as a template without exposing the actual API key.



\## Running the Application



The application can be started using:



```text

python -m uvicorn main:app --reload

