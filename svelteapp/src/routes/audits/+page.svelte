<script lang="ts">
	import { defaultLocale, translations } from '$lib/i18n';
	import { goto } from '$app/navigation';
	import { base } from '$app/paths';

	let { data } = $props();
	const currentLocale = $derived(data.locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);

	const goBack = () => {
		if (typeof window !== 'undefined' && window.history.length > 1) {
			window.history.back();
			return;
		}
		goto(base || '/');
	};
</script>

<div class="container">
	<section class="section">
		<h1>{copy.audits.title}</h1>
		<p class="lead">{copy.audits.lead}</p>
	</section>

	<section class="section">
		<div class="panel">
			<form method="GET" class="form-grid">
				<label>
					{copy.audits.form.featureId}
					<input
						name="feature_id"
						value={data.featureId}
						placeholder="feat-001"
						list="feature-list"
					/>
				</label>
				<label>
					{copy.audits.form.limit}
					<input name="limit" type="number" min="1" max="200" value={data.limit} />
				</label>
				<div class="form-actions">
					<button class="button primary" type="submit">{copy.audits.form.load}</button>
					<button class="button ghost" type="button" onclick={goBack}>
						{copy.common.backToFeatures}
					</button>
				</div>
			</form>
			<datalist id="feature-list">
				{#each data.features as feature}
					<option value={feature.id}>{feature.name} ({feature.key})</option>
				{/each}
			</datalist>
			<p class="subtle">{copy.audits.featureHint}</p>
			{#if data.featureListError}
				<p class="subtle">{copy.audits.featureListError}</p>
			{/if}
			{#if data.features.length > 0}
				<div class="tag-row">
					{#each data.features.slice(0, 6) as feature}
						<a
							class="button ghost"
							href={`${base}/audits?feature_id=${encodeURIComponent(feature.id)}&limit=${data.limit}`}
						>
							{feature.name}
						</a>
					{/each}
				</div>
			{:else}
				<p class="subtle">{copy.audits.noFeatures}</p>
			{/if}
			{#if data.error}
				<p class="banner error" role="alert">{data.error}</p>
			{/if}
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">{copy.audits.entriesTitle}</h2>
			<span class="subtle">
				{copy.audits.featureLabel}: {data.featureId || copy.common.noneSelected}
			</span>
		</div>
		{#if !data.featureId}
			<div class="panel">
				<p>{copy.audits.prompt}</p>
			</div>
		{:else if data.audits.length === 0}
			<div class="panel">
				<p>{copy.audits.emptyState}</p>
			</div>
		{:else}
			<div class="panel">
				<table class="table">
					<thead>
						<tr>
							<th>{copy.audits.table.decidedAt}</th>
							<th>{copy.audits.table.requestId}</th>
							<th>{copy.audits.table.userId}</th>
							<th>{copy.audits.table.variant}</th>
							<th>{copy.audits.table.reason}</th>
							<th>{copy.audits.table.payload}</th>
						</tr>
					</thead>
					<tbody>
						{#each data.audits as entry}
							<tr>
								<td>{entry.decided_at}</td>
								<td>{entry.request_id}</td>
								<td>{entry.user_id}</td>
								<td>
									<div>{entry.variant_key}</div>
									{#if entry.experiment_id}
										<div class="subtle">exp: {entry.experiment_id}</div>
									{/if}
								</td>
								<td>{entry.reason}</td>
								<td>
									<code>{JSON.stringify(entry.variant_payload)}</code>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
				{#if data.nextCursor}
					<div class="form-actions">
						<a
							class="button ghost"
							href={`?feature_id=${encodeURIComponent(data.featureId)}&limit=${data.limit}&cursor=${encodeURIComponent(data.nextCursor)}`}
						>
							{copy.audits.nextPage}
						</a>
					</div>
				{/if}
			</div>
		{/if}
	</section>
</div>
