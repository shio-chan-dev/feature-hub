export const locales = ['en', 'zh'] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = 'en';

export const localeLabels: Record<Locale, string> = {
	en: 'English',
	zh: '中文'
};

export const isLocale = (value: string | null | undefined): value is Locale =>
	Boolean(value) && locales.includes(value as Locale);

export const format = (template: string, params: Record<string, string>) =>
	template.replace(/\{(\w+)\}/g, (_, key) => params[key] ?? '');

export const translations = {
	en: {
		header: {
			brandTitle: 'Feature Hub',
			brandSubtitle: 'Experiment Console',
			nav: {
				features: 'Features',
				audits: 'Audits',
				decisions: 'Decisions'
			},
			docs: 'Docs',
			newFeature: 'New Feature',
			apiLabel: 'API Local',
			syncing: 'Syncing...',
			language: 'Language'
		},
		common: {
			backToFeatures: 'Back to features',
			open: 'Open',
			none: 'none',
			noneSelected: 'none selected',
			unknown: 'unknown',
			yes: 'yes',
			no: 'no'
		},
		statuses: {
			off: 'off',
			on: 'on',
			experiment: 'experiment',
			draft: 'draft',
			running: 'running',
			paused: 'paused'
		},
		messages: {
			featureCreated: 'Feature {key} created.',
			featureUpdated: 'Feature updated.',
			experimentCreated: 'Experiment created.',
			experimentUpdated: 'Experiment updated.',
			variantAdded: 'Variant added.',
			decisionResolved: 'Decision resolved.'
		},
		features: {
			eyebrow: 'Feature flags and experiments',
			title: 'Feature Hub Console',
			lead:
				'Manage feature states, configure experiments, and trace decisions with a single surface for the rollout pipeline.',
			createFeature: 'Create a feature',
			reviewAudits: 'Review audits',
			metrics: {
				featuresTracked: 'features tracked',
				experimentMode: 'in experiment mode',
				steady: 'steady (off or on)'
			},
			createTitle: 'Create feature',
			createHint: 'Feature key should be unique.',
			form: {
				key: 'Key',
				name: 'Name',
				create: 'Create',
				helper: 'Default status is off.'
			},
			portfolioTitle: 'Feature portfolio',
			totalLabel: '{count} total',
			emptyState: 'No features yet. Create the first one to begin experiments.',
			activeExperiment: 'Active experiment',
			tryDecision: 'Try decision'
		},
		featureDetail: {
			titleFallback: 'Feature detail',
			keyLabel: 'Key',
			idLabel: 'ID',
			statusTitle: 'Feature status',
			statusLabel: 'Status',
			activeExperimentLabel: 'Active experiment',
			activeExperimentNone: 'None',
			updateFeature: 'Update feature',
			updateHint: 'Experiment mode requires an active experiment.',
			experimentsTitle: 'Experiments',
			experimentsHint: 'Configure rollout and status per experiment.',
			experimentForm: {
				name: 'Name',
				seed: 'Seed',
				rollout: 'Rollout percent',
				create: 'Create experiment',
				helper: 'Default status is draft.'
			},
			noExperiments: 'No experiments yet. Create one to start testing.',
			experimentSeedLabel: 'Seed',
			experimentRolloutLabel: 'Rollout',
			experimentUpdate: 'Update',
			manageVariants: 'Manage variants',
			variantsTitle: 'Variants',
			variantsFor: 'For experiment: {name}',
			variantsHint: 'Select an experiment to manage variants.',
			variantsPrompt: 'Choose an experiment to load variants.',
			variantTable: {
				key: 'Key',
				weight: 'Weight',
				control: 'Control',
				payload: 'Payload'
			},
			noVariants: 'No variants yet for this experiment.',
			variantForm: {
				key: 'Key',
				weight: 'Weight',
				payload: 'Payload (JSON)',
				control: 'Control',
				add: 'Add variant',
				helper: 'Control is required for safe fallback.'
			}
		},
		audits: {
			title: 'Audit log',
			lead:
				'Track configuration changes across features. Provide a feature ID to view audit entries.',
			form: {
				featureId: 'Feature ID',
				limit: 'Limit',
				load: 'Load audits'
			},
			entriesTitle: 'Entries',
			featureLabel: 'Feature',
			prompt: 'Enter a feature ID to view audit history.',
			emptyState: 'No audit entries yet for this feature.',
			stubHint: 'The backend currently returns an empty list (stub).',
			table: {
				timestamp: 'Timestamp',
				actor: 'Actor',
				action: 'Action',
				diff: 'Diff'
			},
			nextPage: 'Next page'
		},
		decisions: {
			title: 'Decision playground',
			lead:
				'Simulate a decision response using the live API. Use this when validating rollout logic and payload delivery.',
			form: {
				requestId: 'Request ID',
				featureKey: 'Feature key',
				userId: 'User ID',
				context: 'Context (JSON)',
				submit: 'Resolve decision'
			},
			responseTitle: 'Decision response',
			reasonHint: 'Reason codes: feature_off, feature_on, experiment_inactive, assigned.',
			emptyState: 'Submit a request to see the decision payload.'
		},
		docs: {
			eyebrow: 'Documentation',
			title: 'How to use Feature Hub',
			lead:
				'This console manages feature flags and experiments. Use the flow below to create features, configure experiments, and validate decisions against the live API.',
			openFeatures: 'Open features',
			apiReference: 'API reference',
			apiBaseUrl: 'API base URL',
			interactiveDocs: 'Interactive docs',
			openDocs: 'Open /docs',
			quickStartTitle: 'Quick start',
			quickStartHint: 'Follow this once per environment.',
			quickStartSteps: {
				start: 'Start the API server at {apiBaseUrl}.',
				runApp: 'Run the Svelte app with {command} in {appDir}.',
				createFeature: 'Create a feature, then add an experiment under it.',
				addVariants:
					'Add variants (control required), set rollout percent, and mark status running.',
				activateExperiment:
					'Switch the feature to experiment and choose the active experiment.',
				validateDecision: 'Use the Decisions page to validate the payload returned.'
			},
			capabilitiesTitle: 'What you can do',
			capabilitiesHint: 'Feature-first workflow aligned to the API.',
			cards: {
				featureLifecycle: {
					title: 'Feature lifecycle',
					body:
						'Create features, switch status (off/on/experiment), and pin the active experiment.'
				},
				experimentControl: {
					title: 'Experiment control',
					body:
						'Define experiments with rollout percent, seed, and running/paused state.'
				},
				variantSetup: {
					title: 'Variant setup',
					body: 'Add control + treatment variants with weight and payload JSON.'
				},
				decisionPreview: {
					title: 'Decision preview',
					body: 'Send a request_id, feature_key, and user_id to see the resolved variant.'
				}
			},
			integration: {
				title: 'Service integration',
				hint: 'Call the decision API from your service or BFF to route traffic.',
				steps: {
					call: 'From your service/BFF, call {endpoint} with request_id, feature_key, user_id, and context.',
					route: 'Use variant_key or variant_payload to route to the correct implementation.',
					fallback: 'If reason is feature_off or experiment_inactive, fall back to control.',
					stability: 'Keep user_id stable for consistent bucketing; log request_id for debugging.'
				},
				sampleTitle: 'Routing example',
				sampleHint: 'Decision request/response',
				sampleRequest: 'Request',
				sampleResponse: 'Response'
			},
			reasonsTitle: 'Decision reasons',
			reasonsHint: 'Returned by /decisions.',
			reasons: {
				featureOff: 'feature is off, returns control.',
				featureOn: 'feature is on, returns enabled variant.',
				experimentInactive: 'experiment not running, returns control.',
				assigned: 'experiment running, variant selected.'
			},
			notesTitle: 'Notes',
			notesHint: 'Known constraints in the MVP.',
			notes: {
				inMemory: 'Storage is in-memory; restart resets all data.',
				decisionLogic:
					'Decision logic currently picks the first variant (weights/rollout TBD).',
				auditStub: 'Audit endpoint returns empty results (stub).'
			}
		}
	},
	zh: {
		header: {
			brandTitle: 'Feature Hub',
			brandSubtitle: '实验控制台',
			nav: {
				features: '功能',
				audits: '审计',
				decisions: '决策'
			},
			docs: '文档',
			newFeature: '新建功能',
			apiLabel: '本地 API',
			syncing: '同步中...',
			language: '语言'
		},
		common: {
			backToFeatures: '返回功能列表',
			open: '打开',
			none: '无',
			noneSelected: '未选择',
			unknown: '未知',
			yes: '是',
			no: '否'
		},
		statuses: {
			off: '关闭',
			on: '开启',
			experiment: '实验',
			draft: '草稿',
			running: '运行中',
			paused: '暂停'
		},
		messages: {
			featureCreated: '已创建功能 {key}。',
			featureUpdated: '功能已更新。',
			experimentCreated: '实验已创建。',
			experimentUpdated: '实验已更新。',
			variantAdded: '变体已添加。',
			decisionResolved: '决策已生成。'
		},
		features: {
			eyebrow: '功能开关与实验',
			title: '功能实验控制台',
			lead: '管理功能状态、配置实验并跟踪决策，统一灰度流程。',
			createFeature: '创建功能',
			reviewAudits: '查看审计',
			metrics: {
				featuresTracked: '已跟踪功能',
				experimentMode: '处于实验模式',
				steady: '稳定状态（关闭/开启）'
			},
			createTitle: '创建功能',
			createHint: '功能 Key 需唯一。',
			form: {
				key: '键值',
				name: '名称',
				create: '创建',
				helper: '默认状态为 off。'
			},
			portfolioTitle: '功能列表',
			totalLabel: '共 {count} 项',
			emptyState: '暂无功能。创建第一个功能以开始实验。',
			activeExperiment: '当前实验',
			tryDecision: '试算决策'
		},
		featureDetail: {
			titleFallback: '功能详情',
			keyLabel: '键值',
			idLabel: 'ID',
			statusTitle: '功能状态',
			statusLabel: '状态',
			activeExperimentLabel: '当前实验',
			activeExperimentNone: '无',
			updateFeature: '更新功能',
			updateHint: '实验模式需要选择当前实验。',
			experimentsTitle: '实验',
			experimentsHint: '配置每个实验的灰度与状态。',
			experimentForm: {
				name: '名称',
				seed: '种子',
				rollout: '灰度比例',
				create: '创建实验',
				helper: '默认状态为 draft。'
			},
			noExperiments: '暂无实验。创建一个实验以开始测试。',
			experimentSeedLabel: '种子',
			experimentRolloutLabel: '灰度',
			experimentUpdate: '更新',
			manageVariants: '管理变体',
			variantsTitle: '变体',
			variantsFor: '所属实验：{name}',
			variantsHint: '选择一个实验以管理变体。',
			variantsPrompt: '请选择一个实验加载变体。',
			variantTable: {
				key: '键值',
				weight: '权重',
				control: '对照',
				payload: '载荷'
			},
			noVariants: '该实验暂无变体。',
			variantForm: {
				key: '键值',
				weight: '权重',
				payload: '载荷 (JSON)',
				control: '对照',
				add: '添加变体',
				helper: '需要对照变体以保证回退。'
			}
		},
		audits: {
			title: '审计日志',
			lead: '跟踪功能配置变更。输入 Feature ID 查看审计记录。',
			form: {
				featureId: 'Feature ID',
				limit: '条数',
				load: '加载审计'
			},
			entriesTitle: '记录',
			featureLabel: '功能',
			prompt: '请输入 Feature ID 查看审计记录。',
			emptyState: '该功能暂无审计记录。',
			stubHint: '后端当前返回空列表（占位）。',
			table: {
				timestamp: '时间',
				actor: '操作人',
				action: '动作',
				diff: '变更'
			},
			nextPage: '下一页'
		},
		decisions: {
			title: '决策调试',
			lead: '使用实时 API 模拟决策响应，用于验证灰度逻辑与 payload。',
			form: {
				requestId: '请求 ID',
				featureKey: 'Feature key',
				userId: '用户 ID',
				context: '上下文 (JSON)',
				submit: '生成决策'
			},
			responseTitle: '决策结果',
			reasonHint: '原因码：feature_off、feature_on、experiment_inactive、assigned。',
			emptyState: '提交请求后显示决策结果。'
		},
		docs: {
			eyebrow: '使用文档',
			title: 'Feature Hub 使用说明',
			lead: '该控制台用于管理功能与实验，请按下列流程创建功能、配置实验并验证决策。',
			openFeatures: '打开功能列表',
			apiReference: 'API 文档',
			apiBaseUrl: 'API 基础地址',
			interactiveDocs: '交互文档',
			openDocs: '打开 /docs',
			quickStartTitle: '快速开始',
			quickStartHint: '每个环境执行一次。',
			quickStartSteps: {
				start: '启动 API 服务：{apiBaseUrl}',
				runApp: '在 {appDir} 目录运行 {command}',
				createFeature: '创建功能，并在其下创建实验。',
				addVariants: '添加变体（需包含对照），设置灰度比例，并将状态设为 running。',
				activateExperiment: '将功能状态切换为 experiment 并选择当前实验。',
				validateDecision: '使用决策页验证返回的 payload。'
			},
			capabilitiesTitle: '你可以做什么',
			capabilitiesHint: '与 API 对齐的 Feature-first 流程。',
			cards: {
				featureLifecycle: {
					title: '功能生命周期',
					body: '创建功能、切换状态（off/on/experiment），并选择当前实验。'
				},
				experimentControl: {
					title: '实验管理',
					body: '配置实验的灰度比例、种子与运行状态。'
				},
				variantSetup: {
					title: '变体配置',
					body: '添加对照与实验变体，设置权重与 payload JSON。'
				},
				decisionPreview: {
					title: '决策预览',
					body: '提交 request_id 等参数查看决策结果。'
				}
			},
			integration: {
				title: '服务接入',
				hint: '在你的服务/BFF 中调用决策接口进行分流。',
				steps: {
					call: '在你的服务/BFF 中调用 {endpoint}，提交 request_id、feature_key、user_id、context。',
					route: '根据 variant_key 或 variant_payload 将请求路由到对应实现。',
					fallback: '若 reason 为 feature_off 或 experiment_inactive，则回退到 control。',
					stability: '确保 user_id 稳定用于一致分桶，并记录 request_id 便于排查。'
				},
				sampleTitle: '路由示例',
				sampleHint: '决策请求/响应',
				sampleRequest: '请求',
				sampleResponse: '响应'
			},
			reasonsTitle: '决策原因',
			reasonsHint: '由 /decisions 返回。',
			reasons: {
				featureOff: '功能关闭，返回对照。',
				featureOn: '功能开启，返回 enabled 变体。',
				experimentInactive: '实验未运行，返回对照。',
				assigned: '实验运行中，返回分配的变体。'
			},
			notesTitle: '注意事项',
			notesHint: '当前版本限制。',
			notes: {
				inMemory: '存储为内存，重启即清空。',
				decisionLogic: '当前决策逻辑总是选择第一个变体（权重/灰度待实现）。',
				auditStub: '审计接口当前返回空结果（占位）。'
			}
		}
	}
} as const;
