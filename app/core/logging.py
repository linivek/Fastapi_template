import logging
import sys
from pathlib import Path
from typing import List, Optional

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    将标准库logging输出拦截到loguru
    """

    def emit(self, record):
        # 获取相应的loguru级别
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 获取调用信息
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    json_logs: bool = False,
    log_modules: List[str] = None,
) -> None:
    """
    配置日志，将标准库logging和第三方库的日志一并定向到loguru
    """
    # 移除所有默认的处理器
    logger.remove()
    # 添加标准输出处理器
    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=True,
        level=log_level.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        serialize=json_logs,
    )
    # 如果指定了日志文件，则添加文件处理器
    if log_file:
        logger.add(
            log_file,
            rotation="10 MB",
            retention="7 days",
            enqueue=True,
            backtrace=True,
            level=log_level.upper(),
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            serialize=json_logs,
        )

    # 配置标准库的logging -> loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # 将所需模块的日志重定向到loguru
    modules = log_modules or ["uvicorn", "uvicorn.error", "fastapi"]
    for module in modules:
        logging.getLogger(module).handlers = [InterceptHandler()]

    # 设置默认的logger
    logger.configure(handlers=[{"sink": sys.stderr, "level": log_level.upper()}])
