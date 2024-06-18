import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

import { getAllTransactions } from '$lib/apis/transactions';
import { getCurrentMonth } from '$lib/utils';

const loadData = async (token: string) => {
	const [transactions] = await Promise.all([getAllTransactions(token, 1, 32, getCurrentMonth())]);

	return {
		transactions
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
