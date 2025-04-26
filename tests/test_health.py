import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """
    测试健康检查接口
    """
    response = await client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Service is running"}


@pytest.mark.asyncio
async def test_db_health_check(client: AsyncClient) -> None:
    """
    测试数据库健康检查接口
    """
    response = await client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
