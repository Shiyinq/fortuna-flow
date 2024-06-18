import { getCurrentMonth } from '$lib/utils';
import cookie from 'cookie';
import { jwtDecode } from 'jwt-decode';
import { writable } from 'svelte/store';


const defaultWallet = {
	walletId: 'all',
	userId: 'null',
	walletIcon: null,
	name: 'All Wallet',
	balance: 0,
	createdAt: 'null',
	updatedAt: 'null'
}

const initialWallets: Wallet[] = [
	defaultWallet
];

export interface Wallet {
	walletId: string;
	userId: string;
	walletIcon: string | null;
	name: string;
	balance: number;
	createdAt: string;
	updatedAt: string;
}

const createPersistedStore = (key: string, startValue: string) => {
	let parsedValue = startValue;

	if (typeof document !== 'undefined') {
		const cookies = cookie.parse(document.cookie);
		const storedValue = cookies[key];

		try {
			parsedValue = storedValue ? JSON.parse(storedValue) : startValue;
		} catch (e) {
			console.error('Error parsing stored value: ', e);
			parsedValue = startValue;
		}
	}

	const store = writable(parsedValue);

	if (typeof document !== 'undefined') {
		store.subscribe((value) => {
			if (value !== '') {
				let maxAge = 365 * 24 * 60 * 60;
				if (key === 'token') {
					const { exp } = jwtDecode(value);
					if (exp) {
						const currentTime = Math.floor(Date.now() / 1000);
						maxAge = exp - currentTime;
						if (maxAge < 0) {
							maxAge = 0;
						}
					} else {
						maxAge = -1;
					}
				}
				document.cookie = cookie.serialize(key, JSON.stringify(value), {
					path: '/',
					maxAge: maxAge
				});
			}
		});
	}

	return store;
};

const toggleTheme = () => {
	let initialTheme = 'light';

	if (typeof document !== 'undefined') {
		const cookies = cookie.parse(document.cookie);
		initialTheme = cookies['theme'] || 'light';
	}

	const theme = writable(initialTheme);

	if (typeof document !== 'undefined') {
		theme.subscribe((value) => {
			document.cookie = cookie.serialize('theme', value, {
				path: '/',
				maxAge: 365 * 24 * 60 * 60
			});
			document.documentElement.setAttribute('data-theme', value);
		});
	}

	return theme;
};

export const theme = toggleTheme();
export const token = createPersistedStore('token', '');
export const wallets = writable<Wallet[]>(initialWallets);
export const activeWallet = writable<Wallet>(defaultWallet);
export const activeMonth = writable<string>(getCurrentMonth())
