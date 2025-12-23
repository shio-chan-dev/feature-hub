import { redirect } from '@sveltejs/kit';
import { defaultLocale, isLocale } from '$lib/i18n';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request, cookies, url }) => {
	const formData = await request.formData();
	const localeValue = formData.get('locale');
	const redirectValue = formData.get('redirect');
	const resolvedLocale = isLocale(typeof localeValue === 'string' ? localeValue : null)
		? localeValue
		: defaultLocale;

	cookies.set('locale', resolvedLocale, { path: '/', sameSite: 'lax' });

	const target =
		typeof redirectValue === 'string' && redirectValue.startsWith('/')
			? redirectValue
			: `${url.pathname}${url.search}`;

	throw redirect(303, target);
};
