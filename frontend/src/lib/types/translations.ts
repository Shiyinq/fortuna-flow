export interface TranslationData {
	common?: {
		loading?: string;
		save?: string;
		cancel?: string;
		delete?: string;
		edit?: string;
		add?: string;
		close?: string;
		back?: string;
		next?: string;
		previous?: string;
		search?: string;
		filter?: string;
		sort?: string;
		all?: string;
		none?: string;
		yes?: string;
		no?: string;
		ok?: string;
		error?: string;
		success?: string;
		warning?: string;
		info?: string;
		total?: string;
		locale?: string;
		welcome?: string;
		months?: {
			january?: string;
			february?: string;
			march?: string;
			april?: string;
			may?: string;
			june?: string;
			july?: string;
			august?: string;
			september?: string;
			october?: string;
			november?: string;
			december?: string;
		};
		days?: {
			sunday?: string;
			monday?: string;
			tuesday?: string;
			wednesday?: string;
			thursday?: string;
			friday?: string;
			saturday?: string;
		};
	};
	[key: string]: unknown;
} 