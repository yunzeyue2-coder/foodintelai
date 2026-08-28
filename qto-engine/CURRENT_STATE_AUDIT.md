---
id: QTO-OS-AUDIT-001
title: 青藤OS Decision Operating System V1.0 缺口地图
version: V1.0
created: 2026-08-10
status: Sprint 0 完成（审计不编码）
category: 系统审计
---

> **背景：** 沧林拍板：青藤OS 从"报告生成系统"重构为"食品商业决策模拟系统"。炸鸡只是第一个 Benchmark。
> **原则：** 不做"优化炸鸡报告"，做"任何食品项目输入后都能进行生存推演的 AI 商业模拟器"。

# CURRENT STATE AUDIT

## 一、现有资产（能用的）

```
✅ 数据层
   - 高德采集管线（郑州金水区米线 / 炸鸡 2397家原始门店）
   - FID 数据标准（扫描/清洗/评级/边界）

✅ 品类画像
   - FAS 引擎（品类无关决策树：炸鸡19问/米线21问）
   - MI-XIAN-V1 米线插件 / 炸鸡插件（行业约束）

✅ 六轴 Ontology V0.3
   - 风格/工艺/价格/产品/品牌/空间（消费者视角）

✅ 分析引擎
   - Evidence Graph（JSON 网络，无孤儿可反查）
   - Hypothesis Engine（证据+反证+Unknown）

✅ 评分与决策
   - FDE Evidence Binding（评分绑定证据+置信度）
   - DecisionGraph（统一节点注册表+Authority Ceiling 传播）
   - Sample Coverage Gate / Evidence Authority Gate / 组合裁决
   - Model Registry（版本/参数/预测/回测入口）

✅ 流程控制
   - Workflow Engine（8态状态机，Failure Path 支持）
   - FQA 质量闸（100项检查）

✅ 交付
   - Report Compiler（JSON→FQA→HTML→PDF→6件套）
```

## 二、缺口地图（没有的）

```
❌ Business Model Simulator
   - 没有商业模型模拟：输入预算/经验 → 输出启动资金结构/风险区间
   - 缺: 投资结构（设备/装修/租金/现金流/试错资金）

❌ Unit Economics Engine
   - 没有单店经济模型：收入结构/成本结构/盈亏平衡/回本周期
   - 缺: 日销X单/客单价Y/毛利Z 的敏感性分析

❌ Site Decision Engine
   - 没有选址决策：商圈类型×租金区间×竞争密度×人流 决策矩阵
   - 缺: 选址评分卡

❌ Risk Engine
   - 没有风险量化：风险×概率×影响×应对
   - 缺: Risk Gate（风险触发→决策降级）

❌ Validation Engine
   - 没有验证计划：90-Day Battle Plan（验证什么/指标/达标进/不达标退）
   - 缺: Kill Criteria（止损线）

❌ Business Twin（商业数字孪生）
   - 没有生存压力测试：低/中/理想销量场景 → 现金还能撑多久

❌ Veto 机制
   - FDE 只有 Score→Recommendation，没有 Gate Check→Risk Penalty→Veto

❌ 企业视角 Ontology
   - 现有六轴是消费者视角，缺：需求/产品/工艺/供应链/成本/运营/复制/风险
```

## 三、架构升级路径（7 Sprint）

```
Sprint 0 系统审计（本文件）✅
Sprint 1 FDR Decision Schema V2.0（10模块）⬜
Sprint 2 Business Twin Engine（投资结构+生存压力）⬜
Sprint 3 FDE Gate Engine（Gate Check+Risk Penalty+Veto）⬜
Sprint 4 Food Business Ontology V1.0（企业视角）⬜
Sprint 5 Report Renderer V2（15页核心决策页）⬜
Sprint 6 重新生成炸鸡 FDR（V3.0 benchmark）⬜
```

## 四、目标形态

```
输入: 城市+品类+预算+经验+目标（如：郑州+炸鸡+20万+无经验+夫妻创业）
  ↓
青藤OS V1.0
  ├── 市场情报（Market Intelligence）
  ├── 机会矩阵（Opportunity Matrix）
  ├── 商业模型模拟（Business Twin）
  ├── 运营生存模型（Survival Model）
  ├── 风险闸门（Risk Gate）
  ├── 验证计划（Validation Plan）
  └── 最终决策（Final Decision + Kill Criteria）
  ↓
输出: 动态创业决策模拟（不是静态报告）
```

## 五、验证基准

```
炸鸡 = Benchmark 1（有全量数据 2397家 + 六轴）
米线 = Benchmark 2（金水区 200 家）
卤味/早餐/饮料 = 后续（同一 OS 上跑）
```

*2026-08-10 · Sprint 0 完成*
