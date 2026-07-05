"""
embedding_service.py

Enterprise Embedding Service

Responsibilities
----------------
- Load embedding model only once (Singleton)
- Generate embedding for one text
- Generate embeddings for multiple chunks
- Return normalized NumPy vectors
"""

from __future__ import annotations

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Wrapper around SentenceTransformer.

    The model is loaded only once and reused
    across the entire application.
    """

    _model = None

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5"
    ):

        if EmbeddingService._model is None:

            print(f"Loading embedding model: {model_name}")

            EmbeddingService._model = SentenceTransformer(
                model_name
            )

            print("Embedding model loaded successfully.")

        self.model = EmbeddingService._model

    ###########################################################

    def embed_text(
        self,
        text: str
    ) -> np.ndarray:
        """
        Generate embedding for a single text.
        """

        embedding = self.model.encode(

            text,

            normalize_embeddings=True,

            convert_to_numpy=True

        )

        return embedding

    ###########################################################

    def embed_documents(
        self,
        chunks: List[dict]
    ) -> np.ndarray:
        """
        Generate embeddings for all chunks.
        """

        texts = [

            chunk["content"]

            for chunk in chunks

        ]

        embeddings = self.model.encode(

            texts,

            batch_size=32,

            show_progress_bar=True,

            normalize_embeddings=True,

            convert_to_numpy=True

        )

        return embeddings

    ###########################################################

    def embedding_dimension(self) -> int:
        """
        Returns embedding dimension.
        """

        return self.model.get_embedding_dimension()

    ###########################################################

    def model_name(self) -> str:
        """
        Returns loaded model name.
        """

        return self.model._first_module().auto_model.name_or_path