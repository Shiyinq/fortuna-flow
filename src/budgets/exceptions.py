from src.exceptions import NotFound
from src.budgets.constants import ErrorCode

class BudgetNotFound(NotFound):
    DETAIL = ErrorCode.BUDGET_NOT_FOUND 