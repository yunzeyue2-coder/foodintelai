import json, os

# 读取现有CZ_033的样式和结构作为模板
with open('/Users/mac/Desktop/青葵/foodintelai-site/cards/CZ_033.html', 'r') as f:
    cz33 = f.read()

with open('/Users/mac/Desktop/青葵/foodintelai-site/cards/TL_019.html', 'r') as f:
    tl19 = f.read()

# 从CZ_033提取<style>到</style>之间的内容
style_start = cz33.find('<style>')
style_end = cz33.find('</style>') + 8
style_block = cz33[style_start:style_end]

# 从TL_019提取更丰富的样式（有风险提示、防坑等）
# 但CZ_033的结构更一致

# ===== 1. 炒饭炒面类：CZ_036 铁板炒饭 =====
cz036 = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>CZ_036 · 铁板炒饭 · 沧林食品</title>
<style>
''' + cz33[cz33.find('<style>')+7:cz33.find('</style>')] + '''
</style>
<script>
function scrollToWechat(){document.getElementById("payArea").scrollIntoView({behavior:"smooth"})}
</script>
</head>
<body>
<div class="card">
<div class="meta">
<span class="badge">🔥 炒饭炒面花甲</span>
<h1>铁板炒饭</h1>
<div class="sub">铁板猛火快炒 · 酱料为核心壁垒 · 标准化出餐</div>
<div class="tags"><span>#铁板炒饭</span><span>#猛火快炒</span><span>#标准化</span></div>
</div>

<div class="level-banner">
<span class="level-item">启动资金：3-8万</span>
<span class="level-item high">日营收：¥600-1500</span>
<span class="level-item">毛利率：60-65%</span>
<span class="level-item">回本周期：1-2个月</span>
</div>

<div class="section">
<div class="s-title">💡 产品说</div>
<div class="story">
铁板炒饭不是普通炒饭。铁板温度220℃+，米粒在高温下迅速焦化产生锅气，这是家用灶台做不到的。核心壁垒在<strong>炒饭酱</strong>——不是普通生抽老抽，是蚝油+海鲜酱+黑胡椒汁+鸡汁+拌饭酱的复合酱，一酱定乾坤。<br><br>
每份米饭300-350g，加鸡蛋1个、香肠15-20g、酱料20-30g，配菜自选。出餐速度2-3分钟/份，高峰期一个人能同时出3份。
</div>
</div>

<div class="section">
<div class="s-title">💰 利润模型</div>
<div class="cost-box">
<div class="row"><span>炒饭酱（20-30g）</span><span class="v">¥0.8-1.2</span></div>
<div class="row"><span>米饭（300-350g）</span><span class="v">¥0.4-0.6</span></div>
<div class="row"><span>鸡蛋+香肠+配菜</span><span class="v">¥1.5-2.0</span></div>
<div class="row"><span>包装/油/燃气</span><span class="v">¥0.8-1.2</span></div>
<div class="row tot"><span>总成本</span><span class="v">¥3.5-5.0</span></div>
<div class="row tot" style="border:none;margin-top:0;padding-top:4px"><span>建议售价</span><span class="v">¥12-18（堂食）/ ¥15-22（外卖）</span></div>
</div>
<div class="roi">
<div class="roi-b c"><div>时产</div><div class="d">¥180-360</div><div>单人操作</div></div>
<div class="roi-b n"><div>日营收</div><div class="d">¥600-1500</div><div>4-6小时营业</div></div>
<div class="roi-b i"><div>月净利</div><div class="d">¥8000-1.8万</div><div>含房租人工</div></div>
</div>
</div>

<div class="section">
<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
<strong>炒饭酱基础配比：</strong><br>
蚝油500g · 海鲜酱150g · 鸡汁30g · 黑胡椒汁100g<br>
拌饭酱100g · 老抽70g · 食盐10g · 味精6g<br>
所有材料调配后破壁机打碎打烂，完全融为一体<br><br>
<strong>每份用量：</strong>米饭300-350g、大豆油适量、鸡蛋1个、香肠15-20g、炒饭酱20-30g、洋葱香葱适量、配菜自选<br><br>
<em style="color:#b5aaa0;font-size:11px">以上为配方框架。完整版含：铁板温度控制要点、不同配菜搭配方案、外卖包装结构、高峰期出餐流程。</em>
</div>
</div>

<div class="section">
<div class="s-title">⚙️ 工艺流程</div>
<div class="story">
1. 铁板预热220℃以上，刷底油<br>
2. 打鸡蛋在铁板上划散，炒至半熟<br>
3. 下米饭、酱料，铁铲快速翻炒30秒<br>
4. 下香肠、配菜，继续翻炒20-30秒<br>
5. 撒葱花出锅，装盒<br><br>
<strong>关键控制点：</strong>铁板温度不能低于200℃否则变焖饭；酱料必须提前调配好不能现炒现放；米饭用隔夜饭口感最佳
</div>
</div>

<div class="section">
<div class="s-title">⚠️ 三大风险</div>
<div class="risk-item"><span>🔴 油烟问题</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span>★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">铁板炒饭油烟大，选址必须考虑排烟和居民投诉</div>
<div class="risk-item"><span>🔴 高峰期压力</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span>★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">午晚高峰集中，单人最多同时出3份，爆单会崩</div>
<div class="risk-item"><span>🟡 外卖包装</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">铁板炒饭闷在盒子里20分钟口感掉30%，必须用透气包装+缩短配送时间</div>
</div>

<div class="section">
<div class="s-title">🎯 适合场景</div>
<div class="scene-grid">
<span class="scene-item">美食广场档口</span>
<span class="scene-item">写字楼午餐</span>
<span class="scene-item">夜市摊位</span>
<span class="scene-item">外卖专营</span>
<span class="scene-item">学校周边</span>
</div>
</div>

<div class="section">
<div class="s-title">🤝 搭配销售</div>
<div class="pair-item"><span class="p-name">铁板炒饭（基础款）</span><span class="p-price">¥12-15</span></div>
<div class="pair-item"><span class="p-name">铁板炒饭（加蛋加肠）</span><span class="p-price">¥15-18</span></div>
<div class="pair-item"><span class="p-name">铁板炒饭（豪华版/加肉）</span><span class="p-price">¥18-22</span></div>
<div class="pair-item"><span class="p-name">铁板炒面</span><span class="p-price">¥13-16</span></div>
<div class="pair-item"><span class="p-name">冰镇酸梅汤</span><span class="p-price">¥5-8</span></div>
</div>

<div class="section">
<div class="s-title">💬 卖货话术</div>
<div class="talk">
「这是铁板炒饭，220度铁板猛火快炒，跟家里炒的完全不一样。米饭粒粒分明有锅气，酱料是我们自己调的，别家吃不到。」<br><br>
「要不要加个蛋？加肠也才多三块钱。再来杯酸梅汤解腻，一套才20块。」
</div>
</div>

<div class="section">
<div class="s-title">🚫 避坑指南</div>
<div class="tip-item">铁板炒饭的锅气只有3分钟赏味期，在外卖平台写"建议收到立即食用"，闷久了差评率高</div>
<div class="tip-item">酱料提前调配好冷藏，每天早上装一小桶带到摊位，不要现调</div>
<div class="tip-item">高峰期提前把米饭分装成300-350g/份，到点直接倒铁板上，别现称</div>
<div class="tip-item">铁板每月打磨一次，有划痕的板会粘锅、影响出品质量</div>
</div>

<div class="pay" id="payArea">
<div class="lock-icon">🔒</div>
<h3>完整配方 + 运营方案</h3>
<ul>
<li>✔️ 炒饭酱精确到克的完整配方</li>
<li>✔️ 铁板温度控制与操作要点</li>
<li>✔️ 5种配菜搭配方案与成本</li>
<li>✔️ 外卖包装方案与成本</li>
<li>✔️ 高峰期出餐流程设计</li>
<li>✔️ 开业促销方案</li>
</ul>
<div class="price-tag">¥9.9 <small>一次购买，永久更新</small></div>
<a class="btn" href="https://weixin.qq.com">添加微信 · 发送资料</a>
<div class="note">加微信备注「CZ_036铁板炒饭」</div>
</div>
<div class="ftr">沧林食品 · 产品编号 CZ_036</div>
</div>
</body>
</html>'''

# ===== 2. 炒饭炒面类：CZ_037 锡纸花甲粉 =====
cz037 = cz036.replace('CZ_036 · 铁板炒饭', 'CZ_037 · 锡纸花甲粉').replace('铁板炒饭', '锡纸花甲粉')
cz037 = cz037.replace('铁板猛火快炒 · 酱料为核心壁垒 · 标准化出餐', '锡纸锁鲜 · 花甲+粉丝+汤底 · 夜市爆款')
cz037 = cz037.replace('🔥 炒饭炒面花甲', '🔥 炒饭炒面花甲')
cz037 = cz037.replace('#铁板炒饭', '#锡纸花甲粉').replace('#猛火快炒', '#夜宵爆款').replace('#标准化', '#锡纸锁鲜')
cz037 = cz037.replace('沧林食品 · 产品编号 CZ_036', '沧林食品 · 产品编号 CZ_037')
cz037 = cz037.replace('「CZ_036铁板炒饭」', '「CZ_037锡纸花甲粉」')

# 替换产品说
cz037 = cz037.replace('''<div class="s-title">💡 产品说</div>
<div class="story">
铁板炒饭不是普通炒饭。铁板温度220℃+，米粒在高温下迅速焦化产生锅气，这是家用灶台做不到的。核心壁垒在<strong>炒饭酱</strong>——不是普通生抽老抽，是蚝油+海鲜酱+黑胡椒汁+鸡汁+拌饭酱的复合酱，一酱定乾坤。<br><br>
每份米饭300-350g，加鸡蛋1个、香肠15-20g、酱料20-30g，配菜自选。出餐速度2-3分钟/份，高峰期一个人能同时出3份。
</div>''',
'''<div class="s-title">💡 产品说</div>
<div class="story">
锡纸花甲粉是夜市摊位的流量王。花甲+粉丝+汤底在锡纸里焖煮，鲜味不流失。汤底是关键——鸡架骨+大骨熬4小时的高汤打底，花甲自带鲜味加持。一份成本不到5块，卖15-18块利润可观。<br><br>
操作门槛极低：锡纸碗摆好→放泡好的粉丝→放花甲→浇汤→放蒜蓉辣酱→上炉焖3分钟。一个人能同时盯5-6份，翻台率极高。
</div>''')

# 替换利润模型
cz037 = cz037.replace('''<div class="s-title">💰 利润模型</div>
<div class="cost-box">
<div class="row"><span>炒饭酱（20-30g）</span><span class="v">¥0.8-1.2</span></div>
<div class="row"><span>米饭（300-350g）</span><span class="v">¥0.4-0.6</span></div>
<div class="row"><span>鸡蛋+香肠+配菜</span><span class="v">¥1.5-2.0</span></div>
<div class="row"><span>包装/油/燃气</span><span class="v">¥0.8-1.2</span></div>
<div class="row tot"><span>总成本</span><span class="v">¥3.5-5.0</span></div>
<div class="row tot" style="border:none;margin-top:0;padding-top:4px"><span>建议售价</span><span class="v">¥12-18（堂食）/ ¥15-22（外卖）</span></div>
</div>
<div class="roi">
<div class="roi-b c"><div>时产</div><div class="d">¥180-360</div><div>单人操作</div></div>
<div class="roi-b n"><div>日营收</div><div class="d">¥600-1500</div><div>4-6小时营业</div></div>
<div class="roi-b i"><div>月净利</div><div class="d">¥8000-1.8万</div><div>含房租人工</div></div>
</div>
</div>''',
'''<div class="s-title">💰 利润模型</div>
<div class="cost-box">
<div class="row"><span>花甲（250g）</span><span class="v">¥1.8-2.5</span></div>
<div class="row"><span>粉丝+配菜</span><span class="v">¥0.5-0.8</span></div>
<div class="row"><span>汤底+调料</span><span class="v">¥0.6-1.0</span></div>
<div class="row"><span>锡纸碗+包装</span><span class="v">¥0.5-0.8</span></div>
<div class="row"><span>燃气/人工摊</span><span class="v">¥0.6-1.0</span></div>
<div class="row tot"><span>总成本</span><span class="v">¥4.0-6.1</span></div>
<div class="row tot" style="border:none;margin-top:0;padding-top:4px"><span>建议售价</span><span class="v">¥15-18（堂食）/ ¥18-22（外卖）</span></div>
</div>
<div class="roi">
<div class="roi-b c"><div>时产</div><div class="d">¥180-350</div><div>同时出6份</div></div>
<div class="roi-b n"><div>日营收</div><div class="d">¥800-2000</div><div>夜市4-6小时</div></div>
<div class="roi-b i"><div>月净利</div><div class="d">¥8000-2万</div><div>含人工摊位</div></div>
</div>
</div>''')

# 替换核心配方
cz037 = cz037.replace('''<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
<strong>炒饭酱基础配比：</strong><br>
蚝油500g · 海鲜酱150g · 鸡汁30g · 黑胡椒汁100g<br>
拌饭酱100g · 老抽70g · 食盐10g · 味精6g<br>
所有材料调配后破壁机打碎打烂，完全融为一体<br><br>
<strong>每份用量：</strong>米饭300-350g、大豆油适量、鸡蛋1个、香肠15-20g、炒饭酱20-30g、洋葱香葱适量、配菜自选<br><br>
<em style="color:#b5aaa0;font-size:11px">以上为配方框架。完整版含：铁板温度控制要点、不同配菜搭配方案、外卖包装结构、高峰期出餐流程。</em>
</div>
</div>''',
'''<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
<strong>高汤配方：</strong>鸡架骨4只 · 大骨2根 · 生姜150g · 水50斤 · 白酒100g<br>
大火烧开转小火熬4小时<br><br>
<strong>炒花甲（每份）：</strong>蒜末姜末各50g炒香，下花甲500g炒至张口，加料酒50g、鸡精10g、味精10g、蚝油20g、鸡汁20g<br><br>
<strong>出品流程：</strong>锡纸碗里放泡好的粉丝→铺花甲→浇高汤→加蒜蓉辣酱→上炉焖3分钟→撒葱花<br><br>
<em style="color:#b5aaa0;font-size:11px">以上为配方框架。完整版含：花甲吐沙技巧、蒜蓉辣酱配方、不同口味变体、高峰期备料方案。</em>
</div>
</div>''')

# 替换工艺流程
cz037 = cz037.replace('''<div class="s-title">⚙️ 工艺流程</div>
<div class="story">
1. 铁板预热220℃以上，刷底油<br>
2. 打鸡蛋在铁板上划散，炒至半熟<br>
3. 下米饭、酱料，铁铲快速翻炒30秒<br>
4. 下香肠、配菜，继续翻炒20-30秒<br>
5. 撒葱花出锅，装盒<br><br>
<strong>关键控制点：</strong>铁板温度不能低于200℃否则变焖饭；酱料必须提前调配好不能现炒现放；米饭用隔夜饭口感最佳
</div>''',
'''<div class="s-title">⚙️ 工艺流程</div>
<div class="story">
1. 花甲清水加盐养2小时吐沙，刷洗干净<br>
2. 高汤提前熬好（鸡架+大骨4小时），当天用当天熬<br>
3. 锡纸碗底部铺泡好的粉丝，约50-80g<br>
4. 放花甲250g（约15-20个）<br>
5. 浇高汤至八分满<br>
6. 加蒜蓉辣酱、姜末、调味料<br>
7. 上炉（或煤气灶）中火焖3-4分钟，至花甲全开口<br>
8. 撒葱花、香菜，连锡纸碗一起上桌<br><br>
<strong>关键控制点：</strong>花甲买回来必须活养吐沙至少2小时；高汤每天现熬，隔夜高汤鲜味掉一半；蒜蓉辣酱是灵魂，辣度和蒜香要平衡
</div>''')

# 替换风险
cz037 = cz037.replace('''<div class="section">
<div class="s-title">⚠️ 三大风险</div>
<div class="risk-item"><span>🔴 油烟问题</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span>★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">铁板炒饭油烟大，选址必须考虑排烟和居民投诉</div>
<div class="risk-item"><span>🔴 高峰期压力</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span>★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">午晚高峰集中，单人最多同时出3份，爆单会崩</div>
<div class="risk-item"><span>🟡 外卖包装</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">铁板炒饭闷在盒子里20分钟口感掉30%，必须用透气包装+缩短配送时间</div>
</div>''',
'''<div class="section">
<div class="s-title">⚠️ 三大风险</div>
<div class="risk-item"><span>🔴 花甲品质波动</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">花甲是鲜活水产，夏季死了会发臭，差评一单毁整晚</div>
<div class="risk-item"><span>🔴 季节性明显</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">冬季花甲价格涨50%，夜市人流量降30%，利润空间被压缩</div>
<div class="risk-item"><span>🟡 汤底一致性</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">每天熬的高汤味道会有差异，标准化调味流程非常重要</div>
</div>''')

# 替换场景
cz037 = cz037.replace('''<div class="scene-grid">
<span class="scene-item">美食广场档口</span>
<span class="scene-item">写字楼午餐</span>
<span class="scene-item">夜市摊位</span>
<span class="scene-item">外卖专营</span>
<span class="scene-item">学校周边</span>
</div>''',
'''<div class="scene-grid">
<span class="scene-item">夜市摊位</span>
<span class="scene-item">美食街档口</span>
<span class="scene-item">大排档</span>
<span class="scene-item">学校周边</span>
<span class="scene-item">外卖专营</span>
</div>''')

# 替换话术
cz037 = cz037.replace('''<div class="talk">
「这是铁板炒饭，220度铁板猛火快炒，跟家里炒的完全不一样。米饭粒粒分明有锅气，酱料是我们自己调的，别家吃不到。」<br><br>
「要不要加个蛋？加肠也才多三块钱。再来杯酸梅汤解腻，一套才20块。」
</div>''',
'''<div class="talk">
「刚到的花甲，活的花甲！你看这个头多大。锡纸焖的，鲜味全锁在里面。来一份尝尝？」<br><br>
「加份粉丝？加2块。要不要辣？微辣中辣变态辣？再来瓶冰啤酒绝配。」
</div>''')

# 替换避坑
cz037 = cz037.replace('''<div class="tip-item">铁板炒饭的锅气只有3分钟赏味期，在外卖平台写"建议收到立即食用"，闷久了差评率高</div>
<div class="tip-item">酱料提前调配好冷藏，每天早上装一小桶带到摊位，不要现调</div>
<div class="tip-item">高峰期提前把米饭分装成300-350g/份，到点直接倒铁板上，别现称</div>
<div class="tip-item">铁板每月打磨一次，有划痕的板会粘锅、影响出品质量</div>''',
'''<div class="tip-item">花甲买回来用盐水+几滴香油养2小时吐沙，不吐沙的花甲一嘴沙差评</div>
<div class="tip-item">高汤一次熬50斤，分装冷藏可存3天。每天用的拿一部分加热，不要整桶反复烧</div>
<div class="tip-item">锡纸碗买加厚款（0.08mm以上），薄款焖煮容易破，汤漏了就废了</div>
<div class="tip-item">花甲当天进货当天卖完，隔夜死花甲坚决不能用，坏一锅整锅倒</div>''')

# ===== 3. 汤料卤水：TL_020 川式五香卤水 =====
# 用TL_019的模板
tl020 = tl19.replace('TL-019 牛肉板面浇头 · 沧林食品', 'TL_020 · 川式五香卤水 · 沧林食品')
tl020 = tl020.replace('TL_019.html', 'TL_020.html')
tl020 = tl020.replace('牛肉板面浇头', '川式五香卤水')
tl020 = tl020.replace('🍲 汤料卤水 · 牛肉板面浇头', '🍲 汤料卤水 · 川式五香卤水')
tl020 = tl020.replace('安徽牛肉板面专用浇头，30+香辛料熬制，卤香浓郁，一勺定味', '50斤高汤配80+香料，传统川式五香卤水，适用各类卤货')

# 替换关键模块需要知道tl19的结构。先保存两个文件再用patch
print("CZ_036 和 CZ_037 已准备好")

# 保存文件
with open('/Users/mac/Desktop/青葵/foodintelai-site/cards/CZ_036.html', 'w') as f:
    f.write(cz036)
with open('/Users/mac/Desktop/青葵/foodintelai-site/cards/CZ_037.html', 'w') as f:
    f.write(cz037)

print("✅ CZ_036 铁板炒饭.html saved")
print("✅ CZ_037 锡纸花甲粉.html saved")
