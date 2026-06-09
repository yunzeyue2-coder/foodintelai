#!/usr/bin/env python3
"""
付费区填充脚本 v3
兼容两种结构：
1. <div class="paywall"> → <div class="desc">  (V4格式)
2. <div class="pay"> → <ul>  (旧格式)
"""

import json, re, os, shutil

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"
MATCH_FILE = "/Users/mac/Desktop/青葵/foodintelai-site/match_result.json"

def load_match():
    with open(MATCH_FILE, encoding='utf-8') as f:
        return json.load(f)

def format_ingredients(content):
    """从配方内容提取原料并格式化"""
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
    
    # 格式化原料
    ing_items = []
    for line in ingredients:
        line = line.strip().lstrip('*').strip()
        if not line or line == '---':
            continue
        # 提取关键原料
        parts = re.split(r'\s{2,}', line)
        if len(parts) < 2:
            ing_items.append(line[:60])
        else:
            ing_items.append(line[:60])
    
    # 格式化工艺
    proc_items = []
    for line in process:
        line = line.strip()
        if not line or line == '---':
            continue
        line = re.sub(r'^[\d]+[\.\)、]\s*', '', line)
        proc_items.append(line)
    
    # 生成付费区HTML
    # 如果是pay格式的卡(用ul列表)
    pay_list = ''
    if ing_items:
        # 前4个关键原料
        for item in ing_items[:4]:
            pay_list += f'    <li>原料：{item}</li>\n'
    
    if proc_items:
        step = ' → '.join(proc_items[:2])
        pay_list += f'    <li>核心工艺链：{step}（完整参数+要点付费解锁）</li>\n'
    
    pay_list += '    <li>精确到克的商用配比（含不同规格换算表）</li>\n'
    pay_list += '    <li>成本拆分：原料/包装/损耗/利润逐项计算</li>\n'
    pay_list += '    <li>翻车解法：新手踩坑指南</li>\n'
    pay_list += '    <li>批量生产换算：家庭→小摊→店铺三档</li>'
    
    return pay_list

def format_paywall_desc(content):
    """生成paywall (V4格式) 的desc内容"""
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
        if line and line != '---':
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
        desc += f'  ✅ 工艺：{" → ".join(proc_items[:2])}<br>\n'
    desc += '  ✅ 精确到克的商用配比<br>\n'
    desc += '  ✅ 成本拆分+利润计算+翻车解法<br>\n'
    desc += '  ✅ 批量换算（家庭→小摊→店铺）'
    
    return desc

def update_card(card_id, recipe_name, recipe_content):
    """更新单张卡的付费区，兼容两种结构"""
    card_path = os.path.join(CARDS_DIR, f"{card_id}.html")
    
    if not os.path.exists(card_path):
        for f in os.listdir(CARDS_DIR):
            if f.startswith(card_id) and f.endswith('.html'):
                card_path = os.path.join(CARDS_DIR, f)
                break
        else:
            print(f"  [跳过] 未找到: {card_id}")
            return False
    
    if not os.path.exists(card_path):
        print(f"  [跳过] 不存在: {card_path}")
        return False
    
    with open(card_path, encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    backup_path = card_path + '.bak'
    if not os.path.exists(backup_path):
        shutil.copy2(card_path, backup_path)
    
    # 尝试多种付费区结构
    has_pay = '<div class="pay">' in content  # 旧结构（ul列表）
    has_paywall = '<div class="paywall">' in content  # V4结构（desc）
    
    if has_pay:
        # 旧结构 <div class="pay"><ul> ... </ul></div>
        # 替换 <ul> ... </ul> 之间的内容
        new_list = format_ingredients(recipe_content)
        
        # 找到<ul>到</ul>
        ul_pattern = r'(<ul>\s*\n?)(.*?)(\s*</ul>)'
        m = re.search(ul_pattern, content, re.DOTALL)
        
        if m:
            new_content = content.replace(m.group(0), f'<ul>\n{new_list}\n  </ul>')
            with open(card_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [成功·旧] {card_id} ← {recipe_name}")
            return True
        else:
            print(f"  [失败] pay结构但无ul: {card_id}")
            return False
    
    elif has_paywall:
        # V4结构 <div class="paywall"><div class="desc"> ... </div>
        new_desc = format_paywall_desc(recipe_content)
        
        # 尝试替换desc
        desc_pattern = r'(<div class="desc">)(.*?)(</div>\s*\n?\s*<a class="btn")'
        m = re.search(desc_pattern, content, re.DOTALL)
        
        if m:
            new_content = content.replace(m.group(0), f'<div class="desc">\n{new_desc}\n  </div>\n  <a class="btn"')
            with open(card_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [成功·V4] {card_id} ← {recipe_name}")
            return True
        else:
            print(f"  [失败] paywall但无desc: {card_id}")
            return False
    else:
        print(f"  [跳过] 无付费结构: {card_id}")
        return False

def main():
    result = load_match()
    matched = result['matched']
    
    high_conf = [m for m in matched if m['score'] >= 0.6]
    low_conf = [m for m in matched if m['score'] < 0.6]
    
    print(f"高置信度 ≥0.6: {len(high_conf)}张")
    print(f"低置信度 <0.6: {len(low_conf)}张")
    print()
    
    success = 0
    skipped = 0
    failed = 0
    
    for m in high_conf:
        ok = update_card(m['card_id'], m['recipe_name'], m['recipe_content'])
        if ok:
            success += 1
        elif '无付费结构' in str(ok) or '不存在' in str(ok):
            skipped += 1
        else:
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"处理完成: 成功{success} 跳过{skipped} 失败{failed}")
    
    # 输出低置信度名单供你确认
    print(f"\n低置信度名单 (需确认):")
    for m in sorted(low_conf, key=lambda x: -x['score']):
        print(f"  [{m['card_id']}] {m['card_name'][:25]:25s} → {m['recipe_name']:15s} (score={m['score']:.2f})")

if __name__ == '__main__':
    main()
