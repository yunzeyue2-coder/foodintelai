---
id: QTO-FQA-001
title: FQA 质量审查标准（Food Quality Assurance）
version: V1.0
status: 已启用（2026-08-10 首版）
owner: 青葵
category: 质量控制
---

> **关联：** [[QTO-V2-ARCH-001_青藤OS_V2_架构蓝图]] · [[FDR-ARCH-001_Decision_Stack_V1.0]] · [[FDR-EVIDENCE-002_Evidence_Boundary_Specification]]

# FQA 质量审查标准

## 一、定位

把 FDR 四层 QC 变成**可执行检查清单机器人**（fqa_check.py）。每份报告生成后自动跑，输出 FQA Score + 问题清单。

## 二、三组检查

### 逻辑组（结论不超过证据）
- 每个 Insight 必须有证据绑定，且绑定的证据存在于 evidence_layer
- 证据等级限制结论强度：A级可 direct；C/D 级不得 direct（Decision Authority）
- D级（Unknown）不形成确定性判断

### 商业组（有赚钱模型）
- 风险模型存在（risk_layer）
- 停止条件存在（90天验证 Gate）
- 单店经济框架存在（允许 Framework-only，Evidence Boundary 合规）

### 咨询组（咨询交付要素）
- Executive Summary（数据模型必须有 executive_summary 字段）
- Decision（明确 Go/Conditional/No-Go）
- Recommendation（推荐方向）
- Action Plan（行动方案）
- Conditions（成立条件）
- Decision Trace（决策理由链）

## 三、评分

```
FQA Score = 通过项 / (通过项 + 问题项) × 100
A ≥90 / B ≥75 / C ≥60 / D <60
```

## 四、炸鸡 V2.1 基线

**FQA Score: 100/100 (A)** —— 14项全过（逻辑5/商业3/咨询6）

## 五、配套

- 模型治理: `model_cards_v1.json`（Model Governance，每个模型带适用场景/输入/逻辑/权重/限制/验证/版本）
- 脚本: `/tmp/fqa_check.py`（可复用）

*2026-08-10 首版启用*
