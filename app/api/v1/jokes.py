from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import JokesService
from app.schemas import JokesSchemaPOST, JokesSchemaPUT
from app.dependencies import get_session

router = APIRouter(prefix="/api/v1/jokes", tags=["jokes"])

@router.get("/")
def get_all_jokes(session: Session = Depends(get_session)):
    result = JokesService(session=session).select_all_jokes()
    return {'jokes': result}

@router.get("/{joke_id}")
def get_jokes_by_id(joke_id):
    result = JokesService(session=None).select_jokes_by_id(joke_id)
    return {'joke': result}

@router.post("/")
def create_joke(new_object: JokesSchemaPOST):
    result = JokesService(session=None).create_jokes(new_object)
    return {'joke_added': result}

@router.put("/")
def update_joke(update_object: JokesSchemaPUT):
    result = JokesService(session=None).update_jokes(update_object)
    return {'joke_updated': result}

@router.delete("/{joke_id}")
def delete_joke(joke_id: int):
    result = JokesService(session=None).delete_jokes(joke_id)
    return {'joke_deleted': result}