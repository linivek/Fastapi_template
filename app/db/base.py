# 导入所有模型，以便Alembic可以检测到它们
from app.db.base_class import Base

# 导入所有模型文件
from app.models.user import User

# 从这里添加更多模型，例如：
# from app.models.item import Item
