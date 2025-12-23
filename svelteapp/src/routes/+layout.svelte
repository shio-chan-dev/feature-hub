<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import AppHeader from '$lib/components/AppHeader.svelte';

	let { children, data } = $props();

	$effect(() => {
		if (data?.locale && typeof document !== 'undefined') {
			document.documentElement.lang = data.locale;
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600;700&family=Space+Grotesk:wght@400;500;600&display=swap"
	/>
	<title>Feature Hub</title>
</svelte:head>

<div class="app-shell">
	<a class="skip-link" href="#main">Skip to content</a>
	<AppHeader locale={data.locale} />
	<main class="page" id="main">{@render children()}</main>
</div>
