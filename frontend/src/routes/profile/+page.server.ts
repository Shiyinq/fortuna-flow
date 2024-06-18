import { getMyProfile } from '$lib/apis/users';
import { loadWithToken } from '$lib/utils/loadPage.js';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async (token: string) => {
	const [profile] = await Promise.all([getMyProfile(token)]);

	return {
		profile
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
