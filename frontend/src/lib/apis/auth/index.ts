import { FORTUNA_API_BASE_URL } from '$lib/constants';

export const userSignUp = async (
	name: string,
	username: string,
	email: string,
	password: string,
	confirmPassword: string
) => {
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

export const sendVerificationEmail = async (email: string) => {
	try {
		const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/send-verification`, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email })
		});
		
		const data = await response.json();
		
		if (!response.ok) {
			throw {
				detail: data.detail || data.message || 'Failed to send verification email',
				status: response.status
			};
		}
		
		return data;
	} catch (error) {
		// If it's already a structured error, re-throw it
		if (error && typeof error === 'object' && 'detail' in error) {
			throw error;
		}
		
		// Handle network errors or other issues
		throw {
			detail: 'Network error. Please check your connection and try again.',
			status: 0
		};
	}
};

export const verifyEmail = async (token: string) => {
	try {
		const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/verify-email`, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ token })
		});
		
		const data = await response.json();
		
		if (!response.ok) {
			throw {
				detail: data.detail || data.message || 'Failed to verify email',
				status: response.status
			};
		}
		
		return data;
	} catch (error) {
		if (error && typeof error === 'object' && 'detail' in error) {
			throw error;
		}
		throw {
			detail: 'Network error. Please check your connection and try again.',
			status: 0
		};
	}
};

export const forgotPassword = async (email: string) => {
	try {
		const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/forgot-password`, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email })
		});
		
		const data = await response.json();
		
		if (!response.ok) {
			throw {
				detail: data.detail || data.message || 'Failed to send password reset email',
				status: response.status
			};
		}
		
		return data;
	} catch (error) {
		if (error && typeof error === 'object' && 'detail' in error) {
			throw error;
		}
		throw {
			detail: 'Network error. Please check your connection and try again.',
			status: 0
		};
	}
};

export const resetPassword = async (token: string, newPassword: string, confirmPassword: string) => {
	try {
		const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/reset-password`, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ 
				token, 
				new_password: newPassword, 
				confirm_password: confirmPassword 
			})
		});
		
		const data = await response.json();
		
		if (!response.ok) {
			throw {
				detail: data.detail || data.message || 'Failed to reset password',
				status: response.status
			};
		}
		
		return data;
	} catch (error) {
		if (error && typeof error === 'object' && 'detail' in error) {
			throw error;
		}
		throw {
			detail: 'Network error. Please check your connection and try again.',
			status: 0
		};
	}
};
