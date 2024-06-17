import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	if (!cookies.get('token') && !/^\/auth\/(signin|signup)$/.test(url.pathname)) {
		redirect(307, '/auth/signin');
	}
};
