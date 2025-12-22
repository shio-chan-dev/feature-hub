import { apiRequest, getErrorMessage } from '$lib/server/api';
import type { AuditList } from '$lib/types';
import type { PageServerLoad } from './$types';

const parseLimit = (value: string | null) => {
	if (!value) {
		return 50;
	}
	const parsed = Number(value);
	return Number.isFinite(parsed) ? parsed : 50;
};

export const load: PageServerLoad = async ({ fetch, url }) => {
	const featureId = url.searchParams.get('feature_id')?.trim() ?? '';
	const cursor = url.searchParams.get('cursor')?.trim() ?? '';
	const limit = parseLimit(url.searchParams.get('limit'));

	if (!featureId) {
		return {
			featureId: '',
			limit,
			audits: [],
			nextCursor: null,
			error: null
		};
	}

	const query = new URLSearchParams({
		feature_id: featureId,
		limit: String(limit)
	});

	if (cursor) {
		query.set('cursor', cursor);
	}

	try {
		const response = await apiRequest<AuditList>(fetch, `/audits?${query.toString()}`);
		return {
			featureId,
			limit,
			audits: response.items,
			nextCursor: response.next_cursor,
			error: null
		};
	} catch (error) {
		return {
			featureId,
			limit,
			audits: [],
			nextCursor: null,
			error: getErrorMessage(error)
		};
	}
};
