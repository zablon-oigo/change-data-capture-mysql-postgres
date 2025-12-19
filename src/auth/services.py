from src.db.models import User
from .schemas import UserCreateModel
from .utils import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import uuid
from datetime import datetime


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        """Fetch a user by email."""
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
