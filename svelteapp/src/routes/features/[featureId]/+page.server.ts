import { fail } from '@sveltejs/kit';
import { apiRequest, getErrorMessage } from '$lib/server/api';
import type { Experiment, Feature, FeatureStatus, ExperimentStatus, Variant } from '$lib/types';
import type { Actions, PageServerLoad } from './$types';

const featureStatusOptions = ['off', 'on', 'experiment'] as const;
const experimentStatusOptions = ['draft', 'running', 'paused'] as const;

const isFeatureStatus = (value: string): value is FeatureStatus =>
	featureStatusOptions.includes(value as FeatureStatus);

const isExperimentStatus = (value: string): value is ExperimentStatus =>
	experimentStatusOptions.includes(value as ExperimentStatus);

const parseString = (value: FormDataEntryValue | null) =>
	typeof value === 'string' ? value.trim() : '';

const parseNumber = (value: FormDataEntryValue | null) => {
	if (typeof value !== 'string') {
		return null;
	}
	const parsed = Number(value);
	return Number.isFinite(parsed) ? parsed : null;
};

const parseOptionalNumber = (value: FormDataEntryValue | null) => {
	if (typeof value !== 'string') {
		return null;
	}
	const trimmed = value.trim();
	if (!trimmed) {
		return null;
	}
	const parsed = Number(trimmed);
	return Number.isFinite(parsed) ? parsed : null;
};

const parseOptionalBoolean = (value: FormDataEntryValue | null) => {
	if (typeof value !== 'string') {
		return null;
	}
	if (value === 'true') {
		return true;
	}
	if (value === 'false') {
		return false;
	}
	return null;
};

export const load: PageServerLoad = async ({ fetch, params, url }) => {
	const featureId = params.featureId;

	try {
		const feature = await apiRequest<Feature>(fetch, `/features/${featureId}`);
		const experiments = await apiRequest<Experiment[]>(fetch, `/features/${featureId}/experiments`);
		const requestedExperimentId = url.searchParams.get('experiment');
		const fallbackExperimentId = feature.active_experiment_id ?? experiments[0]?.id ?? null;
		const selectedExperimentId = requestedExperimentId ?? fallbackExperimentId;
		const selectedExperiment =
			experiments.find((experiment) => experiment.id === selectedExperimentId) ?? null;
		const variants = selectedExperiment
			? await apiRequest<Variant[]>(fetch, `/experiments/${selectedExperiment.id}/variants`)
			: [];

		return {
			feature,
			experiments,
			selectedExperimentId: selectedExperiment?.id ?? null,
			selectedExperiment,
			variants,
			error: null
		};
	} catch (error) {
		return {
			feature: null,
			experiments: [],
			selectedExperimentId: null,
			selectedExperiment: null,
			variants: [],
			error: getErrorMessage(error)
		};
	}
};

export const actions: Actions = {
	updateFeature: async ({ request, fetch, params }) => {
		const formData = await request.formData();
		const nameValue = parseString(formData.get('name'));
		const statusValue = parseString(formData.get('status'));
		const activeExperimentValue = parseString(formData.get('active_experiment_id'));

		if (!statusValue || !isFeatureStatus(statusValue)) {
			return fail(400, {
				action: 'updateFeature',
				error: 'Feature status must be off, on, or experiment.'
			});
		}

		if (statusValue === 'experiment' && !activeExperimentValue) {
			return fail(400, {
				action: 'updateFeature',
				error: 'Active experiment is required for experiment status.'
			});
		}

		try {
			const payload = {
				name: nameValue || undefined,
				status: statusValue,
				active_experiment_id: statusValue === 'experiment' ? activeExperimentValue : null
			};

			const feature = await apiRequest<Feature>(fetch, `/features/${params.featureId}`, {
				method: 'PATCH',
				body: payload
			});

			return {
				action: 'updateFeature',
				success: true,
				message: 'Feature updated.',
				feature
			};
		} catch (error) {
			return fail(400, {
				action: 'updateFeature',
				error: getErrorMessage(error)
			});
		}
	},
	createExperiment: async ({ request, fetch, params }) => {
		const formData = await request.formData();
		const nameValue = parseString(formData.get('name'));
		const seedValue = parseString(formData.get('seed'));
		const rolloutValue = parseNumber(formData.get('rollout_percent'));

		if (!nameValue || !seedValue || rolloutValue === null) {
			return fail(400, {
				action: 'createExperiment',
				error: 'Name, seed, and rollout percent are required.'
			});
		}

		if (rolloutValue < 0 || rolloutValue > 100) {
			return fail(400, {
				action: 'createExperiment',
				error: 'Rollout percent must be between 0 and 100.'
			});
		}

		try {
			const experiment = await apiRequest<Experiment>(
				fetch,
				`/features/${params.featureId}/experiments`,
				{
					method: 'POST',
					body: {
						name: nameValue,
						seed: seedValue,
						rollout_percent: rolloutValue
					}
				}
			);

			return {
				action: 'createExperiment',
				success: true,
				message: 'Experiment created.',
				experiment
			};
		} catch (error) {
			return fail(400, {
				action: 'createExperiment',
				error: getErrorMessage(error)
			});
		}
	},
	updateExperiment: async ({ request, fetch }) => {
		const formData = await request.formData();
		const experimentId = parseString(formData.get('experiment_id'));
		const nameValue = parseString(formData.get('name'));
		const statusValue = parseString(formData.get('status'));
		const seedValue = parseString(formData.get('seed'));
		const rolloutValue = parseNumber(formData.get('rollout_percent'));

		if (!experimentId) {
			return fail(400, {
				action: 'updateExperiment',
				error: 'Experiment id is missing.'
			});
		}

		if (statusValue && !isExperimentStatus(statusValue)) {
			return fail(400, {
				action: 'updateExperiment',
				experimentId,
				error: 'Experiment status must be draft, running, or paused.'
			});
		}

		if (rolloutValue !== null && (rolloutValue < 0 || rolloutValue > 100)) {
			return fail(400, {
				action: 'updateExperiment',
				experimentId,
				error: 'Rollout percent must be between 0 and 100.'
			});
		}

		try {
			const payload = {
				name: nameValue || undefined,
				status: statusValue || undefined,
				seed: seedValue || undefined,
				rollout_percent: rolloutValue ?? undefined
			};

			const experiment = await apiRequest<Experiment>(fetch, `/experiments/${experimentId}`, {
				method: 'PATCH',
				body: payload
			});

			return {
				action: 'updateExperiment',
				success: true,
				experimentId,
				message: 'Experiment updated.',
				experiment
			};
		} catch (error) {
			return fail(400, {
				action: 'updateExperiment',
				experimentId,
				error: getErrorMessage(error)
			});
		}
	},
	createVariant: async ({ request, fetch }) => {
		const formData = await request.formData();
		const experimentId = parseString(formData.get('experiment_id'));
		const keyValue = parseString(formData.get('key'));
		const weightValue = parseNumber(formData.get('weight'));
		const payloadValue = parseString(formData.get('payload'));
		const isControl = formData.get('is_control') !== null;

		if (!experimentId || !keyValue || weightValue === null) {
			return fail(400, {
				action: 'createVariant',
				error: 'Experiment id, key, and weight are required.'
			});
		}

		if (weightValue < 0) {
			return fail(400, {
				action: 'createVariant',
				error: 'Weight must be zero or more.'
			});
		}

		let payload: Record<string, unknown> = {};

		if (payloadValue) {
			try {
				payload = JSON.parse(payloadValue) as Record<string, unknown>;
			} catch (error) {
				return fail(400, {
					action: 'createVariant',
					error: 'Payload must be valid JSON.'
				});
			}
		}

		try {
			const variant = await apiRequest<Variant>(fetch, `/experiments/${experimentId}/variants`, {
				method: 'POST',
				body: {
					key: keyValue,
					weight: weightValue,
					is_control: isControl,
					payload
				}
			});

			return {
				action: 'createVariant',
				success: true,
				experimentId,
				message: 'Variant added.',
				variant
			};
		} catch (error) {
			return fail(400, {
				action: 'createVariant',
				error: getErrorMessage(error)
			});
		}
	},
	updateVariant: async ({ request, fetch }) => {
		const formData = await request.formData();
		const variantId = parseString(formData.get('variant_id'));
		const weightValue = parseOptionalNumber(formData.get('weight'));
		const isControlValue = parseOptionalBoolean(formData.get('is_control'));
		const payloadValue = parseString(formData.get('payload'));

		if (!variantId) {
			return fail(400, {
				action: 'updateVariant',
				error: 'Variant id is missing.'
			});
		}

		if (weightValue !== null && weightValue < 0) {
			return fail(400, {
				action: 'updateVariant',
				variantId,
				error: 'Weight must be zero or more.'
			});
		}

		let payload: Record<string, unknown> | undefined;

		if (payloadValue) {
			try {
				payload = JSON.parse(payloadValue) as Record<string, unknown>;
			} catch (error) {
				return fail(400, {
					action: 'updateVariant',
					variantId,
					error: 'Payload must be valid JSON.'
				});
			}
		}

		const patch: Partial<Pick<Variant, 'weight' | 'is_control' | 'payload'>> = {};

		if (weightValue !== null) {
			patch.weight = weightValue;
		}
		if (isControlValue !== null) {
			patch.is_control = isControlValue;
		}
		if (payload !== undefined) {
			patch.payload = payload;
		}

		if (Object.keys(patch).length === 0) {
			return fail(400, {
				action: 'updateVariant',
				variantId,
				error: 'No updates provided.'
			});
		}

		try {
			const variant = await apiRequest<Variant>(fetch, `/variants/${variantId}`, {
				method: 'PATCH',
				body: patch
			});

			return {
				action: 'updateVariant',
				success: true,
				variantId,
				message: 'Variant updated.',
				variant
			};
		} catch (error) {
			return fail(400, {
				action: 'updateVariant',
				variantId,
				error: getErrorMessage(error)
			});
		}
	}
};
