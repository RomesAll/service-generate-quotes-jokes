import uvicorn
from fastapi import FastAPI
from app.api.v1 import router_quotes, router_jokes, router_author

app = FastAPI()

app.include_router(router_quotes)
app.include_router(router_jokes)
app.include_router(router_author)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)