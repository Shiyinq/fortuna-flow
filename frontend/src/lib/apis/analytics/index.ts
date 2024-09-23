import { myFetch } from '$lib/utils';

export const getTotalTransactions = async (token: string, start_date: string, end_date: string) => {
	const response = await myFetch(
		'GET',
		token,
		`/analytics/recent-transactions?start_date=${start_date}&end_date=${end_date}`
	);
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getActivities = async (token: string) => {
	const response = await myFetch('GET', token, `/analytics/activities`);
	if (!response.ok) throw await response.json();
	return await response.json();
};
