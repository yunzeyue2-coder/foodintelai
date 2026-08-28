#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FDR-ZZ-FRIED-001 V2.0 42页渲染 — JSON → HTML（组件化）→ Playwright PDF"""
import json, os, html as html_mod

OUT = "/tmp/fdr_zz_v2"
os.makedirs(OUT, exist_ok=True)

with open("/tmp/FDR-ZZ-FRIED-001_REPORT_JSON_V2.0.json", encoding="utf-8") as f:
    R = json.load(f)

def esc(t): return html_mod.escape(str(t))

# ============ 深蓝麦肯锡风 CSS（FDR 渲染 UX） ============
CSS = """
@page { size: 297mm 210mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; color: #1F2937; font-size: 10.5pt; background: #fff; }
.page { width: 297mm; height: 210mm; page-break-after: always; padding: 10mm 10mm; position: relative; background: #fff; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 20pt; color: #0B1F3A; margin-bottom: 4mm; }
h2 { font-size: 14pt; color: #0B1F3A; margin-bottom: 3mm; }
h3 { font-size: 11pt; color: #0B1F3A; margin-bottom: 2mm; }
.section-label { font-size: 8pt; letter-spacing: 2px; color: #9CA3AF; text-transform: uppercase; margin-bottom: 1mm; }
.header-bar { border-top: 3px solid #0B1F3A; padding-top: 3mm; margin-bottom: 6mm; }
.subtitle { font-size: 11pt; color: #6B7280; margin-bottom: 6mm; }
.data-card { border: 1px solid #E5E7EB; border-radius: 2mm; padding: 5mm; margin-bottom: 4mm; background: #F8F9FA; }
.value { font-size: 26pt; font-weight: 700; color: #0B1F3A; }
.unit { font-size: 11pt; color: #6B7280; margin-left: 1mm; }
.metric { font-size: 10pt; color: #374151; margin-top: 1mm; }
.meta { font-size: 7.5pt; color: #9CA3AF; margin-top: 1mm; }
.score-card { display: flex; gap: 4mm; margin-bottom: 4mm; }
.score-item { flex: 1; border: 1px solid #E5E7EB; border-radius: 2mm; padding: 4mm; text-align: center; }
.score-item.hl { border-color: #0B1F3A; background: #0B1F3A; color: #fff; }
.label { font-size: 7.5pt; letter-spacing: 1px; color: #6B7280; }
.score-item.hl .label { color: #C4A35A; }
.num { font-size: 24pt; font-weight: 700; color: #0B1F3A; font-family: 'SF Mono', monospace; }
.score-item.hl .num { color: #fff; }
table.data-table { width: 100%; border-collapse: collapse; font-size: 9pt; }
table.data-table th { background: #0B1F3A; color: #fff; padding: 2mm; text-align: left; font-size: 8pt; }
table.data-table td { border: 1px solid #E5E7EB; padding: 2mm; }
table.data-table tr:nth-child(even) td { background: #F8F9FA; }
.matrix2x2 { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; margin: 4mm 0; }
.matrix-cell { border: 1px solid #E5E7EB; border-radius: 2mm; padding: 5mm; min-height: 30mm; }
.matrix-cell.hl { background: #0B1F3A; color: #fff; border-color: #0B1F3A; }
.matrix-cell.hl .mc-title { color: #C4A35A; }
.mc-title { font-weight: 700; color: #0B1F3A; margin-bottom: 2mm; }
.mc-desc { font-size: 9pt; color: #6B7280; line-height: 1.6; }
.matrix-cell.hl .mc-desc { color: #D1D5DB; }
.evidence-chain { border-left: 3px solid #C4A35A; padding-left: 4mm; margin: 4mm 0; }
.evidence-chain .step { margin-bottom: 2.5mm; font-size: 9.5pt; }
.tag { display: inline-block; background: #0B1F3A; color: #fff; font-size: 7pt; padding: 0.5mm 2mm; border-radius: 1mm; margin-right: 2mm; }
.impact-box { border: 1px solid #C4A35A; background: #FDFBF7; padding: 3mm; border-radius: 2mm; font-size: 9pt; margin-top: 4mm; }
.impact-label { font-size: 7.5pt; font-weight: 700; color: #8B6914; letter-spacing: 1px; margin-bottom: 1mm; }
.footer { position: absolute; bottom: 5mm; left: 10mm; right: 10mm; font-size: 7pt; color: #9CA3AF; border-top: 0.5pt solid #E5E7EB; padding-top: 1.5mm; display: flex; justify-content: space-between; }
.cover { background: #0B1F3A; color: #fff; display: flex; flex-direction: column; justify-content: center; padding: 20mm; }
.cover h1 { color: #fff; font-size: 26pt; }
.cover .cover-sub { color: #C4A35A; font-size: 12pt; margin-top: 4mm; }
.cover .cover-meta { color: #8A94A6; font-size: 9pt; margin-top: 8mm; line-height: 1.8; }
.archetype { border: 1px solid #0B1F3A; border-radius: 2mm; padding: 5mm; margin-bottom: 4mm; }
.archetype .at-title { font-size: 12pt; font-weight: 700; color: #0B1F3A; margin-bottom: 2mm; }
.archetype .at-row { font-size: 9pt; margin-bottom: 1.5mm; color: #374151; }
.archetype .at-row b { color: #0B1F3A; }
.memo-box { border: 2px solid #0B1F3A; border-radius: 3mm; padding: 6mm; background: #F8F9FA; }
.memo-box .memo-decision { font-size: 16pt; font-weight: 700; color: #0B1F3A; margin-bottom: 3mm; }
.memo-box .memo-row { font-size: 9.5pt; margin-bottom: 2mm; line-height: 1.7; }
.memo-box .memo-row b { color: #0B1F3A; }
"""

def page(section, title, body, footer_source, page_id):
    return f"""<div class="page">
  <div class="header-bar"><div class="section-label">{esc(section)}</div><h2>{esc(title)}</h2></div>
  {body}
  <div class="footer"><span>{esc(footer_source)}</span><span>FDR-ZZ-FRIED-001 · V2.0 · P{page_id:02d}/42</span></div>
</div>"""

def data_card(ev):
    v = ev.get("value", "—")
    if isinstance(v, dict):
        parts = "  ".join(f"<b>{k}</b> {v2}" for k, v2 in v.items())
        inner = f'<div class="metric">{parts}</div>'
    else:
        inner = f'<div><span class="value">{esc(v)}</span></div>'
    return f'<div class="data-card">{inner}<div class="metric">{esc(ev.get("metric",""))}</div><div class="meta">Confidence: {esc(ev.get("confidence",""))} · {esc(ev.get("source",""))}</div></div>'

def impact(text):
    return f'<div class="impact-box"><div class="impact-label">IMPACT · 为什么这页和你有关</div>{esc(text)}</div>'

def table(headers, rows):
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="data-table"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'

E = R["evidence_layer"]
I = R["insight_layer"]
S = R["score_engine"]["score"]
BM = R["business_model_archetypes"]
pages = []

# P01 封面
pages.append(f"""<div class="page cover">
  <div class="section-label" style="color:#C4A35A;">FOODINTELAI · FDR 专业决策报告</div>
  <h1>{esc(R['report_metadata']['title'])}</h1>
  <div class="cover-sub">{esc(R['report_metadata']['subtitle'])}</div>
  <div class="cover-meta">
    报告编号：FDR-ZZ-FRIED-001 · V2.0<br>
    决策者画像：首次创业者 · 郑州 · 20万预算 · 无餐饮经验<br>
    数据基线：FID-001 郑州餐饮数据（2025H1 快照）2397家炸鸡门店<br>
    Ontology：Category Ontology V0.3（鲁棒性验证通过）<br>
    模型：FDE-V0.3 · 置信度 B<br>
    交付日期：2026-08-10
  </div>
</div>""")

# P02 核心结论
pages.append(page("PART 0 · EXECUTIVE SUMMARY", "核心结论：能不能做/为什么/怎么做",
f"""
<p class="subtitle">一句话：<b>条件进入。</b> 郑州炸鸡不是蓝海，但生炸生态仍有差异化进入窗口；直接与正新在西式裹粉价格带竞争不可取。</p>
{impact("市场存在（2397家），结构可解释（双工艺生态），但竞争已充分展开——需要差异化进入，不是发现空白市场。")}
{data_card(E['E002'])}
{data_card(E['E010'])}
<div class="evidence-chain">
  <div class="step"><span class="tag">L2</span>{esc(I['I001']['statement'])}</div>
  <div class="step"><span class="tag">L2</span>{esc(I['I004']['statement'])}</div>
  <div class="step"><span class="tag">L3</span>{esc(I['I005']['statement'])}</div>
</div>
""", "FID-001 · Ontology V0.3 · FDE-V0.3", 2))

# P03 决策评分
pages.append(page("PART 0 · EXECUTIVE SUMMARY", "决策评分总览",
f"""
<div class="score-card">
  <div class="score-item"><div class="label">INDUSTRY 行业机会</div><div class="num">{S['industry_score']}</div></div>
  <div class="score-item"><div class="label">PERSONAL 个人匹配</div><div class="num">{S['personal_match']}</div></div>
</div>
<div class="score-card">
  <div class="score-item hl"><div class="label">DECISION 综合评分</div><div class="num">{S['decision_score']}</div></div>
  <div class="score-item hl"><div class="label">RECOMMENDATION</div><div class="num">{S['recommendation']}</div></div>
</div>
<div class="impact-box"><div class="impact-label">为什么是 R2</div>行业 78 × 0.7 + 个人 70 × 0.3 = 76。行业机会真实但个人资源（无经验/20万）限制明显——条件进入，验证后决定。</div>
""", "FDE-V0.3 双评分模型", 3))

# P04-07 Decision State
pages.append(page("PART 1 · DECISION STATE", "决策者画像",
f"""
<table class="data-table"><tbody>
<tr><td><b>身份</b></td><td>{esc(R['decision_brief']['user_profile']['identity'])}</td><td><b>资金</b></td><td>{esc(R['decision_brief']['user_profile']['capital'])}</td></tr>
<tr><td><b>城市</b></td><td>郑州</td><td><b>品类</b></td><td>炸鸡</td></tr>
<tr><td><b>经验</b></td><td>{esc(R['decision_brief']['user_profile']['experience'])}</td><td><b>目标</b></td><td>{esc(R['decision_brief']['user_profile']['objective'])}</td></tr>
<tr><td><b>风险偏好</b></td><td>{esc(R['decision_brief']['constraint']['risk_preference'])}</td><td><b>限制</b></td><td>{esc(R['decision_brief']['constraint']['limitation'])}</td></tr>
</tbody></table>
{impact("你是'低风险验证型创业者'：无餐饮经验+20万预算 → 一切决策围绕'低成本验证现金流模型'展开，不赌重资产。")}
""", "FDR-INTAKE-001", 4))

pages.append(page("PART 1 · DECISION STATE", "决策状态与核心冲突",
f"""
<div class="data-card">
<div class="metric" style="font-size:12pt;"><b>Decision State：低风险验证型创业者</b></div>
<div style="margin-top:2mm;font-size:10pt;">
判断依据：<br>
• 缺乏餐饮运营经验 → 试错成本敏感<br>
• 初始资金 20 万有限 → 不适合重资产<br>
• 优先验证现金流模型 → 90天验证期<br><br>
<b style="color:#0B1F3A;">核心冲突：想进入成熟餐饮市场 VS 缺少品牌/供应链/运营优势</b>
</div>
</div>
{impact("本报告的决策框架：市场×用户→进入方式。不是'市场好所以推荐做'，而是'你的条件下，哪个结构值得进、以什么方式进'。")}
""", "FDR-INTAKE-001 · Decision Journey", 5))

pages.append(page("PART 1 · DECISION STATE", "本次分析范围",
f"""
<div class="data-card">
<div class="metric" style="font-size:11pt;"><b>本报告回答：</b></div>
<div style="margin-top:2mm;font-size:10pt;">
✓ 郑州炸鸡市场有多大、由什么组成（2397家 × 六轴）<br>
✓ 竞争结构：生炸 vs 裹粉两个生态如何不同（HHI）<br>
✓ 进入哪个结构、以什么方式进（5 个 Archetype）<br>
✓ 你的条件下建议与不建议（Decision Memo）<br><br>
<b>本报告不包含：</b><br>
✗ 保证盈利 / 经营预测（非经营承诺）<br>
✗ 加盟品牌推荐（不接商单）<br>
✗ 运营托管 / 供应链代采
</div>
</div>
{impact("范围边界就是专业边界——客户可以选择问题，但不能定义分析方法。")}
""", "FDR-CONTENT-001", 6))

pages.append(page("PART 1 · DECISION STATE", "研究方法与数据基线",
f"""
<div class="evidence-chain">
  <div class="step"><span class="tag">方法</span>2397家原始门店 → Category Ontology（六轴）→ 证据分级(A/B/C/D) → 机器初标 → 人工QC → 规则修正 → 交叉分析 → 商业簇</div>
  <div class="step"><span class="tag">数据</span>FID-001 郑州餐饮数据 · 2025H1 快照 · 108,350 条 POI 中识别炸鸡 2397 家</div>
  <div class="step"><span class="tag">Ontology</span>Category Ontology V0.3（2026-08-10 鲁棒性验证：V0.2→V0.3 簇结构稳定）</div>
  <div class="step"><span class="tag">纪律</span>宁可 Unknown 不造假精度；Data Observability ≠ Data Completeness</div>
</div>
""", "QTO-MAT-002 · QTO-PRO-002", 7))

# P07b 术语速查（沧林审稿 2026-08-10 建议）
pages.append(page("PART 1 · DECISION STATE", "术语速查（读报告前先看这页）",
f"""
<div class="data-card">
<div class="metric" style="font-size:11pt;"><b>HHI（赫芬达尔指数）</b></div>
<div style="margin-top:1mm;font-size:9.5pt;color:#374151;">衡量"集中度"的数值，范围 0-10000，越高代表越集中。<b>本报告用两种 HHI：</b><br>
• <b>结构 HHI</b>：衡量"产品/工艺细分簇"是否集中——值高说明市场收敛成少数几个清晰模型<br>
• <b>品牌 HHI</b>：衡量"具体品牌"是否集中——值高说明少数品牌主导<br>
两者可能一升一降（生炸：结构高品牌低；裹粉：结构低品牌高）——这正是本报告的核心发现。</div>
</div>
<div class="data-card">
<div class="metric" style="font-size:11pt;"><b>Confidence 置信度等级</b></div>
<div style="margin-top:1mm;font-size:9.5pt;color:#374151;">
• <b>A</b>：直接证据（菜品/菜单明确出现）<br>
• <b>B</b>：多字段组合证据<br>
• <b>C</b>：品牌/店名推断<br>
• <b>D</b>：无证据（Unknown，不猜测）</div>
</div>
<div class="data-card">
<div class="metric" style="font-size:11pt;"><b>推荐等级 R1-R3</b></div>
<div style="margin-top:1mm;font-size:9.5pt;color:#374151;">
• <b>R1</b>：建议进入<br>
• <b>R2</b>：条件进入（验证后决定）<br>
• <b>R3</b>：不建议/谨慎<br>
本报告结论为 <b>R2 条件进入</b>——不是"可以做"，是"可以验证地做"。</div>
</div>
{impact("术语不是门槛，是工具。看懂这三个概念，报告结论就不会误读。")}
""", "FDR-REPORT-001 · 术语定义", 8))

# P08-16 Market Landscape
pages.append(page("PART 2 · MARKET LANDSCAPE", "市场总览：2397家门店",
f"""
{data_card(E['E002'])}
<div style="display:flex;gap:4mm;">
<div style="flex:1;">{data_card({'metric': '区域覆盖', 'value': '12个区县全覆盖', 'confidence': 'B', 'source': 'FID-001'})}</div>
<div style="flex:1;">{data_card({'metric': '价格带覆盖', 'value': '67.8%', 'confidence': 'B', 'source': 'FID-001'})}</div>
<div style="flex:1;">{data_card({'metric': '品牌化程度', 'value': '12.3%', 'confidence': 'B', 'source': 'FID-001'})}</div>
</div>
<div class="impact-box"><div class="impact-label" style="color:#9F2F2D;">⚠ 阅读前风险提示（Unknown 率）</div>六轴标签中<b>风格 Unknown 44.8%、工艺 Unknown 49.5%</b>——公开 POI 数据对长尾小店的可观测性存在上限。这意味着：<b>长尾市场的实际水深可能比数据显示的更复杂</b>。报告结论基于可观测样本（风格55.2%/工艺50.5%），选址前必须实地验证目标区域，不能仅凭公开数据判断"这里店少就是空白"。</div>
{impact("市场规模明确（2397家），但整体品牌化程度低（12.3%）——结构上更像'长尾市场'，关键在长尾里是否有可进入的缝隙。")}
""", "FID-001", 8))

pages.append(page("PART 2 · MARKET LANDSCAPE", "价格带结构（10-20元为绝对主流）",
f"""
<table class="data-table">
<thead><tr><th>价格带</th><th>门店</th><th>占比</th></tr></thead>
<tbody>
<tr><td>10-15元</td><td>536</td><td>22.4%</td></tr>
<tr><td>15-20元</td><td>505</td><td>21.1%</td></tr>
<tr><td>20-30元</td><td>293</td><td>12.2%</td></tr>
<tr><td>&lt;10元</td><td>194</td><td>8.1%</td></tr>
<tr><td>30-50元</td><td>74</td><td>3.1%</td></tr>
<tr><td>50元以上</td><td>24</td><td>1.0%</td></tr>
<tr style="background:#F8F9FA;"><td><b>已识别小计</b></td><td><b>1,626</b></td><td><b>67.8%</b></td></tr>
<tr><td>Unknown</td><td>771</td><td>32.2%</td></tr>
</tbody></table>
<div class="impact-box"><div class="impact-label">决策含义</div>10-20元占 1,041 家（64%的已识别）——郑州炸鸡是低价高频消费。你的客单价策略必须锚定这个区间，除非进入韩式中高端（20-30元）差异化。已识别 1,626 家（67.8%）与顶部覆盖率一致。</div>
""", "FID-001", 9))

pages.append(page("PART 2 · MARKET LANDSCAPE", "区域分布（12区全覆盖）",
f"""
{data_card({'metric': '空间分布', 'value': {'金水区': '最密 214家', '新郑/中牟/二七/中原': '次密', '覆盖': '12个区县'}, 'confidence': 'B', 'source': 'FID-001'})}
<div class="impact-box"><div class="impact-label">决策含义</div>不是地理市场不同，而是商业定位不同——生炸和裹粉在同一空间里分层竞争（详见 Part 3）。</div>
""", "FID-001", 10))

pages.append(page("PART 2 · MARKET LANDSCAPE", "六轴标签覆盖（Ontology V0.3）",
f"""
{data_card(E['E009'])}
<div class="impact-box"><div class="impact-label">数据透明度</div>风格 Unknown 44.8% / 工艺 Unknown 49.5%——不是缺失，是公开平台数据对部分门店的可观测性上限。结论基于可观测部分，其余如实标注。</div>
""", "Category Ontology V0.3", 11))

pages.append(page("PART 2 · MARKET LANDSCAPE", "风格结构（单一风格分类不足以解释市场）",
f"""
<table class="data-table">
<thead><tr><th>风格</th><th>门店</th><th>占比</th><th>说明</th></tr></thead>
<tbody>
<tr><td>中式</td><td>683</td><td>28.5%</td><td>整鸡/鸡腿/鸡架全覆盖，价格全带</td></tr>
<tr><td>韩式</td><td>337</td><td>14.1%</td><td>鸡块/鸡翅，20-30元中高端</td></tr>
<tr><td>美式/西式</td><td>228</td><td>9.5%</td><td>整鸡/鸡排，10-15元快餐</td></tr>
<tr><td>地方特色</td><td>45</td><td>1.9%</td><td>老武汉/川味等</td></tr>
<tr><td>复合型</td><td>25</td><td>1.0%</td><td>融合/新派</td></tr>
<tr><td>日式/东南亚</td><td>6</td><td>0.3%</td><td>日式4/东南亚2</td></tr>
<tr style="background:#F8F9FA;"><td><b>已识别小计</b></td><td><b>1,324</b></td><td><b>55.2%</b></td><td>覆盖率口径</td></tr>
<tr><td>Unknown</td><td>1,073</td><td>44.8%</td><td>泛名小店（可观测性上限）</td></tr>
</tbody></table>
{impact("风格分类看着直观，但解释力有限——中式里从8元档口到30元专门店都有。真正的结构分水岭是产品×工艺。已识别1,324家（55.2%）与顶部覆盖率一致。")}
""", "Ontology V0.3", 12))

pages.append(page("PART 2 · MARKET LANDSCAPE", "产品结构（卖什么）",
f"""
<table class="data-table">
<thead><tr><th>产品</th><th>门店(Multi拆分)</th><th>主要价格带</th></tr></thead>
<tbody>
<tr><td>鸡块/鸡米花/鸡柳</td><td>752</td><td>15-20元</td></tr>
<tr><td>鸡腿</td><td>665</td><td>15-20元</td></tr>
<tr><td>整鸡/大单品</td><td>592</td><td>10-30元（全带）</td></tr>
<tr><td>鸡架/锁骨/叉骨</td><td>506</td><td>15-20元</td></tr>
<tr><td>鸡翅</td><td>476</td><td>10-30元</td></tr>
<tr><td>鸡排</td><td>420</td><td>10-15元</td></tr>
</tbody></table>
{impact("整鸡是最大产品带（覆盖全价格），鸡排锚定快餐价——产品决定价格逻辑。")}
""", "Ontology V0.3", 13))

pages.append(page("PART 2 · MARKET LANDSCAPE", "工艺结构（生炸 vs 裹粉）",
f"""
{data_card(E['E010'])}
<table class="data-table">
<thead><tr><th>工艺</th><th>门店</th><th>占比</th><th>说明</th></tr></thead>
<tbody>
<tr><td>裹粉炸</td><td>621</td><td>25.9%</td><td>西式/韩式主流工艺</td></tr>
<tr><td>生炸/现炸</td><td>401</td><td>16.7%</td><td>中式新势力主流工艺</td></tr>
<tr><td>卤炸</td><td>77</td><td>3.2%</td><td>延庆观系（本地特色）</td></tr>
<tr><td>烤炸复合</td><td>55</td><td>2.3%</td><td>烤鸡/烤炸</td></tr>
<tr><td>腌炸</td><td>45</td><td>1.9%</td><td>临榆等腌后炸</td></tr>
<tr><td>煸制/复炸</td><td>11</td><td>0.5%</td><td>煸鸡等</td></tr>
<tr style="background:#F8F9FA;"><td><b>已识别小计</b></td><td><b>1,210</b></td><td><b>50.5%</b></td><td>覆盖率口径</td></tr>
<tr><td>Unknown</td><td>1,187</td><td>49.5%</td><td>可观测性上限</td></tr>
</tbody></table>
{impact("这是全文最重要的结构发现：数量多的裹粉（621家）结构反而分散，数量少的生炸（401家）结构反而收敛。两种工艺是两套完全不同的商业生态。已识别1,210家（50.5%）与顶部覆盖率一致。")}
""", "Ontology V0.3 · 商业结构解释矩阵", 14))

pages.append(page("PART 2 · MARKET LANDSCAPE", "经营模型（怎么活）",
f"""
<table class="data-table">
<thead><tr><th>经营模型</th><th>门店</th><th>占比</th></tr></thead>
<tbody>
<tr><td>档口/摊位</td><td>519</td><td>21.7%</td></tr>
<tr><td>堂食+外卖+团购</td><td>440</td><td>18.4%</td></tr>
<tr><td>含外卖</td><td>361</td><td>15.1%</td></tr>
<tr><td>含团购</td><td>304</td><td>12.7%</td></tr>
<tr><td>外卖型</td><td>191</td><td>8.0%</td></tr>
</tbody></table>
{impact("档口是郑州炸鸡主形态（21.7%），外卖+团购双渠道已成标配（渗透率73%+68%）——新店必须同时设计档口与线上渠道。")}
""", "Ontology V0.3", 15))

pages.append(page("PART 2 · MARKET LANDSCAPE", "可观测市场份额",
f"""
{data_card({'metric': '可观测市场份额 (Observable Cluster Coverage)', 'value': '35.2% (843/2397)', 'confidence': 'B', 'source': 'Category Ontology V0.3'})}
<div class="impact-box"><div class="impact-label">专业边界</div>35.2% 形成显著簇（15个，≥25家），剩余 64.8% 不是'没有市场'，而是'当前数据无法形成足够确定的商业结构'。这个表达区分了可观测性和完整性——是 FoodIntelAI 的标准口径。</div>
""", "Category Ontology V0.3 · Rule 03", 16))

# P17-25 Competition Topology
pages.append(page("PART 3 · COMPETITION TOPOLOGY", "竞争拓扑总览：双工艺生态",
f"""
<div class="matrix2x2">
  <div class="matrix-cell hl"><div class="mc-title">生炸生态（401家）</div>
    <div class="mc-desc">结构收敛 HHI 2406<br>品牌分散 HHI 1302<br>价格锚点 15-20元<br>簇覆盖 78.1%<br>多品牌复制相似模型</div></div>
  <div class="matrix-cell"><div class="mc-title">裹粉生态（621家）</div>
    <div class="mc-desc">结构分散 HHI 1091<br>品牌集中 HHI 2442<br>价格锚点 10-15元<br>簇覆盖 60.9%<br>一强（正新）+长尾</div></div>
</div>
{impact("核心发现：品类集中 ≠ 品牌集中。生炸结构集中但品牌分散；裹粉结构分散但品牌集中——两套完全相反的市场逻辑。")}
""", "商业结构解释矩阵 V0.2", 17))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "生炸生态：多品牌复制相似模型",
f"""
<table class="data-table">
<thead><tr><th>生炸簇</th><th>规模</th><th>品牌占比</th><th>代表品牌</th></tr></thead>
<tbody>
<tr><td>中式整鸡·生炸</td><td>137</td><td>80%</td><td>叫了只39 / 刘婉婉23</td></tr>
<tr><td>中式鸡架·生炸</td><td>74</td><td>99%</td><td>御膳27 / 胡夫14</td></tr>
<tr><td>中式鸡腿·生炸</td><td>74</td><td>74%</td><td>爆掌柜19 / 满巍明11</td></tr>
</tbody></table>
<div class="impact-box"><div class="impact-label">推理链（谨慎表述）</div>结构收敛（HHI 2406）说明：这个赛道里多个品牌各自占有的份额相近、格局稳定——<b>通常意味着已有多个独立主体验证过基本可行性</b>。但结构稳定也可能源于各品牌占据了不同的地理/客群壁垒，彼此吃不掉对方。因此"收敛"≠"进入门槛低"≠"模式已验证可复制"——本报告据此判断"模型已被多品牌复制"，但复制成本与难度仍需实地验证。</div>
""", "Ontology V0.3", 18))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "裹粉生态：一强 + 长尾",
f"""
<table class="data-table">
<thead><tr><th>裹粉簇</th><th>规模</th><th>品牌占比</th><th>代表品牌</th></tr></thead>
<tbody>
<tr><td>西式整鸡·裹粉</td><td>82</td><td>62%</td><td>正新51（一家独大）</td></tr>
<tr><td>中式整鸡·裹粉</td><td>63</td><td>0%</td><td>全是无名小店</td></tr>
<tr><td>西式鸡排·裹粉</td><td>68</td><td>37%</td><td>正新25</td></tr>
<tr><td>韩式鸡块·裹粉</td><td>60</td><td>42%</td><td>黎太院15 / HanBang10</td></tr>
<tr><td>韩式鸡翅·裹粉</td><td>46</td><td>54%</td><td>熊家15 / 朴东杰8</td></tr>
</tbody></table>
{impact("裹粉的'结构分散' = 正新垄断 + 大量模仿者。是否处于'模型尚未充分收敛'的阶段——是假设，需时间序列验证。")}
""", "Ontology V0.3", 19))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "品类集中 vs 品牌集中：两个不同的问题",
f"""
<div class="matrix2x2">
  <div class="matrix-cell"><div class="mc-title">结构集中（HHI高）</div><div class="mc-desc">生炸 2406</div></div>
  <div class="matrix-cell"><div class="mc-title">结构分散（HHI低）</div><div class="mc-desc">裹粉 1091</div></div>
  <div class="matrix-cell"><div class="mc-title">品牌集中</div><div class="mc-desc">裹粉 2442（正新）</div></div>
  <div class="matrix-cell"><div class="mc-title">品牌分散</div><div class="mc-desc">生炸 1302</div></div>
</div>
{impact("生炸=结构收敛+品牌分散；裹粉=结构分散+品牌集中。传统行业报告把'集中度'当成一个指标，但这里它必须拆成两个——结构集中度和品牌集中度回答不同问题。")}
""", "商业结构解释矩阵 V0.2", 20))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "品牌生态位图谱",
f"""
{data_card(E['E012'])}
{impact("每个品牌占据完全不同的生态位，互不重叠——正新做西式快餐，延庆观做本地卤炸，满巍明做生炸鸡架，熊家做韩式芝士鸡翅。'炸鸡'这个词底下，是六种不同的生意。")}
""", "Ontology V0.3", 21))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "显著商业簇分布",
f"""
<table class="data-table">
<thead><tr><th>商业簇</th><th>门店</th><th>占比</th></tr></thead>
<tbody>
<tr><td>中式·整鸡/大单品·生炸/现炸</td><td>137</td><td>5.7%</td></tr>
<tr><td>美式/西式·整鸡/大单品·裹粉炸</td><td>82</td><td>3.4%</td></tr>
<tr><td>中式·鸡腿·生炸/现炸</td><td>74</td><td>3.1%</td></tr>
<tr><td>中式·鸡架/锁骨/叉骨·生炸/现炸</td><td>74</td><td>3.1%</td></tr>
<tr><td>美式/西式·鸡排·裹粉炸</td><td>68</td><td>2.8%</td></tr>
<tr><td>中式·整鸡/大单品·裹粉炸</td><td>63</td><td>2.6%</td></tr>
<tr><td>韩式·鸡块/鸡米花/鸡柳·裹粉炸</td><td>60</td><td>2.5%</td></tr>
<tr><td>中式·整鸡/大单品·Unknown</td><td>55</td><td>2.3%</td></tr>
<tr><td>韩式·鸡翅·裹粉炸</td><td>46</td><td>1.9%</td></tr>
<tr><td>中式·鸡腿·腌炸</td><td>38</td><td>1.6%</td></tr>
<tr><td>美式/西式·鸡翅·裹粉炸</td><td>33</td><td>1.4%</td></tr>
<tr><td>中式·整鸡/大单品·卤炸</td><td>32</td><td>1.3%</td></tr>
<tr><td>中式·鸡块/鸡米花/鸡柳·生炸/现炸</td><td>28</td><td>1.2%</td></tr>
<tr><td>中式·鸡腿·卤炸</td><td>27</td><td>1.1%</td></tr>
<tr><td>韩式·整鸡/大单品·裹粉炸</td><td>26</td><td>1.1%</td></tr>
<tr style="background:#F8F9FA;"><td><b>显著簇小计（15个，≥25家）</b></td><td><b>843</b></td><td><b>35.2%</b></td></tr>
</tbody></table>
{impact("15个显著簇覆盖 843 家（35.2%）。进入前先回答：你要进的是哪个簇？不同簇的产品、价格、品牌、竞争完全不同。")}
""", "Ontology V0.3", 22))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "竞争密度（空间）",
f"""
{data_card(E['E007'])}
{impact("最近邻中位 80m，90% 门店 500m 内有同行——扎堆型市场。选址规则：避开 500m 内已有 3 家+ 的区域。进入窗口在低密度节点，不是空白区域（门店少≠需求小）。")}
""", "FID-001 最近邻分析", 23))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "机会与压力并存：结构集中≠蓝海",
f"""
<div class="evidence-chain">
  <div class="step"><span class="tag">L3</span>{esc(I['I005']['statement'])}</div>
  <div class="step"><span class="tag">边界</span>低结构集中度 ≠ 进入容易：正新品牌壁垒明显（品牌HHI 2442）</div>
  <div class="step"><span class="tag">拆解</span>机会三拆：结构机会（空白） / 竞争机会（强对手） / 经营机会（能否赚钱）</div>
</div>
{impact("这篇报告的决策语言不是'蓝海'，而是'有需求验证、但需要差异化进入'。")}
""", "FDR-COMPETITION-001", 24))

pages.append(page("PART 3 · COMPETITION TOPOLOGY", "竞争拓扑结论：进入哪个生态",
f"""
<div class="data-card">
<div class="metric" style="font-size:12pt;"><b>竞争拓扑结论</b></div>
<div style="margin-top:2mm;font-size:10pt;">
• <b>生炸生态</b>：模型已验证（多品牌复制），竞争充分——可进入但必须差异化<br>
• <b>裹粉生态</b>：正新主导，长尾分散——正面竞争不现实，需找避开正新的产品空间<br>
• <b>韩式细分</b>：价格带独立（20-30元），竞争相对小——差异化候选<br>
• <b>卤炸细分</b>：延庆观一家独占32家——已验证但本地品牌壁垒高
</div>
</div>
{impact("进入哪个生态，比'要不要做炸鸡'更重要——这才是 Competition Topology 的价值。")}
""", "FDR-COMPETITION-001", 25))

# P26-31 Business Model
pages.append(page("PART 4 · BUSINESS MODEL", "商业模型 Archetype 总览",
f"""
<table class="data-table">
<thead><tr><th>Archetype</th><th>产品×工艺</th><th>价格带</th><th>模型</th><th>竞争</th><th>进入难度</th><th>是否进入候选打分</th></tr></thead>
<tbody>
<tr><td>BM-01</td><td>中式生炸·整鸡</td><td>20-30元</td><td>品牌化社区型</td><td>叫了只39/刘婉婉23</td><td>中（需差异化）</td><td>✅ 是</td></tr>
<tr><td>BM-02</td><td>中式生炸·鸡架</td><td>15-20元</td><td>低客单高频连锁</td><td>御膳27/胡夫14</td><td>高（品牌已成型）</td><td>❌ 否（进入壁垒过高）</td></tr>
<tr><td>BM-03</td><td>中式生炸·鸡腿</td><td>15-20元</td><td>品牌连锁</td><td>爆掌柜19/满巍明11</td><td>中</td><td>✅ 是</td></tr>
<tr><td>BM-04</td><td>西式裹粉·整鸡/鸡排</td><td>10-15元</td><td>快餐加盟</td><td>正新51（主导）</td><td>高（正面冲突）</td><td>✅ 是（用于对比论证）</td></tr>
<tr><td>BM-05</td><td>韩式裹粉·鸡块/鸡翅</td><td>20-30元</td><td>中高端年轻消费</td><td>黎太院15/熊家15</td><td>中低</td><td>✅ 是</td></tr>
</tbody></table>
<div class="impact-box"><div class="impact-label">筛选说明</div>BM-02（生炸鸡架）因进入壁垒过高——品牌格局已成型（99%品牌占比，御膳/胡夫主导）——未进入 Part 5 候选打分。其余 4 个 Archetype 进入最终对比。5 个 Archetype 是这份报告的产品层——不是"卖什么炸鸡"，而是"以什么模型做生意"。</div>
""", "商业结构解释矩阵 V0.2", 26))

bm_details = {
    "BM-01": ["中式生炸·整鸡", "20-30元", "外卖+团购", "品牌化社区型", "叫了只39 / 刘婉婉23（80%品牌）", "模型已收敛，需差异化进入；可做风味/渠道差异"],
    "BM-02": ["中式生炸·鸡架", "15-20元", "档口", "低客单高频品牌连锁", "御膳27 / 胡夫14（99%品牌）", "品牌格局已形成，进入门槛高——不建议正面"],
    "BM-03": ["中式生炸·鸡腿", "15-20元", "档口+外卖", "品牌连锁", "爆掌柜19 / 满巍明11", "本地新势力集中，可差异化（风味/区域）"],
    "BM-04": ["西式裹粉·整鸡/鸡排", "10-15元", "档口+外卖", "快餐加盟（正新主导）", "正新51（品牌HHI 2442）", "正面打正新不现实，需避开其产品空间"],
    "BM-05": ["韩式裹粉·鸡块/鸡翅", "20-30元", "堂食+外卖", "中高端/年轻消费", "黎太院15 / HanBang10 / 熊家15", "价格带独立，客群不同——差异化候选"],
}
for bid, bm in bm_details.items():
    pages.append(page("PART 4 · BUSINESS MODEL", f"{bid} · {bm[0]}",
    f"""
    <div class="archetype">
      <div class="at-title">{bid} · {esc(bm[0])}</div>
      <div class="at-row"><b>价格带：</b>{esc(bm[1])}</div>
      <div class="at-row"><b>渠道：</b>{esc(bm[2])}</div>
      <div class="at-row"><b>经营模型：</b>{esc(bm[3])}</div>
      <div class="at-row"><b>竞争格局：</b>{esc(bm[4])}</div>
      <div class="at-row"><b>进入建议：</b>{esc(bm[5])}</div>
    </div>
    {impact(f"Archetype {bid} 是{bm[0]}生意的完整画像——产品、价格、渠道、竞争、进入方式一体。")}
    """, "商业结构解释矩阵 V0.2", 26 + list(bm_details.keys()).index(bid) + 1))

# P32-36 Decision Engine
pages.append(page("PART 5 · DECISION ENGINE", "FDE 五维评分",
f"""
<table class="data-table">
<thead><tr><th>维度</th><th>权重</th><th>评分逻辑</th></tr></thead>
<tbody>
<tr><td>市场 Market</td><td>25%</td><td>2397家规模明确，10-20元主流</td></tr>
<tr><td>竞争 Competition</td><td>20%</td><td>双生态：生炸收敛/裹粉正新主导</td></tr>
<tr><td>运营 Operation</td><td>20%</td><td>档口+外卖模式成熟，20万可启动</td></tr>
<tr><td>资源匹配 Match</td><td>25%</td><td>无经验→轻资产验证型匹配</td></tr>
<tr><td>时机 Timing</td><td>10%</td><td>2025H1 快照，市场结构稳定</td></tr>
</tbody></table>
<div class="score-card"><div class="score-item hl"><div class="label">INDUSTRY SCORE</div><div class="num">{S['industry_score']}</div></div></div>
""", "FDE-V0.3", 32))

pages.append(page("PART 5 · DECISION ENGINE", "行业评分 vs 个人匹配",
f"""
<div class="score-card">
  <div class="score-item"><div class="label">INDUSTRY 行业机会</div><div class="num">{S['industry_score']}</div><div class="label">市场真实存在</div></div>
  <div class="score-item"><div class="label">PERSONAL 个人匹配</div><div class="num">{S['personal_match']}</div><div class="label">资源限制明显</div></div>
</div>
<div class="data-card">
<div class="metric" style="font-size:10pt;"><b>综合评分公式说明（FDE-V0.3）</b></div>
<div style="margin-top:1mm;font-size:9pt;color:#374151;line-height:1.8;">
综合评分 = 行业机会 × 0.7 + 个人匹配 × 0.3 = 78×0.7 + 70×0.3 = 76<br>
• 0.7/0.3 是 FDE-V0.3 对<b>低风险验证型创业者</b>画像的固定权重：行业机会权重更高，因为该画像的进入决策主要由"市场是否成立"驱动<br>
• 对"资源充足型"（资金雄厚/经验丰富）画像，权重会调整（个人匹配提升至 0.4-0.5）——同一模型，权重按画像分层<br>
• 本报告结论基于当前画像（首次创业者·20万·无经验），不同画像的 76 分不可直接横向比较<br><br>
<b style="color:#9F2F2D;">操作者技能门槛（已纳入个人匹配评估）</b>：生炸工艺对操作者技能依赖高（油温控制/火候判断/出餐一致性），无经验创业者该项为短板——个人匹配 70 分中已体现该约束。30 天工艺良率测试（≥90% 稳定出品）是该短板的第一道验证阀门。FDE V0.4 起，技能门槛将作为独立权重维度进入评分计算。
</div>
</div>
{impact("行业 78 ≠ 适合你。行业值得做≠你适合做——双评分模型把'市场'和'人'分开，这是决策系统与行业报告的分水岭。")}
""", "FDR-SCORE-002", 33))

pages.append(page("PART 5 · DECISION ENGINE", "备选路径对比（4条）",
f"""
{table(["方案", "行业机会", "个人匹配", "建议", "说明"],
  [[a["name"], a["industry_attractiveness"], a["user_fit"], a["recommendation"], a.get("note","")] for a in R["alternatives"]])}
{impact("自营社区小店·生炸整鸡（78/76 R2）是最优备选；加盟正新系受品牌壁垒压制（70/66 R3）。")}
""", "FDR-SCORE-002", 34))

pages.append(page("PART 5 · DECISION ENGINE", "Decision Trace：为什么推荐这个方向",
f"""
<div class="evidence-chain">
  <div class="step"><span class="tag">证据</span>生炸结构收敛（HHI 2406）+ 品牌分散（HHI 1302）→ 模型被多品牌验证，无绝对垄断</div>
  <div class="step"><span class="tag">证据</span>裹粉正新品牌壁垒明显（HHI 2442）→ 正面进入不现实</div>
  <div class="step"><span class="tag">匹配</span>20万+无经验 → 轻资产档口/外卖模式可行，重资产加盟不可行</div>
  <div class="step"><span class="tag">结论</span>推荐：中式生炸 × 整鸡/鸡腿 × 15-20/20-30元 → R2 条件进入</div>
</div>
{impact("每一步都有证据来源——Decision Trace 是可追溯的判断过程，不是'我觉得不错'。")}
""", "FDR-DECISION-SOURCE-001", 35))

pages.append(page("PART 5 · DECISION ENGINE", "综合决策评分",
f"""
<div class="score-card">
  <div class="score-item hl"><div class="label">DECISION SCORE</div><div class="num">{S['decision_score']}</div></div>
  <div class="score-item hl"><div class="label">RECOMMENDATION</div><div class="num">{S['recommendation']}</div></div>
</div>
<div class="impact-box"><div class="impact-label">R2 含义</div>条件进入（验证进入）——行业存在机会，但个人资源限制明显。90天验证期后决定复制或退出。这不是'可以做'，是'可以验证地做'。</div>
""", "FDE-V0.3", 36))

# P37-41 Risk & Action
pages.append(page("PART 6 · RISK & ACTION", "风险矩阵（4项）",
f"""
{table(["风险", "触发", "应对"],
  [[r["name"], r["trigger"], r["response"]] for r in R["risk_layer"]])}
{impact("每个风险都有触发条件和应对方案——不是'注意风险'，是可执行的预案。")}
""", "FDR-CONTENT-001", 37))

pages.append(page("PART 6 · RISK & ACTION", "机会与风险并存",
f"""
<div class="matrix2x2">
  <div class="matrix-cell hl"><div class="mc-title">机会</div>
    <div class="mc-desc">生炸产品模型已收敛且品牌分散——产品教育已完成，品牌格局未绝对垄断<br>韩式价格带独立（20-30元）竞争相对小</div></div>
  <div class="matrix-cell"><div class="mc-title">风险</div>
    <div class="mc-desc">生炸品牌竞争已充分展开——无差异化将被同质化<br>正新品牌壁垒——裹粉低价带难进<br>数据可观测性上限——部分区域需实地验证</div></div>
</div>
{impact("不是'蓝海'，是'有需求验证、但需要差异化进入'——这才是决策语言。")}
""", "FDR-COMPETITION-001", 38))

pages.append(page("PART 6 · RISK & ACTION", "30天验证动作",
f"""
<table class="data-table">
<thead><tr><th>周期</th><th>目标</th><th>任务</th></tr></thead>
<tbody>
<tr><td>Day 1-7</td><td>确定进入生态</td><td>生炸 vs 裹粉二选一（基于本文Part 3）</td></tr>
<tr><td>Day 8-15</td><td>产品测试</td><td>整鸡/鸡腿/鸡架 三款对比，选差异化产品</td></tr>
<tr><td>Day 8-15</td><td><b style="color:#9F2F2D;">工艺测试（新增·关键）</b></td><td><b>生炸工艺良率测试：标准包浆/腌制配方、油温控制曲线、出品一致性——连续 10 天记录良率，目标 ≥90% 稳定出品</b></td></tr>
<tr><td>Day 16-30</td><td>供应链测试</td><td>原料/腌制/油炸设备供应商验证</td></tr>
<tr><td>Day 16-30</td><td><b style="color:#9F2F2D;">技能门槛评估（新增）</b></td><td><b>生炸对操作者技能依赖高（油温/时间/火候判断）——评估自己/雇工能否稳定执行，或是否需半成品裹粉方案兜底</b></td></tr>
</tbody></table>
<div class="impact-box"><div class="impact-label">为什么必须有工艺测试</div>生炸的标准化难度远高于裹粉半成品炸货——它依赖操作者技能（油温控制、出餐效率、火候判断）。对"无餐饮经验"创业者，这是最容易死在出品不稳定上的环节。供应链能买到原料，但<b>技能买不到，只能验证</b>。</div>
{impact("30天不是'准备开店'，是'验证模型'——先证伪，再投入。工艺良率是生炸路线的第一道生死线。")}
""", "FDR-DELIVERY-001", 39))

pages.append(page("PART 6 · RISK & ACTION", "90天验证指标与停止条件",
f"""
{table(["指标", "目标", "停止条件"],
  [["日销量", "达到验证基线", "日均低于X单持续2周→退出"],
   ["毛利", "≥行业基准", "毛利持续低于Y%→退出"],
   ["复购", "≥Z%", "复购低→产品定位问题→调整或退出"],
   ["人效", "单人可运营", "需2人以上才能转→成本不可行"]] )}
<div class="impact-box"><div class="impact-label">决策系统标志</div>完整链 = Entry Condition → Validation Period（90天）→ Continue Condition → Stop Condition。'什么时候停止'比'什么时候进入'更能区分专业决策产品。</div>
""", "FDR-DECISION-GATE-001", 40))

pages.append(page("PART 6 · RISK & ACTION", "数据局限声明",
f"""
<div class="data-card">
<div class="metric" style="font-size:11pt;"><b>数据边界（如实声明）</b></div>
<div style="margin-top:2mm;font-size:9.5pt;line-height:1.8;">
• 数据为 2025H1 快照，非时间序列——不可推导增长趋势<br>
• 六轴标签 Unknown 率：风格 44.8% / 工艺 49.5%——公开数据可观测性上限<br>
• 无经营数据（生命周期/单店规模/闭店率）——结构收敛 ≠ 商业模式成熟<br>
• 品牌识别基于名称映射，存在误差<br>
• 本报告不构成投资/经营/开店建议
</div>
</div>
{impact("承认边界不是弱点——是数据可信度的基础。假精确比没有数字更糟。")}
""", "FDR-DATA-001 · DI-002", 41))

# P42 Decision Memo
memo = R["decision_memo"]
pages.append(page("PART 7 · DECISION MEMO", "最终决策",
f"""
<div class="memo-box">
  <div class="memo-decision">{esc(memo['decision'])}（{esc(S['recommendation'])}）</div>
  <div class="memo-row"><b>推荐方向：</b>{esc(memo['recommended_direction'])}</div>
  <div class="memo-row"><b>不建议：</b>{esc(memo['not_recommended'])}</div>
  <div class="memo-row"><b>核心理由：</b><br>{esc(memo['reasons'][0])}<br>{esc(memo['reasons'][1])}<br>{esc(memo['reasons'][2])}</div>
  <div class="memo-row"><b>成立条件：</b><br>{esc(memo['conditions'][0])}<br>{esc(memo['conditions'][1])}<br>{esc(memo['conditions'][2])}</div>
  <div class="memo-row"><b>最大风险：</b>{esc(memo['max_risk'])}</div>
  <div class="memo-row"><b>30天验证动作：</b>{esc(memo['action_30days'])}</div>
</div>
{impact("决策闭环：Entry → Validation → Continue → Stop。不做'视情况而定'——每条都有可执行条件。")}
""", "FDR-DECISION-GATE-001", 42))

# 组装 HTML
html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>FDR-ZZ-FRIED-001 V2.0</title>
<style>{CSS}</style></head><body>
{''.join(pages)}
</body></html>"""

with open(f"{OUT}/FDR-ZZ-FRIED-001_V2.0.html", "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"✅ HTML 生成: {OUT}/FDR-ZZ-FRIED-001_V2.0.html ({os.path.getsize(f'{OUT}/FDR-ZZ-FRIED-001_V2.0.html')} bytes)")
print(f"   页面数: {len(pages)}")
