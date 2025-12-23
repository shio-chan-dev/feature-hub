<script lang="ts">
	import { defaultLocale, format, translations } from '$lib/i18n';

	let { data, form } = $props();
	const payloadPlaceholder = '{"ui":"v2"}';
	const currentLocale = $derived(data.locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);
</script>

<div class="container">
	<section class="section">
		<div class="tag-row">
			<a class="button ghost" href="/">{copy.common.backToFeatures}</a>
		</div>
		<h1>{data.feature?.name ?? copy.featureDetail.titleFallback}</h1>
		<p class="subtle">
			{copy.featureDetail.keyLabel}: {data.feature?.key ?? copy.common.unknown} | {copy.featureDetail.idLabel}:
			{data.feature?.id ?? copy.common.unknown}
		</p>
	</section>

	{#if data.error}
		<p class="banner error" role="alert">{data.error}</p>
	{:else if !data.feature}
		<div class="panel">
			<p>{copy.featureDetail.titleFallback}</p>
		</div>
	{:else}
		<section class="section">
			<div class="section-header">
				<h2 class="section-title">{copy.featureDetail.statusTitle}</h2>
				<span class={`status status--${data.feature.status}`}>
					{copy.statuses[data.feature.status]}
				</span>
			</div>
			<div class="panel">
				<form method="POST" action="?/updateFeature" class="form-grid">
					<label>
						{copy.featureDetail.statusLabel}
						<select name="status" required>
							<option value="off" selected={data.feature.status === 'off'}>
								{copy.statuses.off}
							</option>
							<option value="on" selected={data.feature.status === 'on'}>
								{copy.statuses.on}
							</option>
							<option value="experiment" selected={data.feature.status === 'experiment'}>
								{copy.statuses.experiment}
							</option>
						</select>
					</label>
					<label>
						{copy.featureDetail.activeExperimentLabel}
						<select name="active_experiment_id">
							<option value="">{copy.featureDetail.activeExperimentNone}</option>
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
						<button class="button primary" type="submit">
							{copy.featureDetail.updateFeature}
						</button>
						<span class="helper">{copy.featureDetail.updateHint}</span>
					</div>
				</form>
				{#if form?.action === 'updateFeature'}
					{#if form?.error}
						<p class="banner error" role="alert">{form.error}</p>
					{:else if form?.success}
						<p class="banner success">{copy.messages.featureUpdated}</p>
					{/if}
				{/if}
			</div>
		</section>

		<section class="section">
			<div class="section-header">
				<h2 class="section-title">{copy.featureDetail.experimentsTitle}</h2>
				<span class="subtle">{copy.featureDetail.experimentsHint}</span>
			</div>
			<div class="panel">
				<form method="POST" action="?/createExperiment" class="form-grid">
					<label>
						{copy.featureDetail.experimentForm.name}
						<input name="name" placeholder="checkout-test" required />
					</label>
					<label>
						{copy.featureDetail.experimentForm.seed}
						<input name="seed" placeholder="2024q4" required />
					</label>
					<label>
						{copy.featureDetail.experimentForm.rollout}
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
						<button class="button primary" type="submit">
							{copy.featureDetail.experimentForm.create}
						</button>
						<span class="helper">{copy.featureDetail.experimentForm.helper}</span>
					</div>
				</form>
				{#if form?.action === 'createExperiment'}
					{#if form?.error}
						<p class="banner error" role="alert">{form.error}</p>
					{:else if form?.success}
						<p class="banner success">{copy.messages.experimentCreated}</p>
					{/if}
				{/if}
			</div>

			{#if data.experiments.length === 0}
				<div class="panel">
					<p>{copy.featureDetail.noExperiments}</p>
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
								<span class={`status status--${experiment.status}`}>
									{copy.statuses[experiment.status]}
								</span>
							</header>
							<div class="card-meta">
								{copy.featureDetail.experimentSeedLabel}: {experiment.seed}
							</div>
							<div class="card-meta">
								{copy.featureDetail.experimentRolloutLabel}: {experiment.rollout_percent}%
							</div>
							<form method="POST" action="?/updateExperiment" class="form-grid">
								<input type="hidden" name="experiment_id" value={experiment.id} />
								<label>
									{copy.featureDetail.statusLabel}
									<select name="status">
										<option value="draft" selected={experiment.status === 'draft'}>
											{copy.statuses.draft}
										</option>
										<option value="running" selected={experiment.status === 'running'}>
											{copy.statuses.running}
										</option>
										<option value="paused" selected={experiment.status === 'paused'}>
											{copy.statuses.paused}
										</option>
									</select>
								</label>
								<label>
									{copy.featureDetail.experimentForm.rollout}
									<input
										type="number"
										name="rollout_percent"
										min="0"
										max="100"
										value={experiment.rollout_percent}
									/>
								</label>
								<label>
									{copy.featureDetail.experimentForm.seed}
									<input name="seed" value={experiment.seed} />
								</label>
								<div class="form-actions">
									<button class="button primary" type="submit">
										{copy.featureDetail.experimentUpdate}
									</button>
									<a
										class="button ghost"
										href={`?experiment=${encodeURIComponent(experiment.id)}#variants`}
									>
										{copy.featureDetail.manageVariants}
									</a>
								</div>
							</form>
							{#if form?.action === 'updateExperiment' && form?.experimentId === experiment.id}
								{#if form?.error}
									<p class="banner error" role="alert">{form.error}</p>
								{:else if form?.success}
									<p class="banner success">{copy.messages.experimentUpdated}</p>
								{/if}
							{/if}
						</article>
					{/each}
				</div>
			{/if}
		</section>

		<section class="section" id="variants">
			<div class="section-header">
				<h2 class="section-title">{copy.featureDetail.variantsTitle}</h2>
				{#if data.selectedExperiment}
					<span class="subtle">
						{format(copy.featureDetail.variantsFor, { name: data.selectedExperiment.name })}
					</span>
				{:else}
					<span class="subtle">{copy.featureDetail.variantsHint}</span>
				{/if}
			</div>

			{#if !data.selectedExperiment}
				<div class="panel">
					<p>{copy.featureDetail.variantsPrompt}</p>
				</div>
			{:else}
				<div class="panel">
					{#if data.variants.length === 0}
						<p>{copy.featureDetail.noVariants}</p>
					{:else}
						<table class="table">
							<thead>
								<tr>
									<th>{copy.featureDetail.variantTable.key}</th>
									<th>{copy.featureDetail.variantTable.weight}</th>
									<th>{copy.featureDetail.variantTable.control}</th>
									<th>{copy.featureDetail.variantTable.payload}</th>
								</tr>
							</thead>
							<tbody>
								{#each data.variants as variant}
									<tr>
										<td>{variant.key}</td>
										<td>{variant.weight}</td>
										<td>{variant.is_control ? copy.common.yes : copy.common.no}</td>
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
							{copy.featureDetail.variantForm.key}
							<input name="key" placeholder="control" required />
						</label>
						<label>
							{copy.featureDetail.variantForm.weight}
							<input type="number" name="weight" min="0" value="50" required />
						</label>
						<label>
							{copy.featureDetail.variantForm.payload}
							<textarea name="payload" placeholder={payloadPlaceholder}></textarea>
						</label>
						<label class="toggle">
							{copy.featureDetail.variantForm.control}
							<input type="checkbox" name="is_control" />
						</label>
						<div class="form-actions">
							<button class="button primary" type="submit">
								{copy.featureDetail.variantForm.add}
							</button>
							<span class="helper">{copy.featureDetail.variantForm.helper}</span>
						</div>
					</form>
					{#if form?.action === 'createVariant'}
						{#if form?.error}
							<p class="banner error" role="alert">{form.error}</p>
						{:else if form?.success}
							<p class="banner success">{copy.messages.variantAdded}</p>
						{/if}
					{/if}
				</div>
			{/if}
		</section>
	{/if}
</div>
