from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.init_app import init_app
from app.db.session import AsyncSessionLocal, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    async with AsyncSessionLocal() as db:
        await init_app(db)
    yield
    # 关闭事件（如果需要）


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="""
    FastAPI Template 项目 API 文档

    ## 认证
    使用以下方式进行API认证:
    * 可以使用用户名 `admin` 或邮箱 `admin@example.com` 登录（密码: `admin`）
    * 登录后获取JWT令牌，用于访问需要认证的接口

    ## 健康检查
    * `/api/v1/health` - 检查API服务状态
    * `/api/v1/health/db` - 检查数据库连接状态
    """,
    version="0.1.0",
    lifespan=lifespan,
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


def custom_openapi():
    """
    自定义OpenAPI文档
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description=app.description,
        routes=app.routes,
    )

    # 添加认证Schema示例
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": f"{settings.API_V1_STR}/auth/login",
                    "scopes": {},
                }
            },
        }
    }

    # 添加安全要求
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Template Project"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
