import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { loadEnv } from 'vite';

const mode = process.env.NODE_ENV ?? 'development';
const env = loadEnv(mode, process.cwd(), '');

const normalizeBasePath = (value) => {
	if (!value) {
		return '';
	}
	let base = value.trim();
	if (!base.startsWith('/')) {
		base = `/${base}`;
	}
	if (base !== '/' && base.endsWith('/')) {
		base = base.slice(0, -1);
	}
	return base === '/' ? '' : base;
};

const basePath = normalizeBasePath(env.FEATUREHUB_BASE_PATH);

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter(),
		paths: { base: basePath }
	}
};

export default config;
