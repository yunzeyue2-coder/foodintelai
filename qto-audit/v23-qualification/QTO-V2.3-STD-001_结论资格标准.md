---
id: QTO-V2.3-STD-001
title: 青藤OS V2.3 结论资格标准（Decision Qualification Standard）
version: V2.3
status: 已启用（2026-08-10 沧林拍板）
owner: 沧林 + 青葵
category: 系统规则
supersedes: V2.2（从"跨品类能跑"升级为"知道什么时候不能下结论"）
---

> **关联：** [[QTO-V2.2-ACCEPT-001_Sprint2验收报告]] · [[QTO-V2-ARCH-001_青藤OS_V2_架构蓝图]] · [[FDR-EVIDENCE-002_Evidence_Boundary_Specification]]

# 青藤OS V2.3 结论资格标准

> 核心：V2.1 Workflow 能跑 → V2.2 跨品类能跑 → **V2.3 知道什么时候不能下结论**

## 一、Evidence Authority Gate（证据资格闸门）

**问题**（米线 PORT-001 复核⑤暴露）：C/D 级证据与 A 级并列进入同一层级决策理由。

**规则**：
```
Evidence等级  可承担角色
A            主决策理由（Primary）
B            主理由，但需注明限制（Primary + caveat）
C            只能作为条件/假设/待验证项（Conditional）
D/E          不得进入正式决策依据（Rejected）
```

**输出结构**：
```
DECISION REASONS
├── Primary Evidence      A / A / B
└── Conditional Evidence  C → 仅支持条件，不得独立形成方向
```

**机器约束**：`evidence_authority_gate.py` — 决策理由生成时强制分级，D/E 引用直接 FAIL。

## 二、Sample Coverage Gate（样本覆盖闸门）

**原则**：数据存在 ≠ 数据足够 ≠ 可以推导全局结论。样本少→允许分析，但系统自动限制结论外推范围。

**多变量综合（不写死单一阈值）**：
```
Sample Coverage × Sample Selection Bias × Geographic Scope
× Category Penetration × Data Completeness × Temporal Coverage
```

**Decision Scope 判定**：
```
≥0.75  GLOBAL     → 城市/品类级结论，可独立决策
≥0.55  REGIONAL   → 收缩为区域方向，需全量验证
≥0.35  LOCAL      → 仅样本区域初步信号，不得外推
<0.35  INSUFFICIENT → 仅记录，不形成方向
```

**机器约束**：`sample_coverage_gate.py` — 决策输出前自动降级。

## 三、Regression 验证记录（2026-08-10）

| 案例 | 输入 | 结果 | 判定 |
|------|------|------|------|
| Regression 01 炸鸡 | 全城2397家 | GLOBAL，维持R2 | ✅ |
| Regression 02 米线 | 金水区200家 | LOCAL，"样本区域初步信号，需扩大样本验证" | ✅ |
| Regression 03 极端 | 10000家采50家 | INSUFFICIENT，BLOCKED | ✅ |

**Regression 03 关键验证**：系统拒绝"郑州米线应该开社区店"的城市级结论，只输出"样本区域存在初步信号，证据不足以支持全城决策"——机器拦截成立。

## 四、V2.3 升级性质

```
V2.1  Workflow 能跑
V2.2  跨品类能跑
V2.3  知道什么时候不能下结论
     → Decision OS 最重要的能力：不是"给我一个答案"，
       而是"在什么证据条件下有资格给答案；证据不够时，把答案降级到什么程度"
```

*2026-08-10 · V2.3 结论资格标准启用*
