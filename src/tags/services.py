from fastapi import status, HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.services import BookService
from src.db.models import Tag

from .schemas import TagAddModel, TagCreateModel

book_service = BookService()


class TagService: