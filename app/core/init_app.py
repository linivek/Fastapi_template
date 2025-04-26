import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_password_hash
from app.crud.user import user
from app.schemas.user import UserCreate

# 导入相关模型和CRUD
# 以下导入会根据实际的用户模型实现来修改
# from app.crud.user import user
# from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


async def init_superuser(db: AsyncSession) -> None:
    """
    初始化超级用户
    只有在未找到超级用户时才会创建
    """
    # 检查是否需要创建超级用户
    if not all(
        [
            settings.FIRST_SUPERUSER_EMAIL,
            settings.FIRST_SUPERUSER_USERNAME,
            settings.FIRST_SUPERUSER_PASSWORD,
        ]
    ):
        logger.info("超级用户配置不完整，跳过创建")
        return

    try:
        # 检查超级用户是否已存在
        superuser = await user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if superuser:
            logger.info("超级用户已存在，跳过创建")
            return

        # 创建超级用户
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            username=settings.FIRST_SUPERUSER_USERNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        superuser = await user.create(db, obj_in=user_in)
        logger.info(f"创建超级用户成功: {superuser.email}")

    except Exception as e:
        logger.error(f"创建超级用户失败: {e}")


async def init_app(db: AsyncSession) -> None:
    """
    应用程序初始化
    包括创建超级用户、初始数据等
    """
    await init_superuser(db)
