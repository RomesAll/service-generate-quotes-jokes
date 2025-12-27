from fastapi import APIRouter

router = APIRouter()

@router.get("/quotes")
def quotes():
    pass