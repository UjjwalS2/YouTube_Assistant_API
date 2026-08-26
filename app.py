import json
import re

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain.schema import AIMessage, HumanMessage
from dotenv import load_dotenv

from chat_models.models import Summarizer_model, quiz_model, chat_model
from config.constants import VERSION, MAX_HISTORY
from doc_loader.transcript_loader import transcript_loader
from prompts.prompt_templates import summarizer_template, quiz_template
from schema.user_input import SummarizerInput, QuizInput, ChatInput

load_dotenv()

app = FastAPI(title="YouTube Assistant API", version=VERSION)
session_store = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "YouTube Assistant API"}


@app.get("/health")
def health_check():
    return {"status": "OK", "version": VERSION}


@app.post("/summarizer")
async def transcript_summarizer(input_data: SummarizerInput):
    try:
        docs = transcript_loader(str(input_data.url))
        if not docs or not docs[0].page_content.strip():
            raise HTTPException(status_code=400, detail="Transcript is empty or could not be loaded.")

        chain = summarizer_template | Summarizer_model
        response = chain.invoke({"transcript": docs[0].page_content})
        return JSONResponse(
            status_code=201,
            content={"message": {"title": response.title, "summary": response.summary}},
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


@app.post("/quiz")
async def quiz_generator(input_data: QuizInput):
    try:
        docs = transcript_loader(str(input_data.url))
        if not docs or not docs[0].page_content.strip():
            raise HTTPException(status_code=400, detail="Transcript is empty or could not be loaded.")

        chain = quiz_template | quiz_model
        response = chain.invoke(
            {
                "transcript": docs[0].page_content,
                "number_of_questions": input_data.no_of_questions,
            }
        )
        raw_content = response.content
        match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", raw_content, re.DOTALL)
        if not match:
            raise HTTPException(status_code=500, detail="Could not extract valid JSON from model response.")

        try:
            questions_data = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=500, detail=f"Invalid JSON format: {exc}") from exc

        return JSONResponse(status_code=201, content={"questions": questions_data})
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


def get_session_memory(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = {"history": []}
    return session_store[session_id]


@app.post("/chat")
async def chat(input_data: ChatInput):
    try:
        docs = transcript_loader(str(input_data.url))
        if not docs or not docs[0].page_content.strip():
            raise HTTPException(status_code=400, detail="Transcript is empty or could not be loaded.")

        session = get_session_memory(input_data.session_id)
        session["history"].append(HumanMessage(content=input_data.query))

        if len(session["history"]) > MAX_HISTORY * 2:
            session["history"] = session["history"][-MAX_HISTORY * 2 :]

        conversation = "\n".join(
            f"Human: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}"
            for msg in session["history"]
        )
        context = f"Transcript:\n{docs[0].page_content}\n\nConversation:\n{conversation}"
        response = chat_model.invoke([HumanMessage(content=context)])
        session["history"].append(AIMessage(content=response.content))

        return JSONResponse(status_code=200, content={"response": response.content})
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


@app.post("/chat/reset")
async def reset_chat(session_id: str = Query(..., description="Session ID to reset")):
    session_store.pop(session_id, None)
    return {"message": "Session reset successfully."}
