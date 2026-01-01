from app.database import session_maker
from fastapi import Depends
from app.schemas.base import PaginationJokesSchema, SearchJokesSchema
from sqlalchemy.orm import Session
from typing import Annotated

def get_session():
    try:
        session = session_maker()
        yield session
    finally:
        session.close()

pagination_depends = Annotated[PaginationJokesSchema, Depends(PaginationJokesSchema)]
search_depends = Annotated[SearchJokesSchema, Depends(SearchJokesSchema)]
session_depends = Annotated[Session, Depends(get_session)]