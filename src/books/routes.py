from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schemas import BookCreateModel, BookUpdateModel, BookReadModel
from .services import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker


access_token_bearer = AccessTokenBearer()
book_service = BookService()

user_or_admin_checker = RoleChecker(["admin", "user"])  
admin_checker = RoleChecker(["admin"])                

book_router = APIRouter(
    dependencies=[Depends(access_token_bearer)]
)

@book_router.get("/protected", dependencies=[Depends(user_or_admin_checker)])
async def protected_endpoint():
    return {"message": "You have access"}