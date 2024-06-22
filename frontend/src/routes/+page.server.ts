import { getRecentTransactions } from '$lib/apis/transactions';
import { getTotalBalance, getWallets } from '$lib/apis/wallets';
import { getTotalTransactions } from '$lib/apis/analytics';
import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

const getDateRange = () => {
	const today = new Date();

	const endDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);

	const startDate = new Date(today.getFullYear(), today.getMonth() - 3, 1);

	const formatDate = (date: Date): string => {
		const year = date.getFullYear();
		const month = (date.getMonth() + 1).toString().padStart(2, '0');
		const day = date.getDate().toString().padStart(2, '0');
		return `${year}-${month}-${day}`;
	};

	return {
		startDate: formatDate(startDate),
		endDate: formatDate(endDate)
	};
};

const loadData = async (token: string) => {
	const { startDate, endDate } = getDateRange();
	const [balance, wallets, recent, recentTotalTransactions] = await Promise.all([
		getTotalBalance(token),
		getWallets(token),
		getRecentTransactions(token),
		getTotalTransactions(token, startDate, endDate)
	]);

	return {
		balance,
		wallets,
		recent,
		recentTotalTransactions
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
