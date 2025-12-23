import { fail } from '@sveltejs/kit';
import { apiRequest, getErrorMessage } from '$lib/server/api';
import type { DecisionResponse } from '$lib/types';
import type { Actions, PageServerLoad } from './$types';

const parseString = (value: FormDataEntryValue | null) =>
	typeof value === 'string' ? value.trim() : '';

export const load: PageServerLoad = async ({ url }) => {
	return {
		featureKey: url.searchParams.get('feature_key')?.trim() ?? ''
	};
};

export const actions: Actions = {
	makeDecision: async ({ request, fetch }) => {
		const formData = await request.formData();
		const requestId = parseString(formData.get('request_id'));
		const featureKey = parseString(formData.get('feature_key'));
		const userId = parseString(formData.get('user_id'));
		const contextValue = parseString(formData.get('context'));

		if (!requestId || !featureKey || !userId) {
			return fail(400, {
				action: 'makeDecision',
				error: 'Request id, feature key, and user id are required.'
			});
		}

		let context: Record<string, unknown> = {};

		if (contextValue) {
			try {
				context = JSON.parse(contextValue) as Record<string, unknown>;
			} catch (error) {
				return fail(400, {
					action: 'makeDecision',
					error: 'Context must be valid JSON.'
				});
			}
		}

		try {
			const decision = await apiRequest<DecisionResponse>(fetch, '/decisions', {
				method: 'POST',
				body: {
					request_id: requestId,
					feature_key: featureKey,
					user_id: userId,
					context
				}
			});

			return {
				action: 'makeDecision',
				success: true,
				message: 'Decision resolved.',
				decision
			};
		} catch (error) {
			return fail(400, {
				action: 'makeDecision',
				error: getErrorMessage(error)
			});
		}
	}
};
