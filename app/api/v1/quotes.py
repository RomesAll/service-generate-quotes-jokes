from fastapi import APIRouter
from app.services import QuotesService
from app.schemas import QuotesSchemaPUT, QuotesSchemaPOST, QuotesSchemaGET
router = APIRouter(prefix="/api/v1/quotes", tags=["quotes"])

@router.get("/")
def get_all_quotes():
    result = QuotesService(session=None).select_all_quotes()
    return {'quotes': result}

@router.get("/{quote_id}")
def get_quotes_by_id(quote_id):
    result = QuotesService(session=None).select_quotes_by_id(quote_id)
    return {'quote': result}

@router.post("/")
def create_quote(new_object: QuotesSchemaPOST):
    result = QuotesService(session=None).create_quotes(new_object)
    return {'quote_added': result}

@router.put("/")
def update_quote(update_object: QuotesSchemaPUT):
    result = QuotesService(session=None).update_quotes(update_object)
    return {'quote_updated': result}

@router.delete("/{quote_id}")
def delete_quote(quote_id: int):
    result = QuotesService(session=None).delete_quotes(quote_id)
    return {'quote_deleted': result}
