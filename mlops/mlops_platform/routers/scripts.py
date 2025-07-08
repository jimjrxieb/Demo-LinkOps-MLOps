from datetime import datetime

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
