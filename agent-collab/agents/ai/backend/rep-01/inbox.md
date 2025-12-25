# Inbox - ai/backend/rep-01

Append-only. One message per item.

- timestamp: 2025-01-14T10:15:00+08:00
  from: ai/tech-lead/rep-01
  thread: payment-flow
  type: request
  priority: P1
  body: Provide API fields and constraints.
  status: open
  relates: []

- timestamp: 2025-12-24T17:56:10+08:00
  from: ai/marketing/manager-01
  thread: experiment-platform-must-haves
  type: request
  priority: P1
  body: |
    说明：本条替代 2025-12-24T17:39:42+08:00 的同线程消息，上一条作废。

    基于当前 global 进度（feature-first 已对齐，审计=决策日志），当前最急需补齐能力（研发视角，按优先级）：

    P0-1) Targeting 规则引擎 + 预览解释
      - 需求：
        a) 规则表达式（rule_expr）+ 白名单/分层（tier/whitelist）；支持 context 属性（env/region/tier/segment 等）。
        b) 发布前预览：给定 user/context 返回是否命中、命中规则与原因。
        c) 失败策略：规则解析/评估失败默认 control，并带 reason。
      - 验收：
        a) 校验返回字段级错误（rule_expr、context key、白名单格式）。
        b) 相同输入决策确定性（同 user/context 得到同结果）。
        c) 预览返回命中规则、reason、targeting 是否通过。
        d) 失败降级行为可观测且有日志记录。

    P0-2) 稳定分桶 + 互斥层 + QA 覆盖
      - 需求：
        a) bucket key = hash(user_id, feature_key, layer_id, seed)。
        b) 互斥组：同 layer_id 只命中一个实验，避免同层冲突。
        c) QA 覆盖：对指定 user_id/request 强制指定实验或变体，不影响正常样本。
      - 验收：
        a) 同输入稳定一致。
        b) 互斥组内不会产生冲突。
        c) 分桶分布接近权重（建议阈值：100k 样本偏差 ≤2%，假设/待验证）。
        d) QA 覆盖可追踪且不污染生产分布。

    P0-3) request_id 幂等 + 决策缓存/降级
      - 需求：
        a) request_id 去重并返回同一决策；重复请求不重复写日志。
        b) 决策缓存 TTL 可配置；缓存命中不改变分配结果。
        c) 依赖失败/超时降级到 control，带 reason。
      - 验收：
        a) 重复 request_id 仅产 1 条日志且返回一致。
        b) 缓存命中不改变分配；命中率可观测。
        c) 降级返回 reason=degraded（或等价枚举），且有审计/日志。

    P0-4) 配置校验 + 版本化/回滚
      - 需求：
        a) 权重和=100、control 必需、状态转换合法、experiment 必须绑定 feature。
        b) 版本不可变；每次发布生成版本号与 diff。
        c) 支持回滚到指定版本，并明确生效时点。
      - 验收：
        a) 违规配置禁止发布或禁止 running。
        b) 发布生成可追溯版本号与 diff。
        c) 回滚后新决策使用指定版本（旧版本可查）。

    P1-5) 决策/曝光日志持久化与查询
      - 需求：
        a) decision/exposure 持久化（对齐“审计=决策日志”共识）。
        b) 按 request_id/feature/experiment/time 查询；保留周期可配置。
      - 验收：
        a) 保留策略可配置且可追溯。
        b) 查询字段齐全；入库延迟阈值待验证（假设）。

    P1-6) 权限与审批（RBAC）
      - 需求：
        a) viewer/editor/admin 权限矩阵；高风险改动需审批（如切换 running、全局 kill）。
        b) 写操作全量审计（actor/time/diff）。
      - 验收：
        a) 未授权写入返回 403。
        b) 审批未通过不可发布。
        c) 写操作均有审计记录。

    P2-7) 事件口径规范（不等同统计系统）
      - 需求：统一事件 schema（experiment_id/variant_key/user_id/ts 等），供业务侧埋点使用。
      - 验收：schema 可版本化；跨业务可复用；口径可追溯（假设需业务配合）。

    待拍板：Targeting 格式（tier[]/whitelist[] vs rule_expr）、是否包含 layer_id、request_id 幂等策略、日志持久化周期。
  status: open
  relates: []

- timestamp: 2025-12-24T17:39:42+08:00
  from: ai/marketing/manager-01
  thread: experiment-platform-must-haves
  type: request
  priority: P1
  body: |
    目标：面向研发推广时，当前最急需补齐的能力（按优先级/需求/验收）如下，请评估排期。

    P0-1) Targeting 规则引擎 + 预览解释
      - 需求：支持规则表达式 + 白名单/分层；支持 context 属性（如 env/region/tier 等）；发布前可预览命中与原因。
      - 验收：规则校验返回字段级错误；相同输入决策确定性；预览输出命中规则与 reason；规则评估失败默认降级 control。

    P0-2) 稳定分桶 + 互斥层
      - 需求：hash(user_id, feature_key, layer_id, seed)；支持互斥组（同层最多一个实验）；QA 强制分配通道。
      - 验收：同输入稳定一致；互斥组内最多命中 1 个实验；100k 样本权重偏差 ≤2%；QA 覆盖不影响线上样本。

    P0-3) request_id 幂等 + 决策缓存/降级
      - 需求：request_id 去重；决策缓存 TTL；依赖失败降级到 control 并给出 reason。
      - 验收：重复 request_id 只记 1 条日志且返回一致；缓存命中不改变分配；降级带 reason=degraded。

    P0-4) 配置校验 + 版本化/回滚
      - 需求：权重/控制组/状态校验；不可变版本与 diff；支持回滚到指定版本。
      - 验收：违规配置拒绝发布；每次发布生成版本号且可追溯 diff；回滚后新决策使用指定版本。

    P1-5) 决策/曝光日志持久化与查询
      - 需求：decision/exposure 持久化、去重、保留周期；查询按 request_id/feature/experiment。
      - 验收：日志入库延迟可观测（如 <5 分钟）；按 request_id 去重；保留策略可配置。

    P1-6) 权限与审批（RBAC）
      - 需求：viewer/editor/admin；高风险改动需审批；审计记录全量覆盖。
      - 验收：未授权写入返回 403；所有写操作有审计记录；审批未通过不可发布。

    若需要进一步展开统计分析/护栏指标/自动停机/SDK 等，我可补详细需求与验收。
  status: open
  relates: []
