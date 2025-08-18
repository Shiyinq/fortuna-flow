import { myFetch } from '$lib/utils';

export const createApiKey = async (token: string) => {
	const response = await myFetch('POST', token, `/key`);
	if (!response) throw new Error('No response from server');
	if (!response.ok) {
		const body = await response.json();
		throw { status: response.status, ...body };
	}
	return await response.json();
};

export const deleteApiKey = async (token: string) => {
	const response = await myFetch('DELETE', token, `/key`);
	if (!response) throw new Error('No response from server');
	if (!response.ok) {
		const body = await response.json();
		throw { status: response.status, ...body };
	}
	return await response.json();
};
