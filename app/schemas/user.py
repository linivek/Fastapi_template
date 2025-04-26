import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_serializer

from app.utils.time import utc_to_sydney


# 共享属性
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# 创建用户时的属性
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str


# 更新用户时的属性
class UserUpdate(UserBase):
    password: Optional[str] = None


# 数据库中存储的用户属性
class UserInDBBase(UserBase):
    id: UUID
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime, _info):
        """将UTC时间转换为悉尼时间"""
        return utc_to_sydney(dt)

    class Config:
        orm_mode = True
        from_attributes = True


# 返回给API的用户信息
class User(UserInDBBase):
    pass


# 存储在数据库中的用户信息，包含敏感字段
class UserInDB(UserInDBBase):
    hashed_password: str


# 令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str


# 令牌数据
class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
