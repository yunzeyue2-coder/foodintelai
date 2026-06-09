#!/usr/bin/env python3
"""
配方-卡片匹配脚本
1. 读取虾哥 289 条配方数据 (recipes-data.json from 虾哥/h5工作站)
2. 读取我们 382 张 V4 卡片
3. 按产品名语义匹配（关键词+品类过滤）
4. 输出匹配结果 + 未匹配卡片列表
5. 为匹配上的卡片生成付费区 V4 标准内容
"""

import json, re, os, sys
from collections import defaultdict

DIFF_THRESHOLD = 0.3  # 匹配阈值

# ============================================================
# 1. 读取虾哥配方数据
# ============================================================
def load_shige_recipes(path="/Users/mac/Desktop/虾哥/h5工作站/recipes-data.json"):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    print(f"[虾哥配方] 共 {len(data)} 条")
    # 按品类分组
    by_cat = defaultdict(list)
    for r in data:
        by_cat[r['cat']].append(r)
    for cat, items in sorted(by_cat.items()):
        print(f"  {cat}: {len(items)} 条")
    return data, by_cat

# ============================================================
# 2. 读取我们的卡片
# ============================================================
def load_our_cards(cards_dir="/Users/mac/Desktop/青葵/foodintelai-site/cards",
                   data_file="/Users/mac/Desktop/青葵/foodintelai-site/cards-data.js"):
    # 从 cards-data.js 获取卡片元信息
    cards_meta = {}
    with open(data_file, encoding='utf-8') as f:
        content = f.read()
    
    # 解析 ALL_CARDS 对象
    m = re.search(r'const\s+ALL_CARDS\s*=\s*(\{.*)', content, re.DOTALL)
    if not m:
        print("ERROR: 未找到 ALL_CARDS")
        return {}
    
    json_str = m.group(1)
    # 截取到最后一个 } 分号前
    bracket_depth = 0
    end_pos = 0
    for i, ch in enumerate(json_str):
        if ch == '{': bracket_depth += 1
        elif ch == '}': bracket_depth -= 1
        if bracket_depth == 0:
            end_pos = i + 1
            break
    
    if end_pos == 0:
        print("ERROR: JSON 不完整")
        return {}
    
    json_str = json_str[:end_pos]
    
    # 移除 JS 尾部可能的 ;\n\s*
    json_str = re.sub(r';\s*$', '', json_str)
    
    try:
        all_cards = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        # 尝试修复
        # 引号内的换行符问题
        json_str_fixed = re.sub(r'(?<!\\)\n(?!\s*["\}\]])', '', json_str)
        try:
            all_cards = json.loads(json_str_fixed)
        except:
            print("JSON解析彻底失败")
            return {}
    
    # 解析为平面列表
    for cat_name, cat_cards in all_cards.items():
        # 去掉分类名前缀的emoji
        clean_cat = re.sub(r'^[^\w]+', '', cat_name).strip()
        clean_cat = re.sub(r'[^\u4e00-\u9fff\w]', '', clean_cat)
        for card in cat_cards:
            card_id = card.get('f', '').replace('cards/', '').replace('.html', '')
            card_name = card.get('n', '')
            # 从名称提取产品名
            name_clean = re.sub(r'·.*$', '', card_name).strip()
            name_clean = re.sub(r'[\u4e00-\u9fff\w]+\d*$', '', name_clean).strip()
            cards_meta[card_id] = {
                'id': card_id,
                'name': name_clean,
                'file': card.get('f', ''),
                'cat': clean_cat,
                'raw_cat': cat_name,
            }
    
    print(f"\n[我们的卡] 从 cards-data.js 找到 {len(cards_meta)} 张卡片元数据")
    
    # 读取实际HTML文件
    existing = []
    missing = []
    for cid, meta in cards_meta.items():
        html_path = os.path.join(cards_dir, f"{cid}.html") if not meta['file'].startswith('/') else meta['file']
        if not meta['file']:
            html_path = os.path.join(cards_dir, f"{cid}.html")
        else:
            html_path = os.path.join(cards_dir, os.path.basename(meta['file']))
        
        if os.path.exists(html_path):
            meta['html_path'] = html_path
            existing.append(meta)
        else:
            missing.append(cid)
    
    print(f"  存在HTML: {len(existing)}, 缺失HTML: {len(missing)}")
    if missing:
        print(f"  缺失名单(前10): {missing[:10]}")
    
    return existing

# ============================================================
# 3. 语义匹配函数
# ============================================================
def normalize_name(name):
    """标准化名称用于匹配"""
    name = name.lower()
    name = re.sub(r'[^\u4e00-\u9fff\w]', '', name)
    name = re.sub(r'(产品卡|商业版|标准版|产品)$', '', name)
    return name.strip()

def extract_keywords(name):
    """提取关键产品词"""
    # 移除编号前后缀
    name = re.sub(r'^[\w]+[\s_\-]+\d+[\s_\-]*', '', name)
    name = re.sub(r'[\s_\-]*\d+$', '', name)
    
    # 常见产品类型词
    product_types = ['鸡', '鸭', '鱼', '肉', '牛', '羊', '猪', '虾', '蟹', '饭', '面',
                     '粉', '汤', '饼', '包', '饺', '串', '锅', '煲', '酱', '卤', '烤',
                     '炸', '煎', '蒸', '炒', '煮', '焖', '炖', '腌', '腊', '熏',
                     '茶', '奶', '汁', '粥', '豆', '菜', '糖', '冰', '凉', '热',
                     '油', '醋', '酒', '粉', '丝', '丸', '肠', '糕', '酥', '卷',
                     '饭', '面', '粉', '包', '饺', '饼', '粥', '汤']
    
    keywords = []
    for ch in name:
        if ch in product_types:
            keywords.append(ch)
    return set(keywords)

def simple_match(card_name, recipe_name):
    """简单名称匹配"""
    card_norm = normalize_name(card_name)
    recipe_norm = normalize_name(recipe_name)
    
    # 精确匹配
    if card_norm == recipe_norm:
        return 1.0
    
    # 一个包含另一个
    if card_norm in recipe_norm or recipe_norm in card_norm:
        if len(card_norm) >= 2 or len(recipe_norm) >= 2:
            max_len = max(len(card_norm), len(recipe_norm))
            min_len = min(len(card_norm), len(recipe_norm))
            return min_len / max_len
    
    # 关键词匹配
    card_kw = extract_keywords(card_name)
    recipe_kw = extract_keywords(recipe_name)
    
    if not card_kw or not recipe_kw:
        return 0.0
    
    overlap = card_kw & recipe_kw
    if len(overlap) >= 2:  # 至少两个关键词重叠
        return len(overlap) / max(len(card_kw), len(recipe_kw))
    
    return 0.0

# ============================================================
# 4. 主匹配流程
# ============================================================
def main():
    recipes, recipes_by_cat = load_shige_recipes()
    cards = load_our_cards()
    
    # 构建品类映射 (卡片品类 → 虾哥品类)
    cat_map = {
        '炸鸡': ['炸物', '小吃'],
        '炸物': ['炸物', '小吃'],
        '鸡排': ['炸物', '小吃'],
        '酱料': ['酱料'],
        '糖水': ['饮品/甜品'],
        '甜品': ['饮品/甜品'],
        '饮品': ['饮品/甜品'],
        '奶茶': ['饮品/甜品'],
        '柠檬茶': ['饮品/甜品'],
        '咖啡': ['饮品/甜品'],
        '包子': ['面点'],
        '早餐': ['面点', '粥品'],
        '粥品': ['粥品'],
        '粉面': ['面食'],
        '面食': ['面食'],
        '炒饭': ['热菜'],
        '卤煮': ['卤煮肉制品'],
        '冷吃': ['凉菜', '卤煮肉制品'],
        '火锅': ['底料', '汤底/卤水'],
        '汤料': ['汤底/卤水'],
        '小吃': ['小吃', '其他'],
        '摆摊': ['小吃', '炸物', '其他'],
        '招牌': ['热菜', '小吃'],
        '鸡': ['卤煮肉制品', '热菜'],
        '饼': ['面点', '面食'],
    }
    
    # 匹配
    matched = []  # (card_id, card_name, recipe_id, recipe_name, score, recipe_content)
    unmatched = []
    
    for card in cards:
        card_id = card['id']
        card_name = card['name']
        card_cat = card['cat']
        
        best_match = None
        best_score = 0
        
        # 先在本品类相关范围内匹配
        relevant_cats = cat_map.get(card_cat, [])
        candidates = []
        for rc in relevant_cats:
            candidates.extend(recipes_by_cat.get(rc, []))
        
        # 如果没有相关品类，全量匹配
        if not candidates:
            candidates = recipes
        
        for recipe in candidates:
            score = simple_match(card_name, recipe['name'])
            if score > best_score:
                best_score = score
                best_match = recipe
        
        if best_match and best_score >= DIFF_THRESHOLD:
            matched.append({
                'card_id': card_id,
                'card_name': card_name,
                'card_cat': card_cat,
                'recipe_id': best_match['id'],
                'recipe_name': best_match['name'],
                'recipe_cat': best_match['cat'],
                'score': best_score,
                'content': best_match['content'],
            })
        else:
            unmatched.append(card)
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"匹配结果:")
    print(f"  匹配成功: {len(matched)} 张")
    print(f"  未匹配: {len(unmatched)} 张")
    print(f"  匹配率: {len(matched)/(len(matched)+len(unmatched))*100:.1f}%")
    
    # 按品类统计匹配情况
    cat_stats = defaultdict(lambda: {'matched': 0, 'unmatched': 0, 'total': 0})
    for m in matched:
        cat = m['card_cat']
        cat_stats[cat]['matched'] += 1
        cat_stats[cat]['total'] += 1
    for u in unmatched:
        cat = u['cat']
        cat_stats[cat]['unmatched'] += 1
        cat_stats[cat]['total'] += 1
    
    print(f"\n品类匹配详情:")
    for cat in sorted(cat_stats.keys()):
        s = cat_stats[cat]
        pct = s['matched']/s['total']*100 if s['total'] > 0 else 0
        print(f"  {cat}: {s['matched']}/{s['total']} ({pct:.0f}%)")
    
    # 高匹配度卡片列表
    print(f"\n高匹配度 (>0.8):")
    for m in sorted(matched, key=lambda x: -x['score']):
        if m['score'] >= 0.8:
            print(f"  [{m['card_id']}] {m['card_name']} ↔ {m['recipe_name']} (score={m['score']:.2f})")
    
    # 低匹配度但匹配上了的
    print(f"\n低匹配度 (<0.5):")
    for m in sorted(matched, key=lambda x: x['score']):
        if m['score'] < 0.5:
            print(f"  [{m['card_id']}] {m['card_name']} ↔ {m['recipe_name']} (score={m['score']:.2f})")
    
    # 未匹配的卡片
    print(f"\n未匹配卡片 (按品类):")
    un_by_cat = defaultdict(list)
    for u in unmatched:
        un_by_cat[u['cat']].append(u['id'])
    for cat in sorted(un_by_cat.keys()):
        ids = un_by_cat[cat]
        print(f"  {cat} ({len(ids)}张): {', '.join(ids[:10])}{'...' if len(ids) > 10 else ''}")
    
    # 保存匹配结果到文件
    output = {
        'matched': matched,
        'unmatched_ids': [u['id'] for u in unmatched],
        'stats': {
            'total_cards': len(matched) + len(unmatched),
            'matched': len(matched),
            'unmatched': len(unmatched),
            'match_rate': f"{len(matched)/(len(matched)+len(unmatched))*100:.1f}%"
        }
    }
    
    out_path = "/Users/mac/Desktop/青葵/foodintelai-site/match_result.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=1)
    print(f"\n结果已保存到: {out_path}")
    
    return matched, unmatched

if __name__ == '__main__':
    matched, unmatched = main()
