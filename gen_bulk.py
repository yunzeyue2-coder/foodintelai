#!/usr/bin/env python3
"""
批量生成饮料V4产品卡的生成器和数据。
用法：python3 gen_bulk.py <start> <end>
例如：python3 gen_bulk.py 1 20  生成YL_001到YL_020
"""

import sys, json, os

# ===== 模板 =====
def get_template():
    with open("/Users/mac/Desktop/虾哥/网站部署/cards/YL_001.html", "r", encoding="utf-8") as f:
        tpl = f.read()
    start = tpl.find("<style>")
    end = tpl.find("</style>") + len("</style>")
    css = tpl[start:end]
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>__NAME__ · 沧林食品</title>
{css}
</head>
<body>
<div class="card">
<div class="meta">
  <div class="badge">__BADGE__</div>
  <h1>__NAME__</h1>
  <div class="sub">__SUB__</div>
  <div class="tags">__TAGS__</div>
</div>
<div class="level-banner">
  <span class="level-item high">__REC__</span>
  <span class="level-item">__STALL__</span>
  <span class="level-item">__REPEAT__</span>
</div>
<div class="section">
  <div class="s-title">📖 产品说</div>
  <div class="story">__STORY__</div>
</div>
<div class="section">
  <div class="s-title">💰 成本利润</div>
  <div class="cost-box">
    <div class="row"><span>单杯成本</span><span class="v">__COST__</span></div>
    <div class="row"><span>建议售价</span><span class="v">__PRICE__</span></div>
    <div class="row"><span>日销（出摊4h）</span><span class="v">__DS__</span></div>
    <div class="row"><span>日营收</span><span class="v">__DR__</span></div>
    <div class="row"><span>原料成本</span><span class="v">__DC__</span></div>
    <div class="row"><span>摊位+杂费</span><span class="v">__OV__</span></div>
    <div class="row tot"><span>日净赚</span><span class="v">__DP__</span></div>
  </div>
  <div class="roi">
    <div class="roi-b c"><div class="d">__RC__</div>保守</div>
    <div class="roi-b n"><div class="d">__RN__</div>正常</div>
    <div class="roi-b i"><div class="d">__RI__</div>理想</div>
  </div>
</div>
<div class="section">
  <div class="s-title">⚠️ 项目风险</div>
  __RISK__
</div>
<div class="section">
  <div class="s-title">🔧 启动清单</div>
  <div class="launch">__LAUNCH__</div>
</div>
<div class="section">
  <div class="s-title">📍 适合场景</div>
  <div class="scene-grid">__SCENES__</div>
</div>
<div class="section">
  <div class="s-title">🎯 市场对标</div>
  <div class="benchmark">
    <div class="bn">__BN__</div>
    <div class="bd">__BD__</div>
  </div>
</div>
<div class="section">
  <div class="s-title">💬 话术</div>
  <div class="talk">__TALK__</div>
  <div class="alert">勿用「教你赚钱」「包你学会」等收割感话术</div>
</div>
<div class="section">
  <div class="s-title">📋 工艺流程</div>
  <div class="story">__PROC__</div>
</div>
<div class="section">
  <div class="s-title">🚫 避坑</div>
  <div class="story">__PIT__</div>
</div>
<div class="paywall">
  <div class="price">¥9.9</div>
  <div class="desc">__PAY__</div>
  <a class="btn" href="https://foodintelai.com">加微信 canglin1985 获取</a>
  <div class="up" style="font-size:10px;color:#b5aaa0;margin-top:8px">升级 ¥99 利润模型版 / ¥199 完整方案版</div>
</div>
</div>
</body>
</html>'''

PAGE_TPL = None

def stars(n):
    on = '<span class="on">●</span>' * n
    off = '<span class="off">●</span>' * (5 - n)
    return on + off

def make_card(num, d):
    global PAGE_TPL
    if PAGE_TPL is None:
        PAGE_TPL = get_template()
    
    html = PAGE_TPL
    html = html.replace("__BADGE__", f"YL_{num} · 饮料专区")
    html = html.replace("__NAME__", d["n"])
    html = html.replace("__SUB__", d["s"])
    html = html.replace("__TAGS__", ''.join(f'<span>#{t}</span>' for t in d["tg"]))
    html = html.replace("__REC__", d["rec"])
    html = html.replace("__STALL__", d["stall"])
    html = html.replace("__REPEAT__", d["rep"])
    html = html.replace("__STORY__", d["story"])
    html = html.replace("__COST__", d["cost"])
    html = html.replace("__PRICE__", d["price"])
    html = html.replace("__DS__", d["ds"])
    html = html.replace("__DR__", d["dr"])
    html = html.replace("__DC__", d["dc"])
    html = html.replace("__OV__", d["ov"])
    html = html.replace("__DP__", d["dp"])
    html = html.replace("__RC__", d["rc"])
    html = html.replace("__RN__", d["rn"])
    html = html.replace("__RI__", d["ri"])
    
    rk = d["rk"]
    risk = (
        f'<div class="risk-item"><span>季节</span><div class="risk-stars">{stars(rk[0])}</div></div>\n'
        f'  <div class="risk-item"><span>损耗</span><div class="risk-stars">{stars(rk[1])}</div></div>\n'
        f'  <div class="risk-item"><span>监管</span><div class="risk-stars">{stars(rk[2])}</div></div>\n'
        f'  <div class="risk-item"><span>选址</span><div class="risk-stars">{stars(rk[3])}</div></div>'
    )
    html = html.replace("__RISK__", risk)
    html = html.replace("__LAUNCH__", ''.join(f'<span>{l}</span>' for l in d["ln"]))
    html = html.replace("__SCENES__", ''.join(f'<span class="scene-item">{s}</span>' for s in d["scenes"]))
    html = html.replace("__BN__", d["bn"])
    html = html.replace("__BD__", d["bd"])
    html = html.replace("__TALK__", d["talk"])
    html = html.replace("__PROC__", d["proc"])
    html = html.replace("__PIT__", d["pit"])
    html = html.replace("__PAY__", d["pay"])
    
    fname = f"/Users/mac/Desktop/虾哥/网站部署/cards/YL_{num}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    return f"YL_{num}.html"

# ===== 全部59款饮料数据 =====
ALL_DRINKS = {
    "001": {"n":"芝芝莓莓","s":"冷饮700ml · 草莓晶球芝士奶盖","tg":["低投资","夜市爆款","饮品","夏日"],"rec":"🔥 热销推荐","stall":"摆摊指数 8/10","rep":"复购指数 8/10","story":"夜市步行街的饮品摊最怕什么？不是口味不行，是没亮点。芝芝莓莓这杯，<em>杯底晶球+草莓颗粒+草莓冰沙+芝士奶盖</em>四层，看着就想买。草莓浆80ml加茉莉绿茶茶汤，成本6.6块，卖14-16块，毛利妥妥50%+。<br><br>关键是奶盖那层——咸香芝士顶配上酸甜草莓冰沙，第一口就上头。","cost":"约¥6.6","price":"¥14-16/杯","ds":"60-100杯","dr":"≈¥840-1600","dc":"≈¥396-660","ov":"~¥60-120","dp":"≈¥384-820","rc":"18-25天","rn":"12-18天","ri":"7-12天","rk":[4,1,1,2],"ln":["原味晶球","蜜制草莓","冷冻草莓浆","茉莉绿茶茶汤","冰糖糖浆","芝士奶盖","雪克杯","冰沙机","成品杯"],"scenes":["夜市","步行街","学校周边","饮品摊","商场"],"bn":"某茶芝芝莓莓¥28 vs 摆摊¥14-16/杯","bd":"品牌店靠空间溢价，摆摊靠走量。用料一样，少个店面钱，价格打对折还有得赚。","talk":"「四层口感——晶球嚼着、草莓香着、冰沙喝着、奶盖咸着，一杯四种体验。」","proc":"• 杯底加晶球50g、蜜制草莓30g<br>• 冰沙杯加冰块200g+草莓浆80ml+茶汤100ml+冰糖糖浆25ml打碎<br>• 倒入杯中，顶部加芝士奶盖2cm<br>• 装饰用新鲜草莓半颗","pit":"• <em>奶盖太薄</em>——至少2cm厚才有视觉冲击<br>• <em>草莓浆不够</em>——80ml是底线，少了莓味出不来<br>• <em>冰沙太稀</em>——冰块200g打出来的冰沙才挂杯<br>• <em>晶球提前放</em>——晶球现放现卖，泡久了会变软","pay":"解锁完整配方：草莓浆调配比例 + 芝士奶盖秘方 + 晶球处理技巧 + 打包方案"},
    "002": {"n":"莓莓奶冻","s":"冷饮700ml · 草莓双皮奶冻奶油顶","tg":["低投资","甜品饮品","夏日","高颜值"],"rec":"🔥 热销推荐","stall":"摆摊指数 7/10","rep":"复购指数 9/10","story":"第一次看到莓莓奶冻是在广州一个奶茶摊前，<em>排队排了20分钟</em>。拿到手发现——底下是双皮奶冻，中间是草莓牛乳冰沙，顶上挤三圈半奶油，插一根吸管。<br><br>奶冻是自己做的，比直接用果冻多了奶香和滑嫩感。成本5.2元，卖12-14，女生看了基本走不动。","cost":"约¥5.2","price":"¥12-14/杯","ds":"50-80杯","dr":"≈¥600-1120","dc":"≈¥260-416","ov":"~¥50-100","dp":"≈¥290-604","rc":"15-22天","rn":"10-15天","ri":"5-10天","rk":[4,2,1,2],"ln":["双皮奶冻","冷冻草莓浆","蜜制草莓","冰糖糖浆","纯牛奶","倍浓牛乳","喷射奶油","新鲜草莓","冰沙杯"],"scenes":["夜市","步行街","学校周边","饮品摊"],"bn":"某茶莓莓奶冻¥24 vs 摆摊¥12-14/杯","bd":"品牌店奶冻是中央工厂配送，摆摊自己做奶冻成本更低，口感更新鲜。","talk":"「底下奶冻滑溜溜，中间冰沙凉丝丝，顶上奶油甜滋滋——一杯三种口感。」","proc":"• 杯底加双皮奶冻100g<br>• 冰沙杯加草莓浆60ml+蜜制草莓30g+冰糖糖浆25g+牛奶100ml+牛乳20ml+冰块200g打碎<br>• 倒入杯中，挤奶油顶3.5圈<br>• 新鲜草莓装饰","pit":"• <em>奶冻太软</em>——双皮奶冻要冷藏2小时以上，切块时才能成型<br>• <em>奶油顶塌</em>——喷射奶油用前摇匀，挤完马上出餐<br>• <em>冰沙分层</em>——打冰沙时间要够，打到细腻才不分离<br>• <em>草莓装饰切开</em>——草莓切片或对半，整颗放着不高级","pay":"解锁完整配方：双皮奶冻制作工艺 + 牛乳冰沙比例 + 奶油顶技巧 + 出餐SOP"},
    "003": {"n":"霸气莓莓脆啵啵","s":"冷饮700ml · 草莓晶球清爽果茶","tg":["低投资","夜市","果茶","夏日"],"rec":"🔥 热销推荐","stall":"摆摊指数 8/10","rep":"复购指数 7/10","story":"这杯最大的卖点就一个字——<em>脆</em>。原味晶球在嘴里咬破那一瞬间，配上草莓果茶的酸甜，口感直接拉满。<br><br>不需要冰沙机，雪克杯就能搞定，出餐速度飞快。草莓浆80ml配茉莉绿茶150ml，成本6.17元，卖13-15。适合不想添设备的摆摊新手。","cost":"约¥6.17","price":"¥13-15/杯","ds":"80-120杯","dr":"≈¥1040-1800","dc":"≈¥494-740","ov":"~¥60-120","dp":"≈¥486-940","rc":"12-18天","rn":"8-12天","ri":"5-8天","rk":[4,1,1,2],"ln":["原味晶球","冷冻草莓浆","茉莉绿茶茶汤","冰糖糖浆","蜜制草莓颗粒","雪克杯","成品杯"],"scenes":["夜市","步行街","学校周边","饮品摊","公园"],"bn":"某雪霸气莓莓¥22 vs 摆摊¥13-15/杯","bd":"品牌店重在包装和空间体验，摆摊把成本用在原料上，口感差距不大。","talk":"「一口咬破晶球那个脆劲儿——喝过的都回头来找。」","proc":"• 杯底加晶球80g<br>• 雪克杯加冰块200g+茶汤150ml+草莓浆80ml+蜜制草莓50g+冰糖糖浆30ml摇匀<br>• 倒入杯中即出","pit":"• <em>晶球放太多</em>——80g刚好，多了喧宾夺主<br>• <em>雪克不够</em>——摇12-15下让茶汤和果浆完全融合<br>• <em>冰块化水</em>——雪克前冰块要足，摇完马上倒出<br>• <em>蜜制草莓不压</em>——草莓颗粒稍微压一下出味更好","pay":"解锁完整配方：晶球处理技巧 + 草莓果茶调配 + 雪克手法 + 出餐流程"},
    "004": {"n":"草莓小丸子","s":"冷饮700ml · 草莓糯米丸子生椰","tg":["低投资","夜市","甜品饮品","Q弹"],"rec":"🔥 热销推荐","stall":"摆摊指数 7/10","rep":"复购指数 8/10","story":"糯米丸子是这杯的点睛之笔。有次在学校门口试摊，<em>一个女生喝了一口就说丸子好好吃</em>，又回头买了两杯。草莓浆80ml配生椰乳120ml，椰香和莓香混在一起，底下还有水晶冻。成本6.29，卖14-16。<br><br>关键是糯米丸子要现煮，放久了会硬，出餐节奏要卡好。","cost":"约¥6.29","price":"¥14-16/杯","ds":"50-80杯","dr":"≈¥700-1280","dc":"≈¥315-503","ov":"~¥50-100","dp":"≈¥335-677","rc":"15-22天","rn":"10-15天","ri":"5-10天","rk":[4,2,1,2],"ln":["糯米小丸子","水晶冻","草莓浆","茉莉绿茶茶汤","冰糖糖浆","蜜制草莓","生椰乳","雪克杯"],"scenes":["夜市","学校周边","步行街","饮品摊","公园"],"bn":"某co草莓小丸子¥16 vs 摆摊¥14-16/杯","bd":"价格差不多但摆摊用料更扎实，丸子更多，草莓味更浓。","talk":"「杯底有糯糯的小丸子，嚼着嚼着就喝完一杯。」","proc":"• 杯底加小丸子50g+水晶冻50g<br>• 雪克杯加草莓浆80ml+茶汤80ml+冰糖糖浆10ml+蜜制草莓30g+冰块200g摇匀<br>• 倒入杯中，加生椰乳120ml","pit":"• <em>丸子煮过头</em>——糯米丸子煮到浮起就捞，过了就烂<br>• <em>生椰乳直接加冰沙里</em>——先倒果茶再淋生椰乳，分层才好看<br>• <em>水晶冻代替晶球</em>——水晶冻更滑嫩，跟丸子搭","pay":"解锁完整配方：糯米丸子煮制技巧 + 草莓生椰调配比例 + 分层手法 + 出餐SOP"},
    "005": {"n":"草莓桃桃茶","s":"冷饮700ml · 草莓水蜜桃双果茶","tg":["低投资","夜市","双果","夏日"],"rec":"🔥 热销推荐","stall":"摆摊指数 8/10","rep":"复购指数 8/10","story":"草莓和水蜜桃——这两个水果放在一起就是王炸。<em>成本6.9块，卖14-16，毛利拉到55%+</em>。关键是水蜜桃果蓉在杯底打底，草莓浆和茶汤雪克后倒进去，喝的时候能同时感受到两种果味。<br><br>出餐极快，雪克几下就搞定，高峰期一小时能出40杯。","cost":"约¥6.9","price":"¥14-16/杯","ds":"70-110杯","dr":"≈¥980-1760","dc":"≈¥483-759","ov":"~¥60-120","dp":"≈¥437-881","rc":"12-18天","rn":"8-12天","ri":"5-8天","rk":[4,1,1,2],"ln":["原味晶球","水蜜桃果蓉","草莓浆","茉莉绿茶茶汤","冰糖糖浆","蜜制草莓","雪克杯"],"scenes":["夜市","步行街","学校周边","饮品摊"],"bn":"某茶草莓桃桃¥24 vs 摆摊¥14-16/杯","bd":"品牌店贵在房租和营销，摆摊原料同级别，味道差不到哪去。","talk":"「草莓的酸甜和水蜜桃的香甜——一杯喝出两种水果的快乐。」","proc":"• 杯底加晶球80g+水蜜桃果蓉80g<br>• 雪克杯加冰块200g+茶汤150ml+冰糖糖浆20ml+草莓浆40ml+蜜制草莓30g摇匀<br>• 倒入杯中","pit":"• <em>水蜜桃果蓉沉底不均</em>——放杯底前先搅一搅<br>• <em>草莓浆不够</em>——40ml刚好，多了盖掉水蜜桃味<br>• <em>不加冰直接雪克</em>——冰块200g是标配，少冰口感淡","pay":"解锁完整配方：双果比例调配 + 晶球处理 + 雪克手法 + 打包方案"},
    "006": {"n":"生椰可可冰茶","s":"冷饮500ml · 巧克力生椰冰沙","tg":["低投资","创意饮品","甜品","夏日"],"rec":"⭐ 特色推荐","stall":"摆摊指数 6/10","rep":"复购指数 7/10","story":"这杯是从广禧夏季菜单挖来的创意款。<em>杯壁抹巧克力酱，生椰乳打底，可可冰沙顶上，再插一根雪糕</em>——一杯顶三样。成本12.7，卖18-22。适合摆在甜品摊或者炸鸡摊旁边做搭配。<br><br>雪糕成本占大头，可以找批发商拿整箱的，单支能压到3块左右。","cost":"约¥12.7","price":"¥18-22/杯","ds":"40-60杯","dr":"≈¥720-1320","dc":"≈¥508-762","ov":"~¥50-100","dp":"≈¥162-458","rc":"20-30天","rn":"15-20天","ri":"8-12天","rk":[3,3,1,2],"ln":["巧克力酱","生椰乳","可可粉","冰糖糖浆","喷射奶油","雪糕","冰沙机","成品杯"],"scenes":["夜市","商场周边","游乐场","甜品摊"],"bn":"同类创意饮品店¥28-35 vs 摆摊¥18-22/杯","bd":"雪糕成本高，但整杯视觉冲击强，适合发朋友圈拍照打卡。","talk":"「巧克力+生椰+雪糕，一杯下去三个满足。」","proc":"• 杯壁抹巧克力酱，加生椰乳100ml<br>• 冰沙机加生椰乳50ml+可可粉30ml+冰糖糖浆10ml+水50ml+冰块180g搅匀<br>• 倒入杯中，挤奶油顶，插雪糕","pit":"• <em>雪糕融化快</em>——出餐前最后一刻才插雪糕<br>• <em>可可粉结块</em>——先用少量热水化开可可粉再打冰沙<br>• <em>成本控制</em>——雪糕批发比零售便宜一半","pay":"解锁完整配方：可可冰沙调配 + 巧克力挂壁技巧 + 雪糕批发渠道 + 成本控制方案"},
}

if __name__ == "__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    count = 0
    for n in range(start, end + 1):
        key = f"{n:03d}"
        if key in ALL_DRINKS:
            path = make_card(key, ALL_DRINKS[key])
            print(f"OK {path}")
            count += 1
        else:
            print(f"SKIP YL_{key} (no data)")
    print(f"Generated {count} cards (YL_{start:03d}~YL_{end:03d})")
