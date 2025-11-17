from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime
from .schemas import BookCreateModel, BookUpdateModel
from src.db.models import Book


class BookService:
    async def get_all_books(self, session: AsyncSession):
        """Fetch all books, ordered by creation time (descending)."""
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        """Fetch a single book by UID."""
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        return result.first()

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        """Create a new book record."""
        new_book = Book(**book_data.model_dump())
        if isinstance(new_book.published_date, str):
            new_book.published_date = datetime.strptime(
                new_book.published_date, "%Y-%m-%d"
            )

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        return new_book
        
    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        """Update an existing book record."""
        book_to_update = await self.get_book(book_uid, session)

        if not book_to_update:
            return None

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(book_to_update, field, value)

        await session.commit()
        await session.refresh(book_to_update) 

        return book_to_update
