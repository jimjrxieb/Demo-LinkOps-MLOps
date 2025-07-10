from datetime import datetime


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


from fastapi import APIRouter, Body
from logic import storage

router = APIRouter()

SCRIPTS_FILE = "scripts.json"
HISTORY_FILE = "history.csv"


@router.get("/")
def list_scripts():
    scripts = storage.read_json(SCRIPTS_FILE)
    return {"scripts": scripts}


@router.post("/")
def add_script(script: dict = Body(...)):
    storage.append_to_json(SCRIPTS_FILE, script)

    storage.append_to_csv(
        HISTORY_FILE,
        {
            "timestamp": datetime.utcnow().isoformat(),
            "input_type": "script",
            "source": "manual_input",
            "content": script.get("title", str(script)),
            "intent": "store_script",
        },
    )

    return {"message": "Script added successfully.", "script": script}
