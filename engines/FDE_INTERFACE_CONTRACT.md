# FDE Interface Contract V0.1
### CPE → FDE 接口契约 · 定义"CPE 给 FDE 什么"

> 本契约只定义接口，不开发 FDE。目的：下一工作周期接入 FDE Integration V0.4 时不返工。

## 一、接口定位

```
FID（数据）→ CPE（品类认知层）→ [本契约] → FDE（商业决策层）→ FIV（验证层）
```

CPE 输出**品类状态**（行业侧事实+归纳+推断），FDE 消费它做**个体适配判断**（用户侧）。

## 二、CPE → FDE 输入（Category Profile State）

FDE 从 CPE 接收以下标准化品类状态（由 CPE Schema 九字段提炼）：

```yaml
category_state:
  category: 米线                # 品类名
  identity: weak_identity       # strong_identity / weak_identity（独立分类占比）
  competition: fragmented       # concentrated / fragmented（连锁化率阈值）
  price_band: low               # low(<20) / mid(20-40) / high(40+)
  chain_level: low              # low(<5%) / mid(5-15%) / high(>15%)
  quality_signal: mediocre      # strong(4.0+) / mediocre(3.5-4.0) / weak(<3.5)
  opportunity_signal: differentiation_required   # 由 CPE insight 映射
  evidence_level: B+            # 携带证据等级
  coverage: {price: 69%, rating: 59%}
```

**映射规则**（CPE 九字段 → Category State 七字段）：

| CPE 字段 | Category State | 映射逻辑 |
|---|---|---|
| identity | identity | 独立分类占比 ≥60% → strong，否则 weak |
| competition.brand_pattern | competition | 连锁化率 ≥10% → concentrated，否则 fragmented |
| price.median | price_band | <20 low / 20-40 mid / 40+ high |
| competition.chain_rate | chain_level | <5% low / 5-15% mid / >15% high |
| quality.rating | quality_signal | 均值 ≥4.0 strong / 3.5-4.0 mediocre / <3.5 weak |
| insight | opportunity_signal | CPE 结构化判断映射（差异化/进入/饱和） |
| — | evidence_level / coverage | 透传 FID 质量元数据 |

## 三、FDE 消费方式（升级后）

**现状**：Decision State Generator 输入 = 身份/目标/资源/能力/约束
**升级（V0.4）**：+ Category State

```
身份 / 目标 / 资源 / 能力 / 约束
        +
Category State（品类状态）
        ↓
Decision State
        ↓
推荐 / 不推荐 / 原因 / 风险 / 下一步
```

**示例**：
- 用户：20万预算、新手、郑州
- 品类：米线
- CPE 状态：low chain / low brand barrier / high homogeneity
- FDE 判断：不是简单"推荐米线"，而是"**需要差异化定位，否则进入价格竞争**"

## 四、接口约束

- FDE **不得**直接消费 FID 原始数据——必须经由 CPE 转换
- Category State 七字段为 FDE 唯一品类输入（冻结）
- 状态值域固定（上表括号内枚举），FDE 判断逻辑依赖枚举而非自由文本
- evidence_level < B 时，FDE 输出须降置信度标注

## 五、契约版本

| 项 | 值 |
|---|---|
| Contract | FDE_INTERFACE_CONTRACT V0.1 |
| 状态 | 待 FDE Integration V0.4 实施 |
| 关联 | CPE_STANDARD V0.1（frozen）/ Category Profile Schema V0.1（frozen） |
| 日期 | 2026.08.02 |

*FDE Interface Contract V0.1 · 2026.08.02 · 接口先行，实施在后*
