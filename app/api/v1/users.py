from fastapi import APIRouter, Request
from app.dependencies import session_depends
from app.services import UsersService
from app.schemas import UsersSchemaGET, UsersSchemaPOST, UsersSchemaPUT
import uuid

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/")
def get_all_users(request: Request, session: session_depends):
    result = UsersService(session=session, client=request.client.host).select_all_users()
    return {'users': result}

@router.get("/{user_id}")
def get_users_by_id(request: Request, user_id: uuid.UUID, session: session_depends):
    result = UsersService(session=session, client=request.client.host).select_users_by_id(user_id)
    return {'user': result}

@router.post("/")
def create_users(request: Request, new_object: UsersSchemaPOST, session: session_depends):
    result = UsersService(session=session, client=request.client.host).create_users(new_object)
    return {'user_added': result}

@router.put("/")
def update_users(request: Request, update_object: UsersSchemaPUT, session: session_depends):
    result = UsersService(session=session, client=request.client.host).update_users(update_object)
    return {'user_updated': result}

@router.delete("/{user_id}")
def delete_users(request: Request, user_id: uuid.UUID, session: session_depends):
    result = UsersService(session=session, client=request.client.host).delete_users(user_id)
    return {'user_deleted': result}
