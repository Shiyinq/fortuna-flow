from src.database import database


async def aggregate_budgets(pipeline, length=None):
    return await database["budgets"].aggregate(pipeline).to_list(length=length)


async def insert_budget(budget_data: dict):
    return await database["budgets"].insert_one(budget_data)


async def update_budget_db(query: dict, update_dict: dict):
    return await database["budgets"].update_one(query, {"$set": update_dict})


async def delete_budget_db(query: dict):
    return await database["budgets"].delete_one(query)
