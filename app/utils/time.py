import zoneinfo
from datetime import datetime, timezone

# 澳大利亚悉尼时区
SYDNEY_TZ = zoneinfo.ZoneInfo("Australia/Sydney")


def utc_now():
    """
    获取当前UTC时间（带时区信息）
    """
    return datetime.now(timezone.utc)


def sydney_now():
    """
    获取当前悉尼时间（带时区信息）
    """
    return datetime.now(SYDNEY_TZ)


def utc_to_sydney(dt):
    """
    将UTC时间转换为悉尼时间
    如果输入时间没有时区信息，假设是UTC
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SYDNEY_TZ)


def sydney_to_utc(dt):
    """
    将悉尼时间转换为UTC时间
    如果输入时间没有时区信息，假设是悉尼时区
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=SYDNEY_TZ)
    return dt.astimezone(timezone.utc)


def format_sydney_time(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """
    将UTC时间转换为悉尼时间并格式化输出
    """
    sydney_time = utc_to_sydney(dt)
    return sydney_time.strftime(format_str)
