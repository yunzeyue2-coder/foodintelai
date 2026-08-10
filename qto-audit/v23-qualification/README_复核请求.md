# QTO-V2.3 Decision Qualification 全面复核请求

> 审计对象：**V2.3 引擎规范本身**（不是某份报告）
> 审计性质：红队审计——找 Gate 的漏洞、绕过路径、逻辑缺陷，不做建设性评价
> 审计依据：QTO-V2.3-STD-001 + evidence_authority_gate.py + sample_coverage_gate.py + 附件

---

## 背景

青藤OS 版本演进：
```
V2.1 = Workflow 能跑
V2.2 = 跨品类能跑
V2.3 = 有资格才允许决策（Evidence Authority × Sample Coverage → Decision Qualification）
V2.4 = 让系统自己发现"我不知道什么"（未来）
```

V2.3 核心架构变化：
```
Decision 不再只是 Evidence 的必然产物
而是：Evidence → Qualification → 才有资格 → Decision
```

## 请审计 6 件事

### 0. 审计姿态（最高优先，GPT必读）

> **把自己当成攻击者，不证明 V2.3 正确，而是证明 V2.3 可以被绕过。**
> 如果攻击不出漏洞，V2.3 才有资格冻结。

### 0.5 最高优先级：图级审计（Graph-Level Audit）

> **不要在字段级找 D/E，要在 Decision Graph 上找所有 D/E Evidence → Final Decision 的间接路径。**

检查以下路径是否被 Authority Gate 拦截：
```
D Evidence → Insight → Hypothesis → FDE Score → Decision
D Evidence → Insight → Decision（间接引用）
D Evidence → Hypothesis → Decision
D Evidence → Condition → Decision（藏在条件里影响判断）
D Evidence → Narrative（Executive Summary/Recommendation 文本引用）
D Evidence → FDE 评分维度 → Decision
```

**必须证明：D ──X──→ Decision（所有路径）。** 否则 Authority Gate 只是字段校验器，还不是 Decision Authority。

### 0.6 审计重点（沧林 2026-08-10 追加）

#### ① Evidence Lineage（证据谱系）
每个 Decision 必须可追溯：
```
Decision → Reason/Score/Condition → Insight/Hypothesis → Evidence
```
然后检查**最低 Evidence Authority**（链上任一环节是 D/E → 整条链权限不高于 D）。

#### ② Authority Propagation（权限传播）⭐ 当前最缺
Authority 必须沿 Evidence Graph **向上继承**：
```
E008(D) → I005 → I005 的 Authority 不能高于 D
I005(D) → H003 → H003 也不能获得 A/B 权限
H003(D) → FDE Score → 该 Score 不得作为独立 Decision Authority
```
**问题：当前代码是否实现了这个传播？** 还是只有 decision_memo 的 Reason 直连被检查？

#### ③ Negative Evidence（负证据）
```
A/B/C 证据 → Decision（支持）
D 证据 → 反证/挑战信息 → 可以存在，但不能升级成事实
```
例："D级资料提示可能存在盈利模型问题" → 可作为 Challenge/Condition/Unknown，但**不能**变成"盈利模型已被证明存在问题"。
**检查：Evidence Authority ≠ Evidence Utility——低等级证据不是没用，而是权限低。**

### 1. Evidence Authority Gate
- A/B/C/D/E 分级是否符合 Decision Authority 原则？
- C 是否真的只能进入 conditions？代码里是否有路径让 C 混入主理由？
- **D/E 是否在所有入口都被阻断**，还是只在某一测试路径被阻断？
- 检查：gate 只暴露了 check_reasons() 一个入口，但如果报告生成链其他环节（Insight 生成、Hypothesis 评估、FDE 评分）引用 D/E 证据，是否也被拦？还是只有 decision_memo 被拦？

### 2. Sample Coverage Gate
- 六变量（coverage/bias/geographic/penetration/completeness/temporal）定义与权重是否合理？
- GLOBAL/REGIONAL/LOCAL/INSUFFICIENT 四级阈值（0.75/0.55/0.35）是否存在逻辑漏洞？
- **已发现并修复的漏洞（2026-08-10 内部预审）**：加权平均可被"单维度极差但其他满分"绕过（coverage=0.01 但其他满分 → 0.752 → 曾误判 GLOBAL）。已加**单维度硬底线**（HARD_FLOORS：coverage<0.30→最高LOCAL、geographic<0.25→最高REGIONAL、bias<0.40→最高REGIONAL），任一关键维度跌破底线即降级，不被加权稀释。
- **请继续攻击**：硬底线是否有其他绕过路径？如：把 coverage 报高（采样分母造假）、bias 自评虚高、geographic 分类模糊等。Gate 是否有办法识别参数本身的可信度？

### 3. Gate 组合逻辑（最重要）
```
Evidence Authority × Sample Coverage → Decision Qualification
```
- 是否可能：Evidence Authority 全 PASS，但 Sample Coverage 极差 → 仍输出决策？（应该是：任一 Gate 否决 → 整体降级）
- 是否可能：Sample Coverage 全 PASS，但 Evidence Authority 有 D/E → 仍输出决策？
- **两个 Gate 的否决权是否正交**（各自独立否决）？还是其中一个高分可以抵消另一个的否决？

### 4. Regression 三案例
- 炸鸡 GLOBAL / 米线 LOCAL / 极端案例 INSUFFICIENT——三个方向是否稳定可复现？
- 是否有隐藏参数让结果对输入变化过于敏感？

### 5. 反向审计
- 把最终 Decision 遮掉，只看 Evidence + Gate 输出，重新推一次 Scope 和 Decision Qualification，能否推出同样的结论？

### 6. 绕过 Gate 的路径（最关键的红队测试）
> 有没有某种写法，可以不直接把 D 级证据放进 Reason，而是藏在 Insight / Hypothesis / Condition / Narrative 中，最后仍然影响 Decision？

请主动攻击以下绕过路径：
- **藏在 Condition 里**：把 D 级证据写进 conditions（"需验证 X，X 基于某 D 级假设"）→ 是否间接影响决策？
- **藏在 Insight 里**：Insight 引用 D 级证据，Decision 引用该 Insight（间接引用）→ Gate 是否只查直连证据，不查间接路径？
- **藏在 Hypothesis 里**：Hypothesis 用 D 级证据"proposed"，Decision 引用该 Hypothesis → 绕过？
- **藏在 Narrative 里**：Executive Summary 或 Recommendation 文本中直接引用 D 级数据，不经过 Reason 结构 → 绕过？
- **藏在 FDE 评分里**：FDE 评分维度用 C/D 级证据打分，评分进入 Decision → 绕过？

对每种路径，请判断：**当前 Gate 能否拦截？** 如不能，说明缺口在哪。

---

## 输出格式

《QTO-V2.3 Decision Qualification 全面复核报告》
1. 六项审计结果（每项 PASS / ISSUES / CRITICAL）
2. 发现的问题清单（按严重度排序，P0/P1/P2）
3. 关键判断：Gate 是否真正形成"有资格才允许决策"的系统级闭环？还是仍有绕过路径？
4. 结论：V2.3 是否可以冻结？还是需先修 P0？
