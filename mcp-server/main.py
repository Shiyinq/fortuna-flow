import json
from mcp.server.fastmcp import FastMCP

from request import fortuna_get, fortuna_post, fortuna_put, fortuna_delete

mcp = FastMCP("MCP Server Fortuna Flow")

# Wallets
@mcp.tool()
async def get_total_balance() -> str:
    """Get total balance."""

    endpoint = "wallets/total-balance"
    data = await fortuna_get(endpoint)

    if not data:
        return "Unable to fetch total balance."

    balance = data["totalBalance"]
    response = f"Your total balance is {balance}"
    return response

@mcp.tool()
async def get_wallets(page: int = 1, limit: int = 10) -> str:
    """Get a paginated list of wallets for the current user.

    Args:
        page: to acces more data if page more than 1, default page is 1
        limit: limit total data in page, default limit is 10
    """

    endpoint = "wallets"
    data = await fortuna_get(endpoint, params={"page": page, "limit": limit})

    if not data:
        return "Unable to fetch wallets"

    return json.dumps(data)

@mcp.tool()
async def get_wallet(wallet_id: str) -> str:
    """Get a specific wallet by its ID for the current user.

    Args:
        wallet_id: wallet id as string, use get_wallets to chechk wallet id
    """

    endpoint = f"wallets/{wallet_id}"
    data = await fortuna_get(endpoint)

    if not data:
        return "Unable to fetch wallet"

    return json.dumps(data)

@mcp.tool()
async def get_wallet_transaction(wallet_id: str, month_year: str, page: int = 1, limit: int = 32) -> str:
    """Get all transactions from a specific wallet for the current user, with pagination and month/year filter.

    Args:
        wallet_id: wallet id as string, use get_wallets to chechk wallet id or you can ask user for detail
        month_year: example 07/2025, please use current month & year if user not provide speific info
        page: to acces more data if page more than 1, default page is 1
        limit: limit total data in page, default limit is 32
    """

    endpoint = f"wallets/{wallet_id}/transactions"
    data = await fortuna_get(endpoint, params={"page": page, "limit": limit, "month_year": month_year})

    if not data:
        return "Unable to fetch wallet transaction"

    return json.dumps(data)


@mcp.tool()
async def create_wallet(wallet_icon: str, balance: int, name: str) -> str:
    """Create a new wallet for the current user.
        Args:
            walletIcon: icon of the wallet, ask user for spesific emoji or decide your own
            balance: initial balance of the wallet
            name: name of the wallet
    """

    endpoint = "wallets"
    data = await fortuna_post(endpoint, data={"walletIcon": wallet_icon, "balance": balance, "name": name})

    if not data:
        return "Unable to create wallet"
    
    return json.dumps(data)


# Categories
@mcp.tool()
async def get_categories(page: int = 1, limit: int = 10) -> str:
    """Get a paginated list of categories for the current user.

    Args:
        page: page number for pagination (default: 1)
        limit: number of items per page (default: 10)

    Returns:
        CategoriesResponse: Metadata and list of categories
    """
    endpoint = "categories"
    data = await fortuna_get(endpoint, params={"page": page, "limit": limit})
    
    if not data:
        return "Unable to fetch categories"
    
    return json.dumps(data)

@mcp.tool()
async def create_category(name: str, caregory_icon: str, type: str = "expense") -> str:
    """Add a new custom category for the current user.

    Args:
        name: name of the category
        category_icon: icon for the category (emoji or icon name) ask user or decide your own
        type: category type chose expense or income, default: expense
    """
    endpoint = "categories"
    data = {
        "name": name,
        "categoryIcon": caregory_icon,
        "type": type
    }
    
    data = await fortuna_post(endpoint, data=data)
    
    if not data:
        return "Unable to create category"
    
    return json.dumps(data)

# Transactions
@mcp.tool()
async def get_recent_transactions(limit: int = 5) -> str:
    """Get a list of the most recent transactions for the current user.

    Args:
        limit: maximum number of transactions to return (default: 5)
    """

    endpoint = "transactions/recent"
    data = await fortuna_get(endpoint, params={"limit": limit})

    if not data:
        return "Unable to fetch recent transactions."

    return json.dumps(data)

@mcp.tool()
async def get_transactions(month_year: str, page: int = 1, limit: int = 32) -> str:
    """Get list of all transactions for the current user in a specific month and year for all wallets.

    Args:
        month_year: example 07/2025, please use current month & year if user not provide speific info
        page: to acces more data if page more than 1, default page is 1
        limit: limit total data in page, default limit is 32
    """

    endpoint = "transactions"
    data = await fortuna_get(endpoint, params={"page": page, "limit": limit, "month_year": month_year})

    if not data:
        return "Unable to fetch transactions."

    return json.dumps(data)

@mcp.tool()
async def create_transaction(amount: int, category_id: str, wallet_id: str, note: str, transaction_date: str, type: str = "expense") -> str:
    """Create a new transaction for the current user.

    Args:
        amount: total expense or income in integer
        category_id: category id for transaction, aks user for cateogry and then check use get_categories to find category id if not exist create one and get_cateogries again, make sure category id is exist
        note: transaction info ask user for detail or decide your own
        transaction_date: date of transaction in format year-month-date like (2023-07-10), ask user for detail
        type: ask user for detail type of transaction or decide your own default: expense
        wallet_id: wllet id for transaction ask user for wallet name and then check use get_wallets to find wallet id if not exist create one and get_wallets again, make sure wallet id is exist
    """
    endpoint = "transactions"
    data = {
        "walletId": wallet_id,
        "categoryId": category_id,
        "amount": amount,
        "note": note,
        "transactionDate": transaction_date,
        "type": type
    }

    data = await fortuna_post(endpoint, data=data)
    
    if not data:
        return "Unable to create transaction"
    
    return json.dumps(data)

@mcp.tool()
async def update_transaction(transaction_id: str, amount: int, category_id: str, note: str, transaction_date: str, type: str = "expense") -> str:
    """Update transaction for the current user.

    Args:
        transaction_id: transaction id use get_recent_transactions or get_transactions to find transaction id, make sure transaction id is exist you can confirm to user which transaction you want to update
        amount: total expense or income in integer
        category_id: category id for transaction, aks user for cateogry and then check use get_categories to find category id if not exist create one and get_cateogries again, make sure category id is exist
        note: transaction info ask user for detail or decide your own
        transaction_date: date of transaction in format year-month-date like (2023-07-10), ask user for detail
        type: ask user for detail type of transaction or decide your own default: expense
    """
    endpoint = f"transactions/{transaction_id}"
    data = {
        "categoryId": category_id,
        "amount": amount,
        "note": note,
        "transactionDate": transaction_date,
        "type": type
    }

    data = await fortuna_put(endpoint, data=data)
    
    if not data:
        return "Unable to update transaction"
    
    return json.dumps(data)


@mcp.tool()
async def delete_transaction(transaction_id: str) -> str:
    """Delete transaction for the current user.

    Args:
        transaction_id: transaction id use get_recent_transactions or get_transactions to find transaction id, make sure transaction id is exist you can confirm to user which transaction you want to update
    """
    endpoint = f"transactions/{transaction_id}"
    data = await fortuna_delete(endpoint)
    
    if not data:
        return "Unable to delete transaction"
    
    return json.dumps(data)

# Budgets
@mcp.tool()
async def create_budgets(wallet_id: str, category_id: str, name: str, amount: int, type: str, start_date: str = None, end_date: str = None) -> str:
    """Create a new budget for the current user.
    
    Args:
        amount: total amount of budget, example: 2000000 for 2.000.000 IDR
        category_id: category id as string, use get_categories to chechk category id or you can ask user for detail
        name: budget name
        type: default: this_month, options: (this_month, this_week, custom) please ask user for detail, note: for custom start_date & end_date is required (YYY-MM-DD) and end_date must be greater than start_date
        wallet_id: wallet id as string, use get_wallets to chechk wallet id or you can ask user for detail

    """
    endpoint = "budgets"
    data = {
        "walletId": wallet_id, 
        "categoryId": category_id, 
        "name": name, 
        "amount": amount, 
        "type": type,
        "startDate": start_date,
        "endDate": end_date
    }
    data = await fortuna_post(endpoint, data=data)
    
    if not data:
        return "Unable to create budgets"
    
    return json.dumps(data)

@mcp.tool()
async def update_budgets(budget_id: str, wallet_id: str, category_id: str, name: str, amount: int, type: str, start_date: str = None, end_date: str = None) -> str:
    """Update an existing budget for the current user.
    
    Args:
        budget_id: budget id as string, use get_budgets to check budget id or you can ask user for detail
        amount: total amount of budget, example: 2000000 for 2.000.000 IDR
        category_id: category id as string, use get_categories to chechk category id or you can ask user for detail
        name: budget name
        type: default: this_month, options: (this_month, this_week, custom) please ask user for detail, note: for custom start_date & end_date is required (YYY-MM-DD) and end_date must be greater than start_date
        wallet_id: wallet id as string, use get_wallets to chechk wallet id or you can ask user for detail

    """
    endpoint = f"budgets/{budget_id}"
    data = {
        "walletId": wallet_id, 
        "categoryId": category_id, 
        "name": name, 
        "amount": amount, 
        "type": type,
        "startDate": start_date,
        "endDate": end_date
    }
    data = await fortuna_put(endpoint, data=data)
    
    if not data:
        return "Unable to update budgets"
    
    return json.dumps(data)

@mcp.tool()
async def get_budgets(wallet_id: str) -> str:
    """Get a list of budgets for the current user, grouped by type or by custom date range.
    
    Args:
        wallet_id: wallet id as string, use get_wallets to chechk wallet id or you can ask user for detail
    """
    endpoint = "budgets"
    data = await fortuna_get(endpoint, params={"walletId": wallet_id})
    
    if not data:
        return "Unable to get budgets"
    
    return json.dumps(data)

@mcp.tool()
async def get_budget(budget_id: str) -> str:
    """Get a specific budget by its ID for the current user.
    
    Args:
        budget_id: budget id as string, use get_budgets to check budget id or you can ask user for detail
    """
    endpoint = f"budgets/{budget_id}"
    data = await fortuna_get(endpoint)
    
    if not data:
        return "Unable to get budget"
    
    return json.dumps(data)

@mcp.tool()
async def delete_budget(budget_id: str) -> str:
    """Delete a budget by its ID for the current user.
    
    Args:
        budget_id: budget id as string, use get_budgets to check budget id or you can ask user for detail
    """
    endpoint = f"budgets/{budget_id}"
    data = await fortuna_delete(endpoint)
    
    if not data:
        return "Unable to delete budget"
    
    return json.dumps(data)

# Analytics
@mcp.tool()
async def analytic_get_total_transactions(start_date: str, end_date: str) -> str:
    """Get the total recent transactions (income and expense) for the current user within a date range.

    Args:
        start_date: start date in YYYY-MM-DD format, ask user for detail or pelase use current date if you don't know the date 
        end_date: end date in YYYY-MM-DD format, ask user for detail or pelase use current date if you don't know the date 
    """
    endpoint = "analytics/recent-transactions"
    data = await fortuna_get(endpoint, params={"start_date": start_date, "end_date": end_date})
    
    if not data:
        return "Unable to get total transactions"
    
    return json.dumps(data)

@mcp.tool()
async def analytic_get_activities() -> str:
    """Get user activity statistics (daily and monthly aggregation) for the current user."""
    endpoint = "analytics/activities"
    data = await fortuna_get(endpoint)
    
    if not data:
        return "Unable to get activities"
    
    return json.dumps(data)


if __name__ == "__main__":
    mcp.run(transport='stdio')