import cookie from 'cookie';
import { jwtDecode } from 'jwt-decode';
import { writable } from 'svelte/store';
import type { Budget } from '$lib/types/budgets';

const defaultWallet = {
	walletId: 'all',
	userId: 'null',
	walletIcon: null,
	name: 'All Wallet',
	balance: 0,
	createdAt: 'null',
	updatedAt: 'null'
};

const initialWallets: Wallet[] = [defaultWallet];

export const initialTransactionSelected: TransactionSelected = {
	transactionId: '',
	walletId: '',
	categoryId: '',
	type: '',
	amount: '',
	note: '',
	transactionDate: ''
};

export interface Wallet {
	walletId: string;
	userId: string;
	walletIcon: string | null;
	name: string;
	balance: number;
	createdAt: string;
	updatedAt: string;
}

export interface TransactionSelected {
	transactionId: string;
	walletId: string;
	categoryId: string;
	type: string;
	amount: string;
	note: string;
	transactionDate: string;
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

const getCurrentMonth = () => {
	const currentDate = new Date();
	const month = currentDate.getMonth() + 1;
	const year = currentDate.getFullYear();
	const formattedMonth = month < 10 ? `0${month}` : `${month}`;
	return `${formattedMonth}/${year}`;
}

export const token = createPersistedStore('token', '');
export const wallets = writable<Wallet[]>(initialWallets);
export const activeWallet = writable<number>(0);
export const activeMonth = writable<string>(getCurrentMonth());
export const currentTransaction = writable<unknown[]>([]);
export const transactionSelected = writable<TransactionSelected>(initialTransactionSelected);
export const currentBudget = writable<Budget | null>(null);

// Dark mode store
export const darkMode = writable(false);

// Initialize dark mode from localStorage and apply to DOM
if (typeof window !== 'undefined') {
	const savedDarkMode = localStorage.getItem('darkMode');
	if (savedDarkMode !== null) {
		darkMode.set(savedDarkMode === 'true');
	}

	// Save to localStorage and apply to DOM whenever dark mode changes
	darkMode.subscribe((value) => {
		localStorage.setItem('darkMode', value.toString());
		if (value) {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	});
}

// Language store
export const currentLanguage = writable<string>('id'); // Default ke bahasa Indonesia
export const translations = writable<Record<string, Record<string, string>>>({});
