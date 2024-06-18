import { getTotalBalance } from '$lib/apis/wallets';
import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async (token: string) => {
	const [balance] = await Promise.all([
		getTotalBalance(token)
	]);

    console.log(balance);
	return {
		balance
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};