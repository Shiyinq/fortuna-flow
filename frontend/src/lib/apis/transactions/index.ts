import { myFetch } from '$lib/utils';


export const getRecentTransactions = async (token: string, limit: number = 5) => {
	const response = await myFetch(
		'GET',
		token,
		`/transactions/recent?limit=${limit}`
	);
	if (!response.ok) throw await response.json();
	return await response.json();
};


export const getAllTransactions = async (token: string, page: number = 1, limit: number = 32, date: string) => {
	const response = await myFetch(
		'GET',
		token,
		`/transactions?page=${page}&limit=${limit}&month_year=${date}`
	);
	if (!response.ok) throw await response.json();
	return await response.json();
};