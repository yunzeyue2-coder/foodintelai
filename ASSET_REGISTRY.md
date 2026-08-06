# FoodIntelAI Asset Registry · 资产注册中心

> 所有资产的统一登记入口。官网 / 知识库 / Decision OS 查资产先查这里。
> 原则：**数据是原料，资产是可复用的标准与判断。** 四条资产线：Framework / Data / Validation / Research。

更新：2026.08.02 · V0.1（登记现有资产，持续补充）

---

## 一、Framework（框架资产 · FIF 系列）

| Asset ID | 名称 | 类型 | 状态 | 位置 |
|---|---|---|---|---|
| FIP-001~005 | 系统/因果/消费者优先/证据/边界原则 | 研究原则 | 已发布 | frameworks/FIP*.html |
| FIF-001 | 七维产业决策框架 | 分析框架 | 已发布 | frameworks/FIF-001.html |
| FIF-002 | 全国化分析框架 | 分析框架 | 已发布 | frameworks/FIF-002.html |
| FIF-003 | 品类定位框架 | 分析框架 | 已发布 | frameworks/FIF-003.html |
| FIF-004 | 商业模式分析框架 | 分析框架 | 已发布 | frameworks/FIF-004.html |
| FIF-005 | 价值链分析框架 | 分析框架 | 已发布 | frameworks/FIF-005.html |
| **FIF-37** | 区域食品生态模型 | Core Framework | 完善中 | frameworks/FIF-37_区域食品生态模型.html |
| **FBIS-001** | FoodIntelAI Brand Intelligence Standard V1.0（品牌三层命名/连锁化/CRN/工业化矩阵/BSPI） | 品牌分析标准 | active V1.0 | Obsidian 07_Standards/FBIS/FBIS_V1.0_品牌分析标准.md |
| FIM-001~005 | 八步研究法/第一性原理/多模型/交叉验证/认知重构 | 方法论 | 已发布 | frameworks/FIM*.html |
| FIS-001~005 | 食品产业系统/五世界/品类生命周期/老板自由度/压力测试 | 系统模型 | 已发布 | frameworks/FIS*.html |
| FIE | 证据分级（A高可信/D行业经验） | 证据体系 | 已发布 | frameworks/FIE*.html |

## 二、Data（数据资产 · FID 系列）

| Asset ID | 名称 | 快照 | 记录数 | 质量 | 状态 | 位置 |
|---|---|---|---|---|---|---|
| **FID-001** | 郑州餐饮数据集（线上POI样本） | 2025H1 | 108,350 | structure A / analytical B+ / temporal C | frozen V1.2（模板已启用） | data/FID-001_郑州餐饮数据标准.md |
| FID-002 | （待定城市） | — | — | — | template_ready（复制模板） | — |

## 三、Validation（验证资产 · FIV 系列）

| Asset ID | 名称 | 状态 |
|---|---|---|
| — | 暂无（预测 vs 实际回填库，待体系运转后建立） | 待建 |

## 三·五、Engines（引擎资产 · 执行层）

> Framework 是规则，Engine 是执行——引擎资产单独登记。

| Asset ID | 名称 | 状态 | 位置 |
|---|---|---|---|
| **CPE-STD-001** | Category Profile Engine Standard V0.1 | frozen | engines/category-profile/CPE_STANDARD_V0.1.md |
| **CPE-Schema** | Category Profile Schema V0.1 | frozen（双实例验证） | engines/category-profile/schema/category-profile-schema.yaml |
| **CPE-001** | 郑州米线品类画像 | validated | engines/category-profile/CPE-001_郑州米线画像.md |
| **CPE-002** | 郑州炸鸡品类画像 | validated | engines/category-profile/CPE-002_郑州炸鸡画像.md |
| **CPE-RN** | CPE Release Note V0.1 | frozen | engines/category-profile/RELEASE_NOTE_CPE_V0.1.md |
| **FDE-IFC** | FDE Interface Contract V0.1（CPE→FDE） | 接口就绪·待实施 | engines/FDE_INTERFACE_CONTRACT.md |
| **INS-001** | FID Insight Engine V1.0（X1供给结构已固化，X2-X5待扩展） | X1 frozen | data/FID-001_INSIGHT_ENGINE_V1.0.md |
| **BIE-001** | Brand Intelligence Engine V1.0（三层分离/连锁化/CRN/HHI/工业化矩阵/BSPI） | active（郑州已验证） | Obsidian 02_Models/引擎源码/bie.py |
| **BIE-ZZ-001** | 郑州品牌生态分析报告（FBIS V1.0 口径，108,350 POI） | validated 2026-08-06 | Obsidian 03_DataAssets（输出副本 ~/Desktop/滄林/fbis_output/） |
| **BDE** | Business District Engine（商圈画像） | 规划中（Schema 可复用） | — |
| **CE** | Competition Engine（竞争密度） | 规划中（Schema 可复用） | — |

## 四、Research（研究资产 · FIR 系列）

| Asset ID | 名称 | 状态 | 位置 |
|---|---|---|---|
| FIR-001 | 中国米线产业研究（Day1-7 收官） | 已发布 | research/Day*.html |
| FIR-002 | 中国早餐产业研究（7篇） | 已发布 | research/早餐系列*.html |
| FIR-003 | 炸鸡产业研究 | 已发布 | research/炸鸡_*.html |
| FIR-004 | 卤味产业研究 | 已发布 | research/卤味_*.html |
| FIR-005 | 面食产业研究 | 已发布 | research/面食_*.html |
| FIR-006 | 第005期 Weekly Intelligence 内参 | 已发布 | neican/FoodIntelAI-第005期.html |

---

## 注册规范（新增资产时遵循）

1. 每条资产唯一 Asset ID（FIF/FID/FIV/FIR + 序号）
2. Data 资产必须附 YAML 元数据（见 FID-001 头部模板）并做质量评估
3. 数据源须标注：来源/时点/覆盖率/用途边界
4. 状态标记：已发布 / 完善中 / 待建

*V0.1 · 2026.08.02 · 数据是原料，标准是资产，验证是壁垒*
