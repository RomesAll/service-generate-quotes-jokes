from fastapi import APIRouter

router = APIRouter()

@router.get("/jokes")
def jokes():
    pass