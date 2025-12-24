import { fail } from '@sveltejs/kit';
import { apiRequest, getErrorMessage } from '$lib/server/api';
import type { Feature } from '$lib/types';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const features = await apiRequest<Feature[]>(fetch, '/features');
		return { features, error: null };
	} catch (error) {
		return { features: [], error: getErrorMessage(error) };
	}
};

export const actions: Actions = {
	createFeature: async ({ request, fetch }) => {
		const formData = await request.formData();
		const key = formData.get('key');
		const name = formData.get('name');
		const keyValue = typeof key === 'string' ? key.trim() : '';
		const nameValue = typeof name === 'string' ? name.trim() : '';

		if (!keyValue || !nameValue) {
			return fail(400, {
				action: 'createFeature',
				error: 'Key and name are required.'
			});
		}

		try {
			const feature = await apiRequest<Feature>(fetch, '/features', {
				method: 'POST',
				body: { key: keyValue, name: nameValue }
			});

			return {
				action: 'createFeature',
				success: true,
				message: `Feature ${feature.key} created.`,
				feature
			};
		} catch (error) {
			return fail(400, {
				action: 'createFeature',
				error: getErrorMessage(error)
			});
		}
	}
};
