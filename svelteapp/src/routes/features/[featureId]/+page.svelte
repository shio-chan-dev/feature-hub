<script lang="ts">
	import { goto } from '$app/navigation';
	import { slide } from 'svelte/transition';
	import { defaultLocale, format, translations } from '$lib/i18n';

	let { data, form } = $props();
	const payloadPlaceholder = '{"ui":"v2"}';
	const currentLocale = $derived(data.locale ?? defaultLocale);
	const copy = $derived(translations[currentLocale]);
	let isFeatureEditing = $state(false);
	let isCreateExperimentOpen = $state(false);
	let editingExperimentId = $state<string | null>(null);
	let isCreateVariantOpen = $state(false);
	let editingVariantId = $state<string | null>(null);

	const activeExperimentId = $derived(data.feature?.active_experiment_id ?? '');
	const activeExperimentName = $derived(
		data.experiments.find((experiment) => experiment.id === activeExperimentId)?.name ?? ''
	);
	const activeExperimentLabel = $derived(
		activeExperimentId
			? activeExperimentName || activeExperimentId
			: copy.featureDetail.activeExperimentNone
	);

	const toggleFeatureEdit = () => {
		isFeatureEditing = !isFeatureEditing;
	};

	const toggleCreateExperiment = () => {
		isCreateExperimentOpen = !isCreateExperimentOpen;
	};

	const toggleExperimentEdit = (experimentId: string) => {
		editingExperimentId = editingExperimentId === experimentId ? null : experimentId;
	};

	const toggleCreateVariant = () => {
		isCreateVariantOpen = !isCreateVariantOpen;
	};

	const toggleVariantEdit = (variantId: string) => {
		editingVariantId = editingVariantId === variantId ? null : variantId;
	};

	const summarizePayload = (payload: Record<string, unknown>) => {
		const keys = Object.keys(payload ?? {});
		if (keys.length === 0) {
			return copy.common.none;
		}
		if (keys.length <= 2) {
			return keys.join(', ');
		}
		return `${keys.slice(0, 2).join(', ')} +${keys.length - 2}`;
	};

	const goBack = () => {
		if (typeof window !== 'undefined' && window.history.length > 1) {
			window.history.back();
			return;
		}
		goto('/');
	};
</script>

<div class="container">
	<section class="section">
		<div class="tag-row">
			<button class="button ghost" type="button" on:click={goBack}>
				{copy.common.backToFeatures}
			</button>
			{#if data.feature?.id}
				<a class="button ghost" href={`/audits?feature_id=${encodeURIComponent(data.feature.id)}`}>
					{copy.header.nav.audits}
				</a>
			{/if}
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
				<div class="tag-row">
					<button class="button ghost" type="button" on:click={toggleFeatureEdit}>
						{isFeatureEditing ? copy.common.cancel : copy.common.edit}
					</button>
				</div>
			</div>
			<div class="panel">
				{#if !isFeatureEditing}
					<div class="tag-row">
						<span class={`status status--${data.feature.status}`}>
							{copy.statuses[data.feature.status]}
						</span>
						<span class="subtle">
							{copy.featureDetail.activeExperimentLabel}: {activeExperimentLabel}
						</span>
					</div>
				{:else}
					<form method="POST" action="?/updateFeature" class="form-grid" transition:slide>
						<label>
							{copy.featureDetail.nameLabel}
							<input name="name" value={data.feature?.name ?? ''} />
						</label>
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
				{/if}
			</div>
		</section>

		<section class="section">
			<div class="section-header">
				<h2 class="section-title">{copy.featureDetail.experimentsTitle}</h2>
				<div class="tag-row">
					<span class="subtle">{copy.featureDetail.experimentsHint}</span>
					<button class="button ghost" type="button" on:click={toggleCreateExperiment}>
						{isCreateExperimentOpen ? copy.common.cancel : copy.featureDetail.experimentForm.create}
					</button>
				</div>
			</div>
			{#if isCreateExperimentOpen}
				<div class="panel edit-panel" transition:slide>
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
			{/if}

			{#if data.experiments.length === 0}
				<div class="panel">
					<p>{copy.featureDetail.noExperiments}</p>
				</div>
			{:else}
				<div class="feature-grid">
					{#each data.experiments as experiment, index}
						<article class="card reveal" style={`--delay: ${index * 0.04}s`}>
							<header>
								<div class="card-title">{experiment.name}</div>
								<div class="card-header-meta">
									<span class="card-meta">{experiment.id}</span>
									<span class={`status status--${experiment.status}`}>
										{copy.statuses[experiment.status]}
									</span>
									<button
										class="button ghost compact"
										type="button"
										on:click={() => toggleExperimentEdit(experiment.id)}
									>
										{editingExperimentId === experiment.id ? copy.common.cancel : copy.common.edit}
									</button>
								</div>
							</header>
							<div class="meta-row">
								<span class="meta-chip">
									{copy.featureDetail.experimentRolloutLabel}: {experiment.rollout_percent}%
								</span>
								<span class="meta-chip">
									{copy.featureDetail.experimentSeedLabel}: {experiment.seed}
								</span>
							</div>
							<div class="card-actions">
								<a
									class="button ghost"
									href={`?experiment=${encodeURIComponent(experiment.id)}#variants`}
								>
									{copy.featureDetail.manageVariants}
								</a>
							</div>
							{#if editingExperimentId === experiment.id}
								<div class="edit-panel" transition:slide>
									<form method="POST" action="?/updateExperiment" class="form-grid">
										<input type="hidden" name="experiment_id" value={experiment.id} />
										<label>
											{copy.featureDetail.experimentForm.name}
											<input name="name" value={experiment.name} />
										</label>
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
										</div>
									</form>
									{#if form?.action === 'updateExperiment' && form?.experimentId === experiment.id}
										{#if form?.error}
											<p class="banner error" role="alert">{form.error}</p>
										{:else if form?.success}
											<p class="banner success">{copy.messages.experimentUpdated}</p>
										{/if}
									{/if}
								</div>
							{/if}
						</article>
					{/each}
				</div>
			{/if}
		</section>

		<section class="section" id="variants">
			<div class="section-header">
				<h2 class="section-title">{copy.featureDetail.variantsTitle}</h2>
				<div class="tag-row">
					{#if data.selectedExperiment}
						<span class="subtle">
							{format(copy.featureDetail.variantsFor, { name: data.selectedExperiment.name })}
						</span>
						<button class="button ghost" type="button" on:click={toggleCreateVariant}>
							{isCreateVariantOpen ? copy.common.cancel : copy.featureDetail.variantForm.add}
						</button>
					{:else}
						<span class="subtle">{copy.featureDetail.variantsHint}</span>
					{/if}
				</div>
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
						<div class="feature-grid variant-grid">
							{#each data.variants as variant, index}
								<article class="card reveal" style={`--delay: ${index * 0.04}s`}>
									<header>
										<div class="card-title">{variant.key}</div>
										<div class="card-header-meta">
											<span class="card-meta">{variant.id}</span>
											{#if variant.is_control}
												<span class="badge">{copy.featureDetail.variantForm.control}</span>
											{/if}
											<button
												class="button ghost compact"
												type="button"
												on:click={() => toggleVariantEdit(variant.id)}
											>
												{editingVariantId === variant.id ? copy.common.cancel : copy.common.edit}
											</button>
										</div>
									</header>
									<div class="meta-row">
										<span class="meta-chip">
											{copy.featureDetail.variantTable.weight}: {variant.weight}
										</span>
										<span class="meta-chip">
											{copy.featureDetail.variantTable.payload}:
											{summarizePayload(variant.payload)}
										</span>
									</div>
									{#if editingVariantId === variant.id}
										<div class="edit-panel" transition:slide>
											<form method="POST" action="?/updateVariant" class="form-grid variant-form">
												<input type="hidden" name="variant_id" value={variant.id} />
												<label>
													{copy.featureDetail.variantForm.weight}
													<input type="number" name="weight" min="0" value={variant.weight} />
												</label>
												<label>
													{copy.featureDetail.variantForm.control}
													<select name="is_control">
														<option value="true" selected={variant.is_control}>
															{copy.common.yes}
														</option>
														<option value="false" selected={!variant.is_control}>
															{copy.common.no}
														</option>
													</select>
												</label>
												<label>
													{copy.featureDetail.variantForm.payload}
													<textarea name="payload">{JSON.stringify(variant.payload, null, 2)}</textarea>
												</label>
												<div class="form-actions">
													<button class="button primary" type="submit">
														{copy.featureDetail.variantUpdateForm.submit}
													</button>
													<span class="helper">{copy.featureDetail.variantUpdateForm.helper}</span>
												</div>
											</form>
											{#if form?.action === 'updateVariant' && form?.variantId === variant.id}
												{#if form?.error}
													<p class="banner error" role="alert">{form.error}</p>
												{:else if form?.success}
													<p class="banner success">{copy.messages.variantUpdated}</p>
												{/if}
											{/if}
										</div>
									{/if}
								</article>
							{/each}
						</div>
					{/if}
				</div>
				{#if isCreateVariantOpen}
					<div class="panel edit-panel" transition:slide>
						<form method="POST" action="?/createVariant" class="form-grid variant-form">
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
			{/if}
		</section>
	{/if}
</div>
