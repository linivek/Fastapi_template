# FastAPI 通用模板项目

基于 FastAPI 的现代化后端应用程序通用模板，集成了企业级应用开发所需的各种组件和最佳实践。

## 特性

- ✅ **FastAPI** - 快速高效的现代 Python API 框架
- ✅ **异步 SQLAlchemy** - 完全异步的 ORM 支持
- ✅ **PostgreSQL** - 强大的关系型数据库
- ✅ **Alembic** - 数据库迁移工具
- ✅ **Pydantic V2** - 强大的数据验证
- ✅ **JWT 认证** - 基于 JWT 的安全认证
- ✅ **UUID 主键** - 使用 UUID 作为主键代替自增 ID
- ✅ **时区处理** - 内置澳大利亚悉尼时区支持
- ✅ **Celery** - 后台任务处理
- ✅ **Redis** - 高性能缓存和消息代理
- ✅ **Docker** - 容器化部署支持
- ✅ **Pytest** - 全面的测试支持
- ✅ **Poetry** - 现代 Python 依赖管理
- ✅ **Loguru** - 更友好的日志系统
- ✅ **预配置环境变量** - 环境变量控制的配置系统
- ✅ **自动初始化超级用户** - 应用启动时自动创建超级用户

## 项目结构

```
.
├── alembic/                     # 数据库迁移配置
├── app/                         # 应用程序代码
│   ├── api/                     # API路由
│   │   ├── deps.py              # 依赖项（认证等）
│   │   └── v1/                  # API v1版本
│   │       ├── api.py           # API路由注册
│   │       └── endpoints/       # 各个端点实现
│   │           ├── health.py    # 健康检查接口
│   │           └── time_demo.py # 时区演示接口
│   ├── core/                    # 核心模块
│   │   ├── config.py            # 配置管理
│   │   ├── security.py          # 安全工具
│   │   ├── logging.py           # 日志配置
│   │   └── init_app.py          # 应用初始化
│   ├── crud/                    # CRUD操作
│   │   ├── base.py              # 基础CRUD类
│   │   └── user.py              # 用户CRUD操作
│   ├── db/                      # 数据库设置
│   │   ├── base.py              # 导入所有模型
│   │   ├── base_class.py        # 基础模型类
│   │   └── session.py           # 会话管理
│   ├── models/                  # SQLAlchemy模型
│   │   └── user.py              # 用户模型
│   ├── schemas/                 # Pydantic模型
│   │   └── user.py              # 用户Schema
│   ├── services/                # 服务层
│   ├── utils/                   # 工具函数
│   │   └── time.py              # 时区处理工具
│   ├── worker.py                # Celery配置
│   └── main.py                  # 应用入口
├── tests/                       # 测试代码
│   ├── conftest.py              # 测试配置
│   └── test_health.py           # 健康检查测试
├── .env                         # 开发环境变量
├── .env.example                 # 环境变量示例
├── docker-compose.yml           # Docker Compose配置
├── Dockerfile                   # Docker配置
├── pyproject.toml               # Poetry依赖管理
├── .pre-commit-config.yaml      # 预提交钩子配置
├── .gitignore                   # Git忽略文件配置
└── README.md                    # 项目文档
```

## 快速开始

### 环境要求

- Python 3.9+
- PostgreSQL 13+
- Redis 6+

### 使用 Docker Compose

最简单的启动方式是使用 Docker Compose:

1. 克隆项目

```bash
git clone https://your-repository-url/fastapi-template.git
cd fastapi-template
```

2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件以适应您的环境
```

3. 启动所有服务

```bash
docker-compose up -d
```

4. 访问接口文档

```
http://localhost:8000/docs
```

### 本地开发环境

1. 克隆项目

```bash
git clone https://your-repository-url/fastapi-template.git
cd fastapi-template
```

2. 安装依赖

```bash
# 安装 Poetry
pip install poetry

# 安装依赖
poetry install
```

3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件以适应您的环境
```

4. 运行数据库迁移

```bash
poetry run alembic upgrade head
```

5. 启动应用

```bash
poetry run uvicorn app.main:app --reload
```

## 核心功能说明

### 环境变量配置

本模板使用 `.env` 文件进行配置，主要配置项包括：

- **项目设置** - 项目名称、API 前缀
- **服务器设置** - 主机地址、端口
- **安全设置** - JWT 密钥、算法、令牌过期时间
- **数据库设置** - PostgreSQL 连接信息
- **Redis 设置** - Redis 服务器信息
- **Celery 配置** - 后台任务配置
- **超级用户配置** - 初始超级用户信息
- **时区配置** - 默认为澳大利亚悉尼时区

详细配置请参考 `.env.example` 文件。

### 数据库迁移

使用 Alembic 进行数据库迁移:

```bash
# 创建迁移
poetry run alembic revision --autogenerate -m "迁移描述"

# 应用迁移
poetry run alembic upgrade head

# 回滚迁移
poetry run alembic downgrade -1
```

### UUID 主键

本模板使用 UUID 作为用户表主键，相比自增 ID 有如下优势：

- 全局唯一性，避免 ID 冲突
- 更高的安全性，难以猜测
- 适合分布式系统

实现位于 `app/models/user.py`，使用 PostgreSQL 原生 UUID 类型。

### 时区处理

本模板提供了完整的时区处理支持，默认使用澳大利亚悉尼时区：

- 在数据库中存储 UTC 时间（带时区信息）
- API 响应中自动转换为悉尼时区
- 提供时区转换工具函数 `app/utils/time.py`
- 包含时间转换演示接口 `/api/v1/time`

### JWT 认证

内置完整的 JWT 认证支持：

- 安全的密码哈希处理
- 基于角色的访问控制
- 刷新令牌支持
- 依赖项注入认证中间件

### Celery 后台任务

集成 Celery 用于处理后台任务：

- 与 Redis 消息代理集成
- 自动同步悉尼时区设置
- 通过 docker-compose 配置 Celery Worker 和 Flower 监控

### 自动初始化超级用户

应用首次启动时自动检查并创建超级用户：

- 通过环境变量配置超级用户信息
- 只在数据库中不存在超级用户时创建
- 可完全自定义超级用户信息

### 依赖注入系统

利用 FastAPI 的依赖注入系统提供：

- 数据库会话
- 当前用户获取
- 权限检查
- 各种共用组件

## API 文档

启动应用后，可通过以下地址访问自动生成的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试

本模板包含完整的测试框架：

```bash
# 运行所有测试
poetry run pytest

# 生成测试覆盖率报告
poetry run pytest --cov=app --cov-report=html
```

## 开发最佳实践

### 添加新的 API 端点

1. 在 `app/api/v1/endpoints/` 创建新文件
2. 在 `app/api/v1/api.py` 注册路由
3. 创建相应的模型、Schema 和 CRUD 操作

### 添加新的数据模型

1. 在 `app/models/` 创建新模型文件
2. 在 `app/db/base.py` 导入新模型
3. 创建对应的 Pydantic Schema
4. 实现 CRUD 操作

### 代码风格指南

本项目采用以下代码风格：

- **Black** - 自动格式化代码
- **isort** - 导入排序
- **Flake8** - 代码规范检查

在提交代码前，请确保代码符合风格要求：

```bash
# 自动格式化代码
poetry run black app tests
poetry run isort app tests

# 规范检查
poetry run flake8 app tests
```

## 部署指南

### Docker 部署

最推荐的部署方式是使用 Docker Compose:

```bash
# 生产环境部署
docker-compose -f docker-compose.yml up -d
```

### 传统部署

1. 安装 Python 和依赖
2. 配置环境变量
3. 运行数据库迁移
4. 使用 Gunicorn 和 Uvicorn worker 启动应用

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 贡献指南

我们欢迎任何形式的贡献！如果您发现了 bug 或有新功能建议，请先查看 issues 列表。

提交 Pull Request 前，请确保：

1. 代码符合项目风格指南
2. 添加必要的测试
3. 通过现有测试
4. 更新相关文档

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如有任何问题或建议，请联系项目维护者：

- 邮箱: your.email@example.com
- GitHub: [您的 GitHub 用户名](https://github.com/yourusername) 