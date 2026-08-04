# Category Profile Engine Standard V0.1
### CPE 标准 · FoodIntelAI 品类认知层

## 〇、引擎定位

> CPE 是将餐饮数据资产转换为品类结构认知资产的分析引擎。

**输入**：FID 数据资产
**输出**：Category Profile（品类画像）
**定位边界**：CPE 负责回答"这个品类是什么状态"；FDE 负责回答"这个人适不适合做这个品类"——两者边界清晰，FDE 不承担品类解释工作。

**验证状态**：双样本验证通过（CPE-001 米线 / CPE-002 炸鸡）→ 已证明不是"统计器"：两个品类输出的是品类身份、组织化程度、竞争结构差异，而非简单数量比较。

---

## Chapter 1 · 输入规范

数据源：FID Data Asset（如 FID-001 郑州餐饮数据集）

必须包含的实体与最低字段：

| 实体 | 最低字段 |
|---|---|
| Category | 二类/三类分类 |
| Restaurant | 门店名称/id |
| Location | 区/商圈/lng/lat |
| Price | 人均价格 |
| Review | 评论数/评分 |
| Brand | 品牌（店名归一提取） |

输入须通过 FID 质量评估（结构质量 A- 以上），并携带字段覆盖率。

---

## Chapter 2 · 品类定义规范

每个 CPE 必须记录品类定义，**避免城市之间口径漂移**：

```yaml
category_definition:
  keyword: 米线
  includes:
    - 米线
    - 云南米线
    - 过桥米线
    - 酸辣米线
  excludes:
    - 米粉
    - 螺蛳粉
    - 河粉
```

规则：
- keyword 为匹配主词（店名 OR 平台三类分类包含）
- excludes 排除易混淆的邻近品类——否则跨城市比较会失真
- 每个城市执行同一份品类定义，允许按当地习惯补充 includes（须记录）

---

## Chapter 3 · 指标体系（六大模块）

| 模块 | 指标 | 说明 |
|---|---|---|
| 1. Market Scale 规模 | 门店数量 / 占餐饮比例 / 覆盖率 | 覆盖率须标注（价格/评分/评论） |
| 2. Category Identity 品类身份 | 平台分类归属 / 独立分类比例 | 判断品类认知强弱（弱分类=认知弱） |
| 3. Competition Structure 竞争结构 | 品牌数量 / TOP品牌 / 连锁化率 | CR 指标按证据等级标注 |
| 4. Spatial Pattern 空间模式 | 区域分布 / 商圈分布 / 核心场景 | 高校/社区/商圈等场景识别 |
| 5. Price Structure 价格结构 | 中位价 / 主价格带 / 分布 | 价格定义=平台人均，非成交价 |
| 6. Quality Signal 质量信号 | 评分均值/中位 / 高分化比例 | 覆盖率<60%须警示 |

---

## Chapter 4 · 输出 Schema（固定结构）

```yaml
category_profile:
  identity:
    category_name: 米线
    definition: {includes: [], excludes: []}
  market:
    store_count: 0
    coverage: {price: 0%, rating: 0%, comment: 0%}
  structure:
    classification: []       # 平台分类分布
  competition:
    brand_pattern: {}        # 品牌及连锁化率
  space:
    district_pattern: []     # 区县分布
  price:
    median: 0
    bands: {}
  quality:
    rating: {mean: 0.0, median: 0.0}
  insight:
    structural_judgement: "" # 结构化判断（derived）
  risk:
    limitation: []           # 覆盖率/异常/场景依赖
```

冻结规则：本结构（output 九字段）冻结后不得改动；新实例只替换数据，不替换结构。

---

## Chapter 5 · 证据规则（继承 FIE）

每个画像判断必须分级，与 FIF-37 证据校准一致：

| 判断层级 | 示例 | 证据要求 |
|---|---|---|
| 事实（A级） | 门店 1,255 家 | 数据直接支撑 |
| 归纳（B级） | 品牌识别：阿香16家 | 品牌归一规则可追溯 |
| 推断（C级） | 连锁化程度低 | 由 B 级推导，标注"derived" |

**禁令**：
- ❌ 直接从画像写"行业没有机会/值得进入"——那是 FDE 的判断，不是 CPE 的输出
- ❌ 用 <60% 覆盖率的数据下全量结论
- ❌ 把 derived（推断实体）当原始字段使用

---

## 冻结记录

| 项 | 值 |
|---|---|
| Standard | CPE_STANDARD V0.1 |
| Schema | category-profile-schema.yaml V0.1（frozen） |
| 验证实例 | CPE-001 郑州米线 / CPE-002 郑州炸鸡 |
| 冻结日期 | 2026.08.02 |
| 下一步 | CPE-002 文档化 → FDE 接入（FID→CPE→FDE） |

*CPE Standard V0.1 · 2026.08.02 · FoodIntelAI 品类认知层*
