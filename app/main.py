from fastapi import FastAPI, Request, Response, Depends
from app.api.v1 import router_quotes, router_jokes, router_author, router_users, router_auth
from app.core.exception_handler import exception_handler
from app.core import settings
from app.dependencies import http_bearer
import time, uvicorn

app = FastAPI(dependencies=[Depends(http_bearer)])

@app.middleware("http")
async def request_processing(request: Request, call_next):
    settings.logger.info("client: %s url: %s method: %s body: %s", request.client.host, request.url, request.method, request.body)
    time_start = time.time()
    response: Response = await call_next(request)
    result_time = time_start - time.time()
    settings.logger.info("client: %s url: %s method: %s status: %s time: %s", request.client.host,
                         request.url, request.method, response.status_code, str(result_time))
    response.headers['X-Processing-Time-Sec'] = str(result_time)
    return response

exception_handler(app)
app.include_router(router_quotes)
app.include_router(router_jokes)
app.include_router(router_author)
app.include_router(router_users)
app.include_router(router_auth)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)