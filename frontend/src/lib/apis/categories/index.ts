import { myFetch } from '$lib/utils';

export const addCategory = async (token: string, name: string, type: string) => {
	const response = await myFetch('POST', token, `/categories`, {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name,
			type
		})
	});
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getCategories = async (token: string, page: number = 1, limit: number = 10) => {
	const response = await myFetch('GET', token, `/categories?page=${page}&limit=${limit}`);
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const createCategory = async (
	token: string,
	name: string,
	type: 'expense' | 'income',
	categoryIcon?: string
) => {
	const response = await myFetch('POST', token, `/categories`, {
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name,
			type,
			categoryIcon
		})
	});
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};
