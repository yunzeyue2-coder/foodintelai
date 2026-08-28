---
id: QTO-V2.3-FIX-002
title: V2.3-RC3 修复记录（GPT复审 1P0+3P1）
version: RC3
created: 2026-08-10
status: 修复完成，待重送审
category: 系统修复
---

> **关联：** [[QTO-V2.3-FIX-001_RC2修复记录]] · [[GPT独立红队审计_V2.3_20260810]] · [[QTO-V2.3-VERSION_版本状态]]

# V2.3-RC3 修复记录

## 修复摘要（GPT 复审 1 P0 + 3 P1 全修）

| ID | 问题 | 修复 | 验证 |
|----|------|------|------|
| P0 | trace_decision_chain 不是真正递归（1-2 hop） | 升级为**通用递归 Graph Traversal**：DFS + visited + cycle detection + max_depth(10) + 任意节点类型（insight/hypothesis/linked_nodes 统一注册表） | ✅ GPT攻击案例(I009→H003→E008 多跳)阻断 + 1~10层随机图全覆盖 |
| P1 | Condition 免检过宽（continue 跳过） | Condition 语义分类：VALIDATION_REQUIRED/CHALLENGE/UNKNOWN 允许 D；FACTUAL_PREMISE/DECISION_DRIVER/未分类 拒绝 D | ✅ 3a允许/3b拒绝/3c保守拒绝 |
| P1 | Provenance invalid → CONDITIONAL（可绕过） | 升级为 **BLOCKED**（PROVENANCE_INVALID → 不能作为正式决策依据） | ✅ AI自评 6 项 → BLOCKED |
| P1 | 03_TEST 未同步 RC2 | 新增本记录 + attack_test_traversal.py（1-10层随机图攻击） | ✅ 同步完成 |

## P0 攻击案例（GPT 构造，RC3 已阻断）

```
E008(D) → I002 → H003 → I009 → R1 → Decision
R1.linked_insights = [I009]
I009.linked_hypotheses = [H003]
H003.evidence_for = [E008(D)]
旧实现: 到 I009 就停 → D 穿透 ✅ 攻击有效
RC3: 递归展开 I009→H003→E008(D) → 图级阻断 ✅
```

## Condition 语义分类（GPT 建议的 5 类）

```
VALIDATION_REQUIRED / CHALLENGE / UNKNOWN → 允许 D（验证条件，Negative Evidence）
FACTUAL_PREMISE / DECISION_DRIVER        → 拒绝 D（当作事实/决策驱动）
未分类(空)                                → 保守拒绝（不能默认放行）
```

## RC3 验证矩阵（7 场景全过）

| 场景 | 结果 |
|------|------|
| VALIDATION_REQUIRED 含 D | QUALIFIED（验证条件允许） |
| DECISION_DRIVER 含 D | REJECTED（决策驱动拒绝） |
| 未分类条件含 D | REJECTED（保守拒绝） |
| 干净条件 | QUALIFIED |
| AI 自评 provenance | BLOCKED |
| 炸鸡修复后（R4→验证型条件） | QUALIFIED（GLOBAL） |
| GPT 攻击案例（多跳 I009→H003→E008） | REJECTED（图级阻断） |

## 深度攻击测试（1~10 层随机图）

```
深度1-10: D 级证据全部可达可见 ✅（10/10）
环检测: A→B→A 不死循环 ✅
```

## 下一步

```
重打包 QTO-V2.3-AUDIT-PACK（RC3 版）
  → 新增: decision_qualification_gate.py（RC3）+ attack_test_traversal.py
  → 更新: 03_TEST（本记录）
  → 送 GPT 复审
  → 若 P0=0 + Graph Bypass=0 + Authority Propagation PASS → FROZEN
```

*2026-08-10 · RC3 修复完成*
