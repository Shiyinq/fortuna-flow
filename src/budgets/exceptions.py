from src.budgets.constants import ErrorCode
from src.exceptions import NotFound


class BudgetNotFound(NotFound):
    DETAIL = ErrorCode.BUDGET_NOT_FOUND
