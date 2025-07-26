import hashlib
import math
from datetime import datetime, timedelta
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


def pagination_aggregate(page: int, limit: int) -> Dict[str, Any]:
    skip = limit * (page - 1)
    return {
        "metadata": [
            {"$count": "totalData"},
            {
                "$project": {
                    "totalData": 1,
                    "totalPage": {
                        "$toInt": {"$ceil": {"$divide": ["$totalData", limit]}}
                    },
                    "previousPage": {
                        "$cond": {
                            "if": {"$lte": [page, 1]},
                            "then": None,
                            "else": {"$subtract": [page, 1]},
                        }
                    },
                    "currentPage": {
                        "$cond": {
                            "if": {"$eq": [page, 1]},
                            "then": 1,
                            "else": {"$toInt": {"$ceil": {"$divide": [page, 1]}}},
                        }
                    },
                    "nextPage": {
                        "$cond": {
                            "if": {
                                "$lte": [
                                    {"$add": [page, 1]},
                                    {
                                        "$toInt": {
                                            "$ceil": {"$divide": ["$totalData", limit]}
                                        }
                                    },
                                ]
                            },
                            "then": {"$add": [page, 1]},
                            "else": None,
                        }
                    },
                }
            },
        ],
        "data": [{"$skip": skip}, {"$limit": limit}],
    }


def month_year_transactions(month_year: str) -> Dict[str, str]:
    month, year = month_year.split("/")
    start_date = datetime(int(year), int(month), 1)
    end_date = datetime(int(year), int(month) + 1, 1) - timedelta(microseconds=1)

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return {"$gte": start_date_str, "$lte": end_date_str}


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
