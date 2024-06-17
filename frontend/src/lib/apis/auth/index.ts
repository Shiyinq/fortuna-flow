import { FORTUNA_API_BASE_URL } from "$lib/constants";


export const userSignUp = async (name: string, username: string, email: string, password: string, confirmPassword: string) => {
	const response = await fetch(`${FORTUNA_API_BASE_URL}/users/signup`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			name: name,
			username: username,
            email: email,
			password: password,
			confirmPassword: confirmPassword
		})
	});
	if (!response.ok) throw await response.json();
	return await response.json();
};
