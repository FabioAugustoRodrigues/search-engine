from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_schema():
    return "Hiii"