import { API_BASE_URL } from '$lib/server/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		apiBaseUrl: API_BASE_URL
	};
};
