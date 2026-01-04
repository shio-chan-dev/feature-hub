# Feature Hub API 文档

> 编写标准：Roy Fielding 的 REST 约束（资源、统一接口、无状态、可缓存）

## 基础信息
- Base URL: http://localhost:6789
- Content-Type: application/json
- 认证: 无
- 返回格式: JSON
- 版本: 0.1.0
- 存储: 数据库（默认 SQLite，可通过 DB_TYPE 切换 MySQL）


## 目录

<!-- vim-markdown-toc GFM -->

* [资源模型与状态](#资源模型与状态)
  * [Feature](#feature)
  * [Experiment](#experiment)
  * [Variant](#variant)
  * [DecisionResponse](#decisionresponse)
  * [AuditItem](#audititem)
  * [AuditListResponse](#auditlistresponse)
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
- reason: string（常见：feature_off | feature_on | experiment_inactive | not in rollout | assigned）

### AuditItem
- id: string，例：dec-001
- decided_at: datetime（ISO 8601）
- request_id: string
- user_id: string
- feature_id: string
- feature_key: string
- feature_name: string | null
- experiment_id: string | null
- experiment_name: string | null
- variant_id: string | null
- variant_key: string
- is_control: bool | null
- reason: string
- variant_payload: object | null（include_payload=false 时为 null）

### AuditListResponse
- items: AuditItem[]
- next_cursor: string | null（base64 游标）

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
| GET | /audits | 审计查询 |

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

查询参数:
- status: off | on | experiment（可选）
- limit: 默认 200，>0

curl:
```bash
curl -sS "$BASE_URL/features"
```

过滤示例:
```bash
curl -sS "$BASE_URL/features?status=experiment&limit=50"
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
更新 Feature（支持部分字段更新）。

请求体（字段可选）:
```json
{"name":"New Checkout v2","status":"experiment","active_experiment_id":"exp-001"}
```

规则:
- status=experiment 时必须提供 active_experiment_id
- status 非 experiment 时会清空 active_experiment_id
- 仅传 active_experiment_id 时要求当前 status=experiment

curl:
```bash
curl -sS -X PATCH "$BASE_URL/features/feat-001" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Checkout v2","status":"experiment","active_experiment_id":"exp-001"}'
```

响应示例:
```json
{"id":"feat-001","key":"new_checkout","name":"New Checkout v2","status":"experiment","active_experiment_id":"exp-001"}
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
更新 Experiment（支持部分字段更新）。

请求体（字段可选）:
```json
{"name":"checkout-test-v2","status":"running","rollout_percent":50,"seed":"2024q4"}
```

curl:
```bash
curl -sS -X PATCH "$BASE_URL/experiments/exp-001" \
  -H "Content-Type: application/json" \
  -d '{"name":"checkout-test-v2","status":"running","rollout_percent":50,"seed":"2024q4"}'
```

响应示例:
```json
{"id":"exp-001","feature_id":"feat-001","name":"checkout-test-v2","seed":"2024q4","status":"running","rollout_percent":50}
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
- experiment 未激活/非 running → reason=experiment_inactive, variant_key=control
- running → 先做 rollout 分桶，未命中返回 reason=not in rollout + variant_key=control
- rollout 命中 → 按 weight 权重选择 variant，reason=assigned
- request_id 幂等：同一个 request_id 会返回首次决定结果

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
审计查询（返回决策审计记录）。

查询参数:
- feature_id: Feature ID (必填)
- cursor: 分页游标（可选，base64({"offset":N})，兼容纯数字 offset）
- limit: 默认 50，>0
- experiment_id: Experiment ID（可选）
- variant_id: Variant ID（可选，且与 variant_key 互斥）
- variant_key: Variant key（可选，且与 variant_id 互斥）
- reason: string（可多次传入，按字符串过滤）
- user_id: 用户 ID（可选）
- request_id: 请求 ID（可选）
- from: 起始时间（ISO 8601，可选）
- to: 结束时间（ISO 8601，可选）
- include_payload: 是否返回 variant_payload（默认 true，false 时返回 null）

校验规则:
- variant_id 与 variant_key 互斥
- from 不得晚于 to

curl:
```bash
curl -sS "$BASE_URL/audits?feature_id=feat-001&reason=assigned&reason=feature_off&from=2025-12-01T00:00:00Z&to=2025-12-31T23:59:59Z&limit=20&include_payload=false"
```

响应示例:
```json
{
  "items": [
    {
      "id": "dec-001",
      "decided_at": "2025-12-22T12:00:00Z",
      "request_id": "req-001",
      "user_id": "u-123",
      "feature_id": "feat-001",
      "feature_key": "new_checkout",
      "feature_name": "New Checkout",
      "experiment_id": "exp-001",
      "experiment_name": "checkout-test",
      "variant_id": "var-001",
      "variant_key": "control",
      "is_control": true,
      "variant_payload": null,
      "reason": "assigned"
    }
  ],
  "next_cursor": "eyJvZmZzZXQiOjIwfQ=="
}
```

## 已知限制
- 审计记录依赖 /decisions 写入，调用 /decisions 后才可查询到记录。
