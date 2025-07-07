from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_digest():
    return {"message": "Daily digest endpoint (summary of today's tasks/workflows)."}
