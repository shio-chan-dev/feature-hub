# Plan - ai/frontend/ui-01

## Objective
- 整理实验平台前端 UI 方案，形成可评审的页面与数据需求清单。

## Deliverables
- 页面范围与信息架构（Feature 列表 / 详情+实验配置 / 审计日志 / 可选命中解释）
- 每个页面的数据字段需求（以 Feature 为中心）
- 关键交互与风险控制点（状态展示、一键回滚、防误操作）
- API 反推需求草案（GET/PUT features、审计日志）

## Milestones
- 方案整理完成（本轮输出）
- 团队评审讨论，确认 MVP 范围
- 对齐接口口径与状态枚举

## Dependencies
- 后端领域模型与状态枚举
- 权限与审计策略
- 负责人确认 MVP 范围

## Risks
- 前后端状态口径不一致
- 回滚/实验状态切换缺少审计记录
- 分流权重校验与 fallback 规则未统一

## Plan
- 以 Feature 为核心组织 UI，前端只展示与配置，逻辑与状态由后端提供
- MVP 页面仅 3 个：功能列表、功能详情+实验配置、审计日志
- 可选增强：命中解释/调试页
- 明确每页字段：status、activeExperiment、targeting、variants、weights、audit diff
- 讨论产出：页面范围 + API 需求表 + 风险点清单
