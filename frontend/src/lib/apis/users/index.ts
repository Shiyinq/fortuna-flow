import { myFetch } from '$lib/utils';
import { FORTUNA_API_BASE_URL } from '$lib/constants';
import { token } from '$lib/store';

export const userSignIn = async (username: string, password: string) => {
	const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/signin`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		credentials: 'include',
		body: new URLSearchParams({
			username: username,
			password: password
		}).toString()
	});

	if (!response.ok) throw await response.json();
	return await response.json();
};

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

export const refreshAccessToken = async (isServer = false) => {
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
		if (!isServer && typeof window !== 'undefined') {
			window.location.href = '/auth/signin';
		}
		return null;
	}
};
