import { browser } from '$app/environment';
import {
	PUBLIC_CLIENT_SIDE_FORTUNA_API_BASE_URL,
	PUBLIC_SERVER_SIDE_FORTUNA_API_BASE_URL
} from '$env/static/public';

export const FORTUNA_API_BASE_URL = browser
	? PUBLIC_CLIENT_SIDE_FORTUNA_API_BASE_URL
	: PUBLIC_SERVER_SIDE_FORTUNA_API_BASE_URL;

export * from './icons';
