"""
JSON Parser
"""

import json
from pathlib import Path

from indexing.parsers.base_parser import BaseParser
from models.document_model import Document


class JSONParser(BaseParser):

    def flatten(self, obj, prefix=""):

        lines = []

        if isinstance(obj, dict):

            for key, value in obj.items():

                new_prefix = f"{prefix}.{key}" if prefix else key

                lines.extend(self.flatten(value, new_prefix))

        elif isinstance(obj, list):

            for i, item in enumerate(obj):

                lines.extend(self.flatten(item, f"{prefix}[{i}]"))

        else:

            lines.append(f"{prefix}: {obj}")

        return lines

    def parse(self, file_path: str) -> Document:

        path = Path(file_path)

        with open(path, "r", encoding="utf-8") as f:

            data = json.load(f)

        text = "\n".join(self.flatten(data))

        return Document(
            filename=path.name,
            extension=path.suffix,
            content=text,
            source_path=str(path.resolve()),
            metadata={}
        )