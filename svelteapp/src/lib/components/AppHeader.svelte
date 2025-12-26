<script lang="ts">
	// SvelteKit stores for current URL info and navigation state.
	import { page, navigating } from '$app/stores';
	import { base } from '$app/paths';
	// Localization helpers and types.
	import { defaultLocale, localeLabels, locales, translations, type Locale } from '$lib/i18n';
	import logo from '$lib/assets/logo.png';

	// Props injected by the root layout.
	// - locale: current UI language
	// - apiBaseUrl: backend base URL (from server env)
	let { locale, apiBaseUrl } = $props<{ locale: Locale; apiBaseUrl?: string }>();

	const rootPath = base || '/';
	const withBase = (path: string) => (base ? `${base}${path}` : path);
	const featuresPrefix = base ? `${base}/features` : '/features';

	// Top-level navigation links; key maps to i18n labels.
	const navItems = [
		{ href: rootPath, key: 'features' },
		{ href: withBase('/audits'), key: 'audits' },
		{ href: withBase('/decisions'), key: 'decisions' }
	] as const;

	// $derived makes a reactive value that updates when dependencies change.
	const pathname = $derived($page.url.pathname);
	const isSyncing = $derived(Boolean($navigating));
	// Keep the current page + query so language switch can return here.
	const redirectTarget = $derived(`${$page.url.pathname}${$page.url.search}`);
	const currentLocale = $derived(locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);
	// Friendly string for the API base URL shown in the header pill.
	const apiDisplay = $derived(
		(() => {
			if (!apiBaseUrl) {
				return copy.common.unknown;
			}
			try {
				return new URL(apiBaseUrl).host;
			} catch {
				return apiBaseUrl.replace(/^https?:\/\//, '').replace(/\/$/, '');
			}
		})()
	);

	const isActive = (href: string) => {
		if (href === rootPath) {
			return pathname === rootPath || pathname.startsWith(featuresPrefix);
		}

		return pathname.startsWith(href);
	};

	// Submit the locale switch form when the select value changes.
	const submitLocale = (event: Event) => {
		const form = (event.currentTarget as HTMLSelectElement | null)?.form;
		form?.requestSubmit();
	};
</script>

<header class="app-header">
	<!-- Brand / product identity -->
	<a class="brand" href={rootPath}>
		<img class="brand-mark" src={logo} alt="Feature Hub logo" />
		<div class="brand-text">
			<div class="brand-title">{copy.header.brandTitle}</div>
			<div class="brand-subtitle">{copy.header.brandSubtitle}</div>
		</div>
	</a>

	<!-- Primary navigation -->
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

	<!-- Right-side controls and status -->
	<div class="header-meta">
		<!-- Locale switcher posts to /set-locale with a redirect back -->
		<form class="lang-form" method="POST" action={withBase('/set-locale')}>
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
		<!-- Quick links -->
		<a class="button ghost" href={withBase('/docs')}>{copy.header.docs}</a>
		<a class="button primary" href={`${rootPath}#create-feature`}>{copy.header.newFeature}</a>
		<!-- API base URL status pill -->
		<div class="meta-pill" title={apiBaseUrl}>
			<span class="dot" aria-hidden="true"></span>
			<span>{copy.header.apiLabel}: {apiDisplay}</span>
		</div>
		<!-- Live navigation indicator -->
		{#if isSyncing}
			<span class="sync" role="status" aria-live="polite">{copy.header.syncing}</span>
		{/if}
	</div>
</header>
