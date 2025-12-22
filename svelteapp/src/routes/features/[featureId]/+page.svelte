<script lang="ts">
	let { data, form } = $props();
	const payloadPlaceholder = '{"ui":"v2"}';
</script>

<div class="container">
	<section class="section">
		<div class="tag-row">
			<a class="button ghost" href="/">Back to features</a>
		</div>
		<h1>{data.feature?.name ?? 'Feature detail'}</h1>
		<p class="subtle">Key: {data.feature?.key ?? 'unknown'} | ID: {data.feature?.id ?? 'n/a'}</p>
	</section>

	{#if data.error}
		<p class="banner error" role="alert">{data.error}</p>
	{:else if !data.feature}
		<div class="panel">
			<p>Feature not found.</p>
		</div>
	{:else}
		<section class="section">
			<div class="section-header">
				<h2 class="section-title">Feature status</h2>
				<span class={`status status--${data.feature.status}`}>{data.feature.status}</span>
			</div>
			<div class="panel">
				<form method="POST" action="?/updateFeature" class="form-grid">
					<label>
						Status
						<select name="status" required>
							<option value="off" selected={data.feature.status === 'off'}>off</option>
							<option value="on" selected={data.feature.status === 'on'}>on</option>
							<option value="experiment" selected={data.feature.status === 'experiment'}>
								experiment
							</option>
						</select>
					</label>
					<label>
						Active experiment
						<select name="active_experiment_id">
							<option value="">None</option>
							{#each data.experiments as experiment}
								<option
									value={experiment.id}
									selected={experiment.id === data.feature.active_experiment_id}
								>
									{experiment.name} ({experiment.id})
								</option>
							{/each}
						</select>
					</label>
					<div class="form-actions">
						<button class="button primary" type="submit">Update feature</button>
						<span class="helper">Experiment mode requires an active experiment.</span>
					</div>
				</form>
				{#if form?.action === 'updateFeature'}
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
				<h2 class="section-title">Experiments</h2>
				<span class="subtle">Configure rollout and status per experiment.</span>
			</div>
			<div class="panel">
				<form method="POST" action="?/createExperiment" class="form-grid">
					<label>
						Name
						<input name="name" placeholder="checkout-test" required />
					</label>
					<label>
						Seed
						<input name="seed" placeholder="2024q4" required />
					</label>
					<label>
						Rollout percent
						<input
							type="number"
							name="rollout_percent"
							min="0"
							max="100"
							value="50"
							required
						/>
					</label>
					<div class="form-actions">
						<button class="button primary" type="submit">Create experiment</button>
						<span class="helper">Default status is draft.</span>
					</div>
				</form>
				{#if form?.action === 'createExperiment'}
					{#if form?.error}
						<p class="banner error" role="alert">{form.error}</p>
					{:else if form?.success}
						<p class="banner success">{form.message}</p>
					{/if}
				{/if}
			</div>

			{#if data.experiments.length === 0}
				<div class="panel">
					<p>No experiments yet. Create one to start testing.</p>
				</div>
			{:else}
				<div class="feature-grid">
					{#each data.experiments as experiment, index}
						<article class="card reveal" style={`--delay: ${index * 0.04}s`}>
							<header>
								<div>
									<div class="card-title">{experiment.name}</div>
									<div class="card-meta">{experiment.id}</div>
								</div>
								<span class={`status status--${experiment.status}`}>{experiment.status}</span>
							</header>
							<div class="card-meta">Seed: {experiment.seed}</div>
							<div class="card-meta">Rollout: {experiment.rollout_percent}%</div>
							<form method="POST" action="?/updateExperiment" class="form-grid">
								<input type="hidden" name="experiment_id" value={experiment.id} />
								<label>
									Status
									<select name="status">
										<option value="draft" selected={experiment.status === 'draft'}>draft</option>
										<option value="running" selected={experiment.status === 'running'}>
											running
										</option>
										<option value="paused" selected={experiment.status === 'paused'}>
											paused
										</option>
									</select>
								</label>
								<label>
									Rollout percent
									<input
										type="number"
										name="rollout_percent"
										min="0"
										max="100"
										value={experiment.rollout_percent}
									/>
								</label>
								<label>
									Seed
									<input name="seed" value={experiment.seed} />
								</label>
								<div class="form-actions">
									<button class="button primary" type="submit">Update</button>
									<a
										class="button ghost"
										href={`?experiment=${encodeURIComponent(experiment.id)}#variants`}
									>
										Manage variants
									</a>
								</div>
							</form>
							{#if form?.action === 'updateExperiment' && form?.experimentId === experiment.id}
								{#if form?.error}
									<p class="banner error" role="alert">{form.error}</p>
								{:else if form?.success}
									<p class="banner success">{form.message}</p>
								{/if}
							{/if}
						</article>
					{/each}
				</div>
			{/if}
		</section>

		<section class="section" id="variants">
			<div class="section-header">
				<h2 class="section-title">Variants</h2>
				{#if data.selectedExperiment}
					<span class="subtle">For experiment: {data.selectedExperiment.name}</span>
				{:else}
					<span class="subtle">Select an experiment to manage variants.</span>
				{/if}
			</div>

			{#if !data.selectedExperiment}
				<div class="panel">
					<p>Choose an experiment to load variants.</p>
				</div>
			{:else}
				<div class="panel">
					{#if data.variants.length === 0}
						<p>No variants yet for this experiment.</p>
					{:else}
						<table class="table">
							<thead>
								<tr>
									<th>Key</th>
									<th>Weight</th>
									<th>Control</th>
									<th>Payload</th>
								</tr>
							</thead>
							<tbody>
								{#each data.variants as variant}
									<tr>
										<td>{variant.key}</td>
										<td>{variant.weight}</td>
										<td>{variant.is_control ? 'yes' : 'no'}</td>
										<td>
											<code>{JSON.stringify(variant.payload)}</code>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					{/if}
				</div>
				<div class="panel">
					<form method="POST" action="?/createVariant" class="form-grid">
						<input type="hidden" name="experiment_id" value={data.selectedExperiment.id} />
						<label>
							Key
							<input name="key" placeholder="control" required />
						</label>
						<label>
							Weight
							<input type="number" name="weight" min="0" value="50" required />
						</label>
						<label>
							Payload (JSON)
							<textarea name="payload" placeholder={payloadPlaceholder}></textarea>
						</label>
						<label class="toggle">
							Control
							<input type="checkbox" name="is_control" />
						</label>
						<div class="form-actions">
							<button class="button primary" type="submit">Add variant</button>
							<span class="helper">Control is required for safe fallback.</span>
						</div>
					</form>
					{#if form?.action === 'createVariant'}
						{#if form?.error}
							<p class="banner error" role="alert">{form.error}</p>
						{:else if form?.success}
							<p class="banner success">{form.message}</p>
						{/if}
					{/if}
				</div>
			{/if}
		</section>
	{/if}
</div>
