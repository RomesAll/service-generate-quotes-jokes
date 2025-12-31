from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.services import JokesService
from app.schemas import JokesSchemaPOST, JokesSchemaPUT
from app.dependencies import get_session

router = APIRouter(prefix="/api/v1/jokes", tags=["jokes"])

@router.get("/")
def get_all_jokes(request: Request, session: Session = Depends(get_session)):
    result = JokesService(session=session, client=request.client.host).select_all_jokes()
    return {'jokes': result}

@router.get("/{joke_id}")
def get_jokes_by_id(request: Request, joke_id, session: Session = Depends(get_session)):
    result = JokesService(session=session, client=request.client.host).select_jokes_by_id(joke_id)
    return {'joke': result}

@router.post("/")
def create_joke(request: Request, new_object: JokesSchemaPOST, session: Session = Depends(get_session)):
    result = JokesService(session=session, client=request.client.host).create_jokes(new_object)
    return {'joke_added': result}

@router.put("/")
def update_joke(request: Request, update_object: JokesSchemaPUT, session: Session = Depends(get_session)):
    result = JokesService(session=session, client=request.client.host).update_jokes(update_object)
    return {'joke_updated': result}

@router.delete("/{joke_id}")
def delete_joke(request: Request, joke_id: int, session: Session = Depends(get_session)):
    result = JokesService(session=session, client=request.client.host).delete_jokes(joke_id)
    return {'joke_deleted': result}