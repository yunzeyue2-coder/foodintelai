#!/usr/bin/env python3
"""Generate 22 TS (糖水铺) product card HTML files."""

import json, os

OUT_DIR = "/Users/mac/Desktop/虾哥/网站部署/cards"

# Card mapping: (filename, badge_id, title, data_id)
CARDS = [
    ("TS_001.html", "TS-001", "冰糖水（玫瑰/茉莉白桃）", "CD-053"),
    ("TS_002.html", "TS-002", "草莓糖水（草莓酸奶冰沙）", "CD-090"),
    ("TS_003.html", "TS-003", "菠萝冰糖水", "CD-113"),
    ("TS_004.html", "TS-004", "菠萝糖水", "CD-117"),
    ("TS_005.html", "TS-005", "西瓜冰糖水", "CD-123"),
    ("TS_006.html", "TS-006", "红豆莲子百合糖水", "DT-005"),
    ("TS_007.html", "TS-007", "手工冰粉", "CD-072"),
    ("TS_008.html", "TS-008", "烧仙草冻", "CD-091"),
    ("TS_009.html", "TS-009", "烧仙草冻（深褐色）", "CD-121"),
    ("TS_010.html", "TS-010", "双皮奶", "CD-122"),
    ("TS_011.html", "TS-011", "夜市甜饮（桂花甜饮）", "YC-005"),
    ("TS_012.html", "TS-012", "海南灵魂甜品（椰奶清补凉）", "YC-008"),
    ("TS_013.html", "TS-013", "海底椰糖水", "CD-092"),
    ("TS_014.html", "TS-014", "藕粉（桂花藕粉）", "CD-095"),
    ("TS_015.html", "TS-015", "米酒小汤圆", "CD-098"),
    ("TS_016.html", "TS-016", "雪燕桃胶", "CD-103"),
    ("TS_017.html", "TS-017", "菠萝米酒", "CD-089"),
    ("TS_018.html", "TS-018", "芒果西柚糖水（杨枝甘露风）", "CD-083"),
    ("TS_019.html", "TS-019", "芋头芋圆椰奶", "CD-084"),
    ("TS_020.html", "TS-020", "椰奶西米露", "CD-104"),
    ("TS_021.html", "TS-021", "拉丝酸奶（原味/果味）", "CD-035"),
    ("TS_022.html", "TS-022", "炭烧拉丝酸奶", "CD-037"),
]

def load_data():
    with open("/Users/mac/Desktop/虾哥/h5工作站/data-det.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_story(entry):
    t_raw = entry.get("t", "")
    if not t_raw:
        return "夜市糖水摊上发现的宝藏，简单好喝，回头客特别多。"
    lines = [l.strip() for l in t_raw.strip().split("\n") if l.strip()]
    return " ".join(lines)

def get_q_tips(entry):
    q_raw = entry.get("q", "")
    tips = []
    if q_raw:
        parts = q_raw.replace("Q:", "⚠️ ").replace("A:", "").split("⚠️")
        for p in parts:
            p = p.strip()
            if p and len(p) > 3:
                p = p.replace("A:", "").strip()
                if p and len(p) > 3:
                    tips.append(p)
    if len(tips) < 4:
        fallbacks = [
            "糖水熬好彻底放凉再装瓶，热装易变质",
            "器具必须无油无水，否则保存期打折扣",
            "出摊时桶要用冰袋保温，天热不加冰3小时变味",
            "每天出摊前先试喝一杯，味道不对马上调整",
            "糖水定价6-10元最适合夜市消费",
        ]
        while len(tips) < 4:
            tips.append(fallbacks[len(tips) % len(fallbacks)])
    return tips[:6]

def build_cost(product_name):
    if "拉丝酸奶" in product_name or "炭烧" in product_name:
        return {"c": "2-3元/杯", "p": "8-12元", "m": "3-4元", "p60": "180元", "p80": "240元", "p120": "360元", "oh": "约800元", "eq": "约500元"}
    elif "雪燕" in product_name or "桃胶" in product_name:
        return {"c": "2-3元/杯", "p": "10-15元", "m": "3-4元", "p60": "180元", "p80": "240元", "p120": "360元", "oh": "约600元", "eq": "约600元"}
    elif any(k in product_name for k in ["椰子","海底椰","西米","椰奶","清补凉","芋圆","杨枝甘露","芒果西柚","芋头"]):
        return {"c": "2-3元/杯", "p": "8-12元", "m": "3-4元", "p60": "180元", "p80": "240元", "p120": "360元", "oh": "约600元", "eq": "约500元"}
    elif "烧仙草" in product_name or "冰粉" in product_name:
        return {"c": "1-1.5元/杯", "p": "6-8元", "m": "2-3元", "p60": "120元", "p80": "160元", "p120": "240元", "oh": "约400元", "eq": "约300元"}
    elif "双皮奶" in product_name:
        return {"c": "1-1.5元/杯", "p": "6-8元", "m": "2-3元", "p60": "120元", "p80": "160元", "p120": "240元", "oh": "约400元", "eq": "约400元"}
    else:
        return {"c": "1.5-2元/杯", "p": "6-10元", "m": "2-3元", "p60": "120元", "p80": "160元", "p120": "240元", "oh": "约500元", "eq": "约400元"}

def build_tags(product_name):
    tags = ["低投资", "一人可做", "出餐快"]
    if "冰粉" in product_name or "烧仙草" in product_name:
        tags += ["夏天爆款", "不用火"]
    elif "酸奶" in product_name:
        tags += ["健康", "女生最爱"]
    elif "雪燕" in product_name or "桃胶" in product_name:
        tags += ["养颜", "高客单"]
    elif "米酒" in product_name:
        tags += ["女生爱喝", "微醺"]
    elif "桂花" in product_name or "藕粉" in product_name:
        tags += ["传统味", "四季可卖"]
    else:
        tags += ["糖水", "解暑"]
    return tags[:5]

def build_risks(product_name):
    r = [
        ("天气影响", "★★★☆☆", "下雨天客流减半"),
        ("保存时间", "★★★☆☆", "糖水当天卖不完得倒"),
        ("口味竞争", "★★★☆☆", "一条街可能好几家糖水摊"),
    ]
    if "酸奶" in product_name:
        r.append(("发酵控制", "★★★☆☆", "温度不对拉丝效果打折扣"))
    else:
        r.append(("季节波动", "★★☆☆☆", "夏天好卖，冬天要配热饮"))
    return r

def build_scenes(product_name):
    base = ["夜市", "学校门口", "商业街", "美食广场", "公园", "步行街"]
    if "冰粉" in product_name or "烧仙草" in product_name:
        base += ["庙会", "景区"]
    elif "酸奶" in product_name:
        base += ["商场", "健身房"]
    elif "桂花" in product_name or "藕粉" in product_name:
        base += ["古镇", "早市"]
    else:
        base += ["地铁口", "小区门口"]
    return base[:8]

def build_comparisons(product_name):
    if "酸奶" in product_name:
        return [
            ("奶茶店酸奶杯", "品牌溢价", "奶茶店卖15起，你卖8-12"),
            ("超市盒装酸奶", "手工现做", "超市酸奶没拉丝口感"),
            ("甜品店冷饮", "性价比", "甜品店30一杯，你三分之一价"),
        ]
    elif "雪燕" in product_name or "桃胶" in product_name:
        return [
            ("奶茶店养生饮品", "真材实料", "奶茶店用粉冲，你用真雪燕"),
            ("超市速食糖水", "新鲜度", "罐装防腐剂多，没法比"),
            ("甜品店同类", "性价比", "甜品店一碗25起"),
        ]
    else:
        return [
            ("奶茶店饮品", "健康天然", "奶茶一杯15全是添加剂"),
            ("糖水铺同行", "新鲜现熬", "提前批量熬好，出餐快口感稳"),
            ("超市速食糖水", "现熬口感", "罐装跟现熬不是一回事"),
        ]

def build_sales_copy(product_name, data_id):
    lines = [
        f"「来杯{product_name}？现做的，比奶茶健康多了」",
        "「糖水都是我天天喝的，绝对干净放心」",
    ]
    kw = product_name
    if "冰糖水" in kw:
        lines.append("「玫瑰酱自己调的，茉莉白桃也是好牌子」")
    elif "草莓" in kw:
        lines.append("「草莓早上现买现洗的，一杯里全是果肉」")
    elif "菠萝" in kw:
        lines.append("「菠萝用盐水泡过再煮，不麻嘴」")
    elif "西瓜" in kw:
        lines.append("「西瓜现切的，不是隔夜的」")
    elif "红豆" in kw or "莲子" in kw:
        lines.append("「红豆煮了两个小时才起沙，功夫活」")
    elif "冰粉" in kw:
        lines.append("「冰粉手搓的，不是粉冲的，口感不一样」")
    elif "烧仙草" in kw:
        lines.append("「料给得足，芋圆红豆珍珠都有」")
    elif "双皮奶" in kw:
        lines.append("「奶皮子看得见，不是吉利丁粉兑的」")
    elif "桂花" in kw:
        lines.append("「桂花是新货，香得很」")
    elif "清补凉" in kw:
        lines.append("「椰奶自己调的，椰浆放得足」")
    elif "海底椰" in kw:
        lines.append("「海底椰泡了三个小时再熬的」")
    elif "藕粉" in kw:
        lines.append("「藕粉冲到这个浓度不容易」")
    elif "米酒" in kw and "小汤圆" in kw:
        lines.append("「米酒用孝感神霖的，小汤圆糯得很」")
    elif "雪燕" in kw or "桃胶" in kw:
        lines.append("「雪燕泡八小时桃胶泡一晚，都是真料」")
    elif "芒果" in kw and "西柚" in kw:
        lines.append("「芒果打成泥跟椰浆调的，西柚粒现剥的」")
    elif "芋头" in kw or "芋圆" in kw:
        lines.append("「芋头荔浦的，粉糯，芋圆自己搓的」")
    elif "西米露" in kw:
        lines.append("「西米煮到透明，椰奶调的，夏天喝最爽」")
    elif "拉丝酸奶" in kw or "炭烧" in kw:
        lines.append("「看这拉丝——菌种好发酵时间够才有的效果」")
    else:
        lines.append("「糖水当天熬的，卖不完自己喝」")
    lines.append("「加杯酸梅汤？两杯一起买便宜两块钱」")
    return lines

def build_page(card_id, product_name, data_id, entry):
    story = build_story(entry)
    q_tips = get_q_tips(entry)
    cost = build_cost(product_name)
    tags = build_tags(product_name)
    risks = build_risks(product_name)
    scenes = build_scenes(product_name)
    comparisons = build_comparisons(product_name)
    sales_copy = build_sales_copy(product_name, data_id)

    # Tags HTML
    tags_html = "\n    ".join(f'<span>{t}</span>' for t in tags)

    # Risk items
    risk_rows = ""
    for r_name, r_stars, r_desc in risks:
        stars = "".join(f'<span class="on">★</span>' if c == "★" else f'<span class="off">☆</span>' for c in r_stars)
        risk_rows += f"""  <div class="risk-item">
    <span>{r_name}</span>
    <span class="risk-stars">{stars}</span>
    <span style="font-size:10px;color:#b5aaa0;margin-left:auto">{r_desc}</span>
  </div>
"""

    # Scenes
    scenes_html = "\n    ".join(f'<span class="scene-item">{s}</span>' for s in scenes)

    # Pairs (same for all)
    pairs_html = """    <div class="dpair-item"><div class="name">烤肠</div><div class="price">3元/根</div></div>
    <div class="dpair-item"><div class="name">炸串</div><div class="price">5-8元/份</div></div>
    <div class="dpair-item"><div class="name">凉粉</div><div class="price">5元/份</div></div>
    <div class="dpair-item"><div class="name">酸梅汤</div><div class="price">5元/杯</div></div>
"""

    # Comparisons
    comps_html = ""
    for c_name, c_tag, c_desc in comparisons:
        comps_html += f'    <div class="comp-item"><span>{c_name}</span><span class="tag adv">{c_tag}</span><span style="font-size:10px;color:#b5aaa0">{c_desc}</span></div>\n'

    # Sales copy
    copy_html = ""
    for line in sales_copy:
        copy_html += f"    {line}<br>\n"

    # Tips
    tips_html = ""
    for tip in q_tips:
        tips_html += f'  <div class="tip-item">⚠️ {tip}</div>\n'

    # Equipment 
    equip_cost = cost["eq"]
    equip_items = {
        "CD-035": ["商用酸奶机43℃ ¥800", "冷藏柜 ¥1200", "分装杯 0.5元/个"],
        "CD-037": ["商用酸奶机43℃ ¥800", "冷藏柜 ¥1200", "分装杯 0.5元/个"],
        "CD-053": ["不锈钢锅 ¥80", "密封罐 ¥30", "冷藏箱 ¥200", "折叠桌 ¥80"],
        "CD-072": ["搓冰粉盆 ¥30", "纱布 ¥10", "碗 ¥40", "冷藏箱 ¥200"],
        "CD-122": ["模具 ¥50", "冰箱（家用可）¥0", "蒸锅 ¥60"],
    }
    equip_list = equip_items.get(data_id, ["不锈钢锅 ¥80", "密封罐 ¥30", "冷藏箱 ¥200", "折叠桌 ¥80"])
    equip_html = "\n    ".join(f'<span>{item}</span>' for item in equip_list)

    # Cost section
    cost_html = f"""  <div class="cost-box">
    <div class="row"><span>卖价</span><span class="v">{cost["p"]}/杯</span></div>
    <div class="row"><span>成本（原料）</span><span class="v">{cost["c"]}</span></div>
    <div class="row"><span>单杯利润</span><span class="v" style="color:#C0392B">{cost["m"]}</span></div>
    <div class="row"><span>日销60杯日利润</span><span class="v">{cost["p60"]}</span></div>
    <div class="row"><span>日销80杯日利润</span><span class="v">{cost["p80"]}</span></div>
    <div class="row"><span>月固定开销</span><span class="v">{cost["oh"]}</span></div>
    <div class="row tot"><span>设备投入</span><span class="v">{equip_cost}</span></div>
  </div>
  <div style="font-size:12px;font-weight:700;color:#3a322a;margin-top:6px">回本周期</div>
  <div class="roi">
    <div class="roi-b c"><div>保守</div><div class="d">5天</div><div>日销60杯</div></div>
    <div class="roi-b n"><div>正常</div><div class="d">3天</div><div>日销80杯</div></div>
    <div class="roi-b i"><div>理想</div><div class="d">2天</div><div>日销120杯</div></div>
  </div>"""

    pay_items = [
        "完整配方（精确到克的配比）",
        "原料采购清单（品牌规格写清楚）",
        "制作流程图（步骤拆解，新手照做）",
        "保存方法（卖不完怎么存不变味）",
        "三档利润算清（日销60/80/120杯）",
        "摆摊出餐SOP（高峰期不手忙脚乱）",
    ]
    pay_list_html = "\n".join(f"    <li>{item}</li>" for item in pay_items)

    # Story - use as-is from t field
    story_clean = story

    h = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>{card_id} {product_name} · 糖水铺</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:#f0e9e2;color:#2c2c2c;padding:24px 16px;line-height:1.7}}
.card{{max-width:540px;margin:0 auto;background:#faf8f5;border-radius:18px;overflow:hidden;box-shadow:0 2px 20px rgba(0,0,0,.05)}}

.meta{{padding:20px 22px 14px;background:#fdf8f0;border-bottom:1px solid #eee5d8}}
.meta .badge{{display:inline-block;font-size:10px;font-weight:700;color:#C0392B;background:#fef2ee;padding:2px 10px;border-radius:4px;margin-bottom:6px}}
.meta h1{{font-size:20px;font-weight:700;color:#3a322a;line-height:1.3;margin-bottom:2px}}
.meta .sub{{font-size:12px;color:#b5aaa0;margin-bottom:10px}}
.meta .tags{{display:flex;gap:4px;flex-wrap:wrap}}
.meta .tags span{{font-size:10px;padding:2px 10px;background:#f5ede5;border-radius:12px;color:#5a4f44}}

.level-banner{{display:flex;gap:8px;padding:10px 22px;background:#fef9f2;border-bottom:1px solid #eee5d8;flex-wrap:wrap}}
.level-item{{font-size:11px;padding:3px 10px;border-radius:6px;background:#f0e9e2;color:#5a4f44}}
.level-item.high{{background:#C0392B;color:#fff}}
.level-item.med{{background:#E8D5B0;color:#5a4f44}}

.section{{padding:14px 22px;border-bottom:1px solid #eee5d8}}
.s-title{{font-size:14px;font-weight:700;color:#3a322a;margin-bottom:10px;padding-bottom:4px;border-bottom:2px solid #f0ece6}}
.story{{font-size:13px;line-height:2;color:#5a4f44}}
.story em{{color:#C0392B;font-style:normal;font-weight:600}}

.index-grid{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}
.index-item{{background:#f8f4ef;border-radius:8px;padding:8px 10px;text-align:center}}
.index-item .label{{font-size:9px;color:#b5aaa0}}
.index-item .num{{font-size:13px;font-weight:700;color:#C0392B}}
.index-item .desc{{font-size:9px;color:#7a7269;margin-top:2px}}

.cost-box{{padding:12px 14px;background:#f8f4ef;border-radius:10px;margin-bottom:8px}}
.row{{display:flex;justify-content:space-between;font-size:13px;padding:4px 0;color:#3a322a}}
.row .v{{font-weight:600}}
.row.tot{{border-top:1px solid #ddd4ca;margin-top:4px;padding-top:8px;font-weight:700;color:#C0392B}}
.roi{{display:flex;gap:6px;margin-top:8px}}
.roi-b{{flex:1;padding:8px;border-radius:8px;text-align:center;font-size:11px}}
.roi-b .d{{font-size:15px;font-weight:700;margin:2px 0}}
.roi-b.c{{background:#fdf2ee;color:#E8652D}}
.roi-b.n{{background:#fef6ec;color:#D4A574}}
.roi-b.i{{background:#f0f6ec;color:#5a8f3c}}

.risk-item{{display:flex;gap:8px;padding:5px 0;font-size:12px;color:#5a4f44}}
.risk-stars{{display:flex;gap:2px;margin-left:auto;flex-shrink:0;font-size:10px}}
.risk-stars .on{{color:#D4A574}}
.risk-stars .off{{color:#ddd}}

.launch{{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}}
.launch span{{padding:5px 10px;background:#f8f4ef;border-radius:6px;font-size:11px;color:#5a4f44}}

.scene-grid{{display:flex;flex-wrap:wrap;gap:6px}}
.scene-item{{padding:5px 12px;background:#f0f6ec;color:#4a7a3c;border-radius:6px;font-size:11px;font-weight:600}}

.dpair{{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}}
.dpair-item{{flex:1;min-width:140px;padding:8px 10px;background:#f8f4ef;border-radius:8px;text-align:center}}
.dpair-item .name{{font-size:12px;font-weight:600;color:#3a322a}}
.dpair-item .price{{font-size:10px;color:#b5aaa0;margin-top:2px}}

.comp{{display:flex;flex-direction:column;gap:6px}}
.comp-item{{display:flex;gap:8px;font-size:12px;color:#5a4f44;padding:5px 8px;background:#f8f4ef;border-radius:6px}}
.comp-item .tag{{font-size:9px;padding:1px 6px;border-radius:3px;margin-left:auto;flex-shrink:0}}
.comp-item .tag.adv{{background:#f0f6ec;color:#5a8f3c}}

.copy-box{{padding:10px 14px;background:#f8f4ef;border-radius:8px;font-size:12px;color:#5a4f44;line-height:1.8;margin-top:6px}}
.copy-box em{{color:#C0392B;font-style:normal}}

.tip-item{{display:flex;gap:8px;padding:5px 0;font-size:12px;color:#5a4f44}}

.pay{{padding:20px 22px;background:linear-gradient(180deg,#fdf8f0,#f5ede5)}}
.pay .lock-icon{{font-size:28px;text-align:center;margin-bottom:4px}}
.pay h3{{font-size:15px;font-weight:700;text-align:center;color:#3a322a;margin-bottom:8px}}
.pay ul{{list-style:none;padding:0;margin-bottom:10px}}
.pay ul li{{font-size:12px;color:#5a4f44;padding:4px 0 4px 16px;position:relative;line-height:1.6}}
.pay ul li::before{{content:"\\2713";position:absolute;left:0;color:#5a8f3c;font-weight:700}}
.pay .price-tag{{font-size:18px;font-weight:700;color:#C0392B;text-align:center;margin:10px 0 8px}}
.pay .price-tag small{{font-size:12px;font-weight:400;color:#b5aaa0}}
.pay .btn{{display:block;text-align:center;padding:11px;background:#C0392B;color:#fff;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;margin-top:12px}}
.pay .note{{font-size:10px;color:#b5aaa0;text-align:center;margin-top:6px}}

.ftr{{text-align:center;padding:16px 22px;font-size:10px;color:#bbb}}
</style>
</head>
<body>
<div class="card">

<div class="meta">
  <div class="badge">{card_id} · ¥39</div>
  <h1>{card_id} {product_name}</h1>
  <div class="sub">糖水铺 · 摆摊 ✅ 夜市 ✅ 流动 ✅</div>
  <div class="tags">
    {tags_html}
  </div>
</div>

<div class="level-banner">
  <span class="level-item high">推荐 ★★★★★</span>
  <span class="level-item med">新手可做</span>
  <span class="level-item med">回本快</span>
  <span class="level-item med">利润稳</span>
</div>

<div class="section">
  <div class="s-title">发现这款产品</div>
  <div class="story">
    {story_clean}
  </div>
</div>

<div class="section">
  <div class="s-title">项目指数</div>
  <div class="index-grid">
    <div class="index-item"><div class="label">轻资产</div><div class="num">★★★★★</div><div class="desc">投入约{equip_cost}</div></div>
    <div class="index-item"><div class="label">难度</div><div class="num">★★☆☆☆</div><div class="desc">3天上手</div></div>
    <div class="index-item"><div class="label">利润</div><div class="num">★★★★☆</div><div class="desc">利润率充足</div></div>
    <div class="index-item"><div class="label">复购</div><div class="num">★★★★☆</div><div class="desc">夏天天天想喝</div></div>
  </div>
</div>

<div class="section">
  <div class="s-title">成本利润</div>
  {cost_html}
</div>

<div class="section">
  <div class="s-title">项目风险</div>
{risk_rows}</div>

<div class="section">
  <div class="s-title">启动清单</div>
  <div class="launch">
    {equip_html}
  </div>
  <div style="display:flex;gap:12px;margin-top:8px;font-size:11px;color:#5a4f44">
    <span><strong>总投入：</strong>{equip_cost}</span>
    <span><strong>占地：</strong>1.5m摊位</span>
    <span><strong>人员：</strong>1人可做</span>
    <span><strong>上手：</strong>3天</span>
  </div>
</div>

<div class="section">
  <div class="s-title">适合场景</div>
  <div class="scene-grid">
    {scenes_html}
  </div>
</div>

<div class="section">
  <div class="s-title">搭配销售</div>
  <div class="dpair">
{pairs_html}  </div>
  <div style="font-size:11px;color:#7a7269;margin-top:6px">搭烤肠炸串最稳，糖水解腻，客单价从6-10拉到15+</div>
</div>

<div class="section">
  <div class="s-title">对标项目 & 竞争优势</div>
  <div class="comp">
{comps_html}  </div>
</div>

<div class="section">
  <div class="s-title">销售话术</div>
  <div class="copy-box">
{copy_html}  </div>
</div>

<div class="section">
  <div class="s-title">避坑指南</div>
{tips_html}</div>

<div class="pay">
  <div class="lock-icon">🔒</div>
  <h3>¥39 解锁完整方案</h3>
  <ul>
{pay_list_html}
  </ul>
  <div class="price-tag">¥39 <small>一次付费，永久查看</small></div>
  <a class="btn" href="#wechatSection" onclick="window.parent.scrollToWechat && window.parent.scrollToWechat()">📱 加微信购买</a>
  <div class="note">付款后微信发送完整文件</div>
</div>

<div class="ftr">糖水铺 · 摆摊创业决策系统</div>
</div>
</body>
</html>"""
    return h


def main():
    data = load_data()
    for fname, card_id, product_name, data_id in CARDS:
        entry = data.get(data_id, {})
        if not entry:
            print(f"WARNING: {data_id} not found in data!")
            entry = {"t": "", "q": "", "f": [], "s": [], "v": "", "st": ""}
        html = build_page(card_id, product_name, data_id, entry)
        filepath = os.path.join(OUT_DIR, fname)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ {fname}")

if __name__ == "__main__":
    main()
