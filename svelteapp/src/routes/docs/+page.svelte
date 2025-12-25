<script lang="ts">
	import { defaultLocale, format, translations } from '$lib/i18n';
	import { base } from '$app/paths';

	let { data } = $props();

	const currentLocale = $derived(data.locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);
	const apiBaseUrl = $derived(data.apiBaseUrl.replace(/\/$/, ''));
	const rootPath = base || '/';
	const quickStartSteps = $derived([
		format(copy.docs.quickStartSteps.start, {
			apiBaseUrl: `<code>${apiBaseUrl}</code>`
		}),
		format(copy.docs.quickStartSteps.runApp, {
			appDir: '<code>svelteapp/</code>',
			command: '<code>npm run dev</code>'
		}),
		copy.docs.quickStartSteps.createFeature,
		copy.docs.quickStartSteps.addVariants,
		copy.docs.quickStartSteps.activateExperiment,
		copy.docs.quickStartSteps.validateDecision
	]);
	const integrationSteps = $derived([
		format(copy.docs.integration.steps.call, {
			endpoint: `<code>POST ${apiBaseUrl}/decisions</code>`
		}),
		copy.docs.integration.steps.route,
		copy.docs.integration.steps.fallback,
		copy.docs.integration.steps.stability
	]);
	const decisionRequestSample = $derived(`POST ${apiBaseUrl}/decisions
{
  "request_id": "req-001",
  "feature_key": "new_checkout",
  "user_id": "user-123",
  "context": { "tier": "beta" }
}`);
	const decisionResponseSample = `{
  "request_id": "req-001",
  "feature_key": "new_checkout",
  "experiment_id": "exp-001",
  "variant_key": "control",
  "variant_payload": {},
  "reason": "assigned"
}`;
</script>

<div class="container">
	<section class="hero">
		<div class="reveal" style="--delay: 0s">
			<p class="eyebrow">{copy.docs.eyebrow}</p>
			<h1>{copy.docs.title}</h1>
			<p class="lead">{copy.docs.lead}</p>
			<div class="tag-row">
				<a class="button primary" href={rootPath}>{copy.docs.openFeatures}</a>
			</div>
		</div>
		<div class="hero-panel reveal" style="--delay: 0.1s">
			<div class="metric">
				<span class="metric-label">{copy.docs.apiBaseUrl}</span>
				<span class="metric-value" style="font-size: 1.4rem">{apiBaseUrl}</span>
			</div>
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">{copy.docs.quickStartTitle}</h2>
			<span class="subtle">{copy.docs.quickStartHint}</span>
		</div>
		<div class="panel">
			<ol class="doc-list">
				{#each quickStartSteps as step}
					<li>{@html step}</li>
				{/each}
			</ol>
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">{copy.docs.integration.title}</h2>
			<span class="subtle">{copy.docs.integration.hint}</span>
		</div>
		<div class="panel">
			<ol class="doc-list">
				{#each integrationSteps as step}
					<li>{@html step}</li>
				{/each}
			</ol>
		</div>
		<div class="section-header">
			<h3 class="section-title">{copy.docs.integration.sampleTitle}</h3>
			<span class="subtle">{copy.docs.integration.sampleHint}</span>
		</div>
		<div class="feature-grid">
			<div class="card">
				<div class="card-title">{copy.docs.integration.sampleRequest}</div>
				<pre class="code-block">{decisionRequestSample}</pre>
			</div>
			<div class="card">
				<div class="card-title">{copy.docs.integration.sampleResponse}</div>
				<pre class="code-block">{decisionResponseSample}</pre>
			</div>
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">{copy.docs.reasonsTitle}</h2>
			<span class="subtle">{copy.docs.reasonsHint}</span>
		</div>
		<div class="panel">
			<ul class="doc-list">
				<li><code>feature_off</code> — {copy.docs.reasons.featureOff}</li>
				<li><code>feature_on</code> — {copy.docs.reasons.featureOn}</li>
				<li><code>experiment_inactive</code> — {copy.docs.reasons.experimentInactive}</li>
				<li><code>assigned</code> — {copy.docs.reasons.assigned}</li>
			</ul>
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">{copy.docs.notesTitle}</h2>
			<span class="subtle">{copy.docs.notesHint}</span>
		</div>
		<div class="panel">
			<ul class="doc-list">
				<li>{copy.docs.notes.inMemory}</li>
				<li>{copy.docs.notes.decisionLogic}</li>
				<li>{copy.docs.notes.auditStub}</li>
			</ul>
		</div>
	</section>
</div>
