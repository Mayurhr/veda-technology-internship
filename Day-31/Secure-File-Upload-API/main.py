"""
Secure File Upload API
Day 31 - Veda Technology Python Programming Internship

A simple FastAPI application that demonstrates secure file upload
handling: file type validation, file size limits, safe filename
generation, and path traversal protection.
"""

import os
import re
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Secure File Upload API")

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".txt", ".csv", ".pdf", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def validate_file_type(filename: str) -> str:
    """Check the file extension against the allowed list.

    Returns the lowercase extension if valid, otherwise raises
    an HTTPException.
    """
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed",
        )
    return extension


def validate_file_size(size: int) -> None:
    """Reject files larger than MAX_FILE_SIZE."""
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the allowed limit",
        )


def safe_filename(extension: str) -> str:
    """Generate a random, safe filename.

    Never trust the original filename. A UUID-based name removes
    any risk of path traversal or unsafe characters, since the
    original name is not used to build the stored path at all.
    """
    return f"{uuid.uuid4().hex}{extension}"


def save_upload(file_bytes: bytes, stored_filename: str) -> Path:
    """Save file bytes inside the uploads directory only.

    Resolves the final path and confirms it is still inside
    UPLOAD_DIR before writing, as a defense-in-depth check.
    """
    destination = (UPLOAD_DIR / stored_filename).resolve()

    if UPLOAD_DIR.resolve() not in destination.parents and destination.parent != UPLOAD_DIR.resolve():
        # Should never happen since stored_filename is a UUID we generate,
        # but this guard keeps the function safe if that ever changes.
        raise HTTPException(status_code=400, detail="Invalid upload path")

    with open(destination, "wb") as f:
        f.write(file_bytes)

    return destination


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

@app.get("/")
def read_root():
    """Simple status endpoint."""
    return {"status": "ok", "message": "Secure File Upload API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Accept a file upload, validate it, and store it safely."""
    try:
        original_filename = file.filename or "unnamed_file"

        # Basic sanity check: reject empty filenames outright.
        if not original_filename.strip():
            raise HTTPException(status_code=400, detail="Filename is missing")

        extension = validate_file_type(original_filename)

        file_bytes = await file.read()
        validate_file_size(len(file_bytes))

        stored_filename = safe_filename(extension)
        save_upload(file_bytes, stored_filename)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "file_size_bytes": len(file_bytes),
                "message": "File uploaded successfully",
            },
        )

    except HTTPException:
        # Re-raise expected validation errors as-is.
        raise
    except Exception:
        # Never leak internal filesystem details in the error response.
        raise HTTPException(status_code=500, detail="An error occurred while uploading the file")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
