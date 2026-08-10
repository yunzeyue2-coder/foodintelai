---
id: FDR-ARCH-001
title: FDR Decision Stack V1.0 规范
version: V1.0
status: 已冻结（2026-08-10 沧林最终校准）
owner: 沧林 + 青葵 + GPT审计吸收
category: FDR 报告架构
supersedes: FDR-ARCH-001 Draft（2026-08-10 初版）
---

> **关联：** [[FDR-EVIDENCE-002_Evidence_Boundary_Specification]] · [[FDR-WRITE-003_Writing_Standard]] · [[FDR-REPORT-001_报告结构与页面规格规范]] · [[外部AI对话记录_2026-08-10_FDR架构重构]]

# FDR Decision Stack V1.0 规范

## 一、核心架构理解（最重要）

> **M01–M15 是 Decision Schema（决策变量集合），不是 PDF 目录。**

模块是系统里的"决策变量集合"，不是报告里必须一章一章写出来的章节。

**生成 PDF 时：**
- 有价值的模块 → 展开
- 没有证据的模块 → 压缩成 "Unknown / Framework / Validation Required"
- **禁止为了凑 15 章而变水**

## 二、总体架构

```
                    FDR V1.0
                        │
             ┌──────────┴──────────┐
             │                     │
      Decision Stack         Evidence Layer
             │                     │
    ┌────────┴────────┐     ┌──────┼──────┐
    │                 │     │      │      │
  Market          Business  Data  Expert Experiment
    │                 │
M01 Market        M06 Product
M02 Structure     M07 Channel
M03 Demand        M08 Unit Econ
                  M09 Capital
                  M10 Supply
                  M11 Operation
    │                 │
    └────────┬────────┘
             ↓
      M04 Competition
      M05 Opportunity
             ↓
      M12 Scenario
      M13 Risk
      M14 FDE Decision
      M15 Validation
             ↓
         Go / Modify / Stop
             ↓
         Real-world Data
             ↓
           Feedback
             ↓
         Model Update
```

## 三、15 模块定义（5 层）

```
Layer A Market Intelligence
  M01 Market        市场规模/门店规模/价格/区域
  M02 Structure     六轴/市场结构/商业簇/Observable Coverage
  M03 Demand        需求与消费场景

Layer B Competition & Opportunity
  M04 Competition   HHI/CR/品牌/竞争拓扑
  M05 Opportunity   市场空白/结构性机会/进入窗口（独立模块）

Layer C Business Model
  M06 Product Architecture  产品结构/SKU/引流-利润-形象品
  M07 Channel Economics     堂食/外卖/团购/档口
  M08 Unit Economics        客单/订单/毛利/贡献/盈亏平衡
  M09 Capital Fit           资金需求/资金结构/现金流

Layer D Execution
  M10 Supply Chain          原料/规格/供应/冷链/包材
  M11 Operational Complexity 技能/良率/产能/人员依赖/标准化

Layer E Decision
  M12 Scenario              Bull/Base/Bear（框架，不编数字）
  M13 Risk                  风险矩阵/触发器/应对
  M14 FDE Decision          Score + Gate + Match
  M15 Validation Protocol   30/90/180天实验与 Stop/Go
```

## 四、模块证据状态五级（炸鸡当前快照）

| 模块 | 状态 | 含义 |
|------|------|------|
| M01 Market | A | 有真相源（2397家POI） |
| M02 Structure | A | 六轴 V0.3 已验证 |
| M03 Demand | D | 无消费者数据，Unknown |
| M04 Competition | A | HHI/CR 可重算 |
| M05 Opportunity | A/B | 结构机会数据 + 判断 |
| M06 Product | B | 专家判断（沧林食品经验） |
| M07 Channel | A/B | 外卖/团购字段 + 判断 |
| M08 Unit Economics | C | Framework-only |
| M09 Capital Fit | C | Framework-only |
| M10 Supply Chain | B | 专家判断 |
| M11 Operation | B | 专家判断 |
| M12 Scenario | E | 需实验获得 |
| M13 Risk | A/B/C | 混合 |
| M14 FDE Decision | A+B+C | 混合 |
| M15 Validation | E | 实验协议 |

## 五、Evidence Status 必须进入数据模型（不是写作规范）

每个 Metric / Insight / Decision 必须带结构化字段（完整定义见 FDR-EVIDENCE-002）：

```json
{
  "evidence_status": "A",
  "evidence_type": "data",
  "source": "...",
  "coverage": 0.678,
  "denominator": 2397,
  "formula": "...",
  "version": "...",
  "confidence": "high"
}
```

**目的：系统结构上不允许绕过 DI-004——不是 AI"记住"纪律，是 Schema 不允许。**

## 六、Evidence → Confidence → Decision Authority（证据决定决策权限）

| 证据等级 | 决策权限 |
|---------|---------|
| A 数据证据 | 可直接进入 Decision |
| B 专家判断 | 可进入 Conditional Decision |
| C Framework | 不得直接形成 Go |
| D Unknown | 不得形成确定性判断 |
| E Validation | 必须通过实验 Gate 后才能升级 |

**这是普通 AI 报告和 FDR 最大的区别：证据等级直接决定结论等级。**

## 七、Product Tier（按决策深度分级）

| 产品 | 价格 | 回答 | 覆盖 |
|------|------|------|------|
| Market Brief | ¥199 | 这个市场是什么样？ | Market+Structure |
| Decision Report | ¥699 | 应不应该进入？ | +Competition+Opportunity+Business Model+Risk+Decision |
| Decision & Validation | ¥1299 | 决定进入后怎么验证？ | +Unit Econ Framework+Capital+Scenario+Validation+Stop/Go |
| 定制 | ¥2999+ | 个体化决策 | 全模块 |

**禁止机械按页数收费。**

## 八、生产规则

- **换数据不换发动机**：新品类只换 Data + Ontology + Decision State
- 炸鸡 V2.1 最大价值 = 把 FDR 生产标准做成 100 分（不是把炸鸡报告做到 100 分）
- Decision Density：每页回答一个决策问题（详见 FDR-WRITE-003）

*2026-08-10 最终冻结 · 沧林拍板*
