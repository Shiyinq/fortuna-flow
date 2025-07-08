import { getBudgets } from '$lib/apis/budgets';
import { loadWithToken } from '$lib/utils/loadPage';
import type { RequestEvent } from '@sveltejs/kit';

export const load = async (event: RequestEvent) => {
  return await loadWithToken(event, async (token: string) => {
    const budgets = await getBudgets(token);
    return { budgets };
  });
}; 