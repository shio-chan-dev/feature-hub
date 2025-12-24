export type FeatureStatus = 'off' | 'on' | 'experiment';
export type ExperimentStatus = 'draft' | 'running' | 'paused';

export type Feature = {
	id: string;
	key: string;
	name: string;
	status: FeatureStatus;
	active_experiment_id: string | null;
};

export type Experiment = {
	id: string;
	feature_id: string;
	name: string;
	seed: string;
	status: ExperimentStatus;
	rollout_percent: number;
};

export type Variant = {
	id: string;
	experiment_id: string;
	key: string;
	weight: number;
	is_control: boolean;
	payload: Record<string, unknown>;
};

export type DecisionResponse = {
	request_id: string;
	feature_key: string;
	experiment_id: string | null;
	variant_key: string;
	variant_payload: Record<string, unknown>;
	reason: 'feature_off' | 'feature_on' | 'experiment_inactive' | 'assigned';
};

export type AuditItem = {
	id: string;
	request_id: string;
	feature_id: string;
	feature_key: string;
	experiment_id: string | null;
	user_id: string;
	variant_key: string;
	variant_payload: Record<string, unknown>;
	reason: string;
	decided_at: string;
};

export type AuditList = {
	items: AuditItem[];
	next_cursor: string | null;
};
