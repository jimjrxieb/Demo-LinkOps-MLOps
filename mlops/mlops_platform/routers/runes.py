from fastapi import APIRouter, Body


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


router = APIRouter()


@router.get("/")
def list_runes():
    return {"message": "All solution Runes will be listed here."}


@router.post("/")
def add_rune(rune: dict = Body(...)):
    return {"message": "Rune added.", "rune": rune}
