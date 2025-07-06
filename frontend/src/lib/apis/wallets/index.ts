import { myFetch } from '$lib/utils';

export const addWallet = async (token: string, name: string, balance: number, walletIcon?: string) => {
	const response = await myFetch('POST', token, `/wallets`, {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name,
			balance,
			walletIcon
		})
	});
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getTotalBalance = async (token: string) => {
	const response = await myFetch('GET', token, `/wallets/total-balance`);
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getWallets = async (token: string, page: number = 1, limit: number = 5) => {
	const response = await myFetch('GET', token, `/wallets?page=${page}&limit=${limit}`);
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getWallet = async (token: string, walletId: string) => {
	const response = await myFetch('GET', token, `/wallets/${walletId}`);
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getWalletTransactions = async (
	token: string,
	walletId: string,
	date: string,
	page: number = 1,
	limit: number = 32
) => {
	const response = await myFetch(
		'GET',
		token,
		`/wallets/${walletId}/transactions?page=${page}&limit=${limit}&month_year=${date}`
	);
	if (!response.ok) throw await response.json();
	return await response.json();
};
