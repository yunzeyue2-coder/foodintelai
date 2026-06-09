#!/usr/bin/env python3
"""
付费区填充脚本 v1
读取匹配结果(match_result.json)，对高置信度(score >= 0.6)的卡片
生成V4标准付费内容并写入HTML
"""

import json, re, os, shutil

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"
MATCH_FILE = "/Users/mac/Desktop/青葵/foodintelai-site/match_result.json"

def load_match():
    with open(MATCH_FILE, encoding='utf-8') as f:
        return json.load(f)

def format_paid_content(recipe_name, recipe_content):
    """将虾哥配方格式化为V4标准付费区HTML"""
    # 解析配方内容
    lines = recipe_content.strip().split('\n')
    
    # 提取原料部分和工艺部分
    ingredients = []
    process = []
    current_section = 'other'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('**原料**') or line.startswith('**原料:'):
            current_section = 'ingredients'
            continue
        elif line.startswith('**制作') or line.startswith('**制作过程') or line.startswith('**工艺'):
            current_section = 'process'
            continue
        elif line.startswith('**') and line.endswith('**'):
            current_section = 'other'
            continue
        
        if current_section == 'ingredients':
            ingredients.append(line)
        elif current_section == 'process':
            process.append(line)
    
    # 格式化原料
    html_ingredients = ''
    for line in ingredients:
        line_clean = line.strip().lstrip('*').strip()
        if line_clean:
            # 提取关键原料和用量
            # 处理格式: "色拉油 2500 克" 或 "**猪油** 1000 克"
            parts = re.split(r'\s{2,}|\t', line_clean)
            if len(parts) < 2:
                # 尝试单空格分割
                parts = line_clean.split(' ')
            
            # 过滤掉数量词
            counts = []
            items = []
            for p in parts:
                p = p.strip().lstrip('*').strip()
                # 检查是否为数量/单位
                if re.match(r'^[\d.]+$', p) or p in ['克', '千克', 'g', 'kg', '斤', '两', '毫升', '升', 'ml', 'L', '包', '袋', '瓶', '桶']:
                    counts.append(p)
                elif p:
                    items.append(p)
            
            if items:
                item_name = ''.join(items)
                count_str = ' '.join(counts)
                html_ingredients += f'      <li><strong>{item_name}</strong>：{count_str}</li>\n'
    
    # 格式化工艺步骤
    html_process = ''
    step_num = 1
    for line in process:
        line = line.strip()
        if not line:
            continue
        # 移除编号前缀
        line = re.sub(r'^[\d]+[\.\)、]\s*', '', line)
        html_process += f'      <li>步骤{step_num}：{line}</li>\n'
        step_num += 1
    
    if not html_process:
        html_process = '      <li>（详细工艺步骤在交付包中提供）</li>\n'
    
    # V4标准付费模板
    html = f'''
  <div class="paywall">
    <div class="pw-title">🔐 完整版配方 ¥39 解锁</div>
    <div class="pw-body">
      <strong>精确配方</strong>
      <ul>
{html_ingredients}
      </ul>
      <strong>工艺步骤</strong>
      <ol>
{html_process}
      </ol>
      <strong>交付内容：</strong><br>
      • 精确到克的商用配方（含多种规格换算）<br>
      • 完整操作步骤参数和要点<br>
      • 成本拆分：原料/包装/损耗/利润逐项计算<br>
      • 常见翻车解法：新手踩坑指南<br>
      • 出餐效率优化方案
    </div>
    <a class="pw-btn" href="#">📱 微信联系解锁完整版</a>
  </div>'''
    
    return html

def update_card_paid_area(card_id, html_content, card_path=None):
    """更新卡片付费区内容"""
    if not card_path:
        card_path = os.path.join(CARDS_DIR, f"{card_id}.html")
    
    if not os.path.exists(card_path):
        # 尝试其他路径
        alt_path = os.path.join(CARDS_DIR, card_id)
        if os.path.exists(alt_path):
            card_path = alt_path
        else:
            print(f"  [跳过] 未找到文件: {card_id}")
            return False
    
    with open(card_path, encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有pw-body
    if '.pw-body' not in content:
        print(f"  [跳过] 无paywall结构: {card_id}")
        return False
    
    # 替换pw-body内容
    old_pattern = r'(<div class="pw-body">)(.*?)(</div>\s*<a class="pw-btn")'
    
    def replace_pw(m):
        return m.group(1) + '\n' + html_content + '\n' + m.group(3)
    
    new_content = re.sub(old_pattern, replace_pw, content, count=1, flags=re.DOTALL)
    
    if new_content == content:
        print(f"  [失败] 未替换成功: {card_id}")
        return False
    
    # 备份
    backup_path = card_path + '.bak'
    if not os.path.exists(backup_path):
        shutil.copy2(card_path, backup_path)
    
    with open(card_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  [成功] {card_id}")
    return True

def process_all():
    result = load_match()
    matched = result['matched']
    
    # 按评分排序，先处理高分
    matched_sorted = sorted(matched, key=lambda x: -x['score'])
    
    high_conf = [m for m in matched_sorted if m['score'] >= 0.6]
    low_conf = [m for m in matched_sorted if m['score'] < 0.6]
    
    print(f"高置信度(≥0.6): {len(high_conf)}张")
    print(f"低置信度(<0.6): {len(low_conf)}张")
    print()
    
    # 处理高置信度
    success = 0
    skip = 0
    fail = 0
    
    for m in high_conf:
        paid_html = format_paid_content(m['recipe_name'], m['recipe_content'])
        if update_card_paid_area(m['card_id'], paid_html):
            success += 1
        else:
            skip += 1
    
    print(f"\n处理结果：成功 {success} 张，跳过 {skip} 张，失败 {fail} 张")
    
    # 保存成功处理的名单
    processed = {
        'high_conf_processed': [m['card_id'] for m in high_conf],
        'low_conf_remaining': low_conf,
    }
    
    with open("/Users/mac/Desktop/青葵/foodintelai-site/paid_fill_result.json", 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=1)
    
    print(f"\n低置信度 {len(low_conf)} 张已保留，等你确认后再填")

if __name__ == '__main__':
    process_all()
