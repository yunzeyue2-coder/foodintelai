---
id: QTO-V3-ARCH-001
title: 青藤OS V3.0 AI Cognitive Layer 设计蓝图
version: V3.0-DRAFT
status: 设计中（2026-08-10 沧林定方向，不打断V2.3）
owner: 沧林 + 青葵
category: 架构设计
---

> **关联：** [[QTO-V2.3-STD-001_结论资格标准]] · [[QTO-V2-ARCH-001_青藤OS_V2_架构蓝图]] · [[FDR-EVIDENCE-002_Evidence_Boundary_Specification]]

# 青藤OS V3.0 AI Cognitive Layer

## 〇、架构原则（沧林拍板）

> **AI负责"想"，OS负责"管"。** 结构负责纪律，AI负责认知。
> OS 决定 AI 能看什么、必须比较什么、可以说什么；AI 负责在边界内寻找人类没有提前写出来的关系。

**前提**：V2.3 已建立 Evidence Authority + Scope Gate + Decision Qualification——没有这三个之前接 AI，容易变成"AI报告生成器"。

## 一、为什么需要 AI Layer

规则系统擅长"约束"，不擅长"理解"：
```
系统能算: 价格分布/品牌集中度/空间分布/评分
系统难答: "这些数据放在一起意味着什么？"
例: 云南系30家 = 品牌认知形成？ 还是标签相似？ 还是商圈聚集？ 还是无品牌势能？
```

## 二、核心概念：AIN（AI认知节点）

**AIN 不是 Agent，是受约束的 AI 工作单元。** 每一个 AIN 必须有：

```
AIN ID / 任务定义 / 输入Schema / 数据权限 / 检索范围
交叉验证规则 / 推理任务 / 输出Schema / Evidence要求
Confidence / 禁止事项 / Fallback
```

**定位：AI 是插槽，不是发动机。**

```
青藤OS
├── 确定性引擎  数据处理/规则校验
├── AI Node     认知判断（受约束）
└── 确定性引擎  Evidence绑定/Scope Gate
        ↓
     Decision
```

## 三、AIN Node Contract（接口协议，非Prompt）

```yaml
AIN:
  id: AIN-COMP-003
  name: Competition Structure Analysis
  input:
    - evidence_graph
    - price_distribution
    - brand_concentration
    - geographic_distribution
  required_cross_checks:
    - brand_vs_price
    - brand_vs_geography
    - chain_vs_independent
  reasoning:
    - identify_structure
    - search_counter_evidence
    - identify_alternative_explanation
  output:
    - finding
    - supporting_evidence
    - contradicting_evidence
    - confidence
    - unknowns
  constraints:
    - no_external_knowledge
    - no_unsupported_claim
    - no_global_extrapolation
  authority:
    C: hypothesis_only
    B: conditional
    A: decision_candidate
```

## 四、首批 7 个 AIN（设计清单）

| AIN ID | 名称 | 任务 | 模型强度 |
|--------|------|------|---------|
| AIN-HYP | Hypothesis Generator | 从 Evidence 找值得验证的问题 | 强模型 |
| AIN-XCHK | Cross-Check Agent | 指定数据间交叉验证 | 中模型 |
| AIN-RED | Red Team Agent | 主动寻找反证 | 强模型 |
| AIN-PAT | Pattern Agent | 找确定性规则没捕捉的结构模式 | 中/强模型 |
| AIN-ALT | Alternative Explanation | 寻找第二种解释 | 强模型 |
| AIN-DEC | Decision Challenger | 挑战 FDE 当前结论 | 顶级模型 |
| AIN-GAP | Knowledge Gap Agent | 明确系统还缺什么证据 | 中模型 |

## 五、AIN 工作流（闭环）

```
AI提出 → OS约束 → Evidence验证 → Gate裁决 → AI再挑战 → FDE决策
```

## 六、模型路由（Model Routing）

| 节点 | AI任务 | 模型要求 |
|------|--------|---------|
| 数据异常检测 | Pattern | 小模型 |
| 标签归一 | Classification | 小/中模型 |
| Evidence冲突 | Reasoning | 强模型 |
| Hypothesis生成 | Research | 强模型 |
| 反证搜索 | Adversarial | 强模型 |
| Decision Challenge | Deep Reasoning | 顶级模型 |
| FQA | Deterministic | 不需要AI |
| PDF渲染 | Deterministic | 不需要AI |

不同 AI API / 本地模型 / 云模型 = AIN 的可替换执行器。

## 七、示例：AIN-EC-001（Unit Economics Challenge）

```
系统先算: 营业时段/客单价/翻台数据/外卖占比/SKU/二次烹饪约束
AIN-EC-001 任务: 寻找变量间矛盾、异常关系、潜在解释
例: 客单低 + 翻台有限 + 时段集中 + 二次烹饪
    AI提出: "瓶颈可能不是需求不足，而是单位时间产能受限"
    → Evidence Gate 检查: 有无证据？ → 无 → 转 Hypothesis
    → 系统验证 → Evidence支持 → 才能进入 Decision
```

## 八、与 V2.3 的关系（不冲突）

```
V2.3 已冻结: Evidence Authority + Scope Gate + Decision Qualification
V3.0 新增: AI Cognitive Layer（确定性引擎不变，AI 只做认知插槽）
两者正交：Gate 管"结论有没有资格"，AIN 管"结论怎么想出来"
```

## 九、落地顺序（建议）

```
Phase A: AIN-HYP + AIN-GAP（最安全，只提问题不下结论）
Phase B: AIN-RED + AIN-XCHK（反证与交叉验证，增强Gate）
Phase C: AIN-PAT + AIN-ALT + AIN-DEC（认知深化）
每期先定义 Contract → 再接执行器 → 回归验证
```

*2026-08-10 · V3.0 设计蓝图*
