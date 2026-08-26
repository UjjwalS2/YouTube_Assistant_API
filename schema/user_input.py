from pydantic import BaseModel, Field, HttpUrl


class SummarizerInput(BaseModel):
    url: HttpUrl = Field(..., description="URL of the YouTube video to summarize")


class QuizInput(BaseModel):
    url: HttpUrl = Field(..., description="URL of the YouTube video")
    no_of_questions: int = Field(..., ge=1, le=50, description="Number of questions")


class ChatInput(BaseModel):
    url: HttpUrl = Field(..., description="URL of the YouTube video")
    query: str = Field(..., min_length=1, description="Question to ask")
    session_id: str = Field(..., min_length=1, description="Unique session ID")
