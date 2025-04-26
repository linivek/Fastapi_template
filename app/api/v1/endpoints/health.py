from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "ok", "message": "Service is running"}


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    数据库健康检查接口
    """
    try:
        # 简单查询测试数据库连接
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database connection is healthy"}
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
