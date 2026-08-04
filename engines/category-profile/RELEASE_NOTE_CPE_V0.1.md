# CPE Release Note V0.1
### Category Profile Engine · 发布记录

```yaml
engine: CPE (Category Profile Engine)
version: V0.1
status: frozen
validated:
  - CPE-001 Zhengzhou Mixian (郑州米线)
  - CPE-002 Zhengzhou Fried Chicken (郑州炸鸡)
standard: CPE_STANDARD V0.1
schema: category-profile-schema.yaml V0.1
input_asset: FID-001 (郑州餐饮数据集, 2025H1)
release_date: 2026.08.02
```

---

## 为什么建立 CPE

FoodIntelAI 需要一层**把数据资产转换为行业语义认知**的中间层：
- 数据是原料（FID）：108,350 家门店，40 字段
- 直接给 FDE 吃数据 → FDE 要承担品类解释工作，边界混乱
- CPE 负责回答"**这个品类是什么状态**"，FDE 负责"**这个人适不适合做**"

## 输入

- FID 数据资产（经 FID 标准清洗/评级，结构质量 A 级）
- 品类定义（includes/excludes，防城市口径漂移）

## 输出

- Category Profile 统一画像（九字段固定结构）：
  - identity 品类身份（强分类/弱分类）
  - market 市场规模（含覆盖率）
  - structure 品类结构
  - competition 竞争结构（品牌/连锁化率）
  - space 空间模式（区域/商圈/场景）
  - price 价格结构
  - quality 质量信号
  - insight 结构化判断（derived）
  - risk 风险项

## 已验证案例

| 实例 | 品类 | 关键发现 |
|---|---|---|
| CPE-001 | 米线（1,255家） | **弱分类品类**：无独立平台身份（69%寄生小吃快餐）、连锁化率 1.5%（阿香16家）、价格中位 ¥16 |
| CPE-002 | 炸鸡（2,397家） | **强分类品类**：77.7%独立分类、连锁化率 4.7%（正新94家）、高校+县域双场景 |

**双样本验证结论**：CPE 输出的是品类身份/组织化程度/竞争结构差异，不是简单数量比较——引擎不是"统计器"。

## 当前限制

- 数据源为 2025H1 静态快照，无时间维度，**不可做趋势判断**
- 价格/评分覆盖率约 50-69%，结论须标注覆盖率
- 品类定义依赖平台分类 + 店名关键词，存在口径边界（excludes 已记录）
- 品牌识别为关键词匹配（Rule-002），非语义识别
- insight 为 derived 判断（C 级证据），非数据事实

## 下一步（下一工作周期）

- FDE Interface Contract 已定义（见 FDE_INTERFACE_CONTRACT.md），接入 FDE Integration V0.4：Decision State 增加 Category State 输入
- 数据源扩展：FID-002 新城市 → CPE 直接复用（只换数据不换结构）

*CPE V0.1 · 2026.08.02 · FoodIntelAI 品类认知层首个冻结版本*
