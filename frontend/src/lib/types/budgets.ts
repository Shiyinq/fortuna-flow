export interface Budget {
  budgetId: string;
  userId: string;
  name: string;
  amount: number;
  icon?: string | null;
  startDate: string;
  endDate: string;
  createdAt: string;
  updatedAt: string;
  totalSpent?: number;
}

export interface BudgetsGroupedResponse {
  [period: string]: {
    totalBudget: number;
    datas: Budget[];
  };
} 