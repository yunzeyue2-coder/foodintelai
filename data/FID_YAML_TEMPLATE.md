# FID YAML 元数据模板
### FoodIntelAI Data Standard V1.1 · 新城市数据集登记时复制此模板

> 用法：新增 FID-00X 时复制本模板到数据标准文档头部，替换占位值。质量三维（structure/analytical/temporal）必须填写，与其他 FID 直接可比。

```yaml
asset_id: FID-00X            # 按序分配
asset_type: Data
title: XX餐饮数据集
standard: FoodIntelAI Data Standard V1.1
version: 1.0
snapshot: YYYYH1            # 快照时点，如 2025H1
records: 0                   # 门店记录数
fields: 40
coverage:
  price: 0%                  # 有价格字段的记录占比
  rating: 0%                 # 有评分字段的记录占比
  comment: 0%                # 有评论字段的记录占比
quality:
  structure: A-              # 核心身份字段完整率/唯一性（A=≥99%，A-=95-99%）
  analytical: B              # 样本覆盖率与字段可用性（B+≈50%覆盖，B=更低）
  temporal: C                # 时间连续性（C=静态快照，B=多期快照，A=连续时序）
source:
  type: Third-party restaurant POI dataset
  description: 第三方餐饮POI数据快照（门店/品类/评分/价格/位置/菜单）
  attribution_status: 来源待核验    # 状态：来源待核验 / 已核验 / 官方授权
last_update: YYYY-MM
supported_engines: [Category, BusinessDistrict, Competition, Position]
limitation: 静态快照，无时间戳，不可做趋势分析；价格/评分为用户贡献值
```

## 填写检查清单

- [ ] asset_id 是否在 Asset Registry 中登记？
- [ ] snapshot 是否标注明确时点（季度级）？
- [ ] coverage 三项是否实测（非估计）？
- [ ] quality 三维是否填写并与其他 FID 可比？
- [ ] source.attribution_status 是否为"来源待核验/已核验"之一（禁用"推测"）？
- [ ] supported_engines 是否与 Chapter 7 兼容表对应？

*FID YAML Template · FoodIntelAI Data Standard V1.1 · 2026.08.02*
