from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from src.books.schemas import BookReadModel  

from .schemas import TagAddModel, TagCreateModel, TagModel
from .services import TagService
