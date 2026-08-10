# 青藤OS V2.0 系统审计资料包（Phase 0）

> 目的：请审计方（GPT）以咨询公司验收视角，评价**生产报告的机器**（青藤OS），而非评价某一份报告。
> 定位：先审生产设备本身，再决定米线 PORT-001 怎么跑。

## 审计要求（沧林 2026-08-10 拍板）

按咨询机构方式做一次《青藤OS架构审计报告 V1.0》，输出：
- 当前成熟度评分（按 QTO-SYSTEM-AUDIT-001 健康检查表，100分制）
- 缺失设备 / 冗余设备 / 职能空白
- 标准缺口
- V2.1 升级路线
- 结论：情况A（系统成熟→直接米线测试）/ 情况B（缺设备→先补）/ 情况C（设备有但标准不足→先补参数规则模板）

## 健康检查表（100分）

| 维度 | 分值 | 检查内容 |
|------|------|---------|
| A 架构完整性 | 20 | 是否分层/是否闭环/是否有治理层 |
| B 模型成熟度 | 20 | Model Card/参数/版本/验证 |
| C 数据可信度 | 20 | 数据来源/清洗/覆盖率/时间 |
| D 咨询标准 | 20 | 问题定义/MECE/假设驱动/证据链 |
| E 输出质量 | 20 | 报告结构/决策逻辑/行动建议/FQA |

## 资料清单（12份）

| # | 文件 | 内容 |
|---|------|------|
| 01 | OS架构蓝图 | 青藤OS V2.0 八层架构 + 11环节标准链路 + 设施优先级 |
| 02 | Decision Stack规范 | FDR-ARCH-001：5层15模块 Schema + Decision Authority |
| 03 | 证据边界规范 | FDR-EVIDENCE-002：A/B/C/D/E 五级证据 Schema |
| 04 | 写作标准 | FDR-WRITE-003：Decision Density 每页一个决策问题 |
| 05 | 引擎验证报告 | FDR-VALIDATE-001：炸鸡 V2.1 压力测试（Schema/Evidence/Authority/Density/Reproducibility） |
| 06 | FCS Project Charter | 咨询标准系统：项目定义卡（炸鸡首张真实卡） |
| 07 | FQA 质量审查 | 质量闸门标准：三组14项检查 + 炸鸡基线 100/100 |
| 08 | Model Cards | 模型治理：5个模型完整卡（M-HHI-STRUCTURE/M-HHI-BRAND/M-OBS-COVERAGE/M-FDE-SCORE/M-SKILL-GATE） |
| 09 | fqa_check.py | FQA 审查机器人源码（可执行） |
| 10 | REPORT JSON V2.1 | 炸鸡报告数据模型（13证据带 Schema + 5 Insight + 6 BM + FDE） |
| 11 | Metrics V2.1 | 可重算指标规格（HHI/Observable 带 formula/filter/denominator） |
| 12 | 数据可信规范 | FDR-DATA-001 数据可信体系 |

## 补充资料（审计需要可再问）

- 原始数据：`../fdr-reports/data/zz_fried_label_table_v03.csv`（2397×30 六轴标签表·真相源）
- 渲染管线：`../fdr-reports/source/render/fdr_render_v2.py`（JSON→HTML→PDF）
- 历史版本：REPORT_JSON V1.0/V1.1（在 Obsidian 07_Standards，未随包）——需要可补充

## 待审计方确认的问题

1. 五层架构（数据/模型/知识/决策/报告/质量）层级关系、数据流、控制流、输出流是否成立？
2. Device Inventory 是否有重复/缺失/职能空白？
3. 每个设备（尤其 FDE）的标准参数是否足够（模型名称/版本/输入/权重/公式/区间/阈值/失效条件）？
4. Evidence Pipeline（数据→结论）是否无黑箱？
5. Report Compiler 是否够标准（输入→Executive Summary/Key Findings/Analysis/Recommendation/Action Plan/Appendix）？

*2026-08-10 · Phase 0 审计启动*
