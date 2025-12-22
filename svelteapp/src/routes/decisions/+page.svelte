<script lang="ts">
	let { data, form } = $props();
	const contextPlaceholder = '{"tier":"beta"}';
</script>

<div class="container">
	<section class="section">
		<h1>Decision playground</h1>
		<p class="lead">
			Simulate a decision response using the live API. Use this when validating rollout logic and
			payload delivery.
		</p>
	</section>

	<section class="section">
		<div class="panel">
			<form method="POST" action="?/makeDecision" class="form-grid">
				<label>
					Request ID
					<input name="request_id" placeholder="req-001" required />
				</label>
				<label>
					Feature key
					<input name="feature_key" value={data.featureKey} placeholder="new_checkout" required />
				</label>
				<label>
					User ID
					<input name="user_id" placeholder="user-123" required />
				</label>
				<label>
					Context (JSON)
					<textarea name="context" placeholder={contextPlaceholder}></textarea>
				</label>
				<div class="form-actions">
					<button class="button primary" type="submit">Resolve decision</button>
					<a class="button ghost" href="/">Back to features</a>
				</div>
			</form>
			{#if form?.action === 'makeDecision'}
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
			<h2 class="section-title">Decision response</h2>
			<span class="subtle">Reason codes: feature_off, feature_on, experiment_inactive, assigned.</span>
		</div>
		{#if form?.decision}
			<div class="panel">
				<pre class="code-block">{JSON.stringify(form.decision, null, 2)}</pre>
			</div>
		{:else}
			<div class="panel">
				<p>Submit a request to see the decision payload.</p>
			</div>
		{/if}
	</section>
</div>
