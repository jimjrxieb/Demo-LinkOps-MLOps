import csv
import io
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter()


class CSVProcessingResult(BaseModel):
    file_id: str
    total_conversations: int
    processed_conversations: int
    failed_conversations: int
    metadata: dict


@router.post("/upload/csv")
async def upload_chatgpt_csv(
    file: UploadFile = File(...),
    source_name: Optional[str] = None,
    tags: Optional[str] = None,
):
    """
    Upload and process ChatGPT conversation CSV exports.
    """
    try:
        # Validate file
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="File must be a CSV")

        file_id = str(uuid.uuid4())
        processed_conversations = []
        failed_conversations = []

        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]

        # Read CSV content
        content = await file.read()
        csv_text = content.decode("utf-8")

        # Parse CSV
        csv_reader = csv.DictReader(io.StringIO(csv_text))

        for row_num, row in enumerate(csv_reader, 1):
            try:
                # Extract conversation data
                conversation_data = {
                    "id": str(uuid.uuid4()),
                    "type": "chatgpt_conversation",
                    "source": source_name or file.filename,
                    "tags": tag_list + ["chatgpt", "csv_import"],
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "pending_processing",
                    "conversation": {
                        "row_number": row_num,
                        "raw_data": row,
                        "messages": _extract_messages(row),
                        "metadata": _extract_metadata(row),
                    },
                }

                processed_conversations.append(conversation_data)

            except Exception as e:
                failed_conversations.append(
                    {"row_number": row_num, "error": str(e), "raw_data": row}
                )

        result = CSVProcessingResult(
            file_id=file_id,
            total_conversations=len(processed_conversations)
            + len(failed_conversations),
            processed_conversations=len(processed_conversations),
            failed_conversations=len(failed_conversations),
            metadata={
                "filename": file.filename,
                "file_size": len(content),
                "source_name": source_name,
                "tags": tag_list,
            },
        )

        # TODO: Send processed conversations to whis_sanitize service
        return {
            "message": "CSV uploaded and processed successfully",
            "result": result,
            "processed_data": processed_conversations[:5],  # Return first 5 for preview
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {str(e)}")


def _extract_messages(row: dict) -> List[dict]:
    """
    Extract conversation messages from CSV row.
    """
    messages = []

    # Common ChatGPT CSV column patterns
    message_columns = [
        "message",
        "content",
        "text",
        "response",
        "user_message",
        "assistant_message",
        "prompt",
        "completion",
    ]

    for col in message_columns:
        if col in row and row[col]:
            messages.append(
                {
                    "role": "user" if "user" in col.lower() else "assistant",
                    "content": row[col],
                    "timestamp": row.get("timestamp", ""),
                    "source_column": col,
                }
            )

    # If no standard columns found, try to infer from all columns
    if not messages:
        for key, value in row.items():
            if value and len(value) > 10:  # Likely a message if longer than 10 chars
                messages.append(
                    {"role": "unknown", "content": value, "source_column": key}
                )

    return messages


def _extract_metadata(row: dict) -> dict:
    """
    Extract metadata from CSV row.
    """
    metadata = {}

    # Common metadata columns
    metadata_columns = [
        "timestamp",
        "date",
        "time",
        "session_id",
        "conversation_id",
        "model",
        "temperature",
        "max_tokens",
        "user_id",
    ]

    for col in metadata_columns:
        if col in row and row[col]:
            metadata[col] = row[col]

    return metadata


@router.get("/csv/{file_id}")
async def get_csv_processing_result(file_id: str):
    """
    Get processing results for a specific CSV upload.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/csv")
async def list_csv_uploads(limit: int = 50, offset: int = 0):
    """
    List all CSV uploads.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")
