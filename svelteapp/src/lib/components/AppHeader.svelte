<script lang="ts">
	import { page, navigating } from '$app/stores';
	import { defaultLocale, localeLabels, locales, translations, type Locale } from '$lib/i18n';

	let { locale } = $props<{ locale: Locale }>();

	const navItems = [
		{ href: '/', key: 'features' },
		{ href: '/audits', key: 'audits' },
		{ href: '/decisions', key: 'decisions' }
	] as const;

	const pathname = $derived($page.url.pathname);
	const isSyncing = $derived(Boolean($navigating));
	const redirectTarget = $derived(`${$page.url.pathname}${$page.url.search}`);
	const currentLocale = $derived(locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);

	const isActive = (href: string) => {
		if (href === '/') {
			return pathname === '/' || pathname.startsWith('/features');
		}

		return pathname.startsWith(href);
	};

	const submitLocale = (event: Event) => {
		const form = (event.currentTarget as HTMLSelectElement | null)?.form;
		form?.requestSubmit();
	};
</script>

<header class="app-header">
	<div class="brand">
		<div class="brand-title">{copy.header.brandTitle}</div>
		<div class="brand-subtitle">{copy.header.brandSubtitle}</div>
	</div>

	<nav class="nav" aria-label="Primary">
		{#each navItems as item}
			<a
				class:active={isActive(item.href)}
				href={item.href}
				aria-current={isActive(item.href) ? 'page' : undefined}
			>
				{copy.header.nav[item.key]}
			</a>
		{/each}
	</nav>

	<div class="header-meta">
		<form class="lang-form" method="POST" action="/set-locale">
			<input type="hidden" name="redirect" value={redirectTarget} />
			<label class="lang-select">
				<span>{copy.header.language}</span>
				<select name="locale" onchange={submitLocale}>
					{#each locales as localeOption}
						<option value={localeOption} selected={localeOption === currentLocale}>
							{localeLabels[localeOption]}
						</option>
					{/each}
				</select>
			</label>
		</form>
		<a class="button ghost" href="/docs">{copy.header.docs}</a>
		<a class="button primary" href="/#create-feature">{copy.header.newFeature}</a>
		<div class="meta-pill">
			<span class="dot" aria-hidden="true"></span>
			<span>{copy.header.apiLabel}: 6789</span>
		</div>
		{#if isSyncing}
			<span class="sync" role="status" aria-live="polite">{copy.header.syncing}</span>
		{/if}
	</div>
</header>
