"""
TXT Parser
"""

from pathlib import Path

from indexing.parsers.base_parser import BaseParser
from models.document_model import Document


class TXTParser(BaseParser):

    def parse(self, file_path: str) -> Document:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        return Document(
            filename=path.name,
            extension=path.suffix,
            content=text,
            source_path=str(path.resolve()),
            metadata={}
        )