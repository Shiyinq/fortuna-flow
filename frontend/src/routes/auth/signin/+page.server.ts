import { fail, redirect } from '@sveltejs/kit';

import { userSignIn } from '$lib/apis/users';

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

export const load = async ({cookies}) => {
	if (cookies.get('token')) {
		redirect(307, '/');
	}
};

export const actions = {
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
