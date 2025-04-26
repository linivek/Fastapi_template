from celery import Celery

from app.core.config import settings

# 使用配置文件中的设置初始化Celery
celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Celery配置
celery_app.conf.update(
    task_track_started=settings.CELERY_TASK_TRACK_STARTED,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    timezone=settings.TIME_ZONE,  # 使用悉尼时区
)

# 任务路由
celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
}


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    """
    测试Celery任务
    """
    return f"test task return {word}"
