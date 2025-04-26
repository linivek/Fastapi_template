from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_current_user,
)
from app.core.config import settings
from app.core.security import create_access_token
from app.crud.user import user
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 兼容的令牌登录，获取访问令牌
    支持使用邮箱或用户名登录
    """
    user_obj = await user.authenticate_by_username_or_email(
        db, username_or_email=form_data.username, password=form_data.password
    )

    if not user_obj:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    elif not user.is_active(user_obj):
        raise HTTPException(status_code=400, detail="用户未激活")

    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user_obj.id, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    获取当前登录用户信息
    """
    return current_user


@router.get("/status", response_model=Dict[str, str])
async def check_auth_status(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    检查认证状态，任何认证用户都可访问
    """
    return {
        "status": "authenticated",
        "user_id": str(current_user.id),
        "username": current_user.username,
    }


@router.get("/admin", response_model=Dict[str, Any])
async def admin_only(
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    仅超级管理员可访问的接口
    """
    return {
        "message": "这是一个仅管理员可访问的API",
        "admin_user": {
            "id": str(current_user.id),
            "username": current_user.username,
            "email": current_user.email,
        },
    }
