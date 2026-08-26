# YouTube Assistant API

An AI-powered REST API built with **FastAPI**, **LangChain**, and **Google Gemini** for understanding YouTube videos through their transcripts.

## Features

- 🎥 Extract YouTube transcripts in English/Hindi
- 📝 Generate concise video summaries
- 🧠 Ask questions about video content
- 💬 Session-based conversational memory
- 📋 Generate multiple-choice quizzes
- ❤️ Health-check endpoint
- 🐳 Docker-ready deployment
- 📚 Automatic interactive API documentation through FastAPI

## Architecture

```text
YouTube URL
    ↓
YouTube Transcript Loader
    ↓
LangChain
    ↓
Google Gemini
    ├── Summarization
    ├── Quiz Generation
    └── Conversational Q&A
    ↓
FastAPI JSON Response
```

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | REST API framework |
| LangChain | LLM orchestration |
| Google Gemini | Generative AI model |
| YouTube Transcript API | Transcript extraction |
| Pydantic | Request/response validation |
| Uvicorn | ASGI server |
| Docker | Containerized deployment |

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/UjjwalS2/YouTube_Assistant_API.git
cd YouTube_Assistant_API
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env` and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_api_key
```

### 5. Start the API

```bash
uvicorn app:app --reload
```

Open the interactive Swagger documentation at:

`http://127.0.0.1:8000/docs`

## API Endpoints

### `GET /`
Returns a welcome message.

### `GET /health`
Returns API status and application version.

### `POST /summarizer`

Request:

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### `POST /quiz`

Request:

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "no_of_questions": 5
}
```

### `POST /chat`

Request:

```json
{
  "session_id": "user-123",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "query": "What is this video about?"
}
```

### `POST /chat/reset`

Reset a conversation session:

```text
POST /chat/reset?session_id=user-123
```

## Docker

Build:

```bash
docker build -t youtube-assistant-api .
```

Run:

```bash
docker run --env-file .env -p 8000:8000 youtube-assistant-api
```

## Project Structure

```text
YouTube_Assistant_API/
├── app.py
├── chat_models/
│   ├── __init__.py
│   └── models.py
├── config/
│   ├── __init__.py
│   └── constants.py
├── doc_loader/
│   ├── __init__.py
│   └── transcript_loader.py
├── prompts/
│   ├── __init__.py
│   └── prompt_templates.py
├── schema/
│   ├── __init__.py
│   ├── output_schema.py
│   └── user_input.py
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Notes

The current chat memory is process-local and keyed by `session_id`. For production-scale deployments, replace it with a shared persistent store such as Redis or a database.

## Author

**Ujjwal Sinha**

GitHub: https://github.com/UjjwalS2
