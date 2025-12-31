from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.dependencies import get_session
from app.services import QuotesService
from app.schemas import QuotesSchemaPUT, QuotesSchemaPOST, QuotesSchemaGET
router = APIRouter(prefix="/api/v1/quotes", tags=["quotes"])

@router.get("/")
def get_all_quotes(request: Request, session: Session = Depends(get_session)):
    result = QuotesService(session=session, client=request.client.host).select_all_quotes()
    return {'quotes': result}

@router.get("/{quote_id}")
def get_quotes_by_id(request: Request, quote_id, session: Session = Depends(get_session)):
    result = QuotesService(session=session, client=request.client.host).select_quotes_by_id(quote_id)
    return {'quote': result}

@router.post("/")
def create_quote(request: Request, new_object: QuotesSchemaPOST, session: Session = Depends(get_session)):
    result = QuotesService(session=session, client=request.client.host).create_quotes(new_object)
    return {'quote_added': result}

@router.put("/")
def update_quote(request: Request, update_object: QuotesSchemaPUT, session: Session = Depends(get_session)):
    result = QuotesService(session=session, client=request.client.host).update_quotes(update_object)
    return {'quote_updated': result}

@router.delete("/{quote_id}")
def delete_quote(request: Request, quote_id: int, session: Session = Depends(get_session)):
    result = QuotesService(session=session, client=request.client.host).delete_quotes(quote_id)
    return {'quote_deleted': result}
