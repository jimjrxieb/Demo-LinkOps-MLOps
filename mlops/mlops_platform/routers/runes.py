from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/")
def list_runes():
    return {"message": "All solution Runes will be listed here."}


@router.post("/")
def add_rune(rune: dict = Body(...)):
    return {"message": "Rune added.", "rune": rune}
