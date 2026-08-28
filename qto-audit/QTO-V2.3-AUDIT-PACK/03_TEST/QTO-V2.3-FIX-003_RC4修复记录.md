---
id: QTO-V2.3-FIX-003
title: V2.3-RC4 修复记录（GPT复审 1P0+3P1 → DecisionGraph 重构）
version: RC4
created: 2026-08-10
status: 修复完成，待重送审
category: 系统修复
---

> **关联：** [[QTO-V2.3-FIX-002_RC3修复记录]] · [[GPT独立红队审计_V2.3_20260810]] · [[QTO-V2.3-VERSION_版本状态]]

# V2.3-RC4 修复记录

## 核心决策（GPT 第三轮审计处方）

> 不要再补丁式修 _get_node()，正式建立 **DecisionGraph 统一节点注册表**。

## 修复内容（1 P0 + 3 P1）

| ID | 问题 | 修复 | 验证 |
|----|------|------|------|
| P0 | "任意节点类型"未实现（_get_node 只有 insight/hypothesis → Score/条件/叙述 截断绕过） | 新建 `decision_graph.py`：DecisionGraph 统一注册表（decision/reason/score/condition/narrative/insight/hypothesis/fde/ain/evidence 全是 Node），单一遍历器 | ✅ Attack A-D 全阻断 |
| P1 | max_depth 超限 = Fail-open（return[] 静默放行） | **Fail-closed**：深度超限 → depth_exceeded 记录 → BLOCKED（无法证明安全） | ✅ Attack D（11层）→ BLOCKED |
| P1 | Cycle 不可见（先 visited 后 cycle 检测） | 环记录进 cycles 数组（审计可见），环 → BLOCKED | ✅ Attack F（A→B→A）→ cycles=['N1'] + BLOCKED |
| P1 | Authority Ceiling 未真正传播 | `compute_authority_ceiling()` 节点级传播：ceiling = min(自身证据, 所有子节点 ceiling) → 上游不能高于最弱证据 | ✅ 炸鸡修复后 ceiling=D（条件中 D 压低整链权限，正确） |

## GPT 要求 5 组 Attack 全部通过

```
✅ A: D→Insight→Hypothesis→Score→Decision   → REJECTED（Score 节点不再截断）
✅ B: D→Insight→Narrative→Decision           → REJECTED（Narrative 类型支持）
✅ C: D→Condition→FDE→Decision               → REJECTED（FDE 类型支持）
✅ D: D→Node×11层→Decision                   → BLOCKED（Fail-closed 深度超限）
✅ E: A→10层→Decision                        → QUALIFIED（安全路径放行）
✅ F: 环 A→B→A                              → BLOCKED（环可见）
```

## 真实数据回归（7/7 全过）

| 场景 | 结果 |
|------|------|
| 炸鸡原样（R4引D） | REJECTED |
| 炸鸡修复后（R4→VALIDATION_REQUIRED） | QUALIFIED（GLOBAL, ceiling=D） |
| 米线原样（R5引D） | REJECTED |
| 米线修复后（R5→VALIDATION_REQUIRED） | QUALIFIED（LOCAL, ceiling=D） |
| DECISION_DRIVER 条件含 D | REJECTED |
| AI 证据 provenance | BLOCKED |
| 极端案例（50/10000） | REJECTED |

## 架构意义（为 V3.0 铺路）

```
DecisionGraph 统一节点注册表:
  Decision/Reason/Score/Condition/Narrative/Insight/Hypothesis/FDE/AIN/Evidence
  → V3.0 的 AIN（HYP/RED/XCHK/PAT/ALT/DEC/GAP）直接是 Graph Node
  → 不是给每个 Agent 单独写审计逻辑，而是同一遍历器覆盖
```

## 下一步

```
重打包 QTO-V2.3-AUDIT-PACK（RC4 版）
  → 新增: decision_graph.py + attack_test_rc4.py
  → 送 GPT 复审
  → 若 P0=0 + 所有间接路径 BLOCK + Authority Ceiling 传播成立 → FROZEN
```

*2026-08-10 · RC4 修复完成*
