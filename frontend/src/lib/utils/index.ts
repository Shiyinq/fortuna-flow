import { FORTUNA_API_BASE_URL } from '$lib/constants';
import { jwtDecode } from 'jwt-decode';

export const myFetch = async (
	method: string,
	token: string,
	endpoint: string,
	options?: RequestInit
) => {
	const headers = {
		...options?.headers,
		Authorization: `Bearer ${token}`
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

export const formatDate = (dateString: string) => {
	const months: string[] = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];

	const days: string[] = [
		'Sunday',
		'Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday'
	];

	const date: Date = new Date(dateString);
	const dayOfWeek: number = date.getDay();
	const dayOfMonth: number = date.getDate();
	const month: number = date.getMonth();
	const year: number = date.getFullYear();

	const formattedDate: string = `${days[dayOfWeek]}, ${dayOfMonth} ${months[month]} ${year}`;
	return formattedDate;
};

export const convertToInteger = (strNumber: string) => {
	const cleanedStr = strNumber.replace(/\./g, '').replace(',', '.');
	const floatValue = parseFloat(cleanedStr);
	return Math.round(floatValue);
};

export const isTokenExpired = (token: string) => {
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
	if (options.plugins && (options.plugins as { legend?: { labels?: Record<string, unknown> } }).legend) {
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
