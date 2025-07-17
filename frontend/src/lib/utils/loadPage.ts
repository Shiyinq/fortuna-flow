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

	try {
		return await loadFunction(token, loadServerFunction);
	} catch (error) {
		console.error('Error loading data:', error);
		throw error;
	}
};
