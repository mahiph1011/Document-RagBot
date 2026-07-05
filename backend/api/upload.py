"""
upload.py

Upload API

Responsibilities
----------------
- Receive uploaded file
- Save file locally
- Trigger indexing
- Return indexing statistics
"""

from __future__ import annotations

import os
import shutil

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from indexing.indexer import Indexer


router = APIRouter(
    prefix="/api",
    tags=["Upload"]
)

UPLOAD_FOLDER = "data/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

indexer = Indexer()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt",
        ".json"
    }

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in allowed_extensions:

        raise HTTPException(

            status_code=400,

            detail="Unsupported file type."

        )

    file_path = os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )

    with open(

        file_path,

        "wb"

    ) as buffer:

        shutil.copyfileobj(

            file.file,

            buffer

        )

    result = indexer.index_document(
        file_path
    )

    return {

        "message": "Document indexed successfully.",

        "file_name": file.filename,

        "details": result

    }