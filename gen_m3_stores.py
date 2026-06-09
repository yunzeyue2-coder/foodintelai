     1|#!/usr/bin/env python3
     2|"""
     3|批量生成M3门店决策卡
     4|每个门店类型 = 一张M3决策卡(免费区展示决策信息+付费区挂载完整单品SOP)
     5|"""
     6|import os, json
     7|
     8|CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"
     9|DELIVERY_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/delivery"
    10|DE_FILE = "/Users/mac/Desktop/青葵/foodintelai-site/decision-engine.html"
    11|
    12|os.makedirs(DELIVERY_DIR, exist_ok=True)
    13|
    14|M3_TPL = '''<!DOCTYPE html>
    15|<html lang="zh-CN">
    16|<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    17|<title>{id} · {name} · 沧林食品 · M3门店决策卡</title>
    18|<style>
    19|*{{margin:0;padding:0;box-sizing:border-box}}
    20|body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#1a1a1a;color:#e8e0d8;padding:20px 12px}}
    21|.card{{max-width:800px;margin:0 auto;background:#2a2220;border-radius:20px;overflow:hidden}}
    22|.hero{{padding:30px 24px;background:linear-gradient(135deg,#3a2a1a,#2a1a10);border-bottom:1px solid #4a3a2a}}
    23|.hero .tag{{display:inline-block;background:{color};color:#fff;font-size:10px;padding:2px 10px;border-radius:4px;margin-bottom:8px}}
    24|.hero h1{{font-size:24px;font-weight:800;color:#f0e8e0;margin-bottom:4px}}
    25|.hero .sub{{font-size:12px;color:#b0a090;margin-bottom:12px}}
    26|.hero .price-big{{font-size:36px;font-weight:900;color:{color}}}
    27|.hero .price-big small{{font-size:14px;font-weight:400;color:#b0a090}}
    28|.section{{padding:20px 24px;border-top:1px solid #3a2a2a}}
    29|.section h2{{font-size:13px;font-weight:700;color:{color};margin-bottom:10px}}
    30|.section .text{{font-size:12px;line-height:1.9;color:#c0b0a0}}
    31|.data-row{{display:flex;justify-content:space-between;padding:6px 0;font-size:12px;border-bottom:1px solid #3a2a2a}}
    32|.data-row .l{{color:#b0a090}}
    33|.data-row .r{{color:#f0e8e0;font-weight:600}}
    34|.score-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}}
    35|.score-item{{padding:10px;background:#3a3028;border-radius:8px;text-align:center}}
    36|.score-item .s-num{{font-size:22px;font-weight:800;color:{color}}}
    37|.score-item .s-label{{font-size:10px;color:#b0a090}}
    38|.product-list{{display:grid;grid-template-columns:1fr 1fr;gap:4px}}
    39|.product-item{{padding:6px 10px;background:#3a3028;border-radius:4px;font-size:11px;color:#c0b0a0}}
    40|.product-item .label{{color:#f0e8e0;font-weight:600}}
    41|.paywall{{padding:24px;background:linear-gradient(135deg,#2a1a10,#1a1a1a);text-align:center;border-top:1px solid #4a3a2a}}
    42|.paywall .lock{{font-size:24px;margin-bottom:4px}}
    43|.paywall .pw-title{{font-size:16px;font-weight:800;color:#f0e8e0;margin-bottom:8px}}
    44|.paywall .pw-desc{{font-size:11px;color:#b0a090;line-height:1.8;margin-bottom:12px}}
    45|.paywall .pw-btn{{display:inline-block;background:{color};color:#fff;padding:12px 40px;border-radius:8px;font-size:14px;font-weight:700;text-decoration:none}}
    46|.paywall .pw-note{{font-size:10px;color:#7a6a5a;margin-top:6px}}
    47|.footer{{padding:16px 24px;text-align:center;font-size:10px;color:#6a5a4a}}
    48|</style></head>
    49|<body><div class="card">
    50|<div class="hero">
    51|  <div class="tag">🏪 门店决策卡 M3</div>
    52|  <h1>{name}</h1>
    53|  <div class="sub">{desc}</div>
    54|  <div class="price-big">¥699 <small>一价全含 · 单品{sop_count}+款SOP</small></div>
    55|</div>
    56|<div class="section">
    57|  <h2>📋 产品体系（{sop_count}款含SOP）</h2>
    58|  <div class="product-list">{products}</div>
    59|</div>
    60|<div class="section">
    61|  <h2>📊 决策评分</h2>
    62|  <div class="score-grid">
    63|    <div class="score-item"><div class="s-num">{score1}</div><div class="s-label">启动难度</div></div>
    64|    <div class="score-item"><div class="s-num">{score2}</div><div class="s-label">回本速度</div></div>
    65|    <div class="score-item"><div class="s-num">{score3}</div><div class="s-label">复购能力</div></div>
    66|    <div class="score-item"><div class="s-num">{score4}</div><div class="s-label">操作复杂度</div></div>
    67|  </div>
    68|</div>
    69|<div class="section">
    70|  <h2>💰 经营数据</h2>
    71|  <div class="data-row"><span class="l">启动资金</span><span class="r">{funds}</span></div>
    72|  <div class="data-row"><span class="l">日营业额</span><span class="r">{daily}</span></div>
    73|  <div class="data-row"><span class="l">毛利率</span><span class="r">{margin}</span></div>
    74|  <div class="data-row"><span class="l">回本周期</span><span class="r">{payback}</span></div>
    75|  <div class="data-row"><span class="l">人员配置</span><span class="r">{staff}</span></div>
    76|  <div class="data-row"><span class="l">面积需求</span><span class="r">{area}</span></div>
    77|</div>
    78|<div class="section">
    79|  <h2>📦 交付内容</h2>
    80|  <div class="text">{delivery}</div>
    81|</div>
    82|<div class="paywall">
    83|  <div class="lock">🔒</div>
    84|  <div class="pw-title">¥699 解锁完整门店方案</div>
    85|  <div class="pw-desc">包含{sop_count}款单品SOP（精确配比）+设备清单+选址指南+开店流程+供应链方案</div>
    86|  <a class="pw-btn" href="#">📱 加微信解锁</a>
    87|  <div class="pw-note">加好友备注"{note}"快速通过</div>
    88|</div>
    89|<div class="footer">沧林食品工作站 · foodintelai.com · 微信 canglin1985</div>
    90|</div></body></html>'''
    91|
    92|STORES = [
    93|    # ===== 1. 奶茶店 =====
    94|    {
    95|        'id': 'MD_NT_000', 'name': '精品奶茶店', 'color': '#E8652D',
    96|        'desc': '新式茶饮完整方案 · 60+款饮品SOP · 瑞幸级配方体系',
    97|        'sop_count': '60+', 'score1': '8.0', 'score2': '8.5', 'score3': '9.0', 'score4': '7.0',
    98|        'funds': '¥5-12万', 'daily': '¥1,500-4,000', 'margin': '65-75%', 'payback': '4-8个月',
    99|        'staff': '2-3人', 'area': '15-30㎡',
   100|        'note': '奶茶店',
   101|        'products': '<div class="product-item"><span class="label">🥤 经典饮品</span><br>芝芝莓莓/杨枝甘露/酷黑莓莓/满杯鲜橙/霸气杨梅/绿豆牛乳冰(20+款)</div>'
   102|                   '<div class="product-item"><span class="label">🍋 手打柠檬茶</span><br>招牌柠檬茶/鸭屎香柠檬茶/芒果柠檬茶/金桔柠檬/霸王杯(47+款)</div>'
   103|                   '<div class="product-item"><span class="label">🧋 奶茶系列</span><br>原味奶茶/鸭屎香奶茶/泰绿奶茶/丝袜奶茶/金钻奶茶/三兄弟(19+款)</div>'
   104|                   '<div class="product-item"><span class="label">🍧 糖水/甜品</span><br>杨枝甘露/清补凉/双皮奶/烧仙草/冰粉/椰奶西米露(30+款)</div>'
   105|                   '<div class="product-item"><span class="label">☕ 咖啡系列</span><br>美式/拿铁/生椰拿铁/摩卡/焦糖玛奇朵/瑞纳冰(8+款)</div>'
   106|                   '<div class="product-item"><span class="label">🧪 小料制备</span><br>芝士奶盖/黑糖珍珠/水晶冻/双皮奶/米麻薯/蜜制草莓</div>',
   107|        'delivery': '<strong>一、饮品SOP体系（60+款）</strong><br>'
   108|                   '• 经典饮品系列（芝芝莓莓·杨枝甘露·桃桃蜜柚·酷黑莓莓·满杯鲜橙·霸气杨梅·绿豆牛乳冰·红豆牛乳冰·生椰可可·椰子三兄弟·清补凉·牛油果芒芒等20+款）<br>'
   109|                   '• 手打柠檬茶系列（招牌·泰绿·鸭屎香·芒果·芭乐·金桔·黑加仑·青桔咸话梅·羊角蜜·霸王杯等47+款）<br>'
   110|                   '• 奶茶系列（原味·丝袜·鸭屎香·泰绿·糯香·香芋·山茶花·鸳鸯·金钻·三兄弟·红豆·布丁等19+款）<br>'
   111|                   '• 糖水甜品（双皮奶·烧仙草·冰粉·椰奶西米露·清补凉·芋圆·拉丝酸奶·桂花糖水等30+款）<br>'
   112|                   '• 小料制备卡（芝士奶盖·黑糖珍珠·水晶冻·双皮奶·米麻薯·蜜制草莓·紫苏汁·咸柠泥·火龙果汁·煮珍珠等）<br><br>'
   113|                   '<strong>二、核心配方参数</strong><br>'
   114|                   '• 茶底泡制标准（茉莉绿茶·山茶花乌龙·鸭屎香·锡兰红茶·阿萨姆红茶·工夫红茶 温度/时间/比例）<br>'
   115|                   '• 糖浆泵数换算（单糖/半糖/多糖三档）<br>'
   116|                   '• 冰块量控制（不同杯型）<br><br>'
   117|                   '<strong>三、设备清单+开店指南</strong><br>'
   118|                   '• 封口机/雪克壶/制冰机/冰沙机/保温桶<br>'
   119|                   '• 选址标准+证照办理+供应链渠道',
   120|    },
   121|    # ===== 2. 炸鸡店 =====
   122|    {
   123|        'id': 'MD_HZ_000', 'name': '韩式炸鸡专门店', 'color': '#C0392B',
   124|        'desc': '韩式炸鸡完整体系 · 20+款产品 · 含腌制/裹粉/酱料全套',
   125|        'sop_count': '40+', 'score1': '7.5', 'score2': '8.0', 'score3': '8.5', 'score4': '7.5',
   126|        'funds': '¥6-15万', 'daily': '¥2,000-5,000', 'margin': '55-65%', 'payback': '6-12个月',
   127|        'staff': '2-3人', 'area': '20-40㎡',
   128|        'note': '炸鸡店',
   129|        'products': '<div class="product-item"><span class="label">🍗 韩式炸鸡系列</span><br>经典甜辣/蒜香酱油/蜂蜜芥末/琥珀酱油/奶香芝士/脆皮/年糕无骨/起司棒/鸡腿汉堡(20+款)</div>'
   130|                   '<div class="product-item"><span class="label">🐔 鸡排/炸物系列</span><br>香鸡排/原味大鸡排/泰式酸辣鸡排/鸡锁骨/甘梅地瓜/洋葱圈(22+款)</div>'
   131|                   '<div class="product-item"><span class="label">🧂 酱料系列</span><br>韩式甜辣酱/蜂蜜芥末酱/嗨辣酱/琥珀酱/芝士酱/杰克丹尼酱/黄芥末/酸奶酱(36+款)</div>'
   132|                   '<div class="product-item"><span class="label">🧪 系统配方</span><br>核心腌料粉/核心炸粉配比/香辣-原味-奥尔良腌制系统/美式粉水粉SOP</div>'
   133|                   '<div class="product-item"><span class="label">🥟 韩式周边</span><br>辣炒年糕/紫菜包饭/石锅拌饭/炸鸡大饭团/韩式炸酱面/酸甜脆萝卜</div>'
   134|                   '<div class="product-item"><span class="label">🔧 工艺标准</span><br>裹粉手法（粉水粉/浆粉/韩式裹浆） 油温/时间标准表 腌制冰水比例</div>',
   135|        'delivery': '<strong>一、炸鸡产品SOP（20+款）</strong><br>'
   136|                   '• 韩式炸鸡系列（原味·蒜香·香辣·奥尔良·甜辣·蜂蜜芥末·琥珀·奶香芝士·脆皮·米粉）<br>'
   137|                   '• 年糕无骨炸鸡（蜜汁·香辣·VC·海鲜·原味5款）<br>'
   138|                   '• 起司棒棒鸡（原味·培根·水果·坚果·海鲜·什锦6款）<br>'
   139|                   '• 鸡排系列（香鸡排·原味·五香·芝麻·虾酱·泰式酸辣等17款）<br>'
   140|                   '• 炸鸡大饭团·鸡腿汉堡·蝴蝶炸虾·酥脆鸡柳·甘梅地瓜·葱香茄子饼·黄金洋葱圈<br><br>'
   141|                   '<strong>二、核心酱料（6+款）</strong><br>'
   142|                   '经典甜辣酱·蜂蜜芥末酱·嗨辣酱·琥珀酱·奶香芝士酱·蒜香酱油酱·黄芥末酱·柚子沙拉酱·杰克丹尼酱·四川炸鸡酱<br><br>'
   143|                   '<strong>三、腌制/裹粉系统</strong><br>'
   144|                   '韩式核心腌料粉配方·核心炸粉（堂食/外卖双版）·香辣腌料(低/中/高)·原味腌料·奥尔良腌料<br>'
   145|                   '粉水粉工艺SOP·浆粉工艺SOP·韩式裹浆SOP<br><br>'
   146|                   '<strong>四、设备清单+开店指南</strong><br>'
   147|                   '炸炉/裹粉台/保温柜/冷藏柜·选址策略·开业前7天准备清单',
   148|    },
   149|    # ===== 3. 粉面店 =====
   150|    {
   151|        'id': 'MD_FM_000', 'name': '粉面/快餐店', 'color': '#27ae60',
   152|        'desc': '粉面饭完整方案 · 20+款主食+浇头 · 出餐快利润稳',
   153|        'sop_count': '25+', 'score1': '7.0', 'score2': '8.5', 'score3': '8.0', 'score4': '6.5',
   154|        'funds': '¥5-10万', 'daily': '¥1,500-3,500', 'margin': '55-65%', 'payback': '5-10个月',
   155|        'staff': '2人', 'area': '20-40㎡',
   156|        'note': '粉面店',
   157|        'products': '<div class="product-item"><span class="label">🍜 粉面系列</span><br>柳州螺蛳粉/武汉热干面/长沙牛肉粉/淮南牛肉汤粉/安徽牛肉板面(5+款)</div>'
   158|                   '<div class="product-item"><span class="label">🍳 炒饭/炒面系列</span><br>馋嘴肉炒饭/孜然炒面/黑椒牛扒饭/蒜香虾尾/香辣炒花甲(7+款)</div>'
   159|                   '<div class="product-item"><span class="label">🥣 汤品系列</span><br>逍遥镇胡辣汤/羊肉胡辣汤/肉丁胡辣汤/面筋胡辣汤(5+款)</div>'
   160|                   '<div class="product-item"><span class="label">🧂 浇头/酱料</span><br>葱香油/江湖酱/万能拌面酱/辣子鸡丁/网红炒鸡/老北京炸酱(5+款)</div>'
   161|                   '<div class="product-item"><span class="label">🥟 早点搭配</span><br>灌汤包/酱肉包/猪肉包/千层饼/鸡蛋饼(可选配)</div>',
   162|        'delivery': '<strong>一、粉面饭SOP（12+款）</strong><br>'
   163|                   '• 柳州螺蛳粉·武汉热干面·长沙牛肉粉·淮南牛肉汤粉·安徽牛肉板面·兰州拉面<br>'
   164|                   '• 馋嘴肉炒饭·孜然炒面·黑椒牛扒饭·香辣炒花甲·蒜香炒虾尾·干炒牛河<br><br>'
   165|                   '<strong>二、浇头/酱料SOP（5+款）</strong><br>'
   166|                   '葱香油·江湖酱(复合辣酱)·万能拌面酱·辣子鸡丁浇头·网红炒鸡浇头·老北京炸酱<br><br>'
   167|                   '<strong>三、汤底系统</strong><br>'
   168|                   '逍遥镇胡辣汤·羊肉胡辣汤·面筋胡辣汤·大料粉配方<br><br>'
   169|                   '<strong>四、设备清单+开店指南</strong><br>'
   170|                   '煮面炉/炒灶/保温汤池/冰柜·出餐动线设计·备料时间表',
   171|    },
   172|    # ===== 4. 熟食/卤味店 =====
   173|    {
   174|        'id': 'MD_LW_000', 'name': '熟食/卤味店', 'color': '#8B4513',
   175|        'desc': '酱卤熟食完整方案 · 10+款经典卤味 · 百年老卤传承',
   176|        'sop_count': '20+', 'score1': '6.5', 'score2': '8.0', 'score3': '8.5', 'score4': '7.0',
   177|        'funds': '¥4-8万', 'daily': '¥1,000-3,000', 'margin': '50-60%', 'payback': '4-8个月',
   178|        'staff': '1-2人', 'area': '10-25㎡',
   179|        'note': '卤味店',
   180|        'products': '<div class="product-item"><span class="label">🐓 整鸡系列</span><br>椒麻鸡/叫花鸡/桶子鸡/道口烧鸡/沟帮子熏鸡/茶香鸡/酱卤牛肉/麻油鸡(8+款)</div>'
   181|                   '<div class="product-item"><span class="label">🥩 卤味系列</span><br>川香辣卤/鸭货系列/鸡货系列/麻辣鸭头/卤藕片/万能卤水(7+款)</div>'
   182|                   '<div class="product-item"><span class="label">🥗 冷吃系列</span><br>麻辣鸡爪/麻辣鸭头/卤藕片/红油拌猪头肉/捞汁小海鲜(5+款)</div>'
   183|                   '<div class="product-item"><span class="label">🧂 酱料系列</span><br>川式五香卤水/万能卤水/凉菜万能汁/红油抄手酱(关联酱料)</div>',
   184|        'delivery': '<strong>一、整鸡系列SOP（8+款）</strong><br>'
   185|                   '椒麻鸡（完整腌卤工艺）·叫花鸡（郑州版）·桶子鸡·道口烧鸡·沟帮子熏鸡·茶香鸡·酱卤牛肉·麻油鸡<br><br>'
   186|                   '<strong>二、卤味系列SOP（7+款）</strong><br>'
   187|                   '川香辣卤方案·鸭货卤制·鸡货卤制·万能卤水配方·五香卤水·酱香卤料·卤味香辣炒鸡料<br><br>'
   188|                   '<strong>三、冷吃/凉菜SOP</strong><br>'
   189|                   '麻辣鸡爪·麻辣鸭头·卤藕片·红油拌猪头肉·捞汁小海鲜·凉菜万能汁<br><br>'
   190|                   '<strong>四、老卤养护+设备清单</strong><br>'
   191|                   '卤水循环使用/保存方法·老卤越卤越香的秘密·日均出餐流程',
   192|    },
   193|    # ===== 5. 火锅/酸汤店 =====
   194|    {
   195|        'id': 'MD_HG_000', 'name': '火锅/酸汤/串串店', 'color': '#E74C3C',
   196|        'desc': '火锅底料+酱料完整方案 · 酸汤/麻辣/番茄/金汤多口味',
   197|        'sop_count': '15+', 'score1': '7.5', 'score2': '7.5', 'score3': '7.5', 'score4': '7.0',
   198|        'funds': '¥8-20万', 'daily': '¥2,000-6,000', 'margin': '55-65%', 'payback': '8-14个月',
   199|        'staff': '3-5人', 'area': '40-80㎡',
   200|        'note': '火锅店',
   201|        'products': '<div class="product-item"><span class="label">🫕 锅底系列</span><br>凯里酸汤鱼/麻辣串串香/酸辣粉冒菜/贵州红酸汤/金汤底料/番茄火锅(6+款)</div>'
   202|                   '<div class="product-item"><span class="label">🌶️ 酱料系列</span><br>红烧汁/麻辣烫底料/酱香卤料/五香卤水/老北京炸酱/椒香麻辣酱(36+款)</div>'
   203|                   '<div class="product-item"><span class="label">🥗 冷吃/小食</span><br>捞汁小海鲜/麻辣鸡爪/卤藕片/凉菜万能汁(搭配)</div>'
   204|                   '<div class="product-item"><span class="label">🧂 蘸料配方</span><br>蒜蓉酱/甜辣酱/芝麻酱/沙茶酱/香油碟(21+款)</div>',
   205|        'delivery': '<strong>一、锅底SOP（6+款）</strong><br>'
   206|                   '凯里酸汤鱼·麻辣串串香·贵州红酸汤·金汤底料·浓汤番茄火锅底料·麻辣烫底料<br><br>'
   207|                   '<strong>二、酱料/底料（36+款）</strong><br>'
   208|                   '红烧汁·酱香卤料·五香卤水·老北京炸酱·椒香麻辣酱·韩式辣椒酱·叉烧酱·金银蒜蓉酱·凉拌菜复制酱油·关东煮蘸酱·糖醋酱·日式照烧酱·红油抄手酱等<br><br>'
   209|                   '<strong>三、蘸料/小料系统</strong><br>'
   210|                   '蒜蓉酱·甜辣酱·麻酱面酱·芝麻酱·沙茶酱·香油碟·羊肉炉蘸酱·贝类海鲜蘸酱·清蒸蟹虾蘸酱等<br><br>'
   211|                   '<strong>四、设备清单+开店指南</strong><br>'
   212|                   '灶台/汤桶/冰柜/排烟·翻台率策略·食材供应链',
   213|    },
   214|]
   215|
   216|def gen_all():
   217|    for store in STORES:
   218|        cid = store['id']
   219|        
   220|        # 生成M3卡HTML
   221|        html = M3_TPL.format(**store)
   222|        
   223|        path = os.path.join(CARDS_DIR, f"{cid}_{store['name'].replace('/', '·')}.html")
   224|        with open(path, 'w', encoding='utf-8') as f:
   225|            f.write(html)
   226|        print(f"  [M3] {cid} {store['name']}")
   227|        
   228|        # 更新decision-engine.html
   229|        update_de(cid, store)
   230|
   231|def update_de(store_id, store):
   232|    """在decision-engine.html添加门店卡片入口"""
   233|    import re
   234|    with open(DE_FILE, encoding='utf-8') as f:
   235|        content = f.read()
   236|    
   237|    # 跳过已有的
   238|    if store['name'] in content:
   239|        print(f"    [跳过] 已在DE中: {store['name']}")
   240|        return
   241|    
   242|    # 在最后一个门店卡后、选址测评前插入
   243|    card_html = '\n      <a class="recipe-card" href="cards/{id}_{name_noslash}.html">\n        <div class="rc-icon">{icon}</div>\n        <div class="rc-name">{name}</div>\n        <div class="rc-badge">M3新版</div>\n        <div class="rc-price">¥699</div>\n      </a>'
   244|    
   245|    icons = {'精品奶茶店': '🥤', '韩式炸鸡专门店': '🍗', '粉面/快餐店': '🍜', '熟食/卤味店': '🥩', '火锅/酸汤/串串店': '🫕'}
   246|    icon = icons.get(store['name'], '🏪')
   247|    name_noslash = store['name'].replace('/', '·')
   248|    
   249|    insert = card_html.format(id=store_id, name=store['name'], icon=icon, name_noslash=name_noslash)
   250|    
   251|    # 找插入点：最后一个recipe-card后面、选址测评前
   252|    markers = ['<!-- ===== ⑥ 选址测评 ===== -->', '<div class="location-section"']
   253|    for marker in markers:
   254|        if marker in content:
   255|            # 找这个marker之前最近的</a> 和 <div>结构
   256|            pos = content.find(marker)
   257|            before = content[:pos]
   258|            last_a = before.rfind('</a>')
   259|            if last_a > 0:
   260|                content = content[:last_a+4] + insert + content[last_a+4:]
   261|                with open(DE_FILE, 'w', encoding='utf-8') as f:
   262|                    f.write(content)
   263|                print(f"    [DE已加] {store['name']}")
   264|                return
   265|    
   266|    print(f"    [跳过] 未找到插入位置")
   267|
   268|if __name__ == '__main__':
   269|    gen_all()
   270|    print(f"\n✅ 共生成 {len(STORES)} 张M3门店决策卡")
   271|