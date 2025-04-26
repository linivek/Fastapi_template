import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.config import settings
from app.db.base import Base
from app.main import app

# 使用测试数据库URL
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"
)

# 创建测试引擎和会话
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    创建事件循环
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator:
    """
    会话依赖覆盖
    """
    # 创建表
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 运行测试
    async with TestSessionLocal() as session:
        yield session

    # 清理
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def db_session(db: AsyncSession) -> AsyncGenerator:
    """
    为每个测试函数获取一个新会话
    """
    async with db.begin():
        yield db
        await db.rollback()


# 依赖覆盖
async def override_get_db() -> AsyncGenerator:
    """
    数据库依赖覆盖
    """
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator:
    """
    测试客户端
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
