from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chatgpt_csv, image_text, info_dump, qna_input, youtube


def sanitize_cmd(cmd):
    import shlex

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {
        "ls",
        "echo",
        "kubectl",
        "helm",
        "python3",
        "cat",
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


app = FastAPI(
    title="Whis Data Input Service",
    description="Entry point for all user and external data into the Whis pipeline",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(qna_input.router, prefix="/api/qna", tags=["Q&A Input"])
app.include_router(chatgpt_csv.router, prefix="/api/csv", tags=["ChatGPT CSV"])
app.include_router(image_text.router, prefix="/api/image", tags=["Image Text"])
app.include_router(info_dump.router, prefix="/api/dump", tags=["Info Dump"])
app.include_router(youtube.router, prefix="/api/youtube", tags=["YouTube"])


@app.get("/")
async def root():
    return {
        "service": "whis_data_input",
        "status": "healthy",
        "version": "1.0.0",
        "description": "Entry point for all user and external data into the Whis pipeline",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "whis_data_input",
        "timestamp": "2024-01-01T00:00:00Z",
    }


@app.get("/api/endpoints")
async def list_endpoints():
    """List all available endpoints."""
    return {
        "endpoints": {
            "qna": {
                "submit": "POST /api/qna/qna",
                "batch": "POST /api/qna/qna/batch",
                "get": "GET /api/qna/qna/{qna_id}",
                "list": "GET /api/qna/qna",
            },
            "csv": {
                "upload": "POST /api/csv/upload/csv",
                "get_result": "GET /api/csv/csv/{file_id}",
                "list": "GET /api/csv/csv",
            },
            "image": {
                "extract_text": "POST /api/image/extract-text",
                "extract_base64": "POST /api/image/extract-text/base64",
                "batch": "POST /api/image/extract-text/batch",
                "get_result": "GET /api/image/extract-text/{image_id}",
                "list": "GET /api/image/extract-text",
            },
            "dump": {
                "submit": "POST /api/dump/dump",
                "batch": "POST /api/dump/dump/batch",
                "structured": "POST /api/dump/dump/structured",
                "get": "GET /api/dump/dump/{dump_id}",
                "list": "GET /api/dump/dump",
            },
            "youtube": {
                "transcript": "POST /api/youtube/youtube/transcript",
                "batch": "POST /api/youtube/youtube/transcript/batch",
                "metadata": "POST /api/youtube/youtube/metadata",
                "playlist": "POST /api/youtube/youtube/playlist",
                "get": "GET /api/youtube/youtube/transcript/{video_id}",
                "list": "GET /api/youtube/youtube/transcript",
            },
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
