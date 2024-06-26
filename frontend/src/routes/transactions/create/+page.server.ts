import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

import { getCategories } from '$lib/apis/categories';
import { getWallets } from '$lib/apis/wallets';

const loadData = async (token: string) => {
	const [categories, wallets] = await Promise.all([
		getCategories(token, 1, 100),
		getWallets(token, 1, 100)
	]);

	return {
		categories: categories.data,
		wallets: wallets.data,
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
