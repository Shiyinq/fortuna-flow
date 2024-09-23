import { redirect } from '@sveltejs/kit';
import { isTokenExpired } from '$lib/utils';

export const load = async ({ cookies, url }) => {
	const token = cookies.get('token');

	if (token && isTokenExpired(token)) {
		cookies.delete('token', { path: '/' });
		throw redirect(307, '/auth/signin');
	}

	if (!token && !/^\/auth\/(signin|signup|callback)$/.test(url.pathname)) {
		throw redirect(307, '/auth/signin');
	}
};
