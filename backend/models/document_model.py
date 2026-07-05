"""
document_model.py

Defines the common document model used throughout the RAG pipeline.

Every parser (PDF, DOCX, TXT, JSON) returns this object so that the
rest of the pipeline remains independent of file format.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    """
    Represents a parsed document.
    """

    filename: str = Field(..., description="Original filename")

    extension: str = Field(..., description="File extension")

    content: str = Field(..., description="Extracted text")

    source_path: str = Field(..., description="Absolute file path")

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    language: Optional[str] = Field(
        default="en",
        description="Detected language"
    )

    def word_count(self) -> int:
        """
        Returns number of words.
        """

        return len(self.content.split())

    def character_count(self) -> int:
        """
        Returns total characters.
        """

        return len(self.content)

    def is_empty(self) -> bool:
        """
        Checks whether document has usable text.
        """

        return len(self.content.strip()) == 0

    def summary(self) -> dict:
        """
        Lightweight metadata summary.
        """

        return {
            "filename": self.filename,
            "extension": self.extension,
            "words": self.word_count(),
            "characters": self.character_count(),
            "language": self.language,
        }