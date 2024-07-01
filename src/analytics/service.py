import calendar
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from src.analytics.schemas import TotalTransactions
from src.database import database


def generate_month_pairs():
    current_date = datetime.now()
    pairs = []
    for i in range(0, 12, 3):
        end_date = (current_date - relativedelta(months=i)).strftime("%Y-%m")
        start_date = (current_date - relativedelta(months=i+2)).strftime("%Y-%m")
        pairs.append((start_date, end_date))
    return pairs


def process_data(data, month_pairs):
    results = []
    for start_date, end_date in month_pairs:
        start_date_obj = datetime.strptime(start_date, "%Y-%m")
        end_date_obj = datetime.strptime(end_date, "%Y-%m")
        
        combined_transactions = []
        total_amount = 0
        total_count = 0
        
        for item in data:
            item_date = datetime.strptime(item['month'], "%Y-%m")
            if start_date_obj <= item_date <= end_date_obj:
                combined_transactions.extend(item['transactions'])
                total_amount += item['totalAmount']
                total_count += item['totalCount']

        combined_transactions.sort(key=lambda x: parse(x['date']))
        
        result = {
            'startDate': start_date,
            'endDate': end_date,
            'totalAmount': total_amount,
            'totalCount': total_count,
            'transactions': combined_transactions
        }
        results.append(result)
    
    return results


async def get_activities(user_id: str):
    query = [
        {
            '$match': {
                'userId': user_id
            }
        }, {
            '$group': {
                '_id': '$transactionDate', 
                'dailyAmount': {
                    '$sum': '$amount'
                }, 
                'dailyCount': {
                    '$sum': 1
                }
            }
        }, {
            '$group': {
                '_id': {
                    'year': {
                        '$year': {
                            '$dateFromString': {
                                'dateString': '$_id'
                            }
                        }
                    }, 
                    'month': {
                        '$month': {
                            '$dateFromString': {
                                'dateString': '$_id'
                            }
                        }
                    }
                }, 
                'transactions': {
                    '$push': {
                        'date': '$_id', 
                        'value': '$dailyCount', 
                        'amount': '$dailyAmount'
                    }
                }, 
                'totalAmount': {
                    '$sum': '$dailyAmount'
                }, 
                'totalCount': {
                    '$sum': '$dailyCount'
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'month': {
                    '$concat': [
                        {
                            '$toString': '$_id.year'
                        }, '-', {
                            '$cond': [
                                {
                                    '$lt': [
                                        '$_id.month', 10
                                    ]
                                }, {
                                    '$concat': [
                                        '0', {
                                            '$toString': '$_id.month'
                                        }
                                    ]
                                }, {
                                    '$toString': '$_id.month'
                                }
                            ]
                        }
                    ]
                }, 
                'transactions': 1, 
                'totalAmount': 1, 
                'totalCount': 1
            }
        }, {
            '$sort': {
                'month': -1
            }
        }
    ]

    cursor = database.transactions.aggregate(query)
    transactions = await cursor.to_list(length=None)

    month_pairs = generate_month_pairs()
    processed_data = process_data(transactions, month_pairs)

    return processed_data

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
