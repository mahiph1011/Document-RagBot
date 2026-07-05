"""
vector_service.py

Enterprise FAISS Vector Service

Responsibilities
----------------
- Create FAISS index
- Store embeddings
- Store chunk metadata
- Search vectors
- Save index
- Load index
"""

from __future__ import annotations

import os
import pickle
from typing import List, Dict

import faiss
import numpy as np


class VectorService:

    def __init__(

        self,

        dimension: int,

        index_path: str = "data/vectorstore/faiss.index",

        metadata_path: str = "data/vectorstore/metadata.pkl"

    ):

        self.dimension = dimension

        self.index_path = index_path

        self.metadata_path = metadata_path

        os.makedirs(
            os.path.dirname(index_path),
            exist_ok=True
        )

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.metadata: List[Dict] = []

    ###########################################################

    def add_embeddings(

        self,

        embeddings: np.ndarray,

        chunks: List[Dict]

    ) -> None:

        """
        Add vectors and corresponding metadata.
        """

        embeddings = embeddings.astype("float32")

        self.index.add(embeddings)

        self.metadata.extend(chunks)

    ###########################################################

    def search(

        self,

        query_embedding: np.ndarray,

        top_k: int = 5

    ) -> List[Dict]:

        """
        Search nearest neighbours.
        """

        query_embedding = np.array(

            [query_embedding],

            dtype="float32"

        )

        scores, indices = self.index.search(

            query_embedding,

            top_k

        )

        results = []

        for score, idx in zip(

            scores[0],

            indices[0]

        ):

            if idx == -1:

                continue

            results.append({

                "score": float(score),

                "chunk": self.metadata[idx]

            })

        return results

    ###########################################################

    def save(self) -> None:
        """
        Persist FAISS index and metadata.
        """

        faiss.write_index(

            self.index,

            self.index_path

        )

        with open(

            self.metadata_path,

            "wb"

        ) as f:

            pickle.dump(

                self.metadata,

                f

            )

    ###########################################################

    def load(self) -> None:
        """
        Load existing index.
        """

        if os.path.exists(

            self.index_path

        ):

            self.index = faiss.read_index(

                self.index_path

            )

        if os.path.exists(

            self.metadata_path

        ):

            with open(

                self.metadata_path,

                "rb"

            ) as f:

                self.metadata = pickle.load(f)

    ###########################################################

    def total_documents(self) -> int:
        """
        Number of stored chunks.
        """

        return len(self.metadata)

    ###########################################################

    def clear(self) -> None:
        """
        Reset vector database.
        """

        self.index = faiss.IndexFlatIP(

            self.dimension

        )

        self.metadata = []