import { getMyProfile } from '$lib/apis/users';
import { loadWithToken } from '$lib/utils/loadPage.js';
import { getActivities } from '$lib/apis/analytics';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async (token: string) => {
	const [profile, activities] = await Promise.all([getMyProfile(token), getActivities(token)]);

	return {
		profile,
		activities
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
