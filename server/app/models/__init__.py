"""
SQLAlchemy 数据模型 — 按依赖顺序导入，避免关系解析失败
"""
from ..extensions import db
from .admin import AdminUser, OperationLog, PushRecord, PushTemplate
from .ai import AiConfig, AiTextRecord
from .checkin import CheckinRecord, DailyTaskConfig, GrowthGoalConfig

# 关系表（依赖上面的基础表）
from .common import PracticeRecord, RecommendConfig, UserFavorite
from .training import TrainingItem

# 基础表（无外键依赖）
from .user import User, UserQuota

# 集训打卡模块
from .jixun import JixunEvent, JixunSignup, JixunRecord  # noqa: F401
