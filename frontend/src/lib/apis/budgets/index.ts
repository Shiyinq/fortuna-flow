import { myFetch } from '$lib/utils';
import type { Budget } from '../../types/budgets';

export interface BudgetsGroupedResponse {
  [period: string]: {
    totalBudget: number;
    datas: Budget[];
  };
}

export const getBudgets = async (token: string) => {
  const response = await myFetch('GET', token, `/budgets`);
  if (!response) throw new Error('No response from server');
  if (!response.ok) throw await response.json();
  return (await response.json()) as BudgetsGroupedResponse;
};

export const createBudget = async (token: string, budget: Partial<Budget>) => {
  const response = await myFetch('POST', token, `/budgets`, {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(budget)
  });
  if (!response) throw new Error('No response from server');
  if (!response.ok) throw await response.json();
  return await response.json();
};

export const updateBudget = async (token: string, budgetId: string, budget: Partial<Budget>) => {
  const response = await myFetch('PUT', token, `/budgets/${budgetId}`, {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(budget)
  });
  if (!response) throw new Error('No response from server');
  if (!response.ok) throw await response.json();
  return await response.json();
};

export const deleteBudget = async (token: string, budgetId: string) => {
  const response = await myFetch('DELETE', token, `/budgets/${budgetId}`);
  if (!response) throw new Error('No response from server');
  if (!response.ok) throw await response.json();
  return await response.json();
};

export const getBudget = async (token: string, budgetId: string) => {
  const response = await myFetch('GET', token, `/budgets/${budgetId}`);
  if (!response) throw new Error('No response from server');
  if (!response.ok) throw await response.json();
  return await response.json();
}; 