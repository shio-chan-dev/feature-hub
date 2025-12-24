import { env } from '$env/dynamic/private';

const DEFAULT_BASE_URL = 'http://localhost:6789';

export const API_BASE_URL = env.API_BASE_URL ?? DEFAULT_BASE_URL;

export class ApiError extends Error {
	status: number;

	constructor(status: number, message: string) {
		super(message);
		this.name = 'ApiError';
		this.status = status;
	}
}

export type ApiRequestInit = Omit<RequestInit, 'body'> & {
	body?: unknown;
};

export async function apiRequest<T>(
	fetcher: typeof fetch,
	path: string,
	options: ApiRequestInit = {}
): Promise<T> {
	const { body, headers, ...rest } = options;
	const init: RequestInit = {
		...rest,
		headers: {
			...(headers ?? {}),
			...(body !== undefined ? { 'Content-Type': 'application/json' } : {})
		}
	};

	if (body !== undefined) {
		init.body = JSON.stringify(body);
	}

	const response = await fetcher(`${API_BASE_URL}${path}`, init);
	const contentType = response.headers.get('content-type') ?? '';
	const hasJson = contentType.includes('application/json');
	const payload = hasJson ? await response.json() : null;

	if (!response.ok) {
		const message =
			payload && typeof payload === 'object' && 'detail' in payload
				? String(payload.detail)
				: `Request failed (${response.status})`;
		throw new ApiError(response.status, message);
	}

	return payload as T;
}

export function getErrorMessage(error: unknown): string {
	if (error instanceof ApiError) {
		return error.message;
	}

	if (error instanceof Error) {
		return error.message;
	}

	return 'Unexpected error.';
}
