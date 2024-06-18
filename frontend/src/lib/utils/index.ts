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
}
