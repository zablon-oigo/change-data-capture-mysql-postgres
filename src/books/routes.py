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


@book_router.get("/", response_model=list[BookReadModel], status_code=status.HTTP_200_OK)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(user_or_admin_checker) 
):
    books = await book_service.get_all_books(session)
    return books



@book_router.get("/{book_uid}", response_model=BookReadModel, status_code=status.HTTP_200_OK)
async def get_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(user_or_admin_checker)
):
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@book_router.post("/", response_model=BookReadModel, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreateModel, 
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(admin_checker)  
):
    new_book = await book_service.create_book(book_data, session)
    return new_book
