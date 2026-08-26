from pydantic import BaseModel, Field


class SummarizerOutput(BaseModel):
    title: str = Field(description="Title of the video")
    summary: str = Field(description="Summary of the video")


class QuizOutput(BaseModel):
    difficulty: str = Field(description="Difficulty of the question")
    question: str = Field(description="Question in detail")
    option1: str = Field(description="First option")
    option2: str = Field(description="Second option")
    option3: str = Field(description="Third option")
    option4: str = Field(description="Fourth option")
    answer: str = Field(description="Correct answer")
