import { myFetch } from '$lib/utils';
import { FORTUNA_API_BASE_URL } from '$lib/constants';
import { token } from '$lib/store';

export const getMyProfile = async (token: string) => {
	const response = await myFetch('GET', token, `/users/profile`);
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const logoutUser = async (token: string) => {
	const response = await myFetch('POST', token, '/auth/logout', { credentials: 'include' });
	if (!response) throw new Error('No response from server');
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const refreshAccessToken = async () => {
	try {
		const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/refresh`, {
			method: 'POST',
			credentials: 'include'
		});
		if (!response.ok) throw new Error('Refresh token invalid');
		const data = await response.json();
		if (data.access_token) {
			token.set(data.access_token);
			return data.access_token;
		}
		throw new Error('No access token');
	} catch {
		token.set('');
		if (typeof document !== 'undefined') {
			document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
			window.location.href = '/auth/signin';
		}
		return null;
	}
};
