import calendar

from src.analytics.schemas import TotalTransactions
from src.database import database


async def get_recent_expense_income(
    user_id: str, start_date: str, end_date: str
) -> TotalTransactions:
    query = [
        {
            "$match": {
                "userId": user_id,
                "transactionDate": {"$gte": start_date, "$lte": end_date},
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {
                        "$year": {"$dateFromString": {"dateString": "$transactionDate"}}
                    },
                    "month": {
                        "$month": {
                            "$dateFromString": {"dateString": "$transactionDate"}
                        }
                    },
                    "type": "$type",
                },
                "totalAmount": {"$sum": "$amount"},
            }
        },
        {
            "$group": {
                "_id": {"year": "$_id.year", "month": "$_id.month"},
                "totals": {
                    "$push": {"type": "$_id.type", "totalAmount": "$totalAmount"}
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "expense": {
                    "$arrayElemAt": [
                        {
                            "$filter": {
                                "input": "$totals",
                                "as": "total",
                                "cond": {"$eq": ["$$total.type", "expense"]},
                            }
                        },
                        0,
                    ]
                },
                "income": {
                    "$arrayElemAt": [
                        {
                            "$filter": {
                                "input": "$totals",
                                "as": "total",
                                "cond": {"$eq": ["$$total.type", "income"]},
                            }
                        },
                        0,
                    ]
                },
            }
        },
        {
            "$project": {
                "year": 1,
                "month": 1,
                "totalExpense": {"$ifNull": ["$expense.totalAmount", 0]},
                "totalIncome": {"$ifNull": ["$income.totalAmount", 0]},
            }
        },
        {"$sort": {"year": 1, "month": 1}},
    ]

    cursor = database.transactions.aggregate(query)
    transactions = await cursor.to_list(length=None)

    recent_transactions = {"month": [], "data": {"income": [], "expense": []}}

    for transaction in transactions:
        month_name = calendar.month_name[transaction["month"]]
        recent_transactions["month"].append(month_name)
        recent_transactions["data"]["income"].append(transaction["totalIncome"])
        recent_transactions["data"]["expense"].append(-transaction["totalExpense"])

    return recent_transactions
