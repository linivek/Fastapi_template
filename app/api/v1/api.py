from fastapi import APIRouter

from app.api.v1.endpoints import health, time_demo

api_router = APIRouter()

# 健康检查路由
api_router.include_router(health.router, prefix="/health", tags=["health"])

# 时间演示路由
api_router.include_router(time_demo.router, prefix="/time", tags=["time"])

# 添加其他路由，例如：
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
