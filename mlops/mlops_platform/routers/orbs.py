from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/")
def list_orbs():
    return {"message": "All best practices (Orbs) will be listed here."}


@router.post("/")
def add_orb(orb: dict = Body(...)):
    return {"message": "Orb saved.", "orb": orb}
