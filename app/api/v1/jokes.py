from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.services import JokesService
from app.schemas import JokesSchemaPOST, JokesSchemaPUT
from app.dependencies import get_session, search_depends, pagination_depends, session_depends

router = APIRouter(prefix="/api/v1/jokes", tags=["jokes"])

@router.get("/")
def get_all_jokes(request: Request, pagination: pagination_depends, session: session_depends):
    result = JokesService(session=session, client=request.client.host).select_all_jokes(pagination)
    return {'jokes': result}

@router.get("/search")
def get_search_jokes(request: Request, search: search_depends, session: session_depends):
    result = JokesService(session=session, client=request.client.host).select_jokes_by_search(search.text, search.count_likes, search.count_dislikes)
    return {'found jokes': result}

@router.get("/filter/{year}")
def get_filter_jokes_by_year(year: int, request: Request, pagination: pagination_depends, session: session_depends):
    result = JokesService(session=session, client=request.client.host).select_filter_jokes_by_year(year, pagination)
    return {'filtered jokes': result}

@router.get("/most-popular")
def get_popular_jokes(request: Request, pagination: pagination_depends, session: session_depends):
    result = JokesService(session=session, client=request.client.host).select_most_popular_jokes(pagination)
    return {'most popular jokes': result}

@router.get("/{joke_id}")
def get_jokes_by_id(request: Request, joke_id, session: session_depends):
    result = JokesService(session=session, client=request.client.host).select_jokes_by_id(joke_id)
    return {'joke': result}

@router.post("/")
def create_joke(request: Request, new_object: JokesSchemaPOST, session: session_depends):
    result = JokesService(session=session, client=request.client.host).create_jokes(new_object)
    return {'joke_added': result}

@router.put("/")
def update_joke(request: Request, update_object: JokesSchemaPUT, session: session_depends):
    result = JokesService(session=session, client=request.client.host).update_jokes(update_object)
    return {'joke_updated': result}

@router.delete("/{joke_id}")
def delete_joke(request: Request, joke_id: int, session: session_depends):
    result = JokesService(session=session, client=request.client.host).delete_jokes(joke_id)
    return {'joke_deleted': result}