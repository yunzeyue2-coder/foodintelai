# 生成汤料卤水T3卡：川式五香卤水、万能卤水+爆炒料、高汤熬制
import os

# 读TL_019模板的完整内容
with open('/Users/mac/Desktop/青葵/foodintelai-site/cards/TL_019.html', 'r') as f:
    tl19 = f.read()

def gen_tl_card(card_id, name, sub, emoji, cost_items, total_cost, sell_price, daily_income, desc_text, skill_text, recipe_text, risk_items, scenes, pairs, talk_text, tips):
    """生成汤料卤水卡"""
    card = tl19[:]
    
    card = card.replace('TL-019', card_id)
    card = card.replace('TL_019', card_id)
    card = card.replace('牛肉板面浇头', name)
    card = card.replace('安徽牛肉板面专用浇头，30+香辛料熬制，卤香浓郁，一勺定味', sub)
    card = card.replace('沧林食品 · 产品编号 TL_019', f'沧林食品 · 产品编号 {card_id}')
    card = card.replace('TL_019.html', f'{card_id}.html')
    
    # 替换利润模型
    cost_rows = ''
    for item_name, item_price in cost_items:
        cost_rows += f'<div class="row"><span>{item_name}</span><span class="v">{item_price}</span></div>\n'
    
    old_cost = '''<div class="cost-box">
<div class="row"><span>牛肉浇头（份）</span><span class="v">¥2.5-3.5</span></div>
<div class="row"><span>面条/粉（份）</span><span class="v">¥0.8-1.2</span></div>
<div class="row"><span>配菜（豆皮/卤蛋）</span><span class="v">¥1.0-1.5</span></div>
<div class="row"><span>汤底+调料</span><span class="v">¥0.5-0.8</span></div>
<div class="row"><span>燃气+包装</span><span class="v">¥0.6-1.0</span></div>
<div class="row tot"><span>总成本</span><span class="v">¥5.4-8.0</span></div>
<div class="row" style="border:none;margin-top:0;padding-top:6px"><span>建议售价</span><span class="v">¥15-20（堂食）/ ¥18-25（外卖）</span></div>
</div>'''
    
    new_cost = f'''<div class="cost-box">
{cost_rows}<div class="row tot"><span>总成本</span><span class="v">{total_cost}</span></div>
<div class="row tot" style="border:none;margin-top:0;padding-top:6px"><span>建议售价</span><span class="v">{sell_price}</span></div>
</div>'''
    card = card.replace(old_cost, new_cost)

    # 替换产品说
    old_desc = card[card.find('<div class="s-title">💡 产品说</div>'):]
    old_desc = old_desc[:old_desc.find('</div>\n</div>\n\n<div class="section">')+len('</div>\n</div>\n\n')]
    new_desc = f'''<div class="s-title">💡 产品说</div>
<div class="story">
{desc_text}
</div>
</div>

'''
    card = card.replace(old_desc, new_desc)

    # 替换核心配方  
    old_rec = card[card.find('<div class="s-title">🔬 核心配方（付费解锁完整版）</div>'):]
    old_rec_end = old_rec.find('</div>\n</div>\n\n<div class="section">')
    old_rec = old_rec[:old_rec_end+len('</div>\n</div>\n\n')]
    new_rec = f'''<div class="s-title">🔬 核心配方（付费解锁完整版）</div>
<div class="recipe-box">
{recipe_text}
</div>
</div>

'''
    card = card.replace(old_rec, new_rec)

    # 替换风险
    risk_html = ''
    for risk_name, risk_level, risk_desc in risk_items:
        stars = ''
        for i in range(5):
            stars += '<span class="on">★</span>' if i < risk_level else '<span>★</span>'
        risk_html += f'<div class="risk-item"><span>{risk_name}</span><span class="risk-stars">{stars}</span></div>\n'
        risk_html += f'<div style="font-size:11px;color:#7a7269;margin:-2px 0 8px 0">{risk_desc}</div>\n'
    
    old_risk = card[card.find('<div class="s-title">⚠️ 三大风险</div>'):]
    old_risk_end = old_risk.find('</div>\n\n<div class="section">')
    old_risk = old_risk[:old_risk_end]
    
    new_risk = f'''<div class="s-title">⚠️ 风险提示</div>
{risk_html}</div>'''
    card = card.replace(old_risk, new_risk)

    # 替换场景
    scene_html = ''.join([f'<span class="scene-item">{s}</span>\n' for s in scenes])
    old_scene = card[card.find('<div class="scene-grid">'):]
    old_scene_end = old_scene.find('</div>\n</div>') + len('</div>')
    old_scene = old_scene[:old_scene_end]
    new_scene = f'''<div class="scene-grid">
{scene_html}</div>'''
    card = card.replace(old_scene, new_scene)

    # 替换搭配销售
    pair_html = ''.join([f'<div class="pair-item"><span class="p-name">{p[0]}</span><span class="p-price">{p[1]}</span></div>\n' for p in pairs])
    old_pair = card[card.find('<div class="s-title">🤝 搭配销售</div>'):]
    old_pair_end = old_pair.find('</div>\n</div>') + len('</div>')
    old_pair = old_pair[:old_pair_end]
    new_pair = f'''<div class="s-title">🤝 搭配销售</div>
{pair_html}</div>'''
    card = card.replace(old_pair, new_pair)

    # 替换卖货话术
    old_talk = card[card.find('<div class="talk">'):]
    old_talk_end = old_talk.find('</div>\n</div>') + len('</div>')
    old_talk = old_talk[:old_talk_end]
    new_talk = f'''<div class="talk">
{talk_text}
</div>'''
    card = card.replace(old_talk, new_talk)

    # 替换避坑
    tip_html = ''.join([f'<div class="tip-item">{t}</div>\n' for t in tips])
    old_tips = card[card.find('role="list" 食品安全'):]
    # 更精确的定位
    old_tips_start = card.find('<div class="tip-item">')
    old_tips_section = card[card.rfind('<div class="s-title">🚫 避坑指南</div>'):]
    old_tips_section_end = old_tips_section.find('</div>\n</div>\n\n<div class="pay"')
    if old_tips_section_end == -1:
        old_tips_section_end = old_tips_section.find('</div>\n</div>\n\n<div class="ftr"')
    if old_tips_section_end > 0:
        old_tips_section = old_tips_section[:old_tips_section_end+len('</div>\n</div>\n\n')]
        card = card.replace(old_tips_section, f'''<div class="s-title">🚫 避坑指南</div>
{tip_html}</div>
</div>

<div class="pay"''')
    
    return card


# ===== TL_020 川式五香卤水 =====
tl020 = gen_tl_card(
    'TL_020', '川式五香卤水', '50斤高汤配80+香料 · 传统川式五香卤水 · 适用各类卤货',
    '🍲',
    [('香料包摊（份）', '¥0.5-1.0'), ('食材（肉类500g）', '¥12-18'), ('高汤+调料', '¥0.8-1.2'), ('燃气+人工摊', '¥0.5-0.8'), ('包装', '¥0.3-0.5')],
    '¥14.1-21.5', '¥25-35/份（卤肉）', '¥800-2000',
    '川式五香卤水是卤味店的灵魂。50斤高汤为底，搭配80+克混合香料（八角、甘松、沙姜、白芷、草果等20+种），加糖色调色，小火慢煮出香。卤出的肉红亮透香，冷吃热吃皆可。可卤：鸡爪、猪蹄、牛肉、豆干、藕片——一锅卤水养得好，越用越香。',
    '卤水每日保养是关键——卤完一批货后过滤残渣，烧开放凉，冷藏保存。卤水越老越香，前三个月是养水期。',
    '<strong>香料包配方框架：</strong><br>八角80g · 甘松20g · 沙姜50g · 白芷50g · 草果30g · 小茴香60g · 肉豆蔻60g · 桂皮35g · 丁香5g · 辣椒王100g · 大红袍花椒50g<br><br><strong>卤汤调制：</strong>高汤50斤+盐750g+糖色1000-1500g+混合油5斤+香料包，小火煮1小时后关火静置1天使用<br><br><em style="color:#b5aaa0;font-size:11px">以上为配方框架。完整版含：20+香料精确到克的配比表、糖色炒制方法、卤水每日保养流程、不同食材卤制时间表。</em>',
    [('🟡 卤水养护', 3, '卤水每天要过滤、烧开、冷藏。3天不动就发酸，一锅废掉损失¥300+'), ('🟡 味道一致性', 3, '香料品质波动大，同一配方不同批次的香料味道可能差20%'), ('🟢 门槛适中', 2, '卤水入门不难但养好需要经验，前三个月是淘汰期')],
    ['卤味熟食店', '外卖专营', '菜市场档口', '社区店'],
    [('卤猪蹄（半只）', '¥25-30'), ('卤牛肉（200g）', '¥30-35'), ('卤鸡爪（5个）', '¥12-15'), ('卤豆干（5片）', '¥6-8'), ('卤藕片（份）', '¥8-10')],
    '「老板，这个卤水是我自己调的，川式五香，你闻闻这个味。要不要来份卤猪蹄？软烂入味，回家微波炉叮2分钟就行。」',
    ['卤水养水期前3个月不要做大货，每天少量卤、勤保养，等卤水稳定了再放量', '香料直接在调料市场批整包的"卤水香料包"比自己配便宜且稳定', '卤水不要用来卤豆制品（豆腐/豆干）——豆制品易酸，会污染整锅老卤', '卤完一批货立马过滤，香料渣不过夜，残渣泡在卤水里12小时就发苦']
)

# ===== TL_021 万能卤水+爆炒料 =====
tl021 = gen_tl_card(
    'TL_021', '万能卤水+爆炒料', '湖式潮卤配方 · 一卤两吃 · 卤完还能爆炒',
    '🍲',
    [('卤水摊（份）', '¥0.3-0.5'), ('食材（500g）', '¥10-18'), ('爆炒料+调料', '¥0.8-1.2'), ('燃气+人工', '¥0.5-0.8'), ('包装', '¥0.3-0.5')],
    '¥11.9-21.0', '¥22-35/份', '¥600-1500',
    '这是一款"一卤两吃"的创新卤水。传统卤水卤完只能冷吃或加热吃，这款卤水卤完的食材还能二次爆炒——卤好的鸭脖、鸡爪捞出，加葱姜蒜香菜爆炒，外焦里嫩，风味翻倍。核心是香料包+卤汤+爆炒料三合一体系。香茅、南姜、苹果等30+种原料构建复合味型，骨味素+鱼露+玫瑰露酒提鲜。',
    '卤水做好后卤第一批食材时香气最浓，这个时候的卤水不要直接卖——先养3天再用。爆炒料是灵魂，卤完的食材不爆炒就浪费了这个体系的价值。',
    '<strong>香料包框架：</strong>香茅30g·八角40g·沙姜40g·小茴香60g·桂皮35g·丁香4粒·南姜600g·生抽300g·棒子骨2500g·清水12.5kg<br><br><strong>调料：</strong>冰糖500g·绍酒700g·蚝油650g·骨味素300g·鱼露150g·玫瑰露酒150g<br><br><strong>爆炒料：</strong>生葱150g·香芹75g·香菜80g·生姜150g·蒜肉75g<br><br><em style="color:#b5aaa0;font-size:11px">完整版含：精确到克的完整配比、卤汤熬制工艺、爆炒火候控制、卤水保养SOP。</em>',
    [('🟡 操作复杂', 3, '一卤两吃体系比传统卤水多一道爆炒工序，培训成本高'), ('🟢 差异化强', 2, '"卤完还能爆炒"的卖点识别度高，竞品少'), ('🟡 备料繁多', 3, '30+种原料备料麻烦，缺一种风味就不完整')],
    ['卤味专门店（差异化路线）', '夜宵大排档', '下酒菜档口', '外卖专营'],
    [('卤鸭脖爆炒（份）', '¥25-30'), ('卤鸡爪爆炒（份）', '¥20-25'), ('卤猪耳爆炒（份）', '¥28-35'), ('卤藕片（素）', '¥8-10')],
    '「我家卤水和别家不一样——卤完还能爆炒。你看这个鸭脖，卤好之后过油爆炒，外焦里嫩，下酒绝了。先尝一个？」',
    ['爆炒料（葱姜蒜香菜）必须当天切当天用，隔夜的不香', '卤水做好前3天卤的食材不要卖——卤水在"养味期"，味道不稳定', '爆炒时火要大、动作要快，翻炒30秒就出锅，炒久了肉会柴', '一份的量不要超过300g食材，多了爆炒不均匀']
)

# ===== TL_022 高汤熬制（底汤技术） =====
tl022 = gen_tl_card(
    'TL_022', '高汤熬制（底汤技术）', '万能高汤底 · 粉面/卤水/汤底的基础 · 一汤多用',
    '🍲',
    [('鸡架骨（摊）', '¥1.0-1.5'), ('大骨（摊）', '¥1.5-2.0'), ('燃气', '¥1.0-1.5'), ('生姜+调料', '¥0.3-0.5')],
    '¥3.8-5.5（每50斤高汤）', '高汤不单独售卖，作为粉面/卤水的加价项', '—',
    '高汤是所有餐饮的"基础设施"。很多小店为了省成本用清水+味精，吃得出和用高汤的区别。4只鸡架+2根大骨+50斤水，加姜片白酒去腥，大火烧开转小火熬4小时——出来的汤白如奶，鲜而不腻。<br><br>用途极广：做粉面汤底、做卤水底汤、做炒菜的高汤、做粥底。一锅高汤可以支撑一家店50%以上的出品品质。投资回报比极高——成本不到5块/50斤，但能让你的产品价格翻倍。',
    '高汤不是什么高科技，但90%的小店做不好——要么熬的时间不够、要么火候不对、要么舍不得下料。熬好一锅高汤是餐饮基本功。',
    '<strong>材料：</strong>鸡架骨4只 · 猪大骨2根 · 生姜150g · 水50斤 · 白酒100g<br><br><strong>流程：</strong>鸡架焯水去浮沫→洗净→入高汤桶→加水50斤→加生姜200g→加白酒50g→大火烧开→转小火熬4小时→过滤取汤<br><br><strong>保存：</strong>放凉后分装冷藏，可存3天。<br><br><em style="color:#b5aaa0;font-size:11px">完整版含：不同用途的高汤配方（粉面汤底/卤水底汤/海鲜高汤）、火候控制技巧、保存与使用规范。</em>',
    [('🟢 入门门槛低', 1, '材料简单、工艺不复杂，关键是耐心和时间'), ('🟡 时间成本', 2, '熬一锅要4小时，每天都要熬——不能因为忙就用清水替代'), ('🟢 投资回报极高', 1, '成本不到5块/50斤，带来的出品品质提升值10倍')],
    ['粉面店', '卤味店', '快餐店', '早餐店', '火锅店（做汤底）'],
    [('高汤粉面（加收）', '¥2-3/碗'), ('高汤卤水（加收）', '成本内化')],
    '「我们的汤底是用4只鸡架+2根大骨熬了4个小时的，不是味精水。你喝一口试试，喝完再吃面。」',
    ['鸡架焯水后一定要洗掉浮沫和血渣，不然汤会浑浊发黑', '熬汤全程不要盖盖子，不然汤会浑浊发白反而不好看', '每天现熬，前一天剩下的汤不要混进新汤里', '不同用途的高汤加盐时机不同——做卤水底汤的不要加盐，做粉面汤底的可以加底盐']
)

# 保存
for card_id, card in [('TL_020', tl020), ('TL_021', tl021), ('TL_022', tl022)]:
    # 修复某些替换可能没完全的情况
    path = f'/Users/mac/Desktop/青葵/foodintelai-site/cards/{card_id}.html'
    with open(path, 'w') as f:
        f.write(card)
    print(f'✅ {card_id}.html saved ({len(card)} chars)')

print('\n✨ 5张卡片全部生成完毕')
