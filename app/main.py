from fastapi import FastAPI, Request, Response, Depends
from app.api.v1 import router_quotes, router_jokes, router_author, router_users, router_auth
from app.core.exception_handler import exception_handler
from app.core import settings
from app.dependencies import http_bearer
from contextlib import asynccontextmanager
from redis import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.redis import Redis
import time, uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(host=settings.redis.host, port=settings.redis.port, db=settings.redis.db.cache)
    FastAPICache.init(RedisBackend(redis), prefix=settings.cache.prefix)
    yield

app = FastAPI(dependencies=[Depends(http_bearer)], lifespan=lifespan)

@app.middleware("http")
async def request_processing(request: Request, call_next):
    settings.logger.info("client: %s url: %s method: %s body: %s", request.client.host, request.url, request.method, request.body)
    time_start = time.time()
    response: Response = await call_next(request)
    result_time = time.time() - time_start
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