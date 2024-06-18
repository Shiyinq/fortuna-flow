import { getRecentTransactions } from '$lib/apis/transactions';
import { getTotalBalance, getWallets } from '$lib/apis/wallets';
import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async (token: string) => {
	const [balance, wallets, recent] = await Promise.all([
		getTotalBalance(token),
		getWallets(token),
		getRecentTransactions(token)
	]);

	return {
		balance,
		wallets,
		recent
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
