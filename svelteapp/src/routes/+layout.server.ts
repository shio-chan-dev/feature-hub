import { defaultLocale, isLocale } from '$lib/i18n';
import type { LayoutServerLoad } from './$types';

const resolveLocale = (cookieValue: string | undefined, acceptLanguage: string | null) => {
	if (isLocale(cookieValue)) {
		return cookieValue;
	}

	if (acceptLanguage && acceptLanguage.toLowerCase().includes('zh')) {
		return 'zh';
	}

	return defaultLocale;
};

export const load: LayoutServerLoad = async ({ cookies, request }) => {
	const locale = resolveLocale(cookies.get('locale'), request.headers.get('accept-language'));
	return { locale };
};
