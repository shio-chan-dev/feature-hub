<script lang="ts">
	import { page, navigating } from '$app/stores';

	const navItems = [
		{ href: '/', label: 'Features' },
		{ href: '/audits', label: 'Audits' },
		{ href: '/decisions', label: 'Decisions' }
	];

	const pathname = $derived($page.url.pathname);
	const isSyncing = $derived(Boolean($navigating));

	const isActive = (href: string) => {
		if (href === '/') {
			return pathname === '/' || pathname.startsWith('/features');
		}

		return pathname.startsWith(href);
	};
</script>

<header class="app-header">
	<div class="brand">
		<div class="brand-title">Feature Hub</div>
		<div class="brand-subtitle">Experiment Console</div>
	</div>

	<nav class="nav" aria-label="Primary">
		{#each navItems as item}
			<a
				class:active={isActive(item.href)}
				href={item.href}
				aria-current={isActive(item.href) ? 'page' : undefined}
			>
				{item.label}
			</a>
		{/each}
	</nav>

	<div class="header-meta">
		<a class="button primary" href="/#create-feature">New Feature</a>
		<div class="meta-pill">
			<span class="dot" aria-hidden="true"></span>
			<span>API Local: 6789</span>
		</div>
		{#if isSyncing}
			<span class="sync" role="status" aria-live="polite">Syncing...</span>
		{/if}
	</div>
</header>
