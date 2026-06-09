#!/usr/bin/env python3
"""
生成M3咖啡门店决策卡
整合瑞幸配方数据作为门店级咖啡体系交付内容
"""
import os

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"
DELIVERY_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/delivery"
DATA_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/m3-data"

for d in [DELIVERY_DIR, DATA_DIR]:
    os.makedirs(d, exist_ok=True)

# ====== M3卡 ======
M3_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0">
<title>MD_CF_000 · 精品咖啡专门店（门店决策卡 M3）· 沧林食品</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#1a1a1a;color:#e8e0d8;padding:20px 12px}}
.card{{max-width:800px;margin:0 auto;background:#2a2220;border-radius:20px;overflow:hidden}}
.hero{{padding:30px 24px;background:linear-gradient(135deg,#3a2a1a,#2a1a10);border-bottom:1px solid #4a3a2a}}
.hero .tag{{display:inline-block;background:#C0392B;color:#fff;font-size:10px;padding:2px 10px;border-radius:4px;margin-bottom:8px}}
.hero h1{{font-size:24px;font-weight:800;color:#f0e8e0;margin-bottom:4px}}
.hero .sub{{font-size:12px;color:#b0a090;margin-bottom:12px}}
.hero .price-big{{font-size:36px;font-weight:900;color:#E8652D}}
.hero .price-big small{{font-size:14px;font-weight:400;color:#b0a090}}
.menu{{padding:20px 24px;background:#2a2220}}
.menu h2{{font-size:13px;font-weight:700;color:#E8652D;margin-bottom:8px;padding-bottom:4px;border-bottom:1px solid #3a2a2a}}
.menu-grid{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}
.menu-item{{padding:8px 12px;background:#3a3028;border-radius:6px;font-size:11px;color:#c0b0a0}}
.menu-item strong{{color:#f0e8e0;font-size:12px}}
.menu-item .p{{float:right;color:#E8652D;font-weight:600}}
.section{{padding:20px 24px;border-top:1px solid #3a2a2a}}
.section h2{{font-size:13px;font-weight:700;color:#E8652D;margin-bottom:10px}}
.section .text{{font-size:12px;line-height:1.9;color:#c0b0a0}}
.data-row{{display:flex;justify-content:space-between;padding:6px 0;font-size:12px;border-bottom:1px solid #3a2a2a}}
.data-row .l{{color:#b0a090}}
.data-row .r{{color:#f0e8e0;font-weight:600}}
.score-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}}
.score-item{{padding:10px;background:#3a3028;border-radius:8px;text-align:center}}
.score-item .s-num{{font-size:22px;font-weight:800;color:#E8652D}}
.score-item .s-label{{font-size:10px;color:#b0a090}}
.paywall{{padding:24px;background:linear-gradient(135deg,#2a1a10,#1a1a1a);text-align:center;border-top:1px solid #4a3a2a}}
.paywall .lock{{font-size:24px;margin-bottom:4px}}
.paywall .pw-title{{font-size:16px;font-weight:800;color:#f0e8e0;margin-bottom:8px}}
.paywall .pw-desc{{font-size:11px;color:#b0a090;line-height:1.8;margin-bottom:12px}}
.paywall .pw-btn{{display:inline-block;background:#E8652D;color:#fff;padding:12px 40px;border-radius:8px;font-size:14px;font-weight:700;text-decoration:none}}
.paywall .pw-note{{font-size:10px;color:#7a6a5a;margin-top:6px}}
.footer{{padding:16px 24px;text-align:center;font-size:10px;color:#6a5a4a}}
</style>
</head>
<body>
<div class="card">

<div class="hero">
  <div class="tag">🏪 门店决策卡 M3</div>
  <h1>精品咖啡专门店</h1>
  <div class="sub">咖啡门店完整经营方案 · 含瑞幸级配方体系 · 从0到1开店</div>
  <div class="price-big">¥699 <small>一价全含</small></div>
</div>

<div class="menu">
  <h2>📋 产品体系（40+款）</h2>
  <div class="menu-grid">
    <div class="menu-item"><strong>☕ 大师咖啡系列</strong><span class="p">8款</span><br>美式/拿铁/卡布奇诺/摩卡/焦糖玛奇朵</div>
    <div class="menu-item"><strong>🧊 瑞纳冰系列</strong><span class="p">15款</span><br>巧克力/抹茶/椰子ok/陨石拿铁/杨枝甘露等</div>
    <div class="menu-item"><strong>🍑 冰摇茶饮系列</strong><span class="p">7款</span><br>杨枝甘露椰子冻/满杯桃桃/牛油果很芒等</div>
    <div class="menu-item"><strong>🥤 经典饮品系列</strong><span class="p">4款</span><br>热巧克力/冰摇柑橘百香果/抹茶好喝椰</div>
    <div class="menu-item"><strong>🧋 奶茶系列</strong><span class="p">4款</span><br>阿华田厚乳/轻乳好茶/抹茶好喝椰</div>
    <div class="menu-item"><strong>🌸 限定特饮</strong><span class="p">3款</span><br>珞珈樱花拿铁/樱花白巧瑞纳冰/椰云拿铁</div>
  </div>
</div>

<div class="section">
  <h2>📊 决策评分</h2>
  <div class="score-grid">
    <div class="score-item"><div class="s-num">8.5</div><div class="s-label">启动难度</div></div>
    <div class="score-item"><div class="s-num">8.0</div><div class="s-label">回本速度</div></div>
    <div class="score-item"><div class="s-num">8.5</div><div class="s-label">复购能力</div></div>
    <div class="score-item"><div class="s-num">7.5</div><div class="s-label">操作复杂度</div></div>
  </div>
</div>

<div class="section">
  <h2>💰 经营数据</h2>
  <div class="data-row"><span class="l">启动资金</span><span class="r">¥8-15万（含设备+装修+首批原料）</span></div>
  <div class="data-row"><span class="l">日营业额</span><span class="r">¥2,000-5,000（商圈店）</span></div>
  <div class="data-row"><span class="l">毛利率</span><span class="r">60-72%（饮品高毛利）</span></div>
  <div class="data-row"><span class="l">回本周期</span><span class="r">6-12个月</span></div>
  <div class="data-row"><span class="l">人员配置</span><span class="r">2-3人（1主做+1辅助+1收银）</span></div>
  <div class="data-row"><span class="l">面积需求</span><span class="r">20-40㎡（操作区+仓储+客座）</span></div>
</div>

<div class="section">
  <h2>📦 交付内容</h2>
  <div class="text">
    🔐 付费解锁完整方案，包含：<br><br>
    <strong>一、产品SOP体系（40款完整配方）</strong><br>
    • 大师咖啡系列：美式/拿铁/卡布奇诺/摩卡/焦糖玛奇朵（热+冰双版）<br>
    • 瑞纳冰系列：巧克力/抹茶/椰子ok/陨石拿铁/杨枝甘露/阿华田等15款冰沙<br>
    • 冰摇茶饮系列：椰子冻/满杯桃桃/牛油果很芒等7款<br>
    • 经典饮品：热巧克力/冰摇柑橘百香果等<br>
    • 奶茶系列：阿华田厚乳/轻乳好茶等<br>
    • 限定特饮：樱花拿铁/椰云拿铁等<br><br>
    <strong>二、核心配方参数</strong><br>
    • 意式浓缩萃取标准（粉量/水温/压力/时间）<br>
    • 糖浆泵数换算标准（单糖/半糖/多糖三档）<br>
    • 冰块量控制标准（不同杯型精确克数）<br>
    • 奶油/顶料操作标准（圈数/高度/装饰）<br><br>
    <strong>三、设备清单</strong><br>
    • 咖啡机选型：双头意式机¥2-5万/单头¥1-2万<br>
    • 磨豆机配置：¥3,000-8,000<br>
    • 冰沙机/制冰机/冷藏柜/保温桶<br>
    • 小工具清单：雪克壶/吧勺/量勺/计时器<br><br>
    <strong>四、开店指南</strong><br>
    • 选址评估：商圈/写字楼/社区/学校四类对比<br>
    • 证照办理：食品经营许可证/营业执照流程<br>
    • 供应链方案：核心原料采购渠道+替代方案<br>
    • 出餐动线设计：操作台→出品台→打包台<br>
    • 小程序/外卖平台搭建方案<br>
    • 开业前7天准备清单
  </div>
</div>

<div class="paywall">
  <div class="lock">🔒</div>
  <div class="pw-title">¥699 解锁完整门店方案</div>
  <div class="pw-desc">
    包含40款饮品SOP+完整配方参数+核心原料配比（精确到泵数/克数）+设备清单+开店全流程<br>
    瑞幸级标准化配方体系·门店可直接落地操作
  </div>
  <a class="pw-btn" href="#">📱 加微信解锁</a>
  <div class="pw-note">加好友备注"咖啡门店"快速通过</div>
</div>

<div class="footer">
  沧林食品工作站 · foodintelai.com<br>
  微信 canglin1985 · 数据来源：瑞幸体系+行业通用配方
</div>

</div>
</body>
</html>'''

# ====== 交付包 ======
DELIVERY_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>精品咖啡专门店 · 交付包</title>
<style>
body{{font-family:-apple-system,"PingFang SC",sans-serif;background:#1a1a1a;color:#e8e0d8;padding:20px;line-height:1.8}}
h1{{color:#E8652D;font-size:20px;border-bottom:2px solid #E8652D;padding-bottom:8px}}
h2{{color:#f0e8e0;font-size:16px;margin-top:20px;background:#3a3028;padding:8px 12px;border-radius:6px}}
h3{{color:#c0b0a0;font-size:13px;margin-top:16px}}
table{{width:100%;border-collapse:collapse;margin:10px 0;font-size:11px}}
th,td{{border:1px solid #4a3a2a;padding:6px 8px;text-align:left}}
th{{background:#3a3028;color:#E8652D}}
.section{{background:#2a2220;padding:16px;border-radius:10px;margin:12px 0}}
.note{{font-size:10px;color:#7a6a5a;margin-top:6px}}
.tag{{display:inline-block;background:#C0392B;color:#fff;font-size:9px;padding:1px 6px;border-radius:3px;margin:2px}}
</style>
</head>
<body>
<h1>☕ 精品咖啡专门店 · 完整交付包</h1>
<p style="font-size:12px;color:#b0a090">编号：MD_CF_000 | 门店决策卡 M3 | ¥699</p>

<h2>一、大师咖啡系列 SOP</h2>

<div class="section">
<h3>1. 标准美式（热/冰双版）</h3>
<table>
<tr><th>项目</th><th>热美式</th><th>冰美式</th></tr>
<tr><td>浓缩咖啡</td><td>双份浓缩60ml</td><td>双份浓缩60ml</td></tr>
<tr><td>原味糖浆</td><td>单糖2泵/半糖1泵</td><td>单糖2泵/半糖1泵</td></tr>
<tr><td>水/冰</td><td>热水至距杯口15mm</td><td>直饮水至冰杯上线+加冰至距杯口6mm</td></tr>
<tr><td>操作按键</td><td>按键"标准美式"</td><td>按键"标准美式"</td></tr>
<tr><td>奶油</td><td>按需热饮奶油1.5圈</td><td>按需冰饮奶油2.5圈</td></tr>
<tr><td>售价参考</td><td>¥18-22</td><td>¥18-22</td></tr>
</table>
</div>

<div class="section">
<h3>2. 拿铁（热/冰）</h3>
<table>
<tr><th>项目</th><th>热拿铁</th><th>冰拿铁</th></tr>
<tr><td>浓缩</td><td>双份60ml</td><td>双份60ml</td></tr>
<tr><td>牛奶</td><td>牛奶（打发至65°C）</td><td>牛奶至冰杯上线</td></tr>
<tr><td>原味糖浆</td><td>2泵/1泵</td><td>2泵/1泵</td></tr>
<tr><td>操作</td><td>按键"热拿铁"</td><td>按键"冰拿铁"</td></tr>
<tr><td>入杯</td><td>距杯口10mm</td><td>加冰至距杯口6mm</td></tr>
<tr><td>售价</td><td>¥20-25</td><td>¥20-25</td></tr>
</table>
</div>

<div class="section">
<h3>3. 卡布奇诺（热）</h3>
<table>
<tr><th>项目</th><th>规格</th></tr>
<tr><td>浓缩</td><td>双份60ml</td></tr>
<tr><td>牛奶</td><td>牛奶打发至绵密奶泡</td></tr>
<tr><td>糖浆</td><td>原味糖浆2泵(单糖)/1泵(半糖)</td></tr>
<tr><td>操作</td><td>按键"热卡布奇诺"</td></tr>
<tr><td>入杯</td><td>距杯口10mm</td></tr>
<tr><td>售价</td><td>¥22-26</td></tr>
</table>
</div>

<div class="section">
<h3>4. 摩卡（有奶油）</h3>
<table>
<tr><th>项目</th><th>热摩卡</th><th>冰摩卡</th></tr>
<tr><td>浓缩</td><td>双份60ml</td><td>双份60ml</td></tr>
<tr><td>巧克力</td><td>巧克力预调液3泵+香草1泵</td><td>巧克力预调液3泵+香草1泵</td></tr>
<tr><td>牛奶</td><td>牛奶至标准线</td><td>牛奶至冰杯上线</td></tr>
<tr><td>操作</td><td>按键"热摩卡"</td><td>按键"冰摩卡"</td></tr>
<tr><td>入杯</td><td>距杯口15mm</td><td>加冰至距杯口15mm</td></tr>
<tr><td>奶油</td><td>1.5圈+巧克力粉2下</td><td>2.5圈+巧克力粉2下</td></tr>
<tr><td>售价</td><td>¥24-28</td><td>¥24-28</td></tr>
</table>
</div>

<div class="section">
<h3>5. 焦糖玛奇朵（热/冰）</h3>
<table>
<tr><th>项目</th><th>热焦玛</th><th>冰焦玛</th></tr>
<tr><td>香草糖浆</td><td>3泵(单糖)/2泵(半糖)</td><td>3泵</td></tr>
<tr><td>牛奶</td><td>牛奶至刻度线</td><td>牛奶至冰杯上线</td></tr>
<tr><td>浓缩</td><td>三份浓缩</td><td>三份浓缩</td></tr>
<tr><td>操作</td><td>按键"热焦玛牛奶"→三份浓缩</td><td>按键"冰焦玛牛奶"→三份浓缩</td></tr>
<tr><td>入杯</td><td>距杯口20mm</td><td>加冰至距杯口10mm</td></tr>
<tr><td>装饰</td><td>淋焦糖糖稀</td><td>淋焦糖糖稀</td></tr>
<tr><td>售价</td><td>¥24-28</td><td>¥24-28</td></tr>
</table>
</div>

<h2>二、瑞纳冰系列 SOP（部分）</h2>

<div class="section">
<h3>6. 巧克力瑞纳冰</h3>
<p>原料：牛奶(冰杯下线) + 原味粉2勺 + 巧克力6泵 + 16oz冰块<br>
操作：按键"4"或"D"冰沙程序<br>
入杯：无奶油距杯口10mm/有奶油距杯口15mm → 奶油2.5圈 + 可可粉2下<br>
售价参考：¥26-32</p>
</div>

<div class="section">
<h3>7. 抹茶瑞纳冰</h3>
<p>原料：抹茶粉4勺+原味粉2勺 + 16oz冰块<br>
操作：冰沙程序 → 距杯口15mm<br>
无奶油版默认<br>
售价参考：¥26-32</p>
</div>

<div class="section">
<h3>8. 陨石拿铁瑞纳冰</h3>
<p>原料：寒天晶球2勺 + 原味糖浆2泵(标准)/1泵(半糖) + 12oz冰块<br>
操作：冰沙程序 → 黑糖挂壁1圈<br>
有奶油：距杯口15mm + 奶油2.5圈 + 黑糖淋酱2圈<br>
无奶油：黑糖挂壁1圈即可<br>
售价参考：¥28-35</p>
</div>

<div class="section">
<h3>9. 椰子OK瑞纳冰</h3>
<p>原料：椰浆(冰杯100ml) + 厚乳(冰杯下线) + 原味粉2勺 + 原味糖浆2泵(标准)/1泵(半糖) + 16oz冰块<br>
操作：冰沙程序 → 距杯口15mm（无奶油）<br>
售价参考：¥26-32</p>
</div>

<div class="section">
<h3>10. 阿华田千层瑞纳冰</h3>
<p>原料：酷脆酱1勺(挂壁) + 芋泥1勺 + 黑糖珍珠2勺 + 牛奶(冰杯100ml) + 芋泥2勺+原味粉2勺 + 16oz冰块<br>
操作：冰沙程序 → 距杯口15mm → 奶油2.5圈 + 可可碎片1勺<br>
售价参考：¥30-38</p>
</div>

<h2>三、冰摇茶饮系列 SOP</h2>

<div class="section">
<h3>11. 杨枝甘露椰子冻（冰）</h3>
<p>原料：椰子冻4勺 + 芒果泥 + 椰浆 + 原味糖浆2泵/1泵<br>
操作：冰版→直饮水至400ml→冰块至550ml线→搅拌8圈→距杯口10mm<br>
去冰版→直饮水至500ml<br>
售价：¥28-35</p>
</div>

<div class="section">
<h3>12. 满杯桃桃（冰）</h3>
<p>原料：原味晶球2勺(或花型果冻1勺) + 水蜜桃 + 茉莉花茶<br>
操作：冰版→直饮水至350ml→冰块至600ml线→搅拌→距杯口10mm<br>
去冰版→直饮水至500ml<br>
售价：¥24-30</p>
</div>

<div class="section">
<h3>13. 牛油果很芒</h3>
<p>原料：芒果50ml + 牛油果泥4勺 + 牛奶 + 原味糖浆3泵/2泵<br>
操作：直饮水至350ml→冰块至500ml线→搅拌→加酸奶至距杯口10mm<br>
售价：¥28-35</p>
</div>

<h2>四、奶茶系列 SOP</h2>

<div class="section">
<h3>14. 轻乳好茶（热/冰）</h3>
<p>热版：茶汤250ml+牛奶400ml → 蒸煮 → 距杯口15mm → 奶油1.5圈+扁桃仁碎1勺<br>
冰版：茶汤200ml+牛奶300ml → 冰摇 → 距杯口15mm → 奶油2.5圈+扁桃仁碎1勺<br>
茶底可选：工夫红茶/茉莉绿茶/鸭屎香<br>
售价：¥16-22</p>
</div>

<div class="section">
<h3>15. 抹茶好喝椰（冰）</h3>
<p>原料：抹茶100ml+椰浆300ml+原味糖浆1泵<br>
操作：加冰至满杯 → 搅拌 → 距杯口10mm（无奶油）<br>
售价：¥20-26</p>
</div>

<h2>五、核心原料采购建议</h2>

<div class="section">
<h3>咖啡豆</h3>
<p>推荐中深烘拼配豆（巴西+哥伦比亚+埃塞俄比亚）<br>
也可选用单一产地SOE做差异化<br>
用量参考：日均100杯约消耗2-3kg豆</p>
</div>

<div class="section">
<h3>牛奶/奶基底</h3>
<p>全脂牛奶：推荐皇氏/蒙牛/味全（蛋白质≥3.2%）<br>
厚椰乳：菲诺厚椰乳<br>
燕麦奶：OATLY咖啡大师<br>
淡奶油：雀巢/安佳</p>
</div>

<div class="section">
<h3>糖浆/果酱</h3>
<p>原味糖浆/果糖/香草/焦糖/巧克力/太妃——通用品牌即可<br>
果酱/果蓉：冷冻草莓浆/芒果浆/水蜜桃果蓉/芭乐汁等<br>
小料：原味晶球/黑糖珍珠/椰子冻/花型果冻等</p>
</div>

<h2>六、设备清单与预算</h2>

<div class="section">
<table>
<tr><th>设备</th><th>规格</th><th>预算(元)</th></tr>
<tr><td>意式咖啡机</td><td>双头商用/单头入门</td><td>10,000-50,000</td></tr>
<tr><td>磨豆机</td><td>商用定量磨</td><td>3,000-8,000</td></tr>
<tr><td>冰沙机</td><td>商用大功率</td><td>1,500-3,000</td></tr>
<tr><td>制冰机</td><td>日产30kg以上</td><td>2,000-5,000</td></tr>
<tr><td>冷藏柜</td><td>操作台一体式</td><td>3,000-6,000</td></tr>
<tr><td>封口机/雪克壶/吧勺等</td><td>全套</td><td>500-1,500</td></tr>
<tr><td>收银系统</td><td>含小程序/外卖对接</td><td>2,000-5,000</td></tr>
<tr><td>装修+吧台</td><td>20-40㎡</td><td>30,000-80,000</td></tr>
<tr><td><strong>总计</strong></td><td></td><td><strong>¥52,000-158,500</strong></td></tr>
</table>
</div>

<h2>七、设备操作标准</h2>

<div class="section">
<h3>意式浓缩萃取标准</h3>
<p>粉量：18g±0.5g（双份）<br>
水温：92°C±1°C<br>
萃取压力：9bar<br>
萃取时间：25-30秒<br>
粉液比：1:2（18g→36ml）<br>
crema标准：金黄色，厚度3-5mm</p>
</div>

<div class="section">
<h3>蒸汽打发牛奶标准</h3>
<p>起始温度：4-6°C（冷藏牛奶直接打）<br>
目标温度：55-65°C（超过70°C乳蛋白变性）<br>
打发时间：15-25秒（视奶量）<br>
奶泡标准：绵密如天鹅绒，倒扣不掉落<br>
不同饮品奶泡厚度：<br>
  拿铁：薄奶泡（约0.5cm）<br>
  卡布奇诺：厚奶泡（约1-1.5cm）<br>
  澳白：微奶泡（约0.2cm）</p>
</div>

<p style="text-align:center;color:#6a5a4a;font-size:10px;margin-top:40px">
沧林食品工作站 · foodintelai.com · 微信 canglin1985<br>
交付包编号：MD_CF_000_交付包 | 版本：V1 | 2026-06
</p>
</body>
</html>'''

# ====== 写入文件 ======
def write_all():
    # M3决策卡
    card_path = os.path.join(CARDS_DIR, "MD_CF_000_精品咖啡专门店.html")
    with open(card_path, 'w', encoding='utf-8') as f:
        f.write(M3_HTML)
    print(f"  [M3卡] MD_CF_000_精品咖啡专门店.html")
    
    # 交付包
    deli_path = os.path.join(DELIVERY_DIR, "MD_CF_000_精品咖啡专门店_交付包.html")
    with open(deli_path, 'w', encoding='utf-8') as f:
        f.write(DELIVERY_HTML)
    print(f"  [交付包] MD_CF_000_精品咖啡专门店_交付包.html")
    
    # 更新decision-engine.html
    update_decision_engine()
    
    print("\n咖啡门店决策卡完成!")

def update_decision_engine():
    """在decision-engine.html里添加咖啡门店入口"""
    de_path = "/Users/mac/Desktop/青葵/foodintelai-site/decision-engine.html"
    if not os.path.exists(de_path):
        print("  [跳过] 未找到decision-engine.html")
        return
    
    with open(de_path, encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有咖啡门店
    if '精品咖啡专门店' in content:
        print("  [跳过] 咖啡门店已在decision-engine.html中")
        return
    
    # 找到最后一个门店模型的结尾，在其后插入
    insert_marker = '</div>\n</div>\n</div>\n</div>\n\n<div class="section"'
    if insert_marker in content:
        new_card = '''
<div class="store-model">
  <div class="sm-badge" style="background:#E8652D">☕ M3</div>
  <h3>精品咖啡专门店</h3>
  <p class="sm-sub">瑞幸级配方体系 · ¥699一价全含</p>
  <div class="sm-data">
    <span>¥8-15万起步</span>
    <span>6-12月回本</span>
    <span>60-72%毛利</span>
  </div>
  <p class="sm-desc">40+款饮品SOP（大师咖啡/瑞纳冰/冰摇茶饮/奶茶），含完整配方参数+设备清单+开店流程。已去品牌化，可直接落地。</p>
  <a class="sm-btn" href="cards/MD_CF_000_精品咖啡专门店.html">查看详情 →</a>
</div>'''
        content = content.replace('</div>\n</div>\n</div>\n</div>\n\n<div class="section"', 
                                  new_card + '\n</div>\n</div>\n</div>\n</div>\n\n<div class="section"', 1)
        with open(de_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  [决策页] 已添加咖啡门店入口")
    else:
        print("  [跳过] 未找到插入位置")

if __name__ == '__main__':
    write_all()
