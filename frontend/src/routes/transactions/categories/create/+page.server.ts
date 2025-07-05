import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async () => {
	// No data needed for create page
	return {};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
}; 