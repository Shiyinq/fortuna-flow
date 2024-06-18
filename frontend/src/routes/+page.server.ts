import { getTotalBalance, getWallets } from '$lib/apis/wallets';
import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async (token: string) => {
	const [balance, wallets] = await Promise.all([
		getTotalBalance(token),
		getWallets(token)
	]);

	return {
		balance,
		wallets,
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};