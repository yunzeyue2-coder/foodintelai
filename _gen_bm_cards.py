# 生成 拌面·浇头面 品类 4张卡
# 编号规则：BM_001~BM_004 (BM = 拌面/Braised Noodle)
# 数据源：桌面 面/ 文件夹内容

with open('/Users/mac/Desktop/青葵/foodintelai-site/cards/CZ_036.html') as f:
    template = f.read()

# 模板中所有关键词替换函数
def replace_all(c, old, new):
    return c.replace(old, new)

def make_noodle_card(data):
    c = template[:]
    
    c = replace_all(c, 'CZ_036', data['id'])
    c = replace_all(c, '铁板炒饭', data['name'])
    c = replace_all(c, '铁板猛火快炒 · 酱料为核心壁垒 · 标准化出餐', data['sub'])
    c = replace_all(c, '#铁板炒饭', data['tag1'])
    c = replace_all(c, '#猛火快炒', data['tag2'])
    c = replace_all(c, '#标准化', data['tag3'])
    c = replace_all(c, '🔥 炒饭炒面花甲', data['badge'])
    c = replace_all(c, '启动资金：3-8万', f'启动资金：{data["invest"]}')
    c = replace_all(c, '日营收：¥600-1500', f'日营收：{data["income"]}')
    c = replace_all(c, '毛利率：60-65%', f'毛利率：{data["gross"]}')
    c = replace_all(c, '回本周期：1-2个月', f'回本周期：{data["roi"]}')
    c = replace_all(c, '沧林食品 · 产品编号 CZ_036', f'沧林食品 · 产品编号 {data["id"]}')
    c = replace_all(c, '「CZ_036铁板炒饭」', f'「{data["id"]}{data["name"]}」')
    
    # 产品说
    old_desc_start = c.find('<div class="story">')
    old_desc_end = c.find('</div>\n</div>\n\n<div class="section">')
    old_desc = c[old_desc_start:old_desc_end]
    new_desc = f'<div class="story">\n{data["desc"]}\n</div>'
    c = replace_all(c, old_desc, new_desc)
    
    # 成本行
    for i in range(5):
        c = replace_all(c, data['cost_old'][i][0], data['cost'][i][0])
        c = replace_all(c, data['cost_old'][i][1], data['cost'][i][1])
    c = replace_all(c, data['cost_old_total'], data['total_cost'])
    c = replace_all(c, data['cost_old_sell'], data['sell_price'])
    
    # ROI
    old_roi_start = c.find('<div class="roi">')
    old_roi_end = c.find('</div>\n</div>', old_roi_start) + 6
    old_roi = c[old_roi_start:old_roi_end]
    c = replace_all(c, old_roi, data['roi_html'])
    
    # 配方
    old_rec_start = c.find('<div class="s-title">🔬 核心配方（付费解锁完整版）</div>')
    old_rec = c[old_rec_start:]
    old_rec_end = old_rec.find('</div>\n</div>\n\n<div class="section">')
    old_rec = old_rec[:old_rec_end+6]
    c = replace_all(c, old_rec, data['recipe_html'])
    
    # 工艺
    old_proc_start = c.find('<div class="s-title">⚙️ 工艺流程</div>')
    old_proc = c[old_proc_start:]
    old_proc_end = old_proc.find('</div>\n</div>\n\n<div class="section">')
    old_proc = old_proc[:old_proc_end+6]
    c = replace_all(c, old_proc, data['process_html'])
    
    # 风险
    old_risk_start = c.find('<div class="s-title">⚠️ 三大风险</div>')
    old_risk = c[old_risk_start:]
    old_risk_end = old_risk.find('</div>\n\n<div class="section">')
    old_risk = old_risk[:old_risk_end]
    c = replace_all(c, old_risk, data['risk_html'])
    
    # 场景
    scene_html = '\n'.join([f'<span class="scene-item">{s}</span>' for s in data['scenes']])
    old_scene = c[c.find('<div class="scene-grid">'):]
    old_scene_end = old_scene.find('</div>\n</div>') + 6
    c = replace_all(c, old_scene, f'<div class="scene-grid">\n{scene_html}\n</div>')
    
    # 搭配
    pair_html = '\n'.join([f'<div class="pair-item"><span class="p-name">{p[0]}</span><span class="p-price">{p[1]}</span></div>' for p in data['pairs']])
    old_pair_start = c.find('<div class="s-title">🤝 搭配销售</div>')
    old_pair = c[old_pair_start:]
    old_pair_end = old_pair.find('</div>\n</div>') + 6
    old_pair = old_pair[:old_pair_end]
    c = replace_all(c, old_pair, f'<div class="s-title">🤝 搭配销售</div>\n{pair_html}</div>')
    
    # 话术
    old_talk_start = c.find('<div class="talk">')
    old_talk = c[old_talk_start:]
    old_talk_end = old_talk.find('</div>\n</div>') + 6
    old_talk = old_talk[:old_talk_end]
    c = replace_all(c, old_talk, f'<div class="talk">\n{data["talk"]}\n</div>')
    
    # 避坑
    tip_html = '\n'.join([f'<div class="tip-item">{t}</div>' for t in data['tips']])
    old_tips_start = c.find('<div class="s-title">🚫 避坑指南</div>')
    old_tips = c[old_tips_start:]
    old_tips_end = old_tips.find('</div>\n</div>\n\n<div class="pay"')
    old_tips = old_tips[:old_tips_end+18]
    c = replace_all(c, old_tips, f'<div class="s-title">🚫 避坑指南</div>\n{tip_html}\n</div>\n</div>\n\n<div class="pay"')
    
    return c

# 在卡数据中内联cost_old
def add_cost_old(data):
    data['cost_old'] = [
        ('炒饭酱（20-30g）', '¥0.8-1.2'),
        ('米饭（300-350g）', '¥0.4-0.6'),
        ('鸡蛋+香肠+配菜', '¥1.5-2.0'),
        ('包装/油/燃气', '¥0.8-1.2'),
        ('包装/油/燃气', '¥0.8-1.2'),
    ]
    data['cost_old_total'] = '¥3.5-5.0'
    data['cost_old_sell'] = '¥12-18（堂食）/ ¥15-22（外卖）'
    return data

# 定义4张卡
cards_noodle = [
    {
        'id': 'BM_001',
        'name': '网红炒鸡拌面',
        'sub': '猛火现炒浇头 · 2025-2026当红品类 · 王繁星同款路线',
        'tag1': '#炒鸡拌面', 'tag2': '#本帮浇头', 'tag3': '#猛火现炒',
        'badge': '🍝 拌面·浇头面',
        'invest': '5-12万', 'income': '¥800-2000', 'gross': '58-65%', 'roi': '2-3个月',
        'desc': '炒鸡拌面是2025-2026年粉面赛道最热单品。本帮面馆靠"猛火现炒浇头+碱水面"模式快速崛起，王繁星面馆已超90家门店。核心壁垒在炒鸡浇头——鸡腿肉+香菇+复合酱料，猛火爆炒出香气，浇在碱水面上。出餐3-4分钟/份，翻台率极高。',
        'cost': [
            ('鸡腿肉（份）', '¥3.0-4.0'),
            ('碱水面（份）', '¥0.6-0.8'),
            ('香菇+配菜', '¥0.8-1.2'),
            ('酱料+调料摊', '¥1.2-1.8'),
            ('燃气+包装', '¥0.6-1.0'),
        ],
        'total_cost': '¥6.2-8.8',
        'sell_price': '¥18-25（堂食）/ ¥22-30（外卖）',
        'roi_html': '''<div class="roi">
<div class="roi-b c"><div>时产</div><div class="d">¥240-450</div><div>同时出4份</div></div>
<div class="roi-b n"><div>日营收</div><div class="d">¥800-2000</div><div>午晚高峰</div></div>
<div class="roi-b i"><div>月净利</div><div class="d">¥1.2-2.5万</div><div>含房租人工</div></div>
</div>''',
        'recipe_html': '''<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
<strong>炒鸡浇头配比框架：</strong><br>
鸡腿肉10斤 · 啤酒1瓶 · 蒸鱼豉油 · 辣鲜露 · 香菇2斤<br>
蒜末300g · 洋葱末300g · 姜末300g · 豆豉300g<br>
柱候酱100g · 花生酱150g · 东北大酱300g · 江湖酱300g<br>
红99火锅底料150g · 红曲粉15g · 辣椒段100g<br><br>
<strong>出品流程：</strong>鸡丁炸至金黄→锅中爆香姜蒜洋葱→加酱料炒香→加鸡丁→加啤酒焖3-5分钟→浇在煮好的碱水面上<br><br>
<em style="color:#b5aaa0;font-size:11px">以上为配方框架。完整版含：鸡肉腌制配方、复合酱料精确克数、炒制火候控制、4种口味变体。</em>
</div>''',
        'process_html': '''<div class="s-title">⚙️ 工艺流程</div>
<div class="story">
1. 鸡腿肉切丁，加料酒、生抽腌制15分钟<br>
2. 油温5成热，下鸡丁炸至金黄色捞出<br>
3. 锅中留底油，煸香姜末、蒜末、洋葱末<br>
4. 加豆豉、柱候酱、花生酱、东北大酱、江湖酱炒香<br>
5. 加火锅底料、香菇末翻炒出红油<br>
6. 下鸡丁，加啤酒1瓶，中火焖3-5分钟<br>
7. 加蒸鱼豉油、辣鲜露调味<br>
8. 碱水面煮至8分熟，过凉水<br>
9. 面入碗，浇炒鸡浇头，撒葱花<br><br>
<strong>关键控制点：</strong>炒酱料要小火慢炒不能糊锅；鸡肉先炸后焖口感才对；面煮好过凉水防坨
</div>''',
        'risk_html': '''<div class="s-title">⚠️ 风险提示</div>
<div class="risk-item"><span>🔴 浇头备料压力</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">浇头现炒需要高峰期提前备料，备多了损耗备少了断货</div>
<div class="risk-item"><span>🔴 出餐速度瓶颈</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">现炒模式决定了高峰期极限，单人最多同时炒3份浇头</div>
<div class="risk-item"><span>🟡 味道一致性</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">不同厨师炒出来的浇头味道有差异，酱料必须标准化预调</div>''',
        'scenes': ['本帮面馆', '美食广场档口', '外卖专营', '写字楼午餐', '社区面店'],
        'pairs': [('炒鸡拌面（基础）', '¥18-22'), ('炒鸡拌面（加卤蛋）', '¥20-25'), ('炒鸡拌面（加豆皮）', '¥22-26'), ('冰镇酸梅汤', '¥5-8'), ('卤味拼盘小份', '¥12-18')],
        'talk': '「老板，炒鸡拌面是我们招牌。鸡腿肉猛火现炒浇在碱水面上，酱料是我们自己调的。要不要加个卤蛋？」',
        'tips': ['浇头酱料必须标准化预调，每天早上按比例兑好，不能现炒现调', '碱水面煮到8分熟就捞出过凉水，放久了会坨成团', '高峰期前把鸡丁提前炸好，客人下单只需加酱料现炒1分钟即可', '外卖配送距离控制在3公里内，超过20分钟面条口感掉一半']
    },
    {
        'id': 'BM_002',
        'name': '辣子鸡拌面',
        'sub': '川式辣子鸡+拌面组合 · 草药粉独门配方 · 夜宵爆款',
        'tag1': '#辣子鸡拌面', 'tag2': '#川式风味', 'tag3': '#草药粉秘方',
        'badge': '🍝 拌面·浇头面',
        'invest': '5-12万', 'income': '¥600-1800', 'gross': '60-68%', 'roi': '2-3个月',
        'desc': '辣子鸡拌面是炒鸡拌面的川式变体，辣味更重、辨识度更高。核心差异在草药粉——甘草、丁香、肉蔻、白芷等20+种香料打粉，赋予鸡肉复合香气。加上猪板油增香、红99底料打底，麻辣鲜香全占齐。',
        'cost': [
            ('鸡丁（份）', '¥2.5-3.5'),
            ('碱水面（份）', '¥0.6-0.8'),
            ('香菇+线椒+配菜', '¥1.0-1.5'),
            ('酱料+草药粉+调料', '¥1.5-2.0'),
            ('燃气+包装', '¥0.6-1.0'),
        ],
        'total_cost': '¥6.2-8.8',
        'sell_price': '¥18-25（堂食）/ ¥22-30（外卖）',
        'roi_html': '''<div class="roi">
<div class="roi-b c"><div>时产</div><div class="d">¥180-380</div><div>单人操作</div></div>
<div class="roi-b n"><div>日营收</div><div class="d">¥600-1800</div><div>午/晚餐+夜宵</div></div>
<div class="roi-b i"><div>月净利</div><div class="d">¥1.0-2.2万</div><div>含房租人工</div></div>
</div>''',
        'recipe_html': '''<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
<strong>草药粉配方（核心壁垒）：</strong><br>
甘草5g · 丁香2g · 肉蔻10g · 陈皮10g · 辛夷10g<br>
槟榔片10g · 当归3g · 香砂20g · 花椒20g · 红栀子5g<br>
香菜籽15g · 白蔻15g · 白芷15g · 山奈15g · 小茴香20g<br>
香叶10g · 肉桂15g · 八角20g · 荜拨15g · 草果15g → 打成粉<br><br>
<strong>辣子鸡浇头框架：</strong>鸡丁10斤 · 猪板油3斤 · 香菇750g · 红99火锅底料400g · 黄豆酱400g · 老干妈2瓶 · 草药粉30g<br><br>
<em style="color:#b5aaa0;font-size:11px">完整版含：草药粉精确比例、鸡丁腌制工艺、不同辣度调整方案、拌面酱配比。</em>
</div>''',
        'process_html': '''<div class="s-title">⚙️ 工艺流程</div>
<div class="story">
1. 鸡腿肉切丁，加料酒、白胡椒粉腌制<br>
2. 油温5成热，下鸡丁大火炸至微金黄色捞出<br>
3. 锅中下猪板油3斤，小火熬出油<br>
4. 煸香姜末、洋葱末、香菇末<br>
5. 加草药粉30g、灯笼椒粉30g、白胡椒粉30g炒香<br>
6. 加黄豆酱、红99火锅底料，小火炒散<br>
7. 加老干妈、老抽调色，下鸡丁翻炒3-5分钟<br>
8. 下线椒末拌匀，加鸡精味精调味出锅<br>
9. 碱水面煮熟，打底拌面酱50g拌匀，浇上辣子鸡丁100g<br><br>
<strong>关键控制点：</strong>草药粉是核心壁垒，缺一味风味就偏；猪板油必须熬出油再用；线椒末最后下保持鲜辣
</div>''',
        'risk_html': '''<div class="s-title">⚠️ 风险提示</div>
<div class="risk-item"><span>🔴 草药粉备料麻烦</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">20+种香料备料复杂，缺一种风味就偏，在调料市场不一定能齐</div>
<div class="risk-item"><span>🟡 辣度接受度</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">不同地区辣度接受度差异大，需要备不辣/微辣/中辣/重辣四档</div>
<div class="risk-item"><span>🟡 口味辨识度</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">草药粉风味独特但并非所有人都接受，需要搭配普通款做分流</div>''',
        'scenes': ['川味面馆', '夜宵大排档', '外卖专营', '美食广场'],
        'pairs': [('辣子鸡拌面（微辣）', '¥18-22'), ('辣子鸡拌面（重辣）', '¥20-25'), ('冰粉', '¥6-8'), ('凉糕', '¥8-10'), ('酸梅汤', '¥5-8')],
        'talk': '「辣子鸡拌面是我们特色，鸡肉先用20多种中药草粉腌过再炸，跟别家的辣子鸡完全不是一个味。你敢不敢试重辣？」',
        'tips': ['草药粉每次打一周的量，密封冷藏保存，打多了香气会散', '辣度用不同类型辣椒调节——微辣用新一代、中辣用灯笼椒、重辣加小米辣粉', '不吃辣的客人可以点原味炒鸡拌面，同一个浇头不加辣椒粉即可', '辣子鸡浇头冷藏可存3天，冷冻可存2周，备货灵活']
    },
    {
        'id': 'BM_003',
        'name': '招牌炸酱拌面',
        'sub': '老北京炸酱工艺 · 复合酱料核心 · 出餐速度极快',
        'tag1': '#炸酱拌面', 'tag2': '#老北京风味', 'tag3': '#复合酱料',
        'badge': '🍝 拌面·浇头面',
        'invest': '3-8万', 'income': '¥500-1500', 'gross': '62-70%', 'roi': '1-2个月',
        'desc': '炸酱拌面是拌面品类的基本款，操作门槛最低、毛利最高。核心在炸酱——干黄酱+黄豆酱+甜面酱+蚝油复合调配，配上五花肉丁炸出油香。出餐速度极快（1分钟/份），一人能撑全店。2025年家庭场景炸酱市场也在增长。',
        'cost': [
            ('炸酱（份/50g）', '¥0.8-1.2'),
            ('碱水面（份）', '¥0.6-0.8'),
            ('黄瓜丝+豆芽+配菜', '¥0.3-0.5'),
            ('燃气+包装', '¥0.4-0.8'),
        ],
        'total_cost': '¥2.1-3.3',
        'sell_price': '¥12-16（堂食）/ ¥15-20（外卖）',
        'roi_html': '''<div class="roi">
<div class="roi-b c"><div>时产</div><div class="d">¥300-500</div><div>极高出餐效率</div></div>
<div class="roi-b n"><div>日营收</div><div class="d">¥500-1500</div><div>全天候营业</div></div>
<div class="roi-b i"><div>月净利</div><div class="d">¥8000-1.8万</div><div>含房租人工</div></div>
</div>''',
        'recipe_html': '''<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
<strong>老北京炸酱配比框架：</strong><br>
五花肉丁30斤 · 海天黄豆酱 · 六必居干黄酱<br>
大豆油 · 姜末 · 蒜末 · 蚝油 · 味精 · 十三香<br><br>
<strong>制作：</strong>五花肉丁下锅煸出油→加姜蒜末炒香→加混合酱料→小火慢炸30分钟→出锅前加味精和十三香<br><br>
<em style="color:#b5aaa0;font-size:11px">完整版含：干黄酱和黄豆酱精确配比、炸酱火候控制、不同保存方式下的保质期、面条选择建议。</em>
</div>''',
        'process_html': '''<div class="s-title">⚙️ 工艺流程</div>
<div class="story">
1. 五花肉切小丁（0.5cm见方）<br>
2. 干黄酱用温水泄开，黄豆酱备好<br>
3. 锅中下大豆油，烧至5成热下五花肉丁<br>
4. 小火煸炒至肉丁出油、表面微焦<br>
5. 下姜末、蒜末炒香<br>
6. 下泄好的干黄酱、黄豆酱、甜面酱，小火慢炒<br>
7. 加蚝油提鲜，持续翻炒30分钟至酱色变深<br>
8. 加味精、十三香出锅<br>
9. 碱水面煮熟过凉水，浇上炸酱，配黄瓜丝、豆芽<br><br>
<strong>关键控制点：</strong>炸酱必须小火慢炸30分钟，急火会糊；肉丁先煸出油再下酱；酱和油比例约3:1
</div>''',
        'risk_html': '''<div class="s-title">⚠️ 风险提示</div>
<div class="risk-item"><span>🟡 同质化严重</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">炸酱面遍地都是，普通炸酱没有辨识度，必须在酱料配方上做差异</div>
<div class="risk-item"><span>🟢 门槛较低</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">操作简单，出餐快，适合餐饮新手起步，但竞争也最激烈</div>
<div class="risk-item"><span>🟡 价格天花板</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">炸酱面客单价天花板15-20元，利润增长靠走量不是提价</div>''',
        'scenes': ['社区面馆', '小吃档口', '外卖专营', '早餐/午餐'],
        'pairs': [('炸酱拌面', '¥12-15'), ('炸酱拌面（加肉）', '¥15-18'), ('炸酱拌面（加卤蛋）', '¥14-17'), ('绿豆汤', '¥4-6'), ('凉菜拼盘', '¥8-12')],
        'talk': '「炸酱面是我们自己炸的酱，六必居干黄酱+五花肉丁小火炸了半小时，你拌开闻闻这个酱香。」',
        'tips': ['炸酱一次做一锅冷藏可存7天，冷冻可存1个月，是拌面品类里最省事的', '配菜要切细丝（黄瓜、豆芽、心里美），粗了影响口感', '炸酱拌面不做外卖——面坨了酱也坨了，建议外卖只做炸酱凉面', '自己炸酱成本2-3元/份，批发市场的预包装炸酱也要1.5元，自己做性价比更高']
    },
    {
        'id': 'BM_004',
        'name': '葱油拌面+本帮浇头',
        'sub': '上海本帮面经典 · 葱油是灵魂 · 浇头换着卖',
        'tag1': '#葱油拌面', 'tag2': '#本帮浇头', 'tag3': '#百搭单品',
        'badge': '🍝 拌面·浇头面',
        'invest': '3-6万', 'income': '¥400-1200', 'gross': '65-75%', 'roi': '1-2个月',
        'desc': '葱油拌面是上海本帮面的灵魂单品。一碗光面+葱油+酱油就能卖，加浇头就是升级版。葱油是核心壁垒——小葱+洋葱+香料炸出的葱香油，配上复合酱油，成本不到2块卖10-12块。2025年本帮面赛道爆发式增长，葱油拌面是每家的必上单品。',
        'cost': [
            ('葱油+酱油（份）', '¥0.4-0.6'),
            ('碱水面（份）', '¥0.6-0.8'),
            ('浇头（葱油+酱油）', '¥0.4-0.6'),
            ('燃气+包装', '¥0.4-0.6'),
        ],
        'total_cost': '¥1.8-2.6（不含浇头）',
        'sell_price': '¥10-12（基础）/ ¥15-22（加浇头）',
        'roi_html': '''<div class="roi">
<div class="roi-b c"><div>时产</div><div class="d">¥350-600</div><div>出餐30秒/份</div></div>
<div class="roi-b n"><div>日营收</div><div class="d">¥400-1200</div><div>搭配浇头上价</div></div>
<div class="roi-b i"><div>月净利</div><div class="d">¥6000-1.5万</div><div>含房租人工</div></div>
</div>''',
        'recipe_html': '''<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
<strong>葱油配方框架：</strong><br>
小葱500g · 洋葱200g · 大葱100g · 香菜50g<br>
八角2个 · 桂皮1小段 · 香叶3片 · 大豆油1000g<br><br>
<strong>复合酱油：</strong>生抽500g · 老抽200g · 白糖150g · 水200g · 鸡精30g，熬开即可<br><br>
<strong>出品：</strong>碱水面煮熟→淋1勺葱油→淋1勺复合酱油→拌匀→加浇头<br><br>
<em style="color:#b5aaa0;font-size:11px">完整版含：5种浇头配方（酱爆猪肝/辣肉/大排/素鸡/雪菜肉丝）、葱油炸制要点、酱油调配比例。</em>
</div>''',
        'process_html': '''<div class="s-title">⚙️ 工艺流程</div>
<div class="story">
<strong>葱油炸制：</strong><br>
1. 小葱切段（葱白葱叶分开），洋葱切丝，大葱切段<br>
2. 锅中下大豆油，冷油下八角、桂皮、香叶，小火炸香<br>
3. 下葱白部分、洋葱丝、大葱段，小火炸至金黄<br>
4. 下葱叶部分、香菜，继续小火炸至焦脆<br>
5. 过滤取油，葱油即成<br><br>
<strong>复合酱油调制：</strong><br>
生抽500g+老抽200g+白糖150g+水200g+鸡精30g，煮开即可<br><br>
<strong>出品（30秒）：</strong><br>
面条煮熟捞出→淋葱油1勺→淋复合酱油1勺→拌匀→加浇头→撒葱花
</div>''',
        'risk_html': '''<div class="s-title">⚠️ 风险提示</div>
<div class="risk-item"><span>🟢 门槛极低</span><span class="risk-stars"><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">葱油拌面是所有面品类里门槛最低的，关键在葱油品质</div>
<div class="risk-item"><span>🟡 基础款利润薄</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">纯葱油拌面卖10-12块利润薄，必须搭配浇头拉客单价</div>
<div class="risk-item"><span>🟡 浇头需要多元化</span><span class="risk-stars"><span class="on">★</span><span class="on">★</span><span class="on">★</span></span></div>
<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">没有4-6款浇头撑不住菜单，每多一款浇头就多一份备料压力</div>''',
        'scenes': ['本帮面馆', '小吃档口', '社区店', '早点摊', '外卖专营'],
        'pairs': [('葱油拌面（基本款）', '¥10-12'), ('酱爆猪肝拌面', '¥18-22'), ('辣肉拌面', '¥16-20'), ('四喜烤麸浇头', '¥6-8'), ('雪菜肉丝浇头', '¥5-8')],
        'talk': '「葱油是我们自己炸的，上海本帮面那个味。光面10块，加个浇头15块，一顿饭搞定。」',
        'tips': ['葱油一次炸5斤，密封冷藏可存2周。每天用多少取多少，不要反复加热', '复合酱油和葱油分开保存，客人点单时先放酱油再放葱油最后拌匀', '浇头提前做好保温放着，客人点单时直接浇，不能现炒', '葱油拌面外卖问题不大——面和酱料分开装，客人自己拌']
    },
]

# 生成
# 在生成之前给每个卡数据加上cost_old
cards_noodle = [add_cost_old(c) for c in cards_noodle]

import os
out_dir = '/Users/mac/Desktop/青葵/foodintelai-site/cards/'
for card_data in cards_noodle:
    html = make_noodle_card(card_data)
    path = os.path.join(out_dir, f"{card_data['id']}.html")
    with open(path, 'w') as f:
        f.write(html)
    print(f"✅ {card_data['id']}.html 已生成 ({len(html)} 字符)")

print(f"\n✨ 4张拌面·浇头面卡片全部生成完毕")
