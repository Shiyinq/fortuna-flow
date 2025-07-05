import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';
import { getCategories } from '$lib/apis/categories';

const loadData = async (token: string) => {
	const categories = await getCategories(token, 1, 100);
	
	return {
		categories
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
}; 