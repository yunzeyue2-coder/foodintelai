#!/usr/bin/env python3
"""批量生成饮料V4产品卡 YL-004 ~ YL-006 (3款，测试批次)"""

import os

TPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>{name} · 沧林食品</title>
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
.section{{padding:14px 22px;border-bottom:1px solid #eee5d8}}
.s-title{{font-size:14px;font-weight:700;color:#3a322a;margin-bottom:10px;padding-bottom:4px;border-bottom:2px solid #f0ece6}}
.story{{font-size:13px;line-height:2;color:#5a4f44}}
.story em{{color:#C0392B;font-style:normal;font-weight:600}}
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
.benchmark{{padding:10px 14px;background:#f8f4ef;border-radius:8px;margin-top:6px}}
.benchmark .bn{{font-weight:600;color:#3a322a}}
.benchmark .bd{{font-size:11px;color:#7a7269;margin-top:2px}}
.talk{{background:#fef9f2;border-radius:8px;padding:10px 14px;margin-top:6px;font-size:12px;color:#5a4f44;line-height:1.8}}
.alert{{background:#fef2ee;border-left:3px solid #C0392B;padding:8px 12px;font-size:10px;color:#C0392B;margin-top:6px;border-radius:0 4px 4px 0}}
.paywall{{background:linear-gradient(135deg,#fdf2f2,#fef9ef);border:1.5px dashed #ddd4ca;border-radius:14px;padding:20px;margin:14px 22px;text-align:center}}
.paywall .price{{font-size:26px;font-weight:800;color:#C0392B}}
.paywall .desc{{font-size:11px;color:#7a7269;margin:4px 0 12px}}
.paywall .btn{{display:inline-block;background:#C0392B;color:#fff;padding:8px 28px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;transition:.2s}}
.paywall .btn:hover{{background:#a33025}}
</style>
</head>
<body>
<div class="card">
<div class="meta">
  <div class="badge">{badge}</div>
  <h1>{name}</h1>
  <div class="sub">{sub}</div>
  <div class="tags">{tags}</div>
</div>
<div class="level-banner">
  <span class="level-item high">{rec_level}</span>
  <span class="level-item">{stall_idx}</span>
  <span class="level-item">{repeat_idx}</span>
</div>
<div class="section">
  <div class="s-title">📖 产品说</div>
  <div class="story">{story}</div>
</div>
<div class="section">
  <div class="s-title">💰 成本利润</div>
  <div class="cost-box">
    <div class="row"><span>单杯成本</span><span class="v">{cost}</span></div>
    <div class="row"><span>建议售价</span><span class="v">{price}</span></div>
    <div class="row"><span>日销（出摊4h）</span><span class="v">{daily_sales}</span></div>
    <div class="row"><span>日营收</span><span class="v">{daily_rev}</span></div>
    <div class="row"><span>原料成本</span><span class="v">{daily_cost}</span></div>
    <div class="row"><span>摊位+杂费</span><span class="v">{overhead}</span></div>
    <div class="row tot"><span>日净赚</span><span class="v">{daily_profit}</span></div>
  </div>
  <div class="roi">
    <div class="roi-b c"><div class="d">{roi_c}</div>保守</div>
    <div class="roi-b n"><div class="d">{roi_n}</div>正常</div>
    <div class="roi-b i"><div class="d">{roi_i}</div>理想</div>
  </div>
</div>
<div class="section">
  <div class="s-title">⚠️ 项目风险</div>
  <div class="risk-item"><span>季节</span><div class="risk-stars">{risk_season}</div></div>
  <div class="risk-item"><span>损耗</span><div class="risk-stars">{risk_loss}</div></div>
  <div class="risk-item"><span>监管</span><div class="risk-stars">{risk_rule}</div></div>
  <div class="risk-item"><span>选址</span><div class="risk-stars">{risk_loc}</div></div>
</div>
<div class="section">
  <div class="s-title">🔧 启动清单</div>
  <div class="launch">{launch}</div>
</div>
<div class="section">
  <div class="s-title">📍 适合场景</div>
  <div class="scene-grid">{scenes}</div>
</div>
<div class="section">
  <div class="s-title">🎯 市场对标</div>
  <div class="benchmark">
    <div class="bn">{bench_name}</div>
    <div class="bd">{bench_desc}</div>
  </div>
</div>
<div class="section">
  <div class="s-title">💬 话术</div>
  <div class="talk">{talk}</div>
  <div class="alert">勿用「教你赚钱」「包你学会」等收割感话术</div>
</div>
<div class="section">
  <div class="s-title">📋 工艺流程</div>
  <div class="story">{process}</div>
</div>
<div class="section">
  <div class="s-title">🚫 避坑</div>
  <div class="story">{pitfalls}</div>
</div>
<div class="paywall">
  <div class="price">¥9.9</div>
  <div class="desc">{pay_desc}</div>
  <a class="btn" href="https://foodintelai.com">加微信 canglin1985 获取</a>
  <div class="up" style="font-size:10px;color:#b5aaa0;margin-top:8px">升级 ¥99 利润模型版 / ¥199 完整方案版</div>
</div>
</div>
</body>
</html>"""


def stars(n):
    on = '<span class="on">\u25cf</span>' * n
    off = '<span class="off">\u25cf</span>' * (5 - n)
    return on + off

def tag(*ts):
    return ''.join(f'<span>#{t}</span>' for t in ts)

def scene(*ss):
    return ''.join(f'<span class="scene-item">{s}</span>' for s in ss)

def launch(*ls):
    return ''.join(f'<span>{l}</span>' for l in ls)


def make_card(num, title, sub_s, tags_list, rec, stall, repeat, story_text, cost_s, price_s, ds_s, dr_s, dc_s, ov_s, dp_s, r_c, r_n, r_i, risks, launch_items, scenes_list, bench_n, bench_d, talk_text, proc_text, pit_text, pay_text):
    badge = f"YL_{num} \xb7 \u996e\u6599\u4e13\u533a"
    html = TPL.format(
        badge=badge, name=title, sub=sub_s,
        tags=tag(*tags_list),
        rec_level=rec, stall_idx=stall, repeat_idx=repeat,
        story=story_text,
        cost=cost_s, price=price_s,
        daily_sales=ds_s, daily_rev=dr_s, daily_cost=dc_s,
        overhead=ov_s, daily_profit=dp_s,
        roi_c=r_c, roi_n=r_n, roi_i=r_i,
        risk_season=stars(risks[0]), risk_loss=stars(risks[1]),
        risk_rule=stars(risks[2]), risk_loc=stars(risks[3]),
        launch=launch(*launch_items),
        scenes=scene(*scenes_list),
        bench_name=bench_n, bench_desc=bench_d,
        talk=talk_text, process=proc_text, pitfalls=pit_text,
        pay_desc=pay_text
    )
    fname = f"/Users/mac/Desktop/虾哥/网站部署/cards/YL_{num}.html"
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  OK YL_{num}.html")


# === 饮料数据 ===

CARDS = [
    ("004", "草莓小丸子", "冷饮700ml \xb7 草莓糯米丸子生椰",
     ["低投资","夜市","甜品饮品","Q弹"],
     "\U0001f525 热销推荐", "摆摊指数 7/10", "复购指数 8/10",
     "糯米丸子是这杯的点睛之笔。有次在学校门口试摊，<em>一个女生喝了一口就说丸子好好吃</em>，又回头买了两杯。草莓浆80ml配生椰乳120ml，椰香和莓香混在一起，底下还有水晶冻。成本6.29，卖14-16。<br><br>关键是糯米丸子要现煮，放久了会硬，出餐节奏要卡好。",
     "约\xa5\x36.29", "\xa5\x31\x34-\x31\x36/杯", "50-80杯", "\u2248\xa5\x37\x30\x30-\x31\x32\x38\x30", "\u2248\xa5\x33\x31\x35-\x35\x30\x33", "~\xa5\x35\x30-\x31\x30\x30", "\u2248\xa5\x33\x33\x35-\x36\x37\x37",
     "15-22天", "10-15天", "5-10天",
     (4,2,1,2),
     ["糯米小丸子","水晶冻","草莓浆","茉莉绿茶茶汤","冰糖糖浆","蜜制草莓","生椰乳","雪克杯"],
     ["夜市","学校周边","步行街","饮品摊","公园"],
     "某co草莓小丸子\xa5\x31\x36 vs 摆摊\xa5\x31\x34-\x31\x36/杯", "价格差不多但摆摊用料更扎实，丸子更多，草莓味更浓。",
     "\u300c杯底有糯糯的小丸子，嚼着嚼着就喝完一杯。\u300d",
     "\u2022 杯底加小丸子50g+水晶冻50g<br>\u2022 雪克杯加草莓浆80ml+茶汤80ml+冰糖糖浆10ml+蜜制草莓30g+冰块200g摇匀<br>\u2022 倒入杯中，加生椰乳120ml",
     "\u2022 <em>丸子煮过头</em>\u2014\u2014糯米丸子煮到浮起就捞，过了就烂<br>\u2022 <em>生椰乳直接加冰沙里</em>\u2014\u2014先倒果茶再淋生椰乳，分层才好看<br>\u2022 <em>水晶冻代替晶球</em>\u2014\u2014水晶冻更滑嫩，跟丸子搭",
     "解锁完整配方：糯米丸子煮制技巧 + 草莓生椰调配比例 + 分层手法 + 出餐SOP"),

    ("005", "草莓桃桃茶", "冷饮700ml \xb7 草莓水蜜桃双果茶",
     ["低投资","夜市","双果","夏日"],
     "\U0001f525 热销推荐", "摆摊指数 8/10", "复购指数 8/10",
     "草莓和水蜜桃\u2014\u2014这两个水果放在一起就是王炸。<em>成本6.9块，卖14-16，毛利拉到55%+</em>。关键是水蜜桃果蓉在杯底打底，草莓浆和茶汤雪克后倒进去，喝的时候能同时感受到两种果味。<br><br>出餐极快，雪克几下就搞定，高峰期一小时能出40杯。",
     "约\xa5\x36.9", "\xa5\x31\x34-\x31\x36/杯", "70-110杯", "\u2248\xa5\x39\x38\x30-\x31\x37\x36\x30", "\u2248\xa5\x34\x38\x33-\x37\x35\x39", "~\xa5\x36\x30-\x31\x32\x30", "\u2248\xa5\x34\x33\x37-\x38\x38\x31",
     "12-18天", "8-12天", "5-8天",
     (4,1,1,2),
     ["原味晶球","水蜜桃果蓉","草莓浆","茉莉绿茶茶汤","冰糖糖浆","蜜制草莓","雪克杯"],
     ["夜市","步行街","学校周边","饮品摊"],
     "某茶草莓桃桃\xa5\x32\x34 vs 摆摊\xa5\x31\x34-\x31\x36/杯", "品牌店贵在房租和营销，摆摊原料同级别，味道差不到哪去。",
     "\u300c草莓的酸甜和水蜜桃的香甜\u2014\u2014一杯喝出两种水果的快乐。\u300d",
     "\u2022 杯底加晶球80g+水蜜桃果蓉80g<br>\u2022 雪克杯加冰块200g+茶汤150ml+冰糖糖浆20ml+草莓浆40ml+蜜制草莓30g摇匀<br>\u2022 倒入杯中",
     "\u2022 <em>水蜜桃果蓉沉底不均</em>\u2014\u2014放杯底前先搅一搅<br>\u2022 <em>草莓浆不够</em>\u2014\u201440ml刚好，多了盖掉水蜜桃味<br>\u2022 <em>不加冰直接雪克</em>\u2014\u2014冰块200g是标配，少冰口感淡",
     "解锁完整配方：双果比例调配 + 晶球处理 + 雪克手法 + 打包方案"),

    ("006", "生椰可可冰茶", "冷饮500ml \xb7 巧克力生椰冰沙",
     ["低投资","创意饮品","甜品","夏日"],
     "\u2b50 特色推荐", "摆摊指数 6/10", "复购指数 7/10",
     "这杯是从广禧夏季菜单挖来的创意款。<em>杯壁抹巧克力酱，生椰乳打底，可可冰沙顶上，再插一根雪糕</em>\u2014\u2014一杯顶三样。成本12.7，卖18-22。适合摆在甜品摊或者炸鸡摊旁边做搭配。<br><br>雪糕成本占大头，可以找批发商拿整箱的，单支能压到3块左右。",
     "约\xa5\x31\x32.7", "\xa5\x31\x38-\x32\x32/杯", "40-60杯", "\u2248\xa5\x37\x32\x30-\x31\x33\x32\x30", "\u2248\xa5\x35\x30\x38-\x37\x36\x32", "~\xa5\x35\x30-\x31\x30\x30", "\u2248\xa5\x31\x36\x32-\x34\x35\x38",
     "20-30天", "15-20天", "8-12天",
     (3,3,1,2),
     ["巧克力酱","生椰乳","可可粉","冰糖糖浆","喷射奶油","雪糕","冰沙机","成品杯"],
     ["夜市","商场周边","游乐场","甜品摊"],
     "同类创意饮品店\xa5\x32\x38-\x33\x35 vs 摆摊\xa5\x31\x38-\x32\x32/杯", "雪糕成本高，但整杯视觉冲击强，适合发朋友圈拍照打卡。",
     "\u300c巧克力+生椰+雪糕，一杯下去三个满足。\u300d",
     "\u2022 杯壁抹巧克力酱，加生椰乳100ml<br>\u2022 冰沙机加生椰乳50ml+可可粉30ml+冰糖糖浆10ml+水50ml+冰块180g搅匀<br>\u2022 倒入杯中，挤奶油顶，插雪糕",
     "\u2022 <em>雪糕融化快</em>\u2014\u2014出餐前最后一刻才插雪糕<br>\u2022 <em>可可粉结块</em>\u2014\u2014先用少量热水化开可可粉再打冰沙<br>\u2022 <em>成本控制</em>\u2014\u2014雪糕批发比零售便宜一半",
     "解锁完整配方：可可冰沙调配 + 巧克力挂壁技巧 + 雪糕批发渠道 + 成本控制方案"),
]

base = "/Users/mac/Desktop/虾哥/网站部署/cards"
for c in CARDS:
    make_card(*c)
print(f"\n\u5171\u751f\u6210 {len(CARDS)} \u6b3e")
