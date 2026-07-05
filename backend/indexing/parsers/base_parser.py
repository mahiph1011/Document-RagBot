"""
base_parser.py

Abstract base class for every parser.
"""

from abc import ABC, abstractmethod

from models.document_model import Document


class BaseParser(ABC):
    """
    Base parser interface.

    Every parser must implement parse().
    """

    @abstractmethod
    def parse(self, file_path: str) -> Document:
        """
        Parses a file and returns a Document object.
        """
        pass