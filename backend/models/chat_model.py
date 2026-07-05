"""
chat_model.py

Pydantic models for Chat API.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question"
    )


class SourceResponse(BaseModel):
    document: str
    section: str
    similarity: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]