<script lang="ts">
	import { defaultLocale, format, translations } from '$lib/i18n';

	let { data, form } = $props();

	const currentLocale = $derived(data.locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);
	const featureCount = $derived(data.features.length);
	const experimentCount = $derived(
		data.features.filter((item) => item.status === 'experiment').length
	);
</script>

<div class="container">
	<section class="hero">
		<div class="reveal" style="--delay: 0s">
			<p class="eyebrow">{copy.features.eyebrow}</p>
			<h1>{copy.features.title}</h1>
			<p class="lead">{copy.features.lead}</p>
			<div class="tag-row">
				<a class="button primary" href="#create-feature">{copy.features.createFeature}</a>
				<a class="button ghost" href="/audits">{copy.features.reviewAudits}</a>
			</div>
		</div>
		<div class="hero-panel reveal" style="--delay: 0.1s">
			<div class="metric">
				<span class="metric-value">{featureCount}</span>
				<span class="metric-label">{copy.features.metrics.featuresTracked}</span>
			</div>
			<div class="metric">
				<span class="metric-value">{experimentCount}</span>
				<span class="metric-label">{copy.features.metrics.experimentMode}</span>
			</div>
			<div class="metric">
				<span class="metric-value">{featureCount - experimentCount}</span>
				<span class="metric-label">{copy.features.metrics.steady}</span>
			</div>
		</div>
	</section>

	<section class="section" id="create-feature">
		<div class="section-header">
			<h2 class="section-title">{copy.features.createTitle}</h2>
			<span class="subtle">{copy.features.createHint}</span>
		</div>
		<div class="panel">
			<form method="POST" action="?/createFeature" class="form-grid">
				<label>
					{copy.features.form.key}
					<input name="key" placeholder="new_checkout" required />
				</label>
				<label>
					{copy.features.form.name}
					<input name="name" placeholder="New checkout" required />
				</label>
				<div class="form-actions">
					<button class="button primary" type="submit">{copy.features.form.create}</button>
					<span class="helper">{copy.features.form.helper}</span>
				</div>
			</form>
			{#if form?.action === 'createFeature'}
				{#if form?.error}
					<p class="banner error" role="alert">{form.error}</p>
				{:else if form?.success}
					<p class="banner success">
						{format(copy.messages.featureCreated, {
							key: form.feature?.key ?? copy.common.unknown
						})}
					</p>
				{/if}
			{/if}
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">{copy.features.portfolioTitle}</h2>
			<span class="badge">
				{format(copy.features.totalLabel, { count: String(featureCount) })}
			</span>
		</div>
		{#if data.error}
			<p class="banner error" role="alert">{data.error}</p>
		{:else if data.features.length === 0}
			<div class="panel">
				<p>{copy.features.emptyState}</p>
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
							<span class={`status status--${feature.status}`}>
								{copy.statuses[feature.status]}
							</span>
						</header>
						<div class="subtle">
							{copy.features.activeExperiment}: {feature.active_experiment_id ?? copy.common.none}
						</div>
						<div class="card-actions">
							<a class="button" href={`/features/${feature.id}`}>{copy.common.open}</a>
							<a
								class="button ghost"
								href={`/decisions?feature_key=${encodeURIComponent(feature.key)}`}
							>
								{copy.features.tryDecision}
							</a>
						</div>
					</article>
				{/each}
			</div>
		{/if}
	</section>
</div>
