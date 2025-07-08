from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import re

router = APIRouter()


class YouTubeRequest(BaseModel):
    url: str
    language: Optional[str] = "en"
    include_timestamps: bool = True
    tags: List[str] = []


class YouTubeTranscript(BaseModel):
    video_id: str
    title: str
    duration: Optional[str] = None
    language: str
    transcript: List[Dict[str, Any]]
    metadata: Dict[str, Any]


@router.post("/youtube/transcript")
async def download_youtube_transcript(request: YouTubeRequest):
    """
    Download and process YouTube video transcript.
    """
    try:
        # Extract video ID from URL
        video_id = _extract_video_id(request.url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        # TODO: Implement actual YouTube transcript download
        # For now, return mock data
        mock_transcript = [
            {
                "start": 0.0,
                "end": 5.0,
                "text": "Welcome to this tutorial on MLOps best practices.",
                "timestamp": "00:00",
            },
            {
                "start": 5.0,
                "end": 10.0,
                "text": "Today we'll cover deployment strategies and monitoring.",
                "timestamp": "00:05",
            },
        ]

        # Prepare transcript data
        transcript_data = {
            "id": str(uuid.uuid4()),
            "type": "youtube_transcript",
            "video_id": video_id,
            "url": request.url,
            "language": request.language,
            "include_timestamps": request.include_timestamps,
            "tags": request.tags + ["youtube", "transcript"],
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending_processing",
            "transcript": mock_transcript,
            "metadata": {
                "title": f"Mock Video Title for {video_id}",
                "duration": "15:30",
                "channel": "Mock Channel",
                "view_count": 1000,
                "upload_date": "2024-01-01",
            },
        }

        # TODO: Send to whis_sanitize service
        return {
            "message": "YouTube transcript downloaded successfully",
            "video_id": video_id,
            "data": transcript_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to download transcript: {str(e)}"
        )


@router.post("/youtube/transcript/batch")
async def download_youtube_transcripts_batch(urls: List[str]):
    """
    Download transcripts from multiple YouTube videos.
    """
    try:
        batch_id = str(uuid.uuid4())
        results = []

        for url in urls:
            try:
                video_id = _extract_video_id(url)
                if video_id:
                    # TODO: Implement actual download
                    result = {
                        "url": url,
                        "video_id": video_id,
                        "status": "downloaded",
                        "transcript_length": 150,  # Mock length
                    }
                else:
                    result = {
                        "url": url,
                        "video_id": None,
                        "status": "failed",
                        "error": "Invalid YouTube URL",
                    }
            except Exception as e:
                result = {
                    "url": url,
                    "video_id": None,
                    "status": "failed",
                    "error": str(e),
                }

            results.append(result)

        return {
            "message": f"Batch processing completed",
            "batch_id": batch_id,
            "total_urls": len(urls),
            "successful": len([r for r in results if r["status"] == "downloaded"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process batch: {str(e)}"
        )


@router.get("/youtube/transcript/{video_id}")
async def get_youtube_transcript(video_id: str):
    """
    Retrieve transcript for a specific YouTube video.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/youtube/transcript")
async def list_youtube_transcripts(
    limit: int = 50, offset: int = 0, language: Optional[str] = None
):
    """
    List all YouTube transcripts with optional filtering.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/youtube/metadata")
async def get_youtube_metadata(url: str):
    """
    Extract metadata from YouTube video without downloading transcript.
    """
    try:
        video_id = _extract_video_id(url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        # TODO: Implement actual metadata extraction
        metadata = {
            "video_id": video_id,
            "title": f"Mock Video Title for {video_id}",
            "description": "Mock video description",
            "duration": "15:30",
            "channel": "Mock Channel",
            "view_count": 1000,
            "like_count": 100,
            "upload_date": "2024-01-01",
            "tags": ["mlops", "tutorial", "best-practices"],
            "language": "en",
            "has_transcript": True,
        }

        return {
            "message": "YouTube metadata extracted successfully",
            "metadata": metadata,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to extract metadata: {str(e)}"
        )


def _extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.
    """
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be\/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


@router.post("/youtube/playlist")
async def process_youtube_playlist(playlist_url: str):
    """
    Process all videos in a YouTube playlist.
    """
    try:
        # TODO: Implement playlist processing
        # Extract all video URLs from playlist
        # Download transcripts for each video
        print("YouTube processing complete.")

        return {
            "message": "Playlist processing initiated",
            "playlist_url": playlist_url,
            "status": "processing",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process playlist: {str(e)}"
        )
