from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import BookCreateModel, BookUpdateModel, BookReadModel
from .services import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker


access_token_bearer = AccessTokenBearer()
book_service = BookService()