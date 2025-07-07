from fastapi import FastAPI
from routers import tasks, scripts, workflows, orbs, runes, digest

app = FastAPI(title="MLOps Platform API", version="0.1.0")

# Register core routers
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(scripts.router, prefix="/scripts", tags=["Scripts"])
app.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
app.include_router(orbs.router, prefix="/orbs", tags=["Orbs"])
app.include_router(runes.router, prefix="/runes", tags=["Runes"])
app.include_router(digest.router, prefix="/digest", tags=["Digest"])

# Register rune executor router
try:
    from rune_executor import router as rune_executor_router

    app.include_router(rune_executor_router, prefix="/rune", tags=["Rune Executor"])
except ImportError:
    print("Warning: Rune executor not available")


@app.get("/")
def root():
    return {
        "message": "Welcome to the MLOps Platform — your personal memory and automation engine."
    }
