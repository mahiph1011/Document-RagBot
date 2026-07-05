"""
pdf_parser.py

Enterprise PDF parser implementation.

Responsible for:
- Reading PDF documents
- Extracting metadata
- Extracting text from every page
- Returning a standardized Document object
"""

from pathlib import Path
import logging

from pypdf import PdfReader

from indexing.parsers.base_parser import BaseParser
from models.document_model import Document


logger = logging.getLogger(__name__)


class PDFParser(BaseParser):
    """
    Enterprise PDF parser.
    """

    def parse(self, file_path: str) -> Document:
        """
        Parse a PDF document.

        Parameters
        ----------
        file_path : str
            Absolute or relative path to PDF.

        Returns
        -------
        Document
            Parsed document object.

        Raises
        ------
        FileNotFoundError
            If file does not exist.

        ValueError
            If file is not a PDF.

        RuntimeError
            If PDF cannot be parsed.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"{path.name} is not a PDF document."
            )

        logger.info("Parsing PDF: %s", path.name)

        try:

            reader = PdfReader(str(path))

            extracted_pages = []

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    extracted_pages.append(page_text.strip())

            content = "\n\n".join(extracted_pages)

            metadata = {

                "page_count": len(reader.pages),

                "title": reader.metadata.title if reader.metadata else None,

                "author": reader.metadata.author if reader.metadata else None,

                "producer": reader.metadata.producer if reader.metadata else None,

                "creator": reader.metadata.creator if reader.metadata else None,
            }

            logger.info(
                "Successfully parsed %s (%d pages)",
                path.name,
                len(reader.pages)
            )

            return Document(

                filename=path.name,

                extension=path.suffix,

                content=content,

                source_path=str(path.resolve()),

                metadata=metadata,
            )

        except Exception as exc:

            logger.exception(
                "Failed parsing PDF %s",
                path.name
            )

            raise RuntimeError(
                f"Unable to parse PDF '{path.name}'."
            ) from exc