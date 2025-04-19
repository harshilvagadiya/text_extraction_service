from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy import select
from src.models.db.user import User
from src.repository.crud.base import BaseCRUDRepository
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.common.password import hash_password, verify_password
from src.utilities.exceptions.exceptions import (
    EntityAlreadyExistsException,
    EntityDoesNotExistException,
)


class AccountCRUDRepository(BaseCRUDRepository):
    async def find_one(self, filters: dict) -> Optional[User]:
        
        if not filters:
            raise ValueError("Filters cannot be empty.")

        stmt = select(User)

        for key, value in filters.items():
            column = getattr(User, key, None)
            if column is None:
                raise ValueError(f"Invalid column name: {key}")
            stmt = stmt.where(column == value)

        result = await self.async_session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def create_account(
        self, email: str, password: str
    ) -> User:
        hashed_password = hash_password(password)

        new_user = User(
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
        )

        self.async_session.add(new_user)
        await self.async_session.commit()
        await self.async_session.refresh(new_user)
        return new_user
    
    async def find_one_without_error(
        self, filters: dict
    ) -> Optional[User]:
        if not filters:
            raise ValueError("Filters cannot be empty.")

        stmt = select(User)

        for key, value in filters.items():
            column = getattr(User, key, None)
            if column is None:
                raise ValueError(f"Invalid column name: {key}")
            stmt = stmt.where(column == value)

        result = await self.async_session.execute(stmt)
        return result.scalar_one_or_none()

    async def authenticate_and_generate_token(
        self, email: str, password: str
    ) -> tuple[User, str, str]:
       
        user = await self.find_one(filters={"email": email})

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        access_token = jwt_generator.generate_access_token(user)
        refresh_token = jwt_generator.generate_refresh_token(user)

        return user, access_token, refresh_token

    async def update_password(self, email: str, new_password: str) -> User:
       
        user = await self.find_one(filters={"email": email})
        if not user:
            raise EntityDoesNotExistException("User not found.")

        user.hashed_password = hash_password(new_password)

        self.async_session.add(user)
        await self.async_session.commit()
        await self.async_session.refresh(user)
        return user
