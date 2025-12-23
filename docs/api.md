# Feature Hub API 文档

> 编写标准：Roy Fielding 的 REST 约束（资源、统一接口、无状态、可缓存）

## 基础信息
- Base URL: http://localhost:6789
- Content-Type: application/json
- 认证: 无
- 返回格式: JSON
- 版本: 0.1.0
- 存储: 内存（重启即丢）


## 目录

<!-- vim-markdown-toc GFM -->

* [资源模型与状态](#资源模型与状态)
  * [Feature](#feature)
  * [Experiment](#experiment)
  * [Variant](#variant)
  * [DecisionResponse](#decisionresponse)
* [通用响应与错误](#通用响应与错误)
* [测试准备](#测试准备)
* [接口一览](#接口一览)
  * [健康检查接口概览](#健康检查接口概览)
  * [Feature 接口概览](#feature-接口概览)
  * [Experiment 接口概览](#experiment-接口概览)
  * [Variant 接口概览](#variant-接口概览)
  * [Decision 接口概览](#decision-接口概览)
  * [Audit 接口概览](#audit-接口概览)
* [接口详情](#接口详情)
  * [健康检查接口](#健康检查接口)
    * [GET /health](#get-health)
  * [Feature 接口](#feature-接口)
    * [POST /features](#post-features)
    * [GET /features](#get-features)
    * [GET /features/{feature_id}](#get-featuresfeature_id)
    * [PATCH /features/{feature_id}](#patch-featuresfeature_id)
  * [Experiment 接口](#experiment-接口)
    * [POST /features/{feature_id}/experiments](#post-featuresfeature_idexperiments)
    * [GET /features/{feature_id}/experiments](#get-featuresfeature_idexperiments)
    * [GET /experiments/{experiment_id}](#get-experimentsexperiment_id)
    * [PATCH /experiments/{experiment_id}](#patch-experimentsexperiment_id)
  * [Variant 接口](#variant-接口)
    * [POST /experiments/{experiment_id}/variants](#post-experimentsexperiment_idvariants)
    * [GET /experiments/{experiment_id}/variants](#get-experimentsexperiment_idvariants)
    * [PATCH /variants/{variant_id}](#patch-variantsvariant_id)
  * [Decision 接口](#decision-接口)
    * [POST /decisions](#post-decisions)
  * [Audit 接口](#audit-接口)
    * [GET /audits](#get-audits)
* [已知限制](#已知限制)

<!-- vim-markdown-toc -->

## 资源模型与状态

### Feature
- id: string，例：feat-001
- key: string，业务唯一键
- name: string
- status: off | on | experiment
- active_experiment_id: string | null

### Experiment
- id: string，例：exp-001
- feature_id: string
- name: string
- seed: string
- status: draft | running | paused
- rollout_percent: int，范围 0..100

### Variant
- id: string，例：var-001
- experiment_id: string
- key: string
- weight: int，>= 0
- is_control: bool
- payload: object

### DecisionResponse
- request_id: string
- feature_key: string
- experiment_id: string | null
- variant_key: string
- variant_payload: object
- reason: feature_off | feature_on | experiment_inactive | assigned

## 通用响应与错误
- 成功: 200
- 业务校验失败: 400
- 资源不存在: 404
- 参数校验失败: 422 (FastAPI 默认)
- 错误体格式:
```json
{"detail": "..."}
```

## 测试准备
```bash
BASE_URL=http://localhost:6789
```

## 接口一览

### 健康检查接口概览
| Method | Path | 说明 |
| --- | --- | --- |
| GET | /health | 健康检查 |

### Feature 接口概览
| Method | Path | 说明 |
| --- | --- | --- |
| POST | /features | 创建 Feature |
| GET | /features | Feature 列表 |
| GET | /features/{feature_id} | 获取 Feature |
| PATCH | /features/{feature_id} | 更新 Feature |

### Experiment 接口概览
| Method | Path | 说明 |
| --- | --- | --- |
| POST | /features/{feature_id}/experiments | 创建 Experiment |
| GET | /features/{feature_id}/experiments | Feature 下的 Experiments |
| GET | /experiments/{experiment_id} | 获取 Experiment |
| PATCH | /experiments/{experiment_id} | 更新 Experiment |

### Variant 接口概览
| Method | Path | 说明 |
| --- | --- | --- |
| POST | /experiments/{experiment_id}/variants | 创建 Variant |
| GET | /experiments/{experiment_id}/variants | Variant 列表 |
| PATCH | /variants/{variant_id} | 更新 Variant |

### Decision 接口概览
| Method | Path | 说明 |
| --- | --- | --- |
| POST | /decisions | 计算分流结果 |

### Audit 接口概览
| Method | Path | 说明 |
| --- | --- | --- |
| GET | /audits | 审计查询（stub） |

## 接口详情

### 健康检查接口

#### GET /health
健康检查。

curl:
```bash
curl -sS "$BASE_URL/health"
```

响应示例:
```json
{"status":"ok"}
```

### Feature 接口

#### POST /features
创建 Feature。

请求体:
```json
{"key":"new_checkout","name":"New Checkout"}
```

curl:
```bash
curl -sS -X POST "$BASE_URL/features" \
  -H "Content-Type: application/json" \
  -d '{"key":"new_checkout","name":"New Checkout"}'
```

响应示例:
```json
{"id":"feat-001","key":"new_checkout","name":"New Checkout","status":"off","active_experiment_id":null}
```

#### GET /features
获取 Feature 列表。

curl:
```bash
curl -sS "$BASE_URL/features"
```

响应示例:
```json
[
  {"id":"feat-001","key":"new_checkout","name":"New Checkout","status":"off","active_experiment_id":null}
]
```

#### GET /features/{feature_id}
获取单个 Feature。

路径参数:
- feature_id: Feature ID

curl:
```bash
curl -sS "$BASE_URL/features/feat-001"
```

响应示例:
```json
{"id":"feat-001","key":"new_checkout","name":"New Checkout","status":"off","active_experiment_id":null}
```

#### PATCH /features/{feature_id}
更新 Feature 状态与激活实验。

请求体:
```json
{"status":"experiment","active_experiment_id":"exp-001"}
```

curl:
```bash
curl -sS -X PATCH "$BASE_URL/features/feat-001" \
  -H "Content-Type: application/json" \
  -d '{"status":"experiment","active_experiment_id":"exp-001"}'
```

响应示例:
```json
{"id":"feat-001","key":"new_checkout","name":"New Checkout","status":"experiment","active_experiment_id":"exp-001"}
```

### Experiment 接口

#### POST /features/{feature_id}/experiments
在 Feature 下创建 Experiment。

请求体:
```json
{"name":"checkout-test","seed":"2024q4","rollout_percent":50}
```

curl:
```bash
curl -sS -X POST "$BASE_URL/features/feat-001/experiments" \
  -H "Content-Type: application/json" \
  -d '{"name":"checkout-test","seed":"2024q4","rollout_percent":50}'
```

响应示例:
```json
{"id":"exp-001","feature_id":"feat-001","name":"checkout-test","seed":"2024q4","status":"draft","rollout_percent":50}
```

#### GET /features/{feature_id}/experiments
获取某 Feature 下的 Experiment 列表。

curl:
```bash
curl -sS "$BASE_URL/features/feat-001/experiments"
```

响应示例:
```json
[
  {"id":"exp-001","feature_id":"feat-001","name":"checkout-test","seed":"2024q4","status":"draft","rollout_percent":50}
]
```

#### GET /experiments/{experiment_id}
获取 Experiment 详情。

curl:
```bash
curl -sS "$BASE_URL/experiments/exp-001"
```

响应示例:
```json
{"id":"exp-001","feature_id":"feat-001","name":"checkout-test","seed":"2024q4","status":"draft","rollout_percent":50}
```

#### PATCH /experiments/{experiment_id}
更新 Experiment。

请求体（字段可选）:
```json
{"status":"running","rollout_percent":50,"seed":"2024q4"}
```

curl:
```bash
curl -sS -X PATCH "$BASE_URL/experiments/exp-001" \
  -H "Content-Type: application/json" \
  -d '{"status":"running","rollout_percent":50,"seed":"2024q4"}'
```

响应示例:
```json
{"id":"exp-001","feature_id":"feat-001","name":"checkout-test","seed":"2024q4","status":"running","rollout_percent":50}
```

### Variant 接口

#### POST /experiments/{experiment_id}/variants
创建 Variant。

请求体:
```json
{"key":"control","weight":50,"is_control":true,"payload":{}}
```

curl:
```bash
curl -sS -X POST "$BASE_URL/experiments/exp-001/variants" \
  -H "Content-Type: application/json" \
  -d '{"key":"control","weight":50,"is_control":true,"payload":{}}'
```

响应示例:
```json
{"id":"var-001","experiment_id":"exp-001","key":"control","weight":50,"is_control":true,"payload":{}}
```

#### GET /experiments/{experiment_id}/variants
获取 Variant 列表。

curl:
```bash
curl -sS "$BASE_URL/experiments/exp-001/variants"
```

响应示例:
```json
[
  {"id":"var-001","experiment_id":"exp-001","key":"control","weight":50,"is_control":true,"payload":{}}
]
```

#### PATCH /variants/{variant_id}
更新 Variant（支持部分字段更新）。

路径参数:
- variant_id: Variant ID

请求体（字段可选）:
```json
{"weight":60,"is_control":false,"payload":{"ui":"v2"}}
```

curl:
```bash
curl -sS -X PATCH "$BASE_URL/variants/var-001" \
  -H "Content-Type: application/json" \
  -d '{"weight":60,"is_control":false,"payload":{"ui":"v2"}}'
```

响应示例:
```json
{"id":"var-001","experiment_id":"exp-001","key":"control","weight":60,"is_control":false,"payload":{"ui":"v2"}}
```

### Decision 接口

#### POST /decisions
计算分流结果。

请求体:
```json
{"request_id":"req-001","feature_key":"new_checkout","user_id":"u-123","context":{}}
```

行为说明:
- feature.status = off → reason=feature_off, variant_key=control
- feature.status = on → reason=feature_on, variant_key=enabled
- experiment 未激活/非 running → reason=experiment_inactive
- running → 选择第一个 variant, reason=assigned

curl:
```bash
curl -sS -X POST "$BASE_URL/decisions" \
  -H "Content-Type: application/json" \
  -d '{"request_id":"req-001","feature_key":"new_checkout","user_id":"u-123","context":{}}'
```

响应示例:
```json
{"request_id":"req-001","feature_key":"new_checkout","experiment_id":"exp-001","variant_key":"control","variant_payload":{},"reason":"assigned"}
```

### Audit 接口

#### GET /audits
审计查询（当前为 stub）。

查询参数:
- feature_id: Feature ID (必填)
- limit: 默认 50
- cursor: 分页游标（可选）

curl:
```bash
curl -sS "$BASE_URL/audits?feature_id=feat-001&limit=50"
```

响应示例:
```json
{"items":[],"next_cursor":null}
```

## 已知限制
- 数据存储为内存，重启即丢。
- 决策逻辑当前不应用 rollout_percent、weight、seed，仅返回第一个 variant。
- /audits 返回空结果（stub）。
