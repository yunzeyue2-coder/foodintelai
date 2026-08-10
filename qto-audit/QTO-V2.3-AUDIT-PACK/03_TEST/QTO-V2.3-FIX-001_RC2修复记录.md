---
id: QTO-V2.3-FIX-001
title: V2.3-RC2 修复记录（GPT红队审计 3P0+2P1）
version: RC2
created: 2026-08-10
status: 修复完成，待重送审
category: 系统修复
---

> **关联：** [[GPT独立红队审计_V2.3_20260810]] · [[QTO-V2.3-STD-001_结论资格标准]] · [[QTO-V2.3-VERSION_版本状态]]

# V2.3-RC2 修复记录

## 修复摘要（GPT 审计 3 P0 + 2 P1 全修）

| ID | 问题 | 修复 | 验证 |
|----|------|------|------|
| P0-1 | Graph-level Authority Propagation 未实现 | 新增 `trace_decision_chain()`：Decision→Reason/Score/Condition→Insight/Hypothesis→Evidence 反向追溯，链路最低 Authority = 上限 | ✅ bypass 场景拦截 |
| P0-2 | Indirect Bypass 未拦截 | 新增 `check_indirect_bypass()`：D/E→Insight/Hypothesis/Score 间接路径阻断（condition 允许 D，Negative Evidence 语义） | ✅ 炸鸡R4/米线R5 原样拦截 |
| P0-3 | 缺 Qualification Orchestrator | 新增 `DecisionQualificationGate.qualify()`：Authority PASS AND Coverage PASS/降级 → Qualification；调用方不能只跑一个 Gate | ✅ 极端案例 Coverage 拒绝 |
| P1-1 | UNKNOWN Evidence 会 PASS | UNKNOWN → VIOLATION → FAIL（condition 链除外） | ✅ E999 拦截 |
| P1-2 | 参数无 provenance | provenance 检查：AI_SELF/UNSPECIFIED → CONDITIONAL（需独立来源） | ✅ AI自评 6 项拦截 |

## 关键语义（Negative Evidence 落地）

```
reasons / scores: D/E 严禁（支撑决策的依据必须有资格）
conditions:       D/E 允许（低权限≠没用——可作验证条件/Unknown，不能升级为事实）
```

## 验证矩阵（RC2 全过）

| 场景 | 结果 |
|------|------|
| 自检 clean（全A/B） | QUALIFIED |
| 自检 bypass（D藏Insight） | REJECTED（图级阻断） |
| 自检 unknown（E999无等级） | REJECTED |
| 自检 no_prov（无来源） | CONDITIONAL |
| 炸鸡修复后（R4→Condition） | QUALIFIED（GLOBAL） |
| 炸鸡原样（R4引D） | REJECTED（修复必要性证实） |
| 米线原样（R5引D） | REJECTED |
| 极端（50/10000） | REJECTED（Coverage INSUFFICIENT） |
| AI自评 provenance | CONDITIONAL |

## 下一步

```
重新打包 QTO-V2.3-AUDIT-PACK（RC2 版）
  → 新增: decision_qualification_gate.py（组合引擎）
  → 更新: 03_TEST（RC2 验证矩阵）
  → 送 GPT 复审
```

*2026-08-10 · RC2 修复完成*
