import { myFetch } from "$lib/utils";


export const getTotalBalance = async (token: string) => {
	const response = await myFetch(
		'GET',
		token,
		`/wallets/total-balance`
	);
	if (!response.ok) throw await response.json();
	return await response.json();
};

export const getWallets = async (token: string, page: number = 1, limit: number = 5) => {
	const response = await myFetch(
		'GET',
		token,
		`/wallets?page=${page}&limit=${limit}`
	);
	if (!response.ok) throw await response.json();
	return await response.json();
}