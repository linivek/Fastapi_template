FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry==1.4.2

# 复制项目文件
COPY poetry.lock pyproject.toml /app/
COPY . /app/

# 配置Poetry不创建虚拟环境
RUN poetry config virtualenvs.create false

# 安装依赖
RUN poetry install --no-dev

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"] 