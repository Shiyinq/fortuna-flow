import math
from typing import Any, Dict


def pagination(total: int, page: int, limit: int) -> Dict[str, Any]:
    total_pages = math.ceil(total / limit)
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    return {
        "page": page,
        "limit": limit,
        "prevPage": prev_page,
        "nextPage": next_page,
        "totalPage": total_pages,
    }
