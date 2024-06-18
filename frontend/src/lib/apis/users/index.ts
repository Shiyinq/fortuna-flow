import { myFetch } from '$lib/utils';
import { FORTUNA_API_BASE_URL } from '$lib/constants';

export const userSignIn = async (username: string, password: string) => {
	const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/signin`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
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
	if (!response.ok) throw await response.json();
	return await response.json();
};
