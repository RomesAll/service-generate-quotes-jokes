from fastapi import APIRouter
from app.services import AuthorService
from app.schemas import AuthorSchemaGET, AuthorSchemaPOST, AuthorSchemaPUT
router = APIRouter(prefix="/api/v1/authors", tags=["authors"])

@router.get("/")
def get_all_authors():
    result = AuthorService(session=None).select_all_author()
    return {'authors': result}

@router.get("/{author_id}")
def get_author_by_id(author_id):
    result = AuthorService(session=None).select_author_by_id(author_id)
    return {'author': result}

@router.post("/")
def create_author(new_object: AuthorSchemaPOST):
    result = AuthorService(session=None).create_author(new_object)
    return {'author_added': result}

@router.put("/")
def update_author(update_object: AuthorSchemaPUT):
    result = AuthorService(session=None).update_author(update_object)
    return {'author_updated': result}

@router.delete("/{author_id}")
def delete_author(author_id: int):
    result = AuthorService(session=None).delete_author(author_id)
    return {'author_deleted': result}
