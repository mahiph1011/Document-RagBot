


"""
chunker.py

Enterprise Hierarchical Chunker

Pipeline

Document
    ↓
Normalize Text
    ↓
Detect Headings
    ↓
Paragraph Detection
    ↓
Sentence Detection
    ↓
Token Based Chunking
    ↓
Sentence Overlap
    ↓
Chunk Metadata
"""

from __future__ import annotations

import re
from typing import List, Dict

import tiktoken

from models.document_model import Document


class Chunker:
    """
    Enterprise hierarchical token-aware chunker.

    Features
    --------
    ✓ Heading preservation
    ✓ Paragraph preservation
    ✓ Sentence aware
    ✓ Token aware
    ✓ Sentence overlap
    ✓ Metadata generation
    """

    def __init__(
        self,
        max_tokens: int = 450,
        overlap_sentences: int = 1,
        encoding_name: str = "cl100k_base"
    ):

        self.max_tokens = max_tokens

        self.overlap_sentences = overlap_sentences

        self.encoding = tiktoken.get_encoding(
            encoding_name
        )

    ###########################################################

    def token_count(self, text: str) -> int:
        """
        Count tokens.
        """

        return len(
            self.encoding.encode(text)
        )

    ###########################################################

    def normalize(self, text: str) -> str:
        """
        Normalize whitespace.
        """

        text = text.replace("\r", "")

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        return text.strip()

    ###########################################################

    def split_paragraphs(
        self,
        text: str
    ) -> List[str]:
        """
        Split document into paragraphs.
        """

        paragraphs = re.split(
            r"\n\s*\n",
            text
        )

        paragraphs = [

            p.strip()

            for p in paragraphs

            if p.strip()

        ]

        return paragraphs

    ###########################################################

    def detect_heading(
        self,
        paragraph: str
    ) -> bool:
        """
        Detect whether paragraph is a heading.
        """

        paragraph = paragraph.strip()

        if len(paragraph) < 80:

            if paragraph.endswith(":"):

                return True

            if paragraph.isupper():

                return True

            if re.match(
                r"^\d+(\.\d+)*",
                paragraph
            ):

                return True

        return False

    ###########################################################

    def split_sentences(
        self,
        paragraph: str
    ) -> List[str]:
        """
        Split paragraph into sentences.
        """

        paragraph = paragraph.replace(
            "\n",
            " "
        )

        sentences = re.split(

            r'(?<=[.!?])\s+',

            paragraph

        )

        return [

            s.strip()

            for s in sentences

            if s.strip()

        ]
    
    ###########################################################

    def build_chunks(
        self,
        document: Document
    ) -> List[Dict]:
        """
        Build hierarchical chunks while preserving:

        Document
            ↓
        Heading
            ↓
        Paragraph
            ↓
        Sentence
            ↓
        Token Limit
        """

        text = self.normalize(document.content)

        paragraphs = self.split_paragraphs(text)

        chunks = []

        current_sentences = []

        current_tokens = 0

        current_heading = "General"

        paragraph_number = 0

        chunk_number = 0

        for paragraph in paragraphs:

            paragraph_number += 1

            # ---------------------------------------
            # Heading detection
            # ---------------------------------------

            if self.detect_heading(paragraph):

                current_heading = paragraph

                continue

            sentences = self.split_sentences(paragraph)

            for sentence in sentences:

                sentence_tokens = self.token_count(sentence)

                # ---------------------------------------
                # Chunk Full
                # ---------------------------------------

                if (
                    current_tokens + sentence_tokens
                    > self.max_tokens
                    and current_sentences
                ):

                    # chunk_text = " ".join(current_sentences)
                    chunk_body = " ".join(current_sentences)
                    chunk_text = f"{current_heading}\n\n{chunk_body}"

                    chunks.append({

                        "chunk_id": chunk_number,

                        "extension": document.extension,

                        "document_name": document.filename,

                        "section": current_heading,

                        "paragraph": paragraph_number,

                        "content": chunk_text,

                        "token_count": current_tokens,

                        "character_count": len(chunk_text),

                        "metadata": document.metadata

                        

                    })

                    chunk_number += 1

                    # ---------------------------------------
                    # Sentence Overlap
                    # ---------------------------------------

                    current_sentences = current_sentences[
                        -self.overlap_sentences:
                    ]

                    current_tokens = sum(

                        self.token_count(s)

                        for s in current_sentences

                    )

                current_sentences.append(sentence)

                current_tokens += sentence_tokens

        # ---------------------------------------
        # Final Chunk
        # ---------------------------------------

        if current_sentences:

            # chunk_text = " ".join(current_sentences)
            chunk_body = " ".join(current_sentences)
            chunk_text = f"{current_heading}\n\n{chunk_body}"

            chunks.append({

                "chunk_id": chunk_number,

                "document_name": document.filename,

                "section": current_heading,

                "paragraph": paragraph_number,

                "content": chunk_text,

                "token_count": current_tokens,

                "character_count": len(chunk_text),

                "metadata": document.metadata

            })

        return chunks

    ###########################################################

    def split(
        self,
        document: Document
    ) -> List[Dict]:
        """
        Public method.

        Used by the indexing pipeline.
        """

        return self.build_chunks(document)
    
    ###########################################################

    def preview(
        self,
        chunks: List[Dict],
        max_characters: int = 120
    ) -> None:
        """
        Pretty print chunks for debugging.
        """

        print("\n" + "=" * 80)

        print("Chunk Preview")

        print("=" * 80)

        for chunk in chunks:

            print()

            print(f"Chunk ID      : {chunk['chunk_id']}")

            print(f"Section       : {chunk['section']}")

            print(f"Paragraph     : {chunk['paragraph']}")

            print(f"Tokens        : {chunk['token_count']}")

            print(f"Characters    : {chunk['character_count']}")

            print()

            print(

                chunk["content"][:max_characters]

            )

            print()

            print("-" * 80)

    ###########################################################

    def statistics(
        self,
        chunks: List[Dict]
    ) -> Dict:
        """
        Compute statistics.
        """

        if not chunks:

            return {}

        token_counts = [

            c["token_count"]

            for c in chunks

        ]

        return {

            "total_chunks": len(chunks),

            "avg_tokens": sum(token_counts) / len(token_counts),

            "max_tokens": max(token_counts),

            "min_tokens": min(token_counts)

        }
