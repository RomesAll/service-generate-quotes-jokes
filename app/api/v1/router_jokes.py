from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/jokes", tags=["jokes"])

@router.get("/")
def jokes():
    pass