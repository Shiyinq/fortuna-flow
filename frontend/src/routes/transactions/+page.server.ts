import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

import { getAllTransactions } from '$lib/apis/transactions';
import { getCurrentMonth } from '$lib/utils';
import { getTotalBalance, getWallets } from '$lib/apis/wallets';

const loadData = async (token: string) => {
	const [transactions, balance, wallets] = await Promise.all([
		getAllTransactions(token, 1, 32, getCurrentMonth()),
		getTotalBalance(token),
		getWallets(token, 1, 10)
	]);

	const allWallet = [
		{
			walletId: 'all',
			userId: 'null',
			walletIcon: null,
			name: 'All Wallet',
			balance: balance.totalBalance,
			createdAt: 'null',
			updatedAt: 'null'
		}
	];

	const listWallet = allWallet.concat(wallets.data);

	return {
		transactions,
		listWallet
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
