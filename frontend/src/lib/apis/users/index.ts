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
