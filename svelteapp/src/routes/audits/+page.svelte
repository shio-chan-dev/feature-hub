<script lang="ts">
	import { defaultLocale, translations } from '$lib/i18n';

	let { data } = $props();
	const currentLocale = $derived(data.locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);
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
					<input name="feature_id" value={data.featureId} placeholder="feat-001" />
				</label>
				<label>
					{copy.audits.form.limit}
					<input name="limit" type="number" min="1" max="200" value={data.limit} />
				</label>
				<div class="form-actions">
					<button class="button primary" type="submit">{copy.audits.form.load}</button>
					<a class="button ghost" href="/">{copy.common.backToFeatures}</a>
				</div>
			</form>
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
				<p class="subtle">{copy.audits.stubHint}</p>
			</div>
		{:else}
			<div class="panel">
				<table class="table">
					<thead>
						<tr>
							<th>{copy.audits.table.timestamp}</th>
							<th>{copy.audits.table.actor}</th>
							<th>{copy.audits.table.action}</th>
							<th>{copy.audits.table.diff}</th>
						</tr>
					</thead>
					<tbody>
						{#each data.audits as entry}
							<tr>
								<td>{entry.timestamp}</td>
								<td>{entry.actor}</td>
								<td>{entry.action}</td>
								<td>
									<code>{JSON.stringify(entry.diff)}</code>
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
