from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        通过email获取用户
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_by_username(
        self, db: AsyncSession, *, username: str
    ) -> Optional[User]:
        """
        通过username获取用户
        """
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        创建用户
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        """
        更新用户
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        """
        通过邮箱验证用户
        """
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def authenticate_by_username(
        self, db: AsyncSession, *, username: str, password: str
    ) -> Optional[User]:
        """
        通过用户名验证用户
        """
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def authenticate_by_username_or_email(
        self, db: AsyncSession, *, username_or_email: str, password: str
    ) -> Optional[User]:
        """
        通过用户名或邮箱验证用户
        """
        # 先尝试邮箱验证
        user = await self.authenticate(db, email=username_or_email, password=password)
        if user:
            return user

        # 尝试用户名验证
        return await self.authenticate_by_username(
            db, username=username_or_email, password=password
        )

    def is_active(self, user: User) -> bool:
        """
        检查用户是否激活
        """
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """
        检查用户是否是超级用户
        """
        return user.is_superuser


user = CRUDUser(User)
