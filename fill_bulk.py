#!/usr/bin/env python3
"""
批量填充低置信度卡 + 完全未匹配卡
按品类用虾哥通用配方填充
"""
import json, re, os, shutil

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"
MATCH_FILE = "/Users/mac/Desktop/青葵/foodintelai-site/match_result.json"
RECIPE_FILE = "/Users/mac/Desktop/虾哥/h5工作站/recipes-data.json"

with open(RECIPE_FILE, encoding='utf-8') as f:
    ALL_RECIPES = json.load(f)

def get_recipe(name):
    """按名称找配方"""
    for r in ALL_RECIPES:
        if name in r['name']:
            return r['content']
    return None

def make_desc_from_recipe(content):
    """把配方内容格式化为付费区desc"""
    lines = content.strip().split('\n')
    ingredients = []
    process = []
    section = 'other'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('**原料**') or line.startswith('**原料:'):
            section = 'ingredients'
            continue
        elif line.startswith('**制作') or line.startswith('**制作过程') or line.startswith('**工艺'):
            section = 'process'
            continue
        elif line.startswith('**'):
            section = 'other'
            continue
        if section == 'ingredients':
            ingredients.append(line)
        elif section == 'process':
            process.append(line)
    
    ing_items = []
    for line in ingredients:
        line = line.strip().lstrip('*').strip()
        if line and line != '---' and len(line) > 3:
            ing_items.append(line[:60])
    
    proc_items = []
    for line in process:
        line = line.strip()
        if line and line != '---':
            line = re.sub(r'^[\d]+[\.\)、]\s*', '', line)
            proc_items.append(line)
    
    desc = ''
    if ing_items:
        for item in ing_items[:4]:
            desc += f'  ✅ {item}<br>\n'
    if proc_items:
        step = ' → '.join(proc_items[:2])
        desc += f'  ✅ 工艺：{step}<br>\n'
    desc += '  ✅ 精确到克的商用配比<br>\n'
    desc += '  ✅ 成本拆分+利润计算+翻车解法<br>\n'
    desc += '  ✅ 批量换算（家庭→小摊→店铺）<br>\n'
    desc += '  ✅ 出餐SOP+效率优化方案'
    
    return desc

# ========== 品类配方映射 ==========
CATEGORY_RECIPES = {
    '🍗 炸鸡系列': '奥尔良炸鸡',  
    '🍗 鸡排系列': '炸串椒料&酱料',  
    '🍗 卤炸帮': '万能卤水+爆炒料',
    '🍧 糖水系列': '西米酸奶水果捞',
    '🥤 手打柠檬茶': '手打柠檬茶',
    '🥟 包子系列': '猪肉万能母馅',
    '🥣 粥品系列': '八宝粥',
    '🥣 胡辣汤': '逍遥镇胡辣汤',
    '🍳 炒饭炒面花甲': '铁板炒饭',
    '🍮 甜品系列': '炒酸奶',
    '🥗 冷吃系列': '凉菜万能汁+大拌菜麻酱汁',
    '🫕 火锅酸汤': '串串香底料',
    '🫕 特色系列': '捞汁小海鲜',
    '🥩 韩式系列': '韩式辣椒酱',
    '🥤 饮品系列': '冰镇酸梅汤',
    '🧂 复合酱料': '老北京炸酱面',
    '📂 其他': '万能卤水+爆炒料',
    '🍜 粉面系列': '粉蒸牛肉',
    '🍜 面食系列': '安徽牛肉板面',
    '🍢 摆摊小吃': '公婆饼（葱肉饼）',
}

# 酱料系列特殊处理——有匹配到的用匹配的，没有才用通用
SAUCE_MAP = {
    'JL_051': '韩式辣椒酱', 'JL_052': '韩式辣椒酱', 
    'JL_055': '土家酱香饼', 'JL_056': '金银蒜蓉酱',
    'JL_057': '椒香麻辣酱', 'JL_059': '叉烧酱+叉烧糖',
    'JL_061': '凉拌菜复制酱油', 'JL_062': '兰州拉面(和面+辣椒油)',
    'JL_064': '奥尔良炸鸡', 'JL_065': '奥尔良炸鸡',
    'JL_066': '奥尔良炸鸡', 'JL_068': '奥尔良炸鸡',
    'JL_069': '炸串椒料&酱料', 'JL_071': '奥尔良炸鸡',
    'JL_072': '奥尔良炸鸡', 'JL_075': '炒酸奶',
    'JL_076': '奥尔良炸鸡', 'JL_079': '关东酱牛肉',
    'JL_081': '土家酱香饼', 'JL_083': '韩式辣椒酱',
    'JL_086': '奥尔良炸鸡',
}

def fill_card(card_id, recipe_name, card_path=None):
    """填充单张卡"""
    if not card_path:
        path = os.path.join(CARDS_DIR, f"{card_id}.html")
        if not os.path.exists(path):
            for f in os.listdir(CARDS_DIR):
                if f.startswith(card_id) and f.endswith('.html'):
                    path = os.path.join(CARDS_DIR, f)
                    break
            else:
                print(f"  [跳过] 找不到: {card_id}")
                return False
        card_path = path
    
    content = open(card_path, encoding='utf-8').read()
    
    # 备份
    bak = card_path + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(card_path, bak)
    
    # 找配方
    recipe_content = get_recipe(recipe_name)
    if not recipe_content:
        print(f"  [跳过] 无配方'{recipe_name}': {card_id}")
        return False
    
    new_desc = make_desc_from_recipe(recipe_content)
    
    # 替换V4结构 <div class="desc">...</div>
    if '<div class="paywall">' in content:
        m = re.search(r'(<div class="desc">)(.*?)(</div>\s*\n?\s*<a class="btn")', content, re.DOTALL)
        if m:
            new_content = content.replace(m.group(0), f'<div class="desc">\n{new_desc}\n  </div>\n  <a class="btn"')
            open(card_path, 'w', encoding='utf-8').write(new_content)
            print(f"  [V4] {card_id} ← {recipe_name}")
            return True
    
    # 替换旧结构 <ul>...</ul> 
    if '<div class="pay">' in content or '<div class="unlock-box">' in content:
        # 找<ul>到</ul>
        m = re.search(r'(<ul>\s*\n?)(.*?)(\s*</ul>)', content, re.DOTALL)
        if m:
            new_list = ''
            ing_lines = new_desc.split('<br>')
            for l in ing_lines[:5]:
                clean = re.sub(r'<[^>]+>', '', l).strip()
                if clean:
                    new_list += f'    <li>{clean}</li>\n'
            new_list += '    <li>精确到克的商用配比</li>\n    <li>成本拆分+利润计算+翻车解法</li>'
            new_content = content.replace(m.group(0), f'<ul>\n{new_list}\n  </ul>')
            open(card_path, 'w', encoding='utf-8').write(new_content)
            print(f"  [旧] {card_id} ← {recipe_name}")
            return True
    
    print(f"  [跳过] 无付费结构: {card_id}")
    return False

def process_low_conf():
    """处理低置信度卡片"""
    with open(MATCH_FILE, encoding='utf-8') as f:
        result = json.load(f)
    
    low_conf = [m for m in result['matched'] if m['score'] < 0.6]
    
    print(f"处理低置信度 {len(low_conf)} 张...")
    
    success = 0
    for m in low_conf:
        cid = m['card_id']
        ccat = m['card_cat']
        
        # 酱料特殊处理
        if '酱料' in ccat or '复合酱料' in ccat:
            recipe_name = SAUCE_MAP.get(cid, '万州烤鱼红油')
        elif ccat in CATEGORY_RECIPES:
            recipe_name = CATEGORY_RECIPES[ccat]
        else:
            recipe_name = m['recipe_name']
        
        if fill_card(cid, recipe_name):
            success += 1
    
    print(f"\n低置信度处理完成: {success}/{len(low_conf)} 张")

def process_unmatched():
    """处理完全未匹配的卡片"""
    with open(MATCH_FILE, encoding='utf-8') as f:
        result = json.load(f)
    
    unmatched_ids = result['unmatched_ids']
    print(f"\n处理未匹配卡片 {len(unmatched_ids)} 张...")
    
    success = 0
    
    for cid in unmatched_ids:
        # 从cards-data.js找卡片信息
        recipe_name = None
        
        # 按前缀判断品类
        prefix_map = {
            'CF': '🍵速食', 'YL': '冰镇酸梅汤', 'NT': '西米酸奶水果捞',
            'TS': '西米酸奶水果捞', 'TP': '炒酸奶', 'ZC': '八宝粥',
            'BZ': '猪肉万能母馅', 'CD': '手打柠檬茶', 'HZ': '奥尔良炸鸡',
            'JP': '炸串椒料&酱料', 'FM': '粉蒸牛肉', 'HLT': '逍遥镇胡辣汤',
            'LZ': '万能卤水+爆炒料', 'DC': '凉菜万能汁+大拌菜麻酱汁',
            'LB': '凉菜万能汁+大拌菜麻酱汁', 'HG': '串串香底料',
            'KR': '韩式辣椒酱', 'YB': '包子配方（全套）',
            'XC': '公婆饼（葱肉饼）', 'ZS': '八宝粥',
            'QS': '捞汁小海鲜', 'NF': '老北京炸酱面',
            'CS': '万能脆皮糊', 'TL': '万州烤鱼红油',
        }
        
        for prefix, rname in prefix_map.items():
            if cid.startswith(prefix):
                recipe_name = rname
                break
        
        if recipe_name:
            if fill_card(cid, recipe_name):
                success += 1
        else:
            print(f"  [跳过] 无法匹配品类: {cid}")
    
    print(f"\n未匹配处理完成: {success} 张已填")

if __name__ == '__main__':
    process_low_conf()
    process_unmatched()
    print("\n全部完成!")
