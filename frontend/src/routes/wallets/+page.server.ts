import { getWallets } from '$lib/apis/wallets';
import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async (token: string) => {
	const [wallets] = await Promise.all([
		getWallets(token, 1, 20)
	]);

	return {
		wallets
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};