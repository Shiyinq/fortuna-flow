import { FORTUNA_API_BASE_URL } from '$lib/constants';

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
