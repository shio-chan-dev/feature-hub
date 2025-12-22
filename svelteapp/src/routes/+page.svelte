<script lang="ts">
	let { data, form } = $props();

	const featureCount = $derived(data.features.length);
	const experimentCount = $derived(
		data.features.filter((item) => item.status === 'experiment').length
	);
</script>

<div class="container">
	<section class="hero">
		<div class="reveal" style="--delay: 0s">
			<p class="eyebrow">Feature flags and experiments</p>
			<h1>Feature Hub Console</h1>
			<p class="lead">
				Manage feature states, configure experiments, and trace decisions with a single surface
				for the rollout pipeline.
			</p>
			<div class="tag-row">
				<a class="button primary" href="#create-feature">Create a feature</a>
				<a class="button ghost" href="/audits">Review audits</a>
			</div>
		</div>
		<div class="hero-panel reveal" style="--delay: 0.1s">
			<div class="metric">
				<span class="metric-value">{featureCount}</span>
				<span class="metric-label">features tracked</span>
			</div>
			<div class="metric">
				<span class="metric-value">{experimentCount}</span>
				<span class="metric-label">in experiment mode</span>
			</div>
			<div class="metric">
				<span class="metric-value">{featureCount - experimentCount}</span>
				<span class="metric-label">steady (off or on)</span>
			</div>
		</div>
	</section>

	<section class="section" id="create-feature">
		<div class="section-header">
			<h2 class="section-title">Create feature</h2>
			<span class="subtle">Feature key should be unique.</span>
		</div>
		<div class="panel">
			<form method="POST" action="?/createFeature" class="form-grid">
				<label>
					Key
					<input name="key" placeholder="new_checkout" required />
				</label>
				<label>
					Name
					<input name="name" placeholder="New checkout" required />
				</label>
				<div class="form-actions">
					<button class="button primary" type="submit">Create</button>
					<span class="helper">Default status is off.</span>
				</div>
			</form>
			{#if form?.action === 'createFeature'}
				{#if form?.error}
					<p class="banner error" role="alert">{form.error}</p>
				{:else if form?.success}
					<p class="banner success">{form.message}</p>
				{/if}
			{/if}
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">Feature portfolio</h2>
			<span class="badge">{featureCount} total</span>
		</div>
		{#if data.error}
			<p class="banner error" role="alert">{data.error}</p>
		{:else if data.features.length === 0}
			<div class="panel">
				<p>No features yet. Create the first one to begin experiments.</p>
			</div>
		{:else}
			<div class="feature-grid">
				{#each data.features as feature, index}
					<article class="card reveal" style={`--delay: ${index * 0.04}s`}>
						<header>
							<div>
								<div class="card-title">{feature.name}</div>
								<div class="card-meta">{feature.key}</div>
							</div>
							<span class={`status status--${feature.status}`}>{feature.status}</span>
						</header>
						<div class="subtle">
							Active experiment: {feature.active_experiment_id ?? 'none'}
						</div>
						<div class="card-actions">
							<a class="button" href={`/features/${feature.id}`}>Open</a>
							<a
								class="button ghost"
								href={`/decisions?feature_key=${encodeURIComponent(feature.key)}`}
							>
								Try decision
							</a>
						</div>
					</article>
				{/each}
			</div>
		{/if}
	</section>
</div>
