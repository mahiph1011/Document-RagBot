"""
rag_service.py

Enterprise RAG Service

Responsibilities
----------------
1. Embed user query
2. Search FAISS vector database
3. Build retrieval context
4. Load system prompt
5. Generate answer using Gemini
6. Return answer with sources
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from google import genai

from services.embedding_service import EmbeddingService
from services.vector_service import VectorService
from utils.config import settings


class RAGService:
    """
    Enterprise Retrieval Augmented Generation Service.
    """

    ############################################################

    def __init__(self):

        # Gemini Client
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_name = settings.GEMINI_MODEL

        # Embedding Service
        self.embedding_service = EmbeddingService()

        # Vector Database
        self.vector_service = VectorService(
            self.embedding_service.embedding_dimension()
        )

        self.vector_service.load()

        # Prompt file
        self.prompt_path = Path(
            "prompts/system_prompt.txt"
        )

    ############################################################

    def load_system_prompt(self) -> str:
        """
        Load system prompt from prompts folder.
        """

        if not self.prompt_path.exists():

            raise FileNotFoundError(
                "prompts/system_prompt.txt not found."
            )

        with open(
            self.prompt_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    ############################################################

    def retrieve_documents(
        self,
        question: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve top matching chunks from FAISS.
        """

        query_embedding = self.embedding_service.embed_text(
            question
        )

        results = self.vector_service.search(
            query_embedding,
            top_k
        )

        return results

    ############################################################

    def build_context(
        self,
        retrieved_chunks: List[Dict]
    ) -> str:
        """
        Convert retrieved chunks into structured context
        for Gemini.
        """

        context = []

        for index, item in enumerate(
            retrieved_chunks,
            start=1
        ):

            chunk = item["chunk"]

            context.append(

f"""
=========================
SOURCE {index}
=========================

Document:
{chunk["document_name"]}

Section:
{chunk.get("section", "General")}

Similarity:
{round(item["score"],3)}

Content:

{chunk["content"]}

"""
            )

        return "\n".join(context)
    

    ############################################################

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:
        """
        Generate answer using Gemini.
        """

        system_prompt = self.load_system_prompt()

        final_prompt = f"""
{system_prompt}

=========================================================
CONTEXT
=========================================================

{context}

=========================================================
QUESTION
=========================================================

{question}

=========================================================
IMPORTANT
=========================================================

Answer ONLY from the context above.

If the answer is not available in the context,
say:

"I could not find this information in the uploaded documents."

Do not hallucinate.
Do not make assumptions.
Keep the answer concise and professional.
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=final_prompt
        )

        return response.text

    ############################################################

    def ask(
        self,
        question: str,
        top_k: int = 5
    ) -> Dict:
        """
        Complete RAG pipeline.

        Question
            ↓
        Query Embedding
            ↓
        FAISS Search
            ↓
        Build Context
            ↓
        Gemini
            ↓
        Final Response
        """

        retrieved_chunks = self.retrieve_documents(
            question,
            top_k
        )

        if len(retrieved_chunks) == 0:

            return {

                "question": question,

                "answer":
                "I could not find any relevant information in the uploaded documents.",

                "sources": []

            }

        context = self.build_context(
            retrieved_chunks
        )

        answer = self.generate_answer(
            question,
            context
        )

        sources = []

        for item in retrieved_chunks:

            chunk = item["chunk"]

            sources.append(

                {

                    "document":
                    chunk.get(
                        "document_name",
                        "Unknown Document"
                    ),

                    "section":
                    chunk.get(
                        "section",
                        "General"
                    ),

                    "similarity":
                    round(
                        item["score"],
                        3
                    )

                }

            )

        return {

            "question": question,

            "answer": answer,

            "sources": sources

        }
