import { myFetch } from '$lib/utils';

export const addTransaction = async (
	token: string,
	walletId: string,
	categoryId: string,
	amount: number,
	type: string,
	note: string,
	transactionDate: string
) => {
	const response = await myFetch('POST', token, `/transactions`, {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			walletId,
			categoryId,
			amount,
			type,
			note,
			transactionDate
		})
	});
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const updateTransaction = async (
	token: string,
	transactionId: string,
	categoryId: string,
	amount: number,
	type: string,
	note: string,
	transactionDate: string
) => {
	const response = await myFetch('PUT', token, `/transactions/${transactionId}`, {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			categoryId,
			amount,
			type,
			note,
			transactionDate
		})
	});
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const deleteTransaction = async (token: string, transactionId: string) => {
	const response = await myFetch('DELETE', token, `/transactions/${transactionId}`);
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getRecentTransactions = async (token: string, limit: number = 5) => {
	const response = await myFetch('GET', token, `/transactions/recent?limit=${limit}`);
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getAllTransactions = async (
	token: string,
	page: number = 1,
	limit: number = 32,
	date: string
) => {
	const response = await myFetch(
		'GET',
		token,
		`/transactions?page=${page}&limit=${limit}&month_year=${date}`
	);
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};
