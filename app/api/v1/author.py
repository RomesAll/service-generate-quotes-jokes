from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import AuthorService
from app.schemas import AuthorSchemaGET, AuthorSchemaPOST, AuthorSchemaPUT
from app.dependencies import get_session
router = APIRouter(prefix="/api/v1/authors", tags=["authors"])

@router.get("/")
def get_all_authors(session: Session = Depends(get_session)):
    result = AuthorService(session=session).select_all_author()
    return {'authors': result}

@router.get("/{author_id}")
def get_author_by_id(author_id, session: Session = Depends(get_session)):
    result = AuthorService(session=session).select_author_by_id(author_id)
    return {'author': result}

@router.post("/")
def create_author(new_object: AuthorSchemaPOST, session: Session = Depends(get_session)):
    result = AuthorService(session=session).create_author(new_object)
    return {'author_added': result}

@router.put("/")
def update_author(update_object: AuthorSchemaPUT, session: Session = Depends(get_session)):
    result = AuthorService(session=session).update_author(update_object)
    return {'author_updated': result}

@router.delete("/{author_id}")
def delete_author(author_id: int, session: Session = Depends(get_session)):
    result = AuthorService(session=session).delete_author(author_id)
    return {'author_deleted': result}
