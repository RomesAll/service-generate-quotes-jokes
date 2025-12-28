from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_session
from app.services import QuotesService
from app.schemas import QuotesSchemaPUT, QuotesSchemaPOST, QuotesSchemaGET
router = APIRouter(prefix="/api/v1/quotes", tags=["quotes"])

@router.get("/")
def get_all_quotes(session: Session = Depends(get_session)):
    result = QuotesService(session=session).select_all_quotes()
    return {'quotes': result}

@router.get("/{quote_id}")
def get_quotes_by_id(quote_id, session: Session = Depends(get_session)):
    result = QuotesService(session=session).select_quotes_by_id(quote_id)
    return {'quote': result}

@router.post("/")
def create_quote(new_object: QuotesSchemaPOST, session: Session = Depends(get_session)):
    result = QuotesService(session=session).create_quotes(new_object)
    return {'quote_added': result}

@router.put("/")
def update_quote(update_object: QuotesSchemaPUT, session: Session = Depends(get_session)):
    result = QuotesService(session=session).update_quotes(update_object)
    return {'quote_updated': result}

@router.delete("/{quote_id}")
def delete_quote(quote_id: int, session: Session = Depends(get_session)):
    result = QuotesService(session=session).delete_quotes(quote_id)
    return {'quote_deleted': result}
