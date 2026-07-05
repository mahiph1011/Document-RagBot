"""
indexer.py

Enterprise Document Indexer

Responsibilities
----------------
- Parse document
- Chunk document
- Generate embeddings
- Store vectors
- Persist FAISS index

This class orchestrates the entire indexing pipeline.
"""

from __future__ import annotations

from typing import Dict

from services.document_service import DocumentService
from services.embedding_service import EmbeddingService
from services.vector_service import VectorService
from indexing.chunker import Chunker


class Indexer:
    """
    Enterprise indexing pipeline.

    Pipeline

    Document
        ↓
    Parser
        ↓
    Chunker
        ↓
    Embeddings
        ↓
    FAISS
    """

    def __init__(self):

        self.document_service = DocumentService()

        self.chunker = Chunker()

        self.embedding_service = EmbeddingService()

        self.vector_service = VectorService(
            self.embedding_service.embedding_dimension()
        )

        # Load existing vector database if available
        self.vector_service.load()

    ###########################################################

    def index_document(
        self,
        file_path: str
    ) -> Dict:
        """
        Index a single document.

        Returns indexing statistics.
        """

        # Parse document
        document = self.document_service.load_document(
            file_path
        )

        # Chunk document
        chunks = self.chunker.split(
            document
        )

        # Generate embeddings
        embeddings = self.embedding_service.embed_documents(
            chunks
        )

        # Store vectors
        self.vector_service.add_embeddings(
            embeddings,
            chunks
        )

        # Persist FAISS
        self.vector_service.save()

        return {

            "status": "success",

            "document": document.filename,

            "chunks_created": len(chunks),

            "total_chunks": self.vector_service.total_documents()

        }

    ###########################################################

    def search(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Search indexed documents.
        """

        embedding = self.embedding_service.embed_text(
            query
        )

        return self.vector_service.search(
            embedding,
            top_k
        ) 