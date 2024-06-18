import { myFetch } from '$lib/utils';


export const getAllTransactions = async (token: string, page: number = 1, limit: number = 32, date: string) => {
	const response = await myFetch(
		'GET',
		token,
		`/transactions?page=${page}&limit=${limit}&month_year=${date}`
	);
	if (!response.ok) throw await response.json();
	return await response.json();
};