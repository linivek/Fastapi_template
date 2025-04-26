# FastAPI 通用模板技术选型汇总

**核心框架与服务器:**

* **Web 框架:**  FastAPI
* **ASGI 服务器:**  Uvicorn (用于运行应用)
* **进程管理器 (生产):**  Gunicorn (用于管理 Uvicorn worker)

**数据库:**

* **数据库:**  PostgreSQL
* **ORM:**  SQLAlchemy (异步模式)
* **数据库迁移:**  Alembic

**认证与授权:**

* **协议:**  OAuth2 (具体实现: Password Bearer Flow)
* **令牌:**  JWT (JSON Web Tokens)
* **密码处理:**  Passlib

**异步处理:**

* **消息队列/缓存:**  Redis
* **后台任务队列:**  Celery (配合 Redis)

**配置管理:**

* **配置加载与校验:**  Pydantic (通过 Pydantic Settings)

**日志:**

* **日志库:**  Loguru (简洁易用，功能强大)

  *  *(替代方案:*  *​`structlog`​*​  *+ 标准* *​`logging`​*​ *，更侧重结构化输出)*

**测试:**

* **测试框架:**  Pytest
* **HTTP 客户端 (测试/外部调用):**  HTTPX (异步)

**代码质量与风格:**

* **格式化:**  Black
* **Import 排序:**  Isort
* **代码规范检查 (Linter):**  Flake8 (或考虑 Ruff 作为更快的替代方案)
* **提交前钩子:**  Pre-commit

**依赖管理:**

* **包管理器:**  Poetry

**容器化与部署:**

* **容器化:**  Docker
* **容器编排 (开发/本地):**  Docker Compose
