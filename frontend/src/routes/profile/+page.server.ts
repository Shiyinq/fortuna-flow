import { getMyProfile } from '$lib/apis/users';
import { loadWithToken } from '$lib/utils/loadPage.js';
import { getActivities } from '$lib/apis/analytics';
import { getWallets } from '$lib/apis/wallets';
import { getCategories } from '$lib/apis/categories';
import type { RequestEvent } from '@sveltejs/kit';

const loadData = async (token: string) => {
	const [profile, activities, walletsRes, categoriesRes] = await Promise.all([
		getMyProfile(token),
		getActivities(token),
		getWallets(token, 1, 10),
		getCategories(token, 1, 20)
	]);

	return {
		profile,
		activities,
		wallets: walletsRes.data || [],
		categories: categoriesRes.data || []
	};
};

export const load = async (loadFunction: RequestEvent) => {
	return await loadWithToken(loadFunction, loadData);
};
