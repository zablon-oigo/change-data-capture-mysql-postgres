from fastapi import FastAPI, Header, status, Request
from typing import Optional
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from src.db.main import initdb
from src.db.redis import init_redis
from src.errors import BookException
from fastapi.responses import JSONResponse
from src.errors import register_error_handlers
from src.middleware import register_middleware

version = "v1"
version_prefix ="/api/{version}"

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
    version=version,
    lifespan=lifespan,
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)

register_error_handlers(app)
register_middleware(app)

@app.exception_handler(BookException)
async def book_exception_handler(request: Request, exc: BookException):
    return JSONResponse(
        status_code=getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST),
        content={"detail": getattr(exc, "detail", "An error occurred")},
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
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
app.include_router(book_router, prefix=f"{version_prefix}/books", tags=["Books"])
app.include_router(review_router, prefix=f"{version_prefix}/reviews", tags=["Reviews"])
app.include_router(tags_router, prefix=f"{version_prefix}/tags", tags=["Tags"])
