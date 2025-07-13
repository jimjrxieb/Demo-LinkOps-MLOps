from demo_api import router as demo_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import orbs, tasks


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
    title="LinkOps MLOps Platform - Demo",
    description="Simplified demo version of the LinkOps MLOps platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register demo API router (main functionality)
app.include_router(demo_router, prefix="/api", tags=["Demo API"])

# Register core routers (simplified for demo)
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(orbs.router, prefix="/orbs", tags=["Orbs"])

# Comment out complex routers for demo
# app.include_router(scripts.router, prefix="/scripts", tags=["Scripts"])
# app.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
# app.include_router(runes.router, prefix="/runes", tags=["Runes"])
# app.include_router(digest.router, prefix="/digest", tags=["Digest"])

# Comment out rune executor for demo
# try:
#     from rune_executor import router as rune_executor_router
#     app.include_router(rune_executor_router, prefix="/rune", tags=["Rune Executor"])
# except ImportError:
#     print("Warning: Rune executor not available")


@app.get("/")
def root():
    return {
        "message": "Welcome to LinkOps MLOps Platform - Demo Version",
        "version": "1.0.0",
        "environment": "demo",
        "description": "Simplified demo version focused on task processing and Orb management",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "mlops-platform",
        "version": "1.0.0",
        "environment": "demo",
    }
