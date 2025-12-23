<script lang="ts">
	import { defaultLocale, translations } from '$lib/i18n';

	let { data, form } = $props();
	const contextPlaceholder = '{"tier":"beta"}';
	const currentLocale = $derived(data.locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);
</script>

<div class="container">
	<section class="section">
		<h1>{copy.decisions.title}</h1>
		<p class="lead">{copy.decisions.lead}</p>
	</section>

	<section class="section">
		<div class="panel">
			<form method="POST" action="?/makeDecision" class="form-grid">
				<label>
					{copy.decisions.form.requestId}
					<input name="request_id" placeholder="req-001" required />
				</label>
				<label>
					{copy.decisions.form.featureKey}
					<input name="feature_key" value={data.featureKey} placeholder="new_checkout" required />
				</label>
				<label>
					{copy.decisions.form.userId}
					<input name="user_id" placeholder="user-123" required />
				</label>
				<label>
					{copy.decisions.form.context}
					<textarea name="context" placeholder={contextPlaceholder}></textarea>
				</label>
				<div class="form-actions">
					<button class="button primary" type="submit">{copy.decisions.form.submit}</button>
					<a class="button ghost" href="/">{copy.common.backToFeatures}</a>
				</div>
			</form>
			{#if form?.action === 'makeDecision'}
				{#if form?.error}
					<p class="banner error" role="alert">{form.error}</p>
				{:else if form?.success}
					<p class="banner success">{copy.messages.decisionResolved}</p>
				{/if}
			{/if}
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">{copy.decisions.responseTitle}</h2>
			<span class="subtle">{copy.decisions.reasonHint}</span>
		</div>
		{#if form?.decision}
			<div class="panel">
				<pre class="code-block">{JSON.stringify(form.decision, null, 2)}</pre>
			</div>
		{:else}
			<div class="panel">
				<p>{copy.decisions.emptyState}</p>
			</div>
		{/if}
	</section>
</div>
