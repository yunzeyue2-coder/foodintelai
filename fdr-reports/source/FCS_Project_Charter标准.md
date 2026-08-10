---
id: QTO-FCS-001
title: FCS 咨询标准系统 · Project Charter 标准
version: V1.0
status: 已启用（2026-08-10 沧林第一优先）
owner: 沧林 + 青葵
category: 咨询标准
---

> **关联：** [[QTO-V2-ARCH-001_青藤OS_V2_架构蓝图]] · [[FDR-ARCH-001_Decision_Stack_V1.0]]

# FCS 咨询标准系统 · Project Charter

## 一、定位

> 一个项目从哪里开始？——先定义问题，不先分析。

**没有 FCS，FAS 和 Hypothesis 没有约束。**

## 二、Project Charter（项目定义卡）字段

| 字段 | 内容 | 示例 |
|------|------|------|
| 1. Decision Question | 真正的问题（不是"行业分析"） | 20万元创业者是否应该进入郑州炸鸡市场？ |
| 2. Decision Boundary | 分析什么/不分析什么 | 分析：市场结构/竞争/进入方式；不分析：加盟品牌内部管理 |
| 3. Success Criteria | 成功标准 | 一年内：盈亏平衡/现金流安全/可复制 |
| 4. Client Profile | 客户画像 | 首次创业者/20万/无餐饮经验/郑州 |
| 5. Constraints | 限制条件 | 预算上限/风险偏好/时间窗口 |
| 6. Output Requirements | 输出要求 | 决策报告+验证协议+停止条件 |

## 三、正确 vs 错误的问题定义

```
❌ 错误: 郑州炸鸡市场怎么样？（行业分析，无法决策）
✅ 正确: 一个20万预算、无餐饮经验创业者，在郑州进入炸鸡品类，
        未来36个月成功概率如何？（可决策）
```

## 四、第一张真实卡：FDR-ZZ-FRIED-001 Project Charter

```json
{
  "project_id": "FDR-ZZ-FRIED-001",
  "decision_question": "一个20万预算、无餐饮经验的首次创业者，是否应该进入郑州炸鸡市场？如果进入，以什么方式进入？",
  "decision_boundary": {
    "in_scope": ["市场结构", "竞争生态", "商业簇", "进入方式", "验证协议"],
    "out_of_scope": ["加盟品牌内部管理", "外卖平台运营细节", "品牌方招商政策"]
  },
  "success_criteria": {
    "time_horizon": "36个月",
    "criteria": ["12个月内盈亏平衡", "现金流安全（不追加投资）", "模型可复制（单店→多店）"]
  },
  "client_profile": {
    "identity": "首次创业者",
    "city": "郑州",
    "category": "炸鸡",
    "capital": "20万",
    "experience": "无餐饮经验",
    "risk_preference": "中低风险"
  },
  "constraints": ["预算上限25万", "不接受重资产", "90天需验证期"],
  "output_requirements": ["FDR决策报告", "30/90/180天验证协议", "停止条件", "Evidence Schema可审计"]
}
```

## 五、用途

- 每个 FDR 项目启动时先产出 Project Charter
- FQA 增加检查项：报告是否对齐 Project Charter 的 Decision Question
- 米线 PORT-001 将产出第二张卡（验证 FCS 品类无关性）

*2026-08-10 启用 · 沧林第一优先项*
