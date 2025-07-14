import { currentLanguage, translations } from '$lib/store';
import { get } from 'svelte/store';

import id from './locales/id.json';
import en from './locales/en.json';
import ja from './locales/ja.json';

export const availableLanguages = [
	{ code: 'id', name: 'Bahasa Indonesia', flag: '🇮🇩' },
	{ code: 'en', name: 'English', flag: '🇺🇸' },
	{ code: 'ja', name: '日本語', flag: '🇯🇵' }
];

const loadTranslations = (lang: string) => {
	switch (lang) {
		case 'id':
			return id;
		case 'en':
			return en;
		case 'ja':
			return ja;
		default:
			return id;
	}
};

export const initI18n = () => {
	const lang = get(currentLanguage);
	const trans = loadTranslations(lang);
	translations.set(trans);
};

export const changeLanguage = (lang: string) => {
	console.log('Changing language to', lang);
	currentLanguage.set(lang);
	const trans = loadTranslations(lang);
	translations.set(trans);
	
	if (typeof document !== 'undefined') {
		document.documentElement.lang = lang;
	}
	
	if (typeof localStorage !== 'undefined') {
		localStorage.setItem('language', lang);
		console.log('localStorage language set to', lang);
	}
};

export const t = (key: string): string => {
	const trans = get(translations);
	const keys = key.split('.');
	let value: unknown = trans;
	
	for (const k of keys) {
		if (value && typeof value === 'object' && k in value) {
			value = (value as Record<string, unknown>)[k];
		} else {
			return key;
		}
	}
	
	return typeof value === 'string' ? value : key;
};

export const loadSavedLanguage = () => {
	if (typeof localStorage !== 'undefined') {
		const savedLang = localStorage.getItem('language');
		if (savedLang && availableLanguages.some(lang => lang.code === savedLang)) {
			changeLanguage(savedLang);
		}
	}
}; 