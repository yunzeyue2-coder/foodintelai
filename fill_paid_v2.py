#!/usr/bin/env python3
"""
付费区填充脚本 v2
对高置信度匹配的卡片(score >= 0.6)：
1. 读取 cards/XXX.html
2. 找到 <div class="paywall"> 里的 <div class="desc">
3. 用虾哥配方的原料+工艺替换其内容
4. 保持V4风格的format
"""

import json, re, os, shutil

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"
MATCH_FILE = "/Users/mac/Desktop/青葵/foodintelai-site/match_result.json"

def load_match():
    with open(MATCH_FILE, encoding='utf-8') as f:
        return json.load(f)

def format_ingredients(content):
    """从配方内容提取原料部分并格式化"""
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
    
    # 格式化原料为简洁列表
    ing_lines = []
    for line in ingredients:
        line = line.strip().lstrip('*').strip()
        if not line:
            continue
        # 去掉末尾的 ---
        if line == '---':
            continue
        ing_lines.append(line)
    
    # 格式化工艺步骤
    proc_lines = []
    for line in process:
        line = line.strip()
        if not line or line == '---':
            continue
        line = re.sub(r'^[\d]+[\.\)、]\s*', '', line)
        proc_lines.append(line)
    
    # 生成desc格式
    desc = ''
    
    if ing_lines:
        # 只取前5行原料（付费区展示关键原料）
        for line in ing_lines[:5]:
            desc += f'  ✅ {line}<br>\n'
        if len(ing_lines) > 5:
            desc += f'  ✅ （共{len(ing_lines)}种原料，完整配比解锁后可见）<br>\n'
    
    if proc_lines:
        step_text = ' → '.join(proc_lines[:3])
        desc += f'  ✅ 核心工艺：{step_text}<br>\n'
        if len(proc_lines) > 3:
            desc += f'  ✅ （共{len(proc_lines)}个工艺步骤，参数+要点完整版提供）<br>\n'
    
    desc += '  ✅ 成本拆分：原料/包装/损耗/利润逐项计算<br>\n'
    desc += '  ✅ 常见翻车解法：新手踩坑指南<br>\n'
    desc += '  ✅ 批量生产换算：家庭→小摊→店铺三档'
    
    return desc

def update_card(card_id, recipe_name, recipe_content):
    """更新单张卡的付费区"""
    card_path = os.path.join(CARDS_DIR, f"{card_id}.html")
    
    # 尝试拼接路径
    if not os.path.exists(card_path):
        # 检查是否有后缀已经包含在card_id里
        for f in os.listdir(CARDS_DIR):
            if f.startswith(card_id) and f.endswith('.html'):
                card_path = os.path.join(CARDS_DIR, f)
                break
        else:
            print(f"  [跳过] 未找到: {card_id}")
            return False
    
    if not os.path.exists(card_path):
        print(f"  [跳过] 文件不存在: {card_path}")
        return False
    
    with open(card_path, encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有paywall
    if '<div class="paywall">' not in content:
        print(f"  [跳过] 无paywall: {card_id}")
        return False
    
    # 检查是否有desc
    old_desc_pattern = r'(<div class="desc">)(.*?)(</div>\s*\n\s*<a class="btn")'
    
    m = re.search(old_desc_pattern, content, re.DOTALL)
    if not m:
        # 尝试另一种格式
        old_desc_pattern2 = r'(<div class="desc">)(.*?)(</div>\s*<a class="btn")'
        m = re.search(old_desc_pattern2, content, re.DOTALL)
    
    if not m:
        print(f"  [跳过] 无desc结构: {card_id}")
        return False
    
    new_desc = format_ingredients(recipe_content)
    new_html = f'<div class="desc">\n{new_desc}\n  </div>\n  <a class="btn"'
    
    old_full = m.group(0)
    new_full = f'<div class="desc">\n{new_desc}\n  </div>\n  <a class="btn" href="https://foodintelai.com">加微信 canglin1985 获取</a>'
    
    # 替换
    new_content = content.replace(old_full, new_full)
    
    if new_content == content:
        print(f"  [失败] 未替换: {card_id}")
        return False
    
    # 备份
    backup_path = card_path + '.bak'
    if not os.path.exists(backup_path):
        shutil.copy2(card_path, backup_path)
    
    with open(card_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  [成功] {card_id} ← {recipe_name} ({len(recipe_content)}字符)")
    return True

def main():
    result = load_match()
    matched = result['matched']
    
    # 按分数分组
    high_conf = [m for m in matched if m['score'] >= 0.6]
    low_conf = [m for m in matched if m['score'] < 0.6]
    
    print(f"高置信度 ≥0.6: {len(high_conf)}张")
    print(f"低置信度 <0.6: {len(low_conf)}张（人工确认后处理）")
    print()
    
    success = 0
    skipped = 0
    failed = 0
    
    for m in high_conf:
        ok = update_card(m['card_id'], m['recipe_name'], m['recipe_content'])
        if ok:
            success += 1
        elif not os.path.exists(os.path.join(CARDS_DIR, m['card_id'] + '.html')):
            skipped += 1
        else:
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"处理完成: 成功{success} 跳过{skipped} 失败{failed}")
    print(f"剩余待处理: {len(low_conf)}张低置信度 + 218张未匹配")

if __name__ == '__main__':
    main()
