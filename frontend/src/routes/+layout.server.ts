import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies, url }) => {
	if (!cookies.get('token') && !/^\/auth\/(signin|signup|callback)$/.test(url.pathname)) {
		redirect(307, '/auth/signin');
	}
};
