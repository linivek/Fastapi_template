from datetime import datetime, timezone
from typing import Dict

from fastapi import APIRouter

from app.utils.time import format_sydney_time, sydney_now, utc_now, utc_to_sydney

router = APIRouter()


@router.get("/")
async def get_time_info() -> Dict:
    """
    获取时间信息接口，展示UTC和悉尼时间
    """
    now_utc = utc_now()
    now_sydney = sydney_now()

    # 转换
    sydney_from_utc = utc_to_sydney(now_utc)

    return {
        "utc_time": now_utc,
        "sydney_time": now_sydney,
        "sydney_from_utc": sydney_from_utc,
        "formatted_sydney_time": format_sydney_time(now_utc),
        "timezone_info": {
            "utc_offset": now_sydney.utcoffset().total_seconds() / 3600,
            "utc_timezone": str(now_utc.tzinfo),
            "sydney_timezone": str(now_sydney.tzinfo),
        },
    }
