from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/quotes", tags=["quotes"])

@router.get("/")
def quotes():
    pass