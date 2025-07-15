from typing import Any, Dict, Optional
from uuid import UUID
from src.budgets.schemas import BudgetCreate, BudgetUpdate
from src.budgets.exceptions import BudgetNotFound
from datetime import datetime, timedelta
import calendar
from collections import defaultdict
from operator import itemgetter
from src.budgets.constants import Info
from src.budgets import repository

async def get_budgets(user_id: str, wallet_id: Optional[str] = None) -> Dict[str, Any]:
    now = datetime.now()
    first_day = now.replace(day=1).strftime('%Y-%m-%d')
    match_query = {"userId": user_id, "endDate": {"$gte": first_day}}
    if wallet_id:
        match_query["walletId"] = wallet_id
    pipeline = [
        {"$match": match_query},
        {"$sort": {"createdAt": -1}},
        {"$lookup": {
            "from": "categories",
            "localField": "categoryId",
            "foreignField": "categoryId",
            "as": "category"
        }},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"icon": "$category.categoryIcon"}},
        {"$lookup": {
            "from": "transactions",
            "let": {"catId": "$categoryId", "uid": "$userId", "wid": "$walletId"},
            "pipeline": [
                {"$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": ["$categoryId", "$$catId"]},
                            {"$eq": ["$userId", "$$uid"]},
                            {"$eq": ["$walletId", "$$wid"]}
                        ]
                    }
                }}
            ],
            "as": "transactions"
        }},
        {"$addFields": {"totalSpent": {"$sum": "$transactions.amount"}}},
        {"$project": {"_id": 0, "category": 0, "transactions": 0}}
    ]
    budgets = await repository.aggregate_budgets(pipeline)

    ordered_keys = ["this_month", "this_week"]
    custom_groups = []
    grouped = {}
    temp_custom = []
    for budget in budgets:
        if budget.get("type") == "custom":
            key = f"{budget.get('startDate')}/{budget.get('endDate')}"
            temp_custom.append((key, budget))
        else:
            key = budget.get("type")
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(budget)

    custom_sorted = sorted(temp_custom, key=lambda x: x[0])
    custom_grouped = {}
    for key, budget in custom_sorted:
        if key not in custom_grouped:
            custom_grouped[key] = []
        custom_grouped[key].append(budget)

    result = {}
    for key in ordered_keys:
        if key in grouped:
            result[key] = {
                "totalBudget": sum(b["amount"] for b in grouped[key]),
                "datas": grouped[key]
            }
    for key in custom_grouped:
        result[key] = {
            "totalBudget": sum(b["amount"] for b in custom_grouped[key]),
            "datas": custom_grouped[key]
        }
    return result

async def get_budget(budget_id: str, user_id: str) -> Dict[str, Any]:
    pipeline = [
        {"$match": {"budgetId": budget_id, "userId": user_id}},
        {"$lookup": {
            "from": "categories",
            "localField": "categoryId",
            "foreignField": "categoryId",
            "as": "category"
        }},
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {"icon": "$category.categoryIcon"}},
        {"$lookup": {
            "from": "transactions",
            "let": {"catId": "$categoryId", "uid": "$userId", "wid": "$walletId"},
            "pipeline": [
                {"$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": ["$categoryId", "$$catId"]},
                            {"$eq": ["$userId", "$$uid"]},
                            {"$eq": ["$walletId", "$$wid"]}
                        ]
                    }
                }}
            ],
            "as": "transactions"
        }},
        {"$addFields": {"totalSpent": {"$sum": "$transactions.amount"}}},
        {"$project": {"_id": 0, "category": 0, "transactions": 0}}
    ]
    result = await repository.aggregate_budgets(pipeline, length=1)
    if not result:
        raise BudgetNotFound
    return result[0]

async def create_budget(budget: BudgetCreate) -> Dict[str, Any]:
    now = datetime.now()
    if budget.type == 'this_month':
        start = now.replace(day=1)
        last_day = calendar.monthrange(now.year, now.month)[1]
        end = now.replace(day=last_day)
        budget.startDate = start.strftime('%Y-%m-%d')
        budget.endDate = end.strftime('%Y-%m-%d')
    elif budget.type == 'this_week':
        start = now
        end = now + timedelta(days=6)
        budget.startDate = start.strftime('%Y-%m-%d')
        budget.endDate = end.strftime('%Y-%m-%d')
    await repository.insert_budget(budget.to_dict())
    return {"detail": Info.BUDGET_CREATED}

async def update_budget(budget_id: str, user_id: str, update_data: BudgetUpdate) -> Dict[str, Any]:
    now = datetime.now()
    update_dict = update_data.to_dict()
    t = update_dict.get('type')
    if t == 'this_month':
        start = now.replace(day=1)
        last_day = calendar.monthrange(now.year, now.month)[1]
        end = now.replace(day=last_day)
        update_dict['startDate'] = start.strftime('%Y-%m-%d')
        update_dict['endDate'] = end.strftime('%Y-%m-%d')
    elif t == 'this_week':
        start = now
        end = now + timedelta(days=6)
        update_dict['startDate'] = start.strftime('%Y-%m-%d')
        update_dict['endDate'] = end.strftime('%Y-%m-%d')
    result = await repository.update_budget_db(
        {"budgetId": budget_id, "userId": user_id},
        update_dict
    )
    if result.matched_count == 0:
        raise BudgetNotFound
    return {"detail": Info.BUDGET_UPDATED}

async def delete_budget(budget_id: str, user_id: str) -> Dict[str, Any]:
    result = await repository.delete_budget_db({"budgetId": budget_id, "userId": user_id})
    if result.deleted_count == 0:
        raise BudgetNotFound
    return {"detail": Info.BUDGET_DELETED} 