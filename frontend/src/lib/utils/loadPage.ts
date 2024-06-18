import type { RequestEvent } from '@sveltejs/kit';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type LoadFunction = (token: string, loadServerFunction: RequestEvent) => Promise<any>;

export const loadWithToken = async (
	loadServerFunction: RequestEvent,
	loadFunction: LoadFunction
) => {
	const { cookies } = loadServerFunction;
	const token = cookies.get('token');
	if (!token) {
		return;
	}

	let parsedToken;
	try {
		parsedToken = JSON.parse(token);
	} catch (error) {
		console.error('Invalid token:', error);
		return;
	}

	try {
		return await loadFunction(parsedToken, loadServerFunction);
	} catch (error) {
		console.error('Error loading data:', error);
		throw error;
	}
};