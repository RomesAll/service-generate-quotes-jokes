from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, DBAPIError, IntegrityError, DatabaseError
from fastapi import FastAPI, Request

class RecordNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
    def __str__(self):
        return self.message

class DuplicateKeyError(Exception):
    def __init__(self, message: str):
        self.message = message
    def __str__(self):
        return self.message

def exception_handler(app: FastAPI):

    @app.exception_handler(DataError)
    def data_error_handler(request: Request, exception: DataError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"message": str(exception)})

    @app.exception_handler(DBAPIError)
    def db_api_error_handler(request: Request, exception: DataError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"message": str(exception)})

    @app.exception_handler(IntegrityError)
    def integrity_error_handler(request: Request, exception: DataError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"message": str(exception)})

    @app.exception_handler(DatabaseError)
    def data_base_error_handler(request: Request, exception: DataError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"message": str(exception)})

    @app.exception_handler(RecordNotFoundError)
    def record_not_found_error_handler(request: Request, exception: RecordNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"message": str(exception)})

    @app.exception_handler(DuplicateKeyError)
    def duplicate_key_error_handler(request: Request, exception: DuplicateKeyError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"message": str(exception)})

