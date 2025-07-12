import { currentLanguage, translations } from '$lib/store';
import { get } from 'svelte/store';

// Import semua file terjemahan
import id from './locales/id.json';
import en from './locales/en.json';

// Daftar bahasa yang tersedia
export const availableLanguages = [
	{ code: 'id', name: 'Bahasa Indonesia', flag: '🇮🇩' },
	{ code: 'en', name: 'English', flag: '🇺🇸' }
];

// Load terjemahan berdasarkan bahasa
const loadTranslations = (lang: string) => {
	switch (lang) {
		case 'id':
			return id;
		case 'en':
			return en;
		default:
			return id; // Fallback ke bahasa Indonesia
	}
};

// Inisialisasi terjemahan
export const initI18n = () => {
	const lang = get(currentLanguage);
	const trans = loadTranslations(lang);
	translations.set(trans);
};

// Fungsi untuk mengubah bahasa
export const changeLanguage = (lang: string) => {
	console.log('Changing language to', lang);
	currentLanguage.set(lang);
	const trans = loadTranslations(lang);
	translations.set(trans);
	
	// Update HTML lang attribute
	if (typeof document !== 'undefined') {
		document.documentElement.lang = lang;
	}
	
	// Simpan ke localStorage
	if (typeof localStorage !== 'undefined') {
		localStorage.setItem('language', lang);
		console.log('localStorage language set to', lang);
	}
};

// Fungsi untuk mendapatkan terjemahan
export const t = (key: string): string => {
	const trans = get(translations);
	const keys = key.split('.');
	let value: unknown = trans;
	
	for (const k of keys) {
		if (value && typeof value === 'object' && k in value) {
			value = (value as Record<string, unknown>)[k];
		} else {
			return key; // Return key jika tidak ditemukan
		}
	}
	
	return typeof value === 'string' ? value : key;
};

// Load bahasa dari localStorage saat startup
export const loadSavedLanguage = () => {
	if (typeof localStorage !== 'undefined') {
		const savedLang = localStorage.getItem('language');
		if (savedLang && availableLanguages.some(lang => lang.code === savedLang)) {
			changeLanguage(savedLang);
		}
	}
}; 