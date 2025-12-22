<script lang="ts">
	let { data } = $props();
</script>

<div class="container">
	<section class="section">
		<h1>Audit log</h1>
		<p class="lead">
			Track configuration changes across features. Provide a feature ID to view audit entries.
		</p>
	</section>

	<section class="section">
		<div class="panel">
			<form method="GET" class="form-grid">
				<label>
					Feature ID
					<input name="feature_id" value={data.featureId} placeholder="feat-001" />
				</label>
				<label>
					Limit
					<input name="limit" type="number" min="1" max="200" value={data.limit} />
				</label>
				<div class="form-actions">
					<button class="button primary" type="submit">Load audits</button>
					<a class="button ghost" href="/">Back to features</a>
				</div>
			</form>
			{#if data.error}
				<p class="banner error" role="alert">{data.error}</p>
			{/if}
		</div>
	</section>

	<section class="section">
		<div class="section-header">
			<h2 class="section-title">Entries</h2>
			<span class="subtle">Feature: {data.featureId || 'none selected'}</span>
		</div>
		{#if !data.featureId}
			<div class="panel">
				<p>Enter a feature ID to view audit history.</p>
			</div>
		{:else if data.audits.length === 0}
			<div class="panel">
				<p>No audit entries yet for this feature.</p>
				<p class="subtle">The backend currently returns an empty list (stub).</p>
			</div>
		{:else}
			<div class="panel">
				<table class="table">
					<thead>
						<tr>
							<th>Timestamp</th>
							<th>Actor</th>
							<th>Action</th>
							<th>Diff</th>
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
						Next page
					</a>
				</div>
			{/if}
		</div>
	{/if}
	</section>
</div>
