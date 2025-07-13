import { FORTUNA_API_BASE_URL } from '$lib/constants';
import { jwtDecode } from 'jwt-decode';
import { refreshAccessToken } from '$lib/apis/users';
import type { TranslationData } from '$lib/types/translations';

export const myFetch = async (
	method: string,
	tokenValue: string,
	endpoint: string,
	options?: RequestInit
) => {
	let currentToken = tokenValue;
	if (isTokenExpired(currentToken)) {
		currentToken = await refreshAccessToken();
		if (!currentToken) {
			return;
		}
	}
	const headers = {
		...options?.headers,
		Authorization: `Bearer ${currentToken}`
	};
	delete options?.headers;
	return await fetch(`${FORTUNA_API_BASE_URL}${endpoint}`, {
		...{ method: method },
		headers,
		...options
	});
};

export const numberToEmoji = (number: number) => {
	const emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'];
	const numString = number.toString();
	let result = '';

	for (let i = 0; i < numString.length; i++) {
		const digit = parseInt(numString[i]);
		if (!isNaN(digit)) {
			result += emojis[digit];
		}
	}

	return result;
};

export const formatCurrency = (amount: number, currencySymbol: string = 'Rp') => {
	let locale: string;

	switch (currencySymbol) {
		case '$':
			locale = 'en-US';
			break;
		case 'Rp':
		default:
			locale = 'id-ID';
			break;
	}

	const formattedAmount = `${currencySymbol} ${amount.toLocaleString(locale)}`;
	return formattedAmount;
};

export const getCurrentMonth = () => {
	const currentDate: Date = new Date();
	const month: number = currentDate.getMonth() + 1;
	const year: number = currentDate.getFullYear();

	const formattedMonth: string = month < 10 ? `0${month}` : `${month}`;

	return `${formattedMonth}/${year}`;
};

export const formatDate = (dateString: string, locale: string = 'en', translations?: TranslationData) => {
	// Use translations if available
	if (translations && translations.common) {
		const months = translations.common.months;
		const days = translations.common.days;
		
		if (months && days) {
			const monthNames = [
				months.january,
				months.february,
				months.march,
				months.april,
				months.may,
				months.june,
				months.july,
				months.august,
				months.september,
				months.october,
				months.november,
				months.december
			];

			const dayNames = [
				days.sunday,
				days.monday,
				days.tuesday,
				days.wednesday,
				days.thursday,
				days.friday,
				days.saturday
			];

			// Check if all translations are available
			if (monthNames.every(name => name) && dayNames.every(name => name)) {
				const date: Date = new Date(dateString);
				const dayOfWeek: number = date.getDay();
				const dayOfMonth: number = date.getDate();
				const month: number = date.getMonth();
				const year: number = date.getFullYear();

				const formattedDate: string = `${dayNames[dayOfWeek]}, ${dayOfMonth} ${monthNames[month]} ${year}`;
				return formattedDate;
			}
		}
	}

	// Fallback to browser's built-in localization
	const date: Date = new Date(dateString);
	const options: Intl.DateTimeFormatOptions = {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	};

	// Completely dynamic approach - no hardcoding needed!
	const getBrowserLocale = (simpleLocale: string): string => {
		// If the locale already looks like a browser locale (contains '-'), use it as is
		if (simpleLocale.includes('-')) {
			return simpleLocale;
		}

		// For unknown languages, try the simple locale as-is
		// The browser will handle it gracefully and fallback to English if needed
		return simpleLocale;
	};

	const browserLocale = getBrowserLocale(locale);
	
	// Try to format with the locale, if it fails, fallback to 'en-US'
	try {
		return date.toLocaleDateString(browserLocale, options);
	} catch {
		console.warn(`Failed to format date with locale ${browserLocale}, falling back to en-US`);
		return date.toLocaleDateString('en-US', options);
	}
};

export const convertToInteger = (strNumber: string) => {
	const cleanedStr = strNumber.replace(/\./g, '').replace(',', '.');
	const floatValue = parseFloat(cleanedStr);
	return Math.round(floatValue);
};

export const isTokenExpired = (token: string) => {
	if (!token || token === '""' || token === "''") {
		return true;
	}
	try {
		const decodedToken = jwtDecode(token);
		if (!decodedToken || !decodedToken.exp) {
			return true;
		}
		const currentTime = Math.floor(Date.now() / 1000);
		return decodedToken.exp < currentTime;
	} catch (error) {
		console.error('Error decoding token:', error);
		return true;
	}
};

export const isEmoji = (icon: string) => {
	return icon && !icon.includes('/') && !icon.includes('.') && !icon.startsWith('data:');
};

// Chart color utilities for dark mode
export const getChartColors = (darkMode: boolean) => {
	return {
		tickColor: darkMode ? '#f1f5f9' : '#222',
		gridColor: darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)',
		labelColor: darkMode ? '#f1f5f9' : '#222',
		fontColor: darkMode ? '#f1f5f9' : '#333'
	};
};

export const getChartOptions = (darkMode: boolean, options: Record<string, unknown> = {}) => {
	const colors = getChartColors(darkMode);
	const baseOptions = {
		responsive: true,
		scales: {
			y: {
				beginAtZero: true,
				ticks: {
					color: colors.tickColor
				},
				grid: {
					color: colors.gridColor
				}
			},
			x: {
				ticks: {
					color: colors.tickColor
				},
				grid: {
					color: colors.gridColor
				}
			}
		},
		plugins: {
			legend: {
				labels: {
					color: colors.labelColor
				}
			}
		}
	};

	let legendLabels: Record<string, unknown> = {};
	if (
		options.plugins &&
		(options.plugins as { legend?: { labels?: Record<string, unknown> } }).legend
	) {
		const legend = (options.plugins as { legend?: { labels?: Record<string, unknown> } }).legend;
		if (legend && legend.labels) {
			legendLabels = legend.labels;
		}
	}
	const merged = {
		...baseOptions,
		...options,
		plugins: {
			...((baseOptions.plugins as Record<string, unknown>) || {}),
			...((options.plugins as Record<string, unknown>) || {}),
			legend: {
				...((baseOptions.plugins && (baseOptions.plugins as Record<string, unknown>).legend) || {}),
				...((options.plugins && (options.plugins as Record<string, unknown>).legend) || {}),
				labels: {
					color: colors.labelColor,
					...legendLabels
				}
			}
		}
	};
	return merged;
};

export function getComputedStyle(variable: string, fallback: string = ''): string {
	if (typeof window !== 'undefined') {
		const value = window.getComputedStyle(document.documentElement).getPropertyValue(variable);
		return value ? value.trim() : fallback;
	}
	return fallback;
}
