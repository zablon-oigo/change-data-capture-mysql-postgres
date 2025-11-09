from fastapi import FastAPI, Header, status, Request
from typing import Optional
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.db.main import initdb
from src.db.redis import init_redis
from src.errors import BookException
from fastapi.responses import JSONResponse

API_VERSION = "v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and Redis when app starts."""
    print("Starting server... initializing database and Redis")
    await initdb()
    await init_redis()
    yield
    print("Server is stopping...")


app = FastAPI(
    title="Book CRUD API",
    description="A RESTful API for a book review web service",
    version=API_VERSION,
    lifespan=lifespan
)

@app.get("/", status_code=status.HTTP_200_OK, tags=["Root"])
async def index():
    """health check."""
    return {"message": "Hello, World"}


@app.get("/get_headers",status_code=status.HTTP_200_OK, tags=["Debug"])
async def get_all_request_headers(
    user_agent: Optional[str] = Header(None),
    accept_encoding: Optional[str] = Header(None),
    referer: Optional[str] = Header(None),
    connection: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    host: Optional[str] = Header(None),
):
    """Return all request headers for debugging."""
    return {
        "User-Agent": user_agent,
        "Accept-Encoding": accept_encoding,
        "Referer": referer,
        "Accept-Language": accept_language,
        "Connection": connection,
        "Host": host,
    }

app.include_router(
    book_router,
    prefix=f"/api/{API_VERSION}",
    tags=["Books"],
)
