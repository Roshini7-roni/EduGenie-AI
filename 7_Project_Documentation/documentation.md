\# 7. Project Documentation



\## Project Title



EduGenie – AI-Powered Personalized Learning Assistant



\## Project Overview



EduGenie is an AI-powered educational assistant designed to help learners understand educational topics and study more effectively.



The application provides multiple learning-support features through a web-based interface.



\## Features



\### 1. AI Explanation



The application provides explanations for educational topics based on the learner's requested level.



\### 2. Question and Answer



Learners can ask questions and receive AI-generated answers related to the requested topic.



\### 3. Summarization



The system can summarize longer educational content into a shorter form while retaining important information.



\### 4. Quiz Generation



The application can generate quiz questions to help learners test their understanding.



\### 5. Personalized Learning Path



The system can generate a structured learning path for a selected topic.



\## Learning Levels



EduGenie supports different explanation levels, including:



\- School

\- College

\- Advanced



This allows the explanation to be adapted to the learner's expected level of understanding.



\## Project Structure



The main application is contained in the `EduGenie` directory.



Important files include:



\- `main.py`

\- `config.py`

\- `explanation\_module.py`

\- `qna.py`

\- `summary\_module.py`

\- `quiz\_module.py`

\- `learning\_path.py`



The project also contains:



\- Frontend files

\- Gemini API integration

\- Test files

\- Configuration files



\## AI Integration



EduGenie uses the Google Gemini API to generate educational responses.



The Gemini API key is stored in the local `.env` file.



The `.env` file is excluded from version control using `.gitignore`.



\## Running the Application



Activate the virtual environment and start the FastAPI server.



```text

python -m uvicorn main:app --reload

