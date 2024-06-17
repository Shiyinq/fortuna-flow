import { fail } from '@sveltejs/kit';

import { userSignUp } from '$lib/apis/auth';
import { userSignIn } from '$lib/apis/users';

const formValidation = (
	name: string,
	username: string,
	email: string,
	password: string,
	confirmPassword: string
) => {
	const validation = { name: '', username: '', email: '', password: '', confirmPassword: '' };
	let valid = true;
	if (!name || typeof name !== 'string') {
		valid = false;
		validation['name'] = 'Name is required!';
	}

	if (!username || typeof username !== 'string') {
		valid = false;
		validation['username'] = 'Username is required!';
	}

	if (!email || typeof email !== 'string') {
		valid = false;
		validation['email'] = 'Email is required!';
	}

	if (!password || typeof password !== 'string') {
		valid = false;
		validation['password'] = 'Password is required!';
	}

	if (!confirmPassword || typeof confirmPassword !== 'string') {
		valid = false;
		validation['confirmPassword'] = 'Confirm password is required!';
	}

	if (confirmPassword != password) {
		valid = false;
		validation['confirmPassword'] = 'Confirm password and password must be the same!';
	}

	return [valid, validation];
};

const signInFormValidation = (username: string, password: string) => {
	const validation = { username: '', password: '' };
	let valid = true;
	if (!username || typeof username !== 'string') {
		valid = false;
		validation['username'] = 'Username is required!';
	}

	if (!password || typeof password !== 'string') {
		valid = false;
		validation['password'] = 'Password is required!';
	}

	return [valid, validation];
};

export const actions = {
	signUp: async ({ request }) => {
		const data = await request.formData();
		const name = data.get('name') as string | null;
		const username = data.get('username') as string | null;
		const email = data.get('email') as string | null;
		const password = data.get('password') as string | null;
		const confirmPassword = data.get('confirmPassword') as string | null;

		const [valid, validation] = formValidation(
			name ?? '',
			username ?? '',
			email ?? '',
			password ?? '',
			confirmPassword ?? ''
		);
		if (!valid) {
			return fail(400, {
				status: false,
				errors: validation,
				message: 'Form not valid.'
			});
		}

		try {
			const result = await userSignUp(
				name ?? '',
				username ?? '',
				email ?? '',
				password ?? '',
				confirmPassword ?? ''
			);
			return { status: true, message: result.detail };
		} catch (err) {
			console.log(err);
			return fail(500, {
				status: false,
				message: 'Sign up failed.'
			});
		}
	},
	signIn: async ({ request }) => {
		const data = await request.formData();
		const username = data.get('username') as string | null;
		const password = data.get('password') as string | null;

		const [valid, validation] = signInFormValidation(username ?? '', password ?? '');
		if (!valid) {
			return fail(400, {
				status: false,
				errors: validation,
				message: 'Form not valid.'
			});
		}

		try {
			const result = await userSignIn(username ?? '', password ?? '');
			return { status: true, message: 'Sign successful.', ...result };
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
		} catch (err: any) {
			console.log(err);
			return fail(500, {
				status: false,
				message: err?.detail ? err.detail : 'Sign in failed.'
			});
		}
	}
};
