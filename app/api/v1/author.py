from fastapi import APIRouter, Request
from app.services import AuthorService, AuthorSchemaPOST, AuthorSchemaPUT
from app.dependencies import session_depends, validate_active_user_depends
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/api/v1/authors", tags=["Authors"])

@router.get("/")
@cache(expire=60)
def get_all_authors(request: Request, session: session_depends):
    result = AuthorService(session=session, client=request.client.host).select_all_author()
    return {'authors': result}

@router.get("/{author_id}")
@cache(expire=60)
def get_author_by_id(request: Request, author_id, session: session_depends):
    result = AuthorService(session=session, client=request.client.host).select_author_by_id(author_id)
    return {'author': result}

@router.post("/")
def create_author(request: Request, new_object: AuthorSchemaPOST,
                  session: session_depends, payload: validate_active_user_depends):
    result = AuthorService(session=session, client=request.client.host).create_author(new_object)
    return {'author_added': result}

@router.put("/")
def update_author(request: Request, update_object: AuthorSchemaPUT,
                  session: session_depends, payload: validate_active_user_depends):
    result = AuthorService(session=session, client=request.client.host).update_author(update_object)
    return {'author_updated': result}

@router.delete("/{author_id}")
def delete_author(request: Request, author_id: int,
                  session: session_depends, payload: validate_active_user_depends):
    result = AuthorService(session=session, client=request.client.host).delete_author(author_id)
    return {'author_deleted': result}
