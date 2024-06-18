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