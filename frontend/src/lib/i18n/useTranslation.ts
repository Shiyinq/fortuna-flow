import { translations } from '$lib/store';
import { derived } from 'svelte/store';

export function useTranslation() {
	const t = derived(translations, ($translations) => {
		return (key: string): string => {
			const keys = key.split('.');
			let value: unknown = $translations;
			
			for (const k of keys) {
				if (value && typeof value === 'object' && k in value) {
					value = (value as Record<string, unknown>)[k];
				} else {
					return key; 
				}
			}
			
			return typeof value === 'string' ? value : key;
		};
	});

	return { t };
} 