"""
document_service.py

Central document ingestion service.

Responsibilities:
- Validate supported file types
- Select the appropriate parser
- Return a standardized Document object
"""

from pathlib import Path
from typing import Dict

from indexing.parsers.pdf_parser import PDFParser
from indexing.parsers.docx_parser import DOCXParser
from indexing.parsers.txt_parser import TXTParser
from indexing.parsers.json_parser import JSONParser
from models.document_model import Document


class DocumentService:
    """
    Handles document ingestion using a parser registry.
    """

    def __init__(self) -> None:

        self.parsers: Dict[str, object] = {
            ".pdf": PDFParser(),
            ".docx": DOCXParser(),
            ".txt": TXTParser(),
            ".json": JSONParser(),
        }

    def supported_extensions(self) -> list[str]:
        """
        Returns all supported file extensions.
        """

        return list(self.parsers.keys())

    def is_supported(self, file_path: str) -> bool:
        """
        Check whether the file extension is supported.
        """

        suffix = Path(file_path).suffix.lower()

        return suffix in self.parsers

    def get_parser(self, file_path: str):
        """
        Returns the parser responsible for the given file.
        """

        suffix = Path(file_path).suffix.lower()

        if suffix not in self.parsers:

            raise ValueError(
                f"Unsupported file type '{suffix}'. "
                f"Supported formats: {', '.join(self.supported_extensions())}"
            )

        return self.parsers[suffix]

    def load_document(self, file_path: str) -> Document:
        """
        Loads and parses a document.

        Parameters
        ----------
        file_path : str

        Returns
        -------
        Document
        """

        parser = self.get_parser(file_path)

        document = parser.parse(file_path)

        if document.is_empty():

            raise ValueError(
                f"{document.filename} contains no readable text."
            )

        return document

    def load_documents(self, directory: str) -> list[Document]:
        """
        Loads every supported document inside a directory.
        """

        documents = []

        directory = Path(directory)

        if not directory.exists():

            raise FileNotFoundError(directory)

        for file in directory.iterdir():

            if file.is_file() and self.is_supported(str(file)):

                try:

                    document = self.load_document(str(file))

                    documents.append(document)

                except Exception as e:

                    print(f"Skipping {file.name}: {e}")

        return documents