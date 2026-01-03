from fastapi import APIRouter, Request
from app.dependencies import session_depends, pagination_depends, search_depends, validate_active_user_depends
from app.services import QuotesService
from app.schemas import QuotesSchemaPUT, QuotesSchemaPOST, QuotesSchemaGET
import uuid

router = APIRouter(prefix="/api/v1/quotes", tags=["quotes"])

@router.get("/")
def get_all_quotes(request: Request, pagination: pagination_depends, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_all_quotes(pagination)
    return {'quotes': result}

@router.get("/extended")
def get_all_quotes_rel(request: Request, pagination: pagination_depends, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_all_quotes_rel(pagination)
    return {'extended quotes': result}

@router.get("/random")
def get_random_quotes(request: Request, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_random_quotes()
    return {'random quotes': result}

@router.get("/search")
def get_search_quotes(request: Request, search: search_depends, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_quotes_by_search(search.text, search.count_likes, search.count_dislikes)
    return {'found quotes': result}

@router.get("/filter/{year}")
def get_filter_quotes_by_year(year: int, request: Request, pagination: pagination_depends, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_filter_quotes_by_year(year, pagination)
    return {'filtered quotes': result}

@router.get("/most-popular")
def get_popular_quotes(request: Request, pagination: pagination_depends, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_most_popular_quotes(pagination)
    return {'most popular quotes': result}

@router.get("/{quote_id}")
def get_quotes_by_id(request: Request, quote_id: uuid.UUID, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_quotes_by_id(quote_id)
    return {'quote': result}

@router.get("/{quote_id}/extended")
def get_quotes_by_id_rel(request: Request, quote_id: uuid.UUID, session: session_depends):
    result = QuotesService(session=session, client=request.client.host).select_quotes_by_id_rel(quote_id)
    return {'extended quote': result}

@router.post("/")
def create_quote(request: Request, new_object: QuotesSchemaPOST,
                 session: session_depends, payload: validate_active_user_depends):
    result = QuotesService(session=session, client=request.client.host).create_quotes(new_object)
    return {'quote_added': result}

@router.put("/")
def update_quote(request: Request, update_object: QuotesSchemaPUT,
                 session: session_depends, payload: validate_active_user_depends):
    result = QuotesService(session=session, client=request.client.host).update_quotes(update_object)
    return {'quote_updated': result}

@router.delete("/{quote_id}")
def delete_quote(request: Request, quote_id: uuid.UUID,
                 session: session_depends, payload: validate_active_user_depends):
    result = QuotesService(session=session, client=request.client.host).delete_quotes(quote_id)
    return {'quote_deleted': result}
