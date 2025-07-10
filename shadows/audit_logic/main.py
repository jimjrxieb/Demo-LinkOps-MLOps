from fastapi import FastAPI
from routers import audit_router


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
    title="Audit Logic Service",
    description=(
        "Best practices, GitOps rules, audit scoring criteria, and logic checklists"
    ),
    version="1.0.0",
)

app.include_router(audit_router.router)
