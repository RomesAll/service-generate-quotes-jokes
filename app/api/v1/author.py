from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services import AuthorService
from app.schemas import AuthorSchemaGET, AuthorSchemaPOST, AuthorSchemaPUT
from app.dependencies import get_session
router = APIRouter(prefix="/api/v1/authors", tags=["authors"])

@router.get("/")
def get_all_authors(request: Request, session: Session = Depends(get_session)):
    result = AuthorService(session=session, client=request.client.host).select_all_author()
    return {'authors': result}

@router.get("/{author_id}")
def get_author_by_id(request: Request, author_id, session: Session = Depends(get_session)):
    result = AuthorService(session=session, client=request.client.host).select_author_by_id(author_id)
    return {'author': result}

@router.post("/")
def create_author(request: Request, new_object: AuthorSchemaPOST, session: Session = Depends(get_session)):
    result = AuthorService(session=session, client=request.client.host).create_author(new_object)
    return {'author_added': result}

@router.put("/")
def update_author(request: Request, update_object: AuthorSchemaPUT, session: Session = Depends(get_session)):
    result = AuthorService(session=session, client=request.client.host).update_author(update_object)
    return {'author_updated': result}

@router.delete("/{author_id}")
def delete_author(request: Request, author_id: int, session: Session = Depends(get_session)):
    result = AuthorService(session=session, client=request.client.host).delete_author(author_id)
    return {'author_deleted': result}
