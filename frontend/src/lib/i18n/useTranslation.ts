import { translations } from '$lib/store';
import { derived } from 'svelte/store';

// Hook untuk menggunakan terjemahan dalam komponen Svelte
export function useTranslation() {
	const t = derived(translations, ($translations) => {
		return (key: string): string => {
			const keys = key.split('.');
			let value: unknown = $translations;
			
			for (const k of keys) {
				if (value && typeof value === 'object' && k in value) {
					value = (value as Record<string, unknown>)[k];
				} else {
					return key; // Return key jika tidak ditemukan
				}
			}
			
			return typeof value === 'string' ? value : key;
		};
	});

	return { t };
} 