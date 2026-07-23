#!/usr/bin/env python3
"""批量生成 Frameworks 详情页"""
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

pages = [
    # (filename, code, name, subtitle, category, version, evidence, definition, why, scope, limit, method, related)
    
    ("FIP-001_系统原则", "FIP-001", "系统原则", "FOODINTELAI PRINCIPLES · SYSTEM", "研究原则", "V1.0", "宪章级",
     "产业不是孤立现象，而是由消费者、需求、场景、渠道、产品、技术、供应链、产业格局构成的八链因果系统。任何单一环节的变化都会通过因果链传导至其他环节。研究不能停留在局部现象，必须放在系统里理解。",
     "食品行业的大量分析停留在品类规模多大的局部描述层面，缺乏对产业运行机制的整体理解。系统原则要求研究者始终追问：这个现象在整条因果链的哪个位置？",
     "所有食品产业研究的第一原则。任何品类分析开始前，先定位它在八链因果链中的位置。",
     "系统原则是分析框架，不是预测工具。它帮助理解结构，不提供时间维度的精确预测。",
     "分析一个产业现象时，先在八链中找到它的位置，再沿因果链追溯上游或推演下游。",
     '<a href="FIS-001_食品产业系统模型.html" class="rt">FIS-001</a> <a href="FIF-001_七维产业决策框架.html" class="rt">FIF-001</a>'),

    ("FIP-002_因果原则", "FIP-002", "因果原则", "FOODINTELAI PRINCIPLES · CAUSALITY", "研究原则", "V1.0", "宪章级",
     "不描述表象，寻找为什么发生、为什么成功、为什么失败。建立现象到原因到规律到模型的完整分析路径。",
     "食品行业大量内容停留在是什么层面。因果原则要求穿透到为什么。",
     "适用于所有深度产业研究。是FoodIntelAI区别于普通行业报道的核心原则。",
     "因果链推演不能跳过缺失的中间环节。没有数据支撑的因果推断需标注为假设。",
     "每完成一个现象描述后，追问三次为什么。第三次追问往往触及产业底层逻辑。",
     '<a href="FIP-001_系统原则.html" class="rt">FIP-001</a>'),

    ("FIP-003_消费者优先原则", "FIP-003", "消费者优先原则", "FOODINTELAI PRINCIPLES · CONSUMER FIRST", "研究原则", "V1.0", "宪章级",
     "所有产业变化的起点是消费者需求变化。技术、供应链、渠道变化都是结果，不是原因。",
     "食品行业容易被技术叙事带偏。真正驱动变化的不是技术，而是消费者需求变了。",
     "适用于消费者端品类分析。在分析任何产业变化时，先问：消费者的什么需求变了？",
     "不适用于纯B2B领域，这类领域的需求链需要单独建立模型。",
     "看到一个技术变化时，向上追溯：是哪一环的消费者需求变化导致了它？",
     '<a href="FIS-001_食品产业系统模型.html" class="rt">FIS-001</a>'),

    ("FIP-004_证据原则", "FIP-004", "证据原则", "FOODINTELAI PRINCIPLES · EVIDENCE", "研究原则", "V1.0", "宪章级",
     "所有判断必须区分事实、判断和假设。三级信息不得作为核心结论依据。",
     "大量信息混杂在一起。证据原则要求研究者始终标注：这句话是事实、判断还是假设？",
     "适用于所有FoodIntelAI输出的内容。是内容生产的底线标准。",
     "证据分级只约束FoodIntelAI内部研究，不约束引用外部观点。",
     "每写一句断言，问自己：这是事实（有来源）、判断（基于事实的分析）还是假设？",
     '<a href="FIE-A_高可信事实.html" class="rt">FIE-A</a> <a href="FIE-B_可信参考信息.html" class="rt">FIE-B</a>'),

    ("FIP-005_边界原则", "FIP-005", "边界原则", "FOODINTELAI PRINCIPLES · BOUNDARY", "研究原则", "V1.0", "宪章级",
     "每一个框架都有适用范围和边界条件。任何分析模型不能超出其验证过的品类和场景。跨品类应用需重新验证。",
     "一个模型在卤味验证了，不等于在小吃也适用。边界原则要求研究者始终清楚框架的适用范围。",
     "适用于所有框架的使用和引用。每个框架的首页必须标注已验证的品类和场景。",
     "边界原则不限制框架的跨品类迁移，但要求迁移后重新验证。",
     "在使用任何框架前，先确认它在什么品类验证过。",
     '<a href="FIM-003_多模型并列分析法.html" class="rt">FIM-003</a>'),

    ("FIF-002_全国化分析框架", "FIF-002", "全国化分析框架", "FOODINTELAI FRAMEWORK · NATIONAL SCALE", "分析框架", "V1.0", "已验证",
     "五变量决定一个品类能否全国化：供应链成熟度、标准化深度、消费认知统一性、场景一致性、组织复制能力。",
     "大量食品企业把供应链标准化等同于可以全国化，忽略消费认知的地域壁垒。",
     "适用于食品品类全国化分析。已验证：早餐、卤味。",
     "不适用于非食品零售连锁。不适用于高端餐饮的稀缺性模式。",
     "五变量逐一评分，有一项低于阈值即说明存在结构性障碍。",
     '<a href="FIF-001_七维产业决策框架.html" class="rt">FIF-001</a>'),

    ("FIF-003_品类定位框架", "FIF-003", "品类定位框架", "FOODINTELAI FRAMEWORK · POSITIONING", "分析框架", "V0.9", "优化中",
     "产品、渠道、场景、供应链四维定位。一个品类在特定位置竞争。",
     "把赛道当作整体分析忽略内部不同定位的竞争逻辑差异。",
     "适用于品类内部分析。帮助定位品类竞争的真实位置。",
     "四维定位是分析框架，不是决策框架。",
     "对任意品类先定义四维坐标，不同坐标位置的竞争逻辑分别讨论。",
     '<a href="FIS-002_五世界分类模型.html" class="rt">FIS-002</a>'),

    ("FIF-004_商业模式分析框架", "FIF-004", "商业模式分析框架", "FOODINTELAI FRAMEWORK · BUSINESS MODEL", "分析框架", "V1.0", "早餐验证",
     "手艺/流程/供应链/品牌/平台五种经营模型，各有各的天花板和杠杆。",
     "卖手艺的钱、卖流程的钱、卖供应链的钱，赚钱逻辑完全不同。",
     "适用于小餐饮及食品创业项目的商业模式归类。",
     "五种模型不是优劣排序，每种模型都有成立的场景。",
     "先确定项目属于哪种模型，不同模型用不同评估标准。",
     '<a href="FIS-004_老板自由度模型.html" class="rt">FIS-004</a>'),

    ("FIF-005_价值链分析框架", "FIF-005", "价值链分析框架", "FOODINTELAI FRAMEWORK · VALUE CHAIN", "分析框架", "V0.9", "定型中",
     "从原料到消费者，利润在哪个环节产生、在哪个环节消耗。",
     "利润分配由价值链结构决定，不是由品牌决定。",
     "适用于产业链中上游分析和利润分配研究。",
     "需要可获取的产业链价格数据，数据不透明时精度下降。",
     "画出从原料到消费者的完整链路，标注每个环节的利润率。",
     '<a href="FIS-001_食品产业系统模型.html" class="rt">FIS-001</a>'),

    ("FIS-001_食品产业系统模型", "FIS-001", "食品产业系统模型", "FOODINTELAI SYSTEM · EIGHT CHAINS", "系统模型", "V1.2", "基础模型",
     "八链因果模型：消费者到需求到场景到渠道到产品到技术到供应链到产业格局。方向不可逆。",
     "没有系统模型时易把相关关系误认为因果关系。",
     "适用于所有品类研究的底层框架。",
     "八链是单向因果链，不可逆推。",
     "先定位研究问题在八链中的位置，再沿链追溯或推演。",
     '<a href="FIP-001_系统原则.html" class="rt">FIP-001</a>'),

    ("FIS-002_五世界分类模型", "FIS-002", "五世界分类模型", "FOODINTELAI SYSTEM · FIVE WORLDS", "系统模型", "V1.0", "已验证",
     "休闲、佐餐、地方、餐饮、工业。同一品类内部不同世界竞争逻辑完全不同。",
     "品类内部包含多个竞争逻辑截然不同的子市场。",
     "适用于内部结构复杂的食品品类。已验证：卤味。",
     "五世界不是固定分类，迁移时需重新定义。",
     "先对品类进行内部分类，再分别分析每个世界。",
     '<a href="FIF-003_品类定位框架.html" class="rt">FIF-003</a>'),

    ("FIS-003_品类生命周期模型", "FIS-003", "品类生命周期模型", "FOODINTELAI SYSTEM · LIFECYCLE", "系统模型", "V1.0", "已验证",
     "导入、成长、成熟、分化、重构。每个阶段的关键变量和竞争焦点不同。",
     "同一品类在不同阶段的进入策略完全不同。",
     "适用于品类层面的阶段判断和创业方向评估。",
     "生命周期不是预测工具，品类可能在同一阶段停留多年。",
     "收集增速、进入者数量、价格趋势等数据综合判断阶段。",
     '<a href="FIF-001_七维产业决策框架.html" class="rt">FIF-001</a>'),

    ("FIS-004_老板自由度模型", "FIS-004", "老板自由度模型", "FOODINTELAI SYSTEM · BOSS FREEDOM", "系统模型", "V1.0", "早餐验证",
     "生产自由度、管理自由度、复制自由度。三个指标判断一家店能否脱离老板独立运转。",
     "大多数分析忽略最根本的问题：老板不在时这家店还能不能赚钱？",
     "适用于小餐饮独立门店的经营模型评估。早餐验证。",
     "老板本人就是品牌核心资产的高端餐饮不适用。",
     "三个指标都指向低的模型就是被老板锁死的模型。",
     '<a href="FIF-004_商业模式分析框架.html" class="rt">FIF-004</a>'),

    ("FIS-005_压力测试与脆弱性分析", "FIS-005", "压力测试与脆弱性分析", "FOODINTELAI SYSTEM · STRESS TEST", "系统模型", "V0.9", "定型中",
     "外部冲击、内部缺陷、极端情景。不只研究为什么成功，也研究为什么可能失败。",
     "传统商业分析只看增长路径，很少问在什么情况下会崩溃。",
     "适用于任何商业模型的完整性评估。",
     "不能量化失败概率，只能揭示脆弱点。",
     "列出三种外部冲击和三种内部缺陷，模拟发生后的结果。",
     '<a href="FIF-001_七维产业决策框架.html" class="rt">FIF-001</a>'),

    ("FIM-001_八步研究法", "FIM-001", "八步研究法", "FOODINTELAI METHOD · 8-STEP RESEARCH", "研究方法", "V1.0", "核心流程",
     "锁定框架、宏观资料、聚焦单篇、审结构、中微观资料、检查对比、写作、审核。数据缺口表先行。",
     "写作前不做充分研究是早期最大的教训。八步法强制先研究后动笔。",
     "适用于所有正式研究文章的生产流程。",
     "不适用于快速反应类内容。",
     "写作前必须完成前五步，未完成数据采集不得进入写作阶段。",
     '<a href="FIM-004_数据交叉验证法.html" class="rt">FIM-004</a>'),

    ("FIM-002_第一性原理分析", "FIM-002", "第一性原理分析", "FOODINTELAI METHOD · FIRST PRINCIPLES", "研究方法", "V1.0", "核心方法",
     "回归产业最基本的物理约束和经济学规律，从零开始推导品类的结构性天花板。",
     "打破行业共识，回到最基本的事实。",
     "适用于创新型品类分析或需要打破既有认知框架的场景。",
     "耗时较长，不适合日常快速分析。",
     "问三个问题：物理上限是什么？最有效率的模型是什么？现有玩家接近上限了吗？",
     '<a href="FIP-001_系统原则.html" class="rt">FIP-001</a>'),

    ("FIM-003_多模型并列分析法", "FIM-003", "多模型并列分析法", "FOODINTELAI METHOD · MULTI-MODEL", "研究方法", "V1.0", "核心方法",
     "任何食品品类不能用单一模型解释。按品类区域规模分别建立模型并列分析。",
     "把早餐当作一个整体来分析是最大的错误。",
     "适用于所有品类分析，是FoodIntelAI的默认方法。",
     "每个模型的分析结论都有边界条件，不能绝对化。",
     "分析时先列出至少三种经营模型，分别分析后再对比。",
     '<a href="FIP-005_边界原则.html" class="rt">FIP-005</a>'),

    ("FIM-004_数据交叉验证法", "FIM-004", "数据交叉验证法", "FOODINTELAI METHOD · CROSS-VERIFY", "研究方法", "V1.0", "核心方法",
     "任何重要数据需要至少两个独立来源验证。无法验证的数据标记为待验证信息。",
     "单一来源数据往往带有目的性，交叉验证是防范数据风险的核心手段。",
     "适用于所有涉及具体数据的分析场景。",
     "多来源冲突时使用区间表述并标注差异。",
     "每个数据点记录来源、采集时间和置信度。",
     '<a href="FIP-004_证据原则.html" class="rt">FIP-004</a>'),

    ("FIM-005_认知重构写作法", "FIM-005", "认知重构写作法", "FOODINTELAI METHOD · COGNITIVE WRITING", "研究方法", "V1.0", "核心方法",
     "重建读者的认知坐标系：反常识事实、拆解表象、揭示矛盾、提出新框架、留下开放问题。",
     "认知重构的阅读体验更强烈，传播性更好。",
     "适用于面向公众的深度分析文章。",
     "不适用于技术白皮书或内部研究笔记。",
     "开篇用一个反常识事实打破读者既有认知，再逐步建立新框架。",
     '<a href="FIM-001_八步研究法.html" class="rt">FIM-001</a>'),

    ("FIE-A_高可信事实", "FIE-A", "高可信事实", "FOODINTELAI EVIDENCE · LEVEL A", "证据体系", "V1.0", "可引用",
     "官方公开数据、上市公司公告、权威机构报告、可验证经营数据。可作为核心结论依据。",
     "A级证据是研究的基础。只有A级数据可以直接用于核心判断。",
     "适用于所有深度研究文章的核心论据引用。",
     "A级不等于100%准确，需关注数据采集时间和口径差异。",
     "使用A级数据时标注来源机构、报告名称和采集时间。",
     '<a href="FIM-004_数据交叉验证法.html" class="rt">FIM-004</a>'),

    ("FIE-B_可信参考信息", "FIE-B", "可信参考信息", "FOODINTELAI EVIDENCE · LEVEL B", "证据体系", "V1.0", "可引用",
     "企业公开信息、行业访谈、专业媒体报道。可作为辅助论据需标注来源。",
     "行业洞察来自访谈和媒体，但缺乏验证路径。B级允许使用但限制用途。",
     "适用于趋势描述、案例背景等非核心论证部分。",
     "不能单独作为核心结论的依据。",
     "引用时标注来源并注明据XX报道。",
     '<a href="FIE-A_高可信事实.html" class="rt">FIE-A</a>'),

    ("FIE-C_待验证信息", "FIE-C", "待验证信息", "FOODINTELAI EVIDENCE · LEVEL C", "证据体系", "V1.0", "有条件使用",
     "企业宣传数据、市场传言、单一来源观点。不得直接作为核心结论依据。",
     "C级信息风险最高，使用不当直接损害可信度。",
     "仅用于信息收集阶段或方向性讨论。",
     "在文章中必须显式标注待验证。",
     "如果只有C级信息支撑，宁可不写这个判断。",
     '<a href="FIE-B_可信参考信息.html" class="rt">FIE-B</a>'),

    ("FIE-D_行业经验判断", "FIE-D", "行业经验判断", "FOODINTELAI EVIDENCE · LEVEL D", "证据体系", "V1.0", "谨慎使用",
     "基于从业经验的定性判断，无公开数据支撑。用于方向性分析需注明行业经验。",
     "大量有价值的洞察来自从业者经验，但经验不等于事实。",
     "适用于方向判断、趋势感知等非精确论证场景。",
     "不能用于财务分析、市场规模估算等需要精确数据的场景。",
     "使用D级信息时在文中注明据行业经验。",
     '<a href="FIE-C_待验证信息.html" class="rt">FIE-C</a>'),
]

template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{code} {name} · FoodIntelAI</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#f7f5f0;font-family:'Inter','Noto Serif SC','PingFang SC','Microsoft YaHei',serif;color:#2a2218;display:flex;justify-content:center;-webkit-font-smoothing:antialiased}}
.page{{max-width:800px;width:100%;padding:48px 40px 60px}}
.meta-bar{{display:flex;gap:14px;margin-bottom:24px;flex-wrap:wrap}}
.meta-bar .mb-item{{font-size:11px;color:#8a7a6a;padding:4px 12px;border:1px solid #e0ddd5;border-radius:6px}}
.meta-bar .mb-item strong{{color:#8b6914}}
h1{{font-size:26px;font-weight:700;color:#1a1a1a;margin-bottom:4px}}
.sub-c{{font-size:11px;color:#c4a35a;letter-spacing:3px;margin-bottom:20px;padding-bottom:16px;border-bottom:2px solid #e0ddd5}}
.field{{margin-bottom:28px}}
.field .fl{{font-size:11px;color:#8b6914;font-weight:600;letter-spacing:2px;margin-bottom:4px;padding-bottom:4px;border-bottom:1px solid #f0ece4}}
.field .fb{{font-size:14px;color:#3a322a;line-height:1.9}}
.field .fb ul{{margin:4px 0 4px 18px}}
.field .fb ul li{{font-size:13px;color:#555;line-height:1.8}}
.rel-tags{{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}}
.rel-tags .rt{{font-size:11px;padding:4px 14px;border-radius:14px;background:#f5f0e8;color:#6a5a3a;text-decoration:none}}
hr{{border:none;border-top:1px solid #e0ddd5;margin:32px 0}}
.footer{{background:linear-gradient(135deg,#faf8f5,#f5f0e8);border:1px solid #e8e3db;border-radius:12px;padding:24px;text-align:center;margin-top:40px}}
.footer .f1{{font-size:15px;font-weight:700;color:#8b6914;letter-spacing:2px}}
@media(max-width:640px){{.page{{padding:28px 16px 40px}}h1{{font-size:22px}}}}
</style>
</head>
<body>
<div class="page">
<div class="meta-bar">
<span class="mb-item"><strong>{code}</strong></span>
<span class="mb-item">{category}</span>
<span class="mb-item"><strong>版本</strong> {version}</span>
<span class="mb-item"><strong>证据</strong> {evidence}</span>
</div>
<h1>{name}</h1>
<div class="sub-c">{subtitle}</div>
<div class="field"><div class="fl">DEFINITION</div><div class="fb">{definition}</div></div>
<div class="field"><div class="fl">WHY</div><div class="fb">{why}</div></div>
<div class="field"><div class="fl">SCOPE</div><div class="fb">{scope}</div></div>
<div class="field"><div class="fl">LIMITATION</div><div class="fb">{limit}</div></div>
<div class="field"><div class="fl">METHOD</div><div class="fb">{method}</div></div>
<div class="field"><div class="fl">RELATED · 关联框架</div>
<div class="rel-tags">{related}</div></div>
<div class="field"><div class="fl">USED IN · 应用于</div>
<div class="rel-tags">
<a href="../research/早餐系列_价格带锁死商业模式.html" class="rt">早餐价格带模型</a>
<a href="../research/早餐系列_包子为什么不是蜜雪.html" class="rt">包子vs蜜雪</a>
<a href="../research/早餐系列_老板隐形成本.html" class="rt">老板自由度</a>
</div></div>
<div class="field"><div class="fl">ASSET INFO · 资产信息</div>
<div class="fb" style="font-size:12px;color:#888">
<table style="width:100%;border-collapse:collapse;font-size:12px;margin-top:6px">
<tr><td style="padding:4px 8px;border:1px solid #eee;color:#888">Asset ID</td><td style="padding:4px 8px;border:1px solid #eee;color:#2a2218">{code}</td>
<td style="padding:4px 8px;border:1px solid #eee;color:#888">版本</td><td style="padding:4px 8px;border:1px solid #eee;color:#2a2218">{version}</td></tr>
<tr><td style="padding:4px 8px;border:1px solid #eee;color:#888">分类</td><td style="padding:4px 8px;border:1px solid #eee;color:#2a2218">{category}</td>
<td style="padding:4px 8px;border:1px solid #eee;color:#888">更新</td><td style="padding:4px 8px;border:1px solid #eee;color:#2a2218">2026.07.23</td></tr>
<tr><td style="padding:4px 8px;border:1px solid #eee;color:#888">证据</td><td style="padding:4px 8px;border:1px solid #eee;color:#2a5a3a">{evidence}</td>
<td style="padding:4px 8px;border:1px solid #eee;color:#888">可见性</td><td style="padding:4px 8px;border:1px solid #eee;color:#2a2218">公开 · 可引用</td></tr>
</table>
</div></div>
<hr>
<div style="text-align:center;font-size:12px;margin-top:20px"><a href="index.html" style="color:#8b6914;text-decoration:none">返回 Frameworks</a></div>
<div class="footer"><div class="f1">FoodIntelAI 研究方法体系</div></div>
</div></body></html>
'''

for fname, code, name, subtitle, category, version, evidence, definition, why, scope, limit, method, related in pages:
    path = os.path.join(base_dir, f"{fname}.html")
    content = template.format(code=code, name=name, subtitle=subtitle, category=category,
                              version=version, evidence=evidence, definition=definition,
                              why=why, scope=scope, limit=limit, method=method, related=related)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  {code} {name}")

print(f"\n共生成 {len(pages)} 个框架详情页")
