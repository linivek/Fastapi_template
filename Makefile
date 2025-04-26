# 定义一个变量，方便后续修改 Poetry 命令
POETRY = poetry run

# 从.env文件导出环境变量
include .env
export

# 代码格式化和 Linting 目标

# 使用 Black 格式化代码，使用 Isort 排序导入
format:
	@echo "运行 Black 格式化代码..."
	$(POETRY) black .
	@echo "运行 Isort 排序导入..."
	$(POETRY) isort .
	@echo "代码格式化和导入排序完成。"

# 使用 Flake8 检查代码风格和质量 (需要 .flake8 配置文件)
lint:
	@echo "运行 Flake8 检查代码风格和质量..."
	$(POETRY) flake8 .
	@echo "Flake8 检查完成。"

# 检查代码中的文件删除操作是否安全
check-file-safety:
	@echo "检查代码中是否存在危险的文件删除操作..."
	$(POETRY) flake8 --select=FPF .
	@echo "文件安全检查完成。"

# 一次运行所有代码质量检查
lint-all: format lint check-file-safety
	@echo "所有代码质量检查已完成。"

# 应用运行目标

# 使用 Gunicorn 在生产模式下运行 FastAPI 应用
# 需要在主依赖中安装 Gunicorn
run:
	@echo "使用 Gunicorn 在生产模式下启动 FastAPI 应用 (端口: $(SERVER_PORT))..."
	$(POETRY) gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind $(SERVER_HOST):$(SERVER_PORT) --log-level info
	@echo "FastAPI 应用已停止。"

# 使用指定端口运行应用 (用法: make run-port PORT=8080)
run-port:
	@echo "使用 Gunicorn 在生产模式下启动 FastAPI 应用 (端口: $(PORT))..."
	$(POETRY) gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind $(SERVER_HOST):$(PORT) --log-level info
	@echo "FastAPI 应用已停止。"

# 使用 Uvicorn 在开发模式下运行 FastAPI 应用
# 启用自动重载和 info 级别日志
dev:
	@echo "使用 Uvicorn 在开发模式下启动 FastAPI 应用 (端口: $(SERVER_PORT))..."
	$(POETRY) uvicorn app.main:app --reload --host $(SERVER_HOST) --port $(SERVER_PORT) --log-level info
	@echo "FastAPI 应用已停止。"

# 使用指定端口运行开发服务器 (用法: make dev-port PORT=8080)
dev-port:
	@echo "使用 Uvicorn 在开发模式下启动 FastAPI 应用 (端口: $(PORT))..."
	$(POETRY) uvicorn app.main:app --reload --host $(SERVER_HOST) --port $(PORT) --log-level info
	@echo "FastAPI 应用已停止。"

# 数据库迁移目标 (使用 Alembic)

# 根据模型变化创建新的迁移脚本
# 用法: make migrate-create message="你的迁移消息"
migrate-create:
	@echo "创建新的 Alembic 迁移脚本..."
	$(POETRY) alembic revision --autogenerate -m "$(message)"
	@echo "迁移脚本已创建。请检查并根据需要编辑。"

# 应用所有待处理的数据库迁移
migrate-up:
	@echo "应用待处理的数据库迁移..."
	$(POETRY) alembic upgrade head
	@echo "数据库迁移完成。"

# 回滚最后一次应用的数据库迁移
# 用法: make migrate-down step=-1 (默认为 -1)
migrate-down:
	@echo "回滚最后一次数据库迁移..."
	$(POETRY) alembic downgrade $(step:-1) # 如果未提供 step，默认为回滚一步
	@echo "数据库回滚完成。"

# 回滚所有数据库迁移到基础状态 (空的数据库 schema)
migrate-down-all:
	@echo "回滚所有数据库迁移到基础状态..."
	$(POETRY) alembic downgrade base
	@echo "数据库已回滚到基础状态。"


# 声明伪目标 (不是实际文件的目标)
.PHONY: format lint check-file-safety lint-all run run-port dev dev-port migrate-create migrate-up migrate-down migrate-down-all
