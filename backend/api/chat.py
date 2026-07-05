"""
chat.py

Enterprise RAG Chat Endpoint
"""

from fastapi import APIRouter, HTTPException
from models.chat_model import (
    ChatRequest,
    ChatResponse,
    SourceResponse
)


from services.rag_service import RAGService


router = APIRouter(
    prefix="/api",
    tags=["Chat"]
)


# --------------------------------------------------------
# Request Model
# --------------------------------------------------------

# class ChatRequest(BaseModel):
#     question: str


# # --------------------------------------------------------
# # Response Model
# # --------------------------------------------------------

# class Source(BaseModel):
#     document: str
#     section: str
#     similarity: float


# class ChatResponse(BaseModel):
#     question: str
#     answer: str
#     sources: list[Source]


# --------------------------------------------------------
# Initialize RAG Service
# --------------------------------------------------------

rag_service = RAGService()


# --------------------------------------------------------
# Chat Endpoint
# --------------------------------------------------------

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Ask questions to the Enterprise RAG Chatbot"
)
async def chat(request: ChatRequest):

    try:

        response = rag_service.ask(
            request.question
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )