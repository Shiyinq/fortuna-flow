import { writable } from 'svelte/store';
import type { Budget } from '$lib/types/budgets';
import type { TranslationData } from '$lib/types/translations';

const defaultWallet = {
	walletId: 'all',
	userId: 'null',
	walletIcon: null,
	name: 'All Wallets',
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

const isClient = typeof localStorage !== 'undefined';

const createLocalStorageStore = (key: string, startValue: string) => {
	let initial = startValue;
	if (isClient) {
		const stored = localStorage.getItem(key);
		if (stored) initial = stored;
	}
	const store = writable(initial);
	if (isClient) {
		store.subscribe((value) => {
			if (value !== undefined) {
				localStorage.setItem(key, value);
			}
		});
	}
	return store;
};

export const token = createLocalStorageStore('token', '');
export const wallets = writable<Wallet[]>(initialWallets);
export const activeWallet = writable<number>(0);
export const activeMonth = writable<string>((() => {
	const currentDate = new Date();
	const month = currentDate.getMonth() + 1;
	const year = currentDate.getFullYear();
	const formattedMonth = month < 10 ? `0${month}` : `${month}`;
	return `${formattedMonth}/${year}`;
})());
export const currentTransaction = writable<unknown[]>([]);
export const transactionSelected = writable<TransactionSelected>(initialTransactionSelected);
export const currentBudget = writable<Budget | null>(null);

// Dark mode store
export const darkMode = writable<'light' | 'dark' | 'auto'>('auto');

// Initialize dark mode from localStorage and apply to DOM
if (typeof window !== 'undefined') {
	const savedDarkMode = localStorage.getItem('darkMode');
	if (savedDarkMode === 'light' || savedDarkMode === 'dark' || savedDarkMode === 'auto') {
		darkMode.set(savedDarkMode);
	}

	function applyTheme(mode: 'light' | 'dark' | 'auto') {
		if (mode === 'auto') {
			const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
			if (prefersDark) {
				document.documentElement.classList.add('dark');
			} else {
				document.documentElement.classList.remove('dark');
			}
		} else if (mode === 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	}

	// Apply theme on store change
	darkMode.subscribe((value) => {
		localStorage.setItem('darkMode', value);
		applyTheme(value);
	});

	// Initial apply
	let $darkMode: 'light' | 'dark' | 'auto' = 'auto';
	darkMode.subscribe((v) => { $darkMode = v; });
	applyTheme($darkMode);

	// Listen to system theme changes if mode is auto
	window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
		if ($darkMode === 'auto') {
			applyTheme('auto');
		}
	});
}

// Language store
export const currentLanguage = writable<string>('id'); // Default to Bahasa Indonesia
export const translations = writable<TranslationData>({});
