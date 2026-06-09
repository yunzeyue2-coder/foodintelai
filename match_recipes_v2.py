#!/usr/bin/env python3
"""
配方-卡片匹配脚本 v2
从 cards-data.js 解析卡片信息
按产品名匹配虾哥 289 条配方
生成匹配结果 + 付费区内容
"""

import json, re, os
from collections import defaultdict

# ============================================================
# 1. 读取虾哥配方
# ============================================================
def load_recipes():
    with open("/Users/mac/Desktop/虾哥/h5工作站/recipes-data.json", encoding='utf-8') as f:
        return json.load(f)

# ============================================================
# 2. 从 cards-data.js 解析卡片
# ============================================================
def parse_cards_data():
    """解析 cards-data.js 提取卡片信息"""
    with open("/Users/mac/Desktop/青葵/foodintelai-site/cards-data.js", encoding='utf-8') as f:
        content = f.read()
    
    cards_list = []
    
    # 匹配每个品类块
    cat_pattern = re.compile(r'"([^"]+)"\s*:\s*\[(.*?)\]\s*,?\s*(?="|$)', re.DOTALL)
    
    for cat_match in cat_pattern.finditer(content):
        cat_name = cat_match.group(1)
        cat_body = cat_match.group(2)
        
        # 匹配每个卡片对象 {e:"...", n:"...", d:"...", f:"..."}
        card_pattern = re.compile(r'\{\s*e\s*:\s*"([^"]*)".*?n\s*:\s*"([^"]*)".*?d\s*:\s*"([^"]*)".*?f\s*:\s*"([^"]*)".*?\}')
        
        for card_match in card_pattern.finditer(cat_body):
            emoji = card_match.group(1)
            name = card_match.group(2)
            desc = card_match.group(3)
            file_path = card_match.group(4)
            
            # 从文件名提取卡片编号
            card_id = os.path.basename(file_path).replace('.html', '')
            
            cards_list.append({
                'id': card_id,
                'name': name,
                'file': file_path,
                'cat': cat_name,
                'desc': desc,
                'emoji': emoji,
            })
    
    return cards_list

# ============================================================
# 3. 匹配逻辑
# ============================================================
def extract_product_keywords(name):
    """提取产品关键词"""
    # 去掉编号和"沧林食品"等后缀
    name = re.sub(r'·.*$', '', name)
    name = re.sub(r'CF-\d+|JL-\d+|TL-\d+', '', name)
    
    # 产品关键词提取
    keywords = set()
    
    # 常见食材词
    foods = ['鸡', '鸭', '鱼', '肉', '牛', '羊', '猪', '虾', '蟹', '蛋', '豆',
             '茶', '奶', '咖啡', '柠檬', '椰', '桃', '莓', '果', '瓜', '薯',
             '米', '面', '粉', '饭', '粥', '汤', '饼', '包', '饺', '丸', '肠',
             '酱', '油', '醋', '糖', '蜜', '椒', '辣', '姜', '蒜', '葱',
             '卤', '烤', '炸', '煎', '蒸', '炒', '煮', '焖', '炖', '熏',
             '冰', '凉', '热', '鲜', '香', '麻', '甜', '酸', '苦', '咸']
    
    for f in foods:
        if f in name.lower():
            keywords.add(f)
    
    return keywords

def match_score(card_name, recipe_name):
    """计算匹配分数"""
    cn = card_name.lower()
    rn = recipe_name.lower()
    
    # 去掉"沧林食品"等
    cn_clean = re.sub(r'·.*$', '', cn).strip()
    rn_clean = re.sub(r'·.*$', '', rn).strip()
    
    # 1. 完全匹配
    if cn_clean == rn_clean:
        return 1.0
    
    # 2. 子串匹配
    if len(cn_clean) >= 2 and cn_clean in rn_clean:
        return len(cn_clean) / max(len(rn_clean), 1)
    if len(rn_clean) >= 2 and rn_clean in cn_clean:
        return len(rn_clean) / max(len(cn_clean), 1)
    
    # 3. 关键词匹配
    card_kw = extract_product_keywords(cn)
    recipe_kw = extract_product_keywords(rn)
    
    if not card_kw or not recipe_kw:
        return 0.0
    
    overlap = card_kw & recipe_kw
    if len(overlap) >= 2:
        return len(overlap) / max(len(card_kw | recipe_kw), 1) * 0.6
    
    return 0.0

# ============================================================
# 4. 品类映射
# ============================================================
CAT_MAP = {
    '咖啡系列': ['饮品/甜品'],
    '酱料系列': ['酱料'],
    '炸物系列': ['炸物', '小吃'],
    '炸鸡系列': ['炸物', '小吃'],
    '鸡排系列': ['炸物', '小吃'],
    '糖水系列': ['饮品/甜品'],
    '甜品系列': ['饮品/甜品'],
    '饮品系列': ['饮品/甜品'],
    '奶茶系列': ['饮品/甜品'],
    '手打柠檬茶': ['饮品/甜品'],
    '包子系列': ['面点'],
    '早餐系列': ['面点', '粥品'],
    '粥品系列': ['粥品'],
    '粉面系列': ['面食'],
    '面食系列': ['面食'],
    '炒饭/拌菜': ['热菜'],
    '炒饭炒面花甲': ['热菜'],
    '冷吃系列': ['凉菜'],
    '火锅酸汤': ['底料', '汤底/卤水'],
    '汤料卤水': ['汤底/卤水'],
    '卤炸帮': ['卤煮肉制品', '炸物'],
    '经典名鸡': ['卤煮肉制品', '热菜'],
    '韩式系列': ['小吃', '酱料'],
    '复合酱料': ['酱料'],
    '特色系列': ['小吃', '其他'],
    '摆摊小吃': ['小吃', '其他'],
    '其他': ['小吃', '其他'],
    '日式系列': ['小吃', '其他'],
    '傣舂系列': ['凉菜', '小吃'],
    '胡辣汤': ['汤底/卤水', '粥品'],
    '预制半成品': ['其他'],
    '门店运营': ['其他'],
}

def main():
    recipes = load_recipes()
    cards = parse_cards_data()
    
    print(f"虾哥配方: {len(recipes)} 条")
    print(f"我们的卡: {len(cards)} 张")
    
    # 按品类分组 配方
    recipes_by_cat = defaultdict(list)
    for r in recipes:
        recipes_by_cat[r['cat']].append(r)
    
    # 匹配
    matched = []
    unmatched = []
    low_conf = []
    
    for card in cards:
        cid = card['id']
        cname = card['name']
        ccat = card['cat']
        
        best = None
        best_score = 0
        
        # 候选品类
        target_cats = CAT_MAP.get(ccat, [])
        candidates = []
        for tc in target_cats:
            candidates.extend(recipes_by_cat.get(tc, []))
        
        # 如果没品类映射，全部配方都试
        if not candidates:
            candidates = recipes
        
        for r in candidates:
            score = match_score(cname, r['name'])
            if score > best_score:
                best_score = score
                best = r
        
        if best and best_score >= 0.3:
            matched.append({
                'card_id': cid,
                'card_name': cname,
                'card_cat': ccat,
                'recipe_id': best['id'],
                'recipe_name': best['name'],
                'recipe_cat': best['cat'],
                'score': round(best_score, 2),
                'recipe_content': best['content'],
            })
            if best_score < 0.6:
                low_conf.append(matched[-1])
        else:
            unmatched.append(card)
    
    # 按品类统计
    cat_stats = defaultdict(lambda: [0, 0])  # [matched, total]
    for m in matched:
        cat_stats[m['card_cat']][0] += 1
        cat_stats[m['card_cat']][1] += 1
    for u in unmatched:
        cat_stats[u['cat']][1] += 1
    
    print(f"\n{'='*60}")
    print(f"匹配率: {len(matched)}/{len(matched)+len(unmatched)} = {len(matched)/(len(matched)+len(unmatched))*100:.1f}%")
    print(f"低置信度 (<0.6): {len(low_conf)}")
    
    print(f"\n--- 品类匹配详情 ---")
    for cat in sorted(cat_stats.keys()):
        m, t = cat_stats[cat]
        pct = m/t*100 if t > 0 else 0
        bars = '█' * int(pct/5) + '░' * (20 - int(pct/5))
        print(f"  {cat:12s} {bars} {m}/{t} ({pct:.0f}%)")
    
    # 保存结果
    result = {
        'matched': matched,
        'unmatched_ids': [u['id'] for u in unmatched],
        'stat': {
            'total': len(matched) + len(unmatched),
            'matched': len(matched),
            'unmatched': len(unmatched),
            'rate': f"{len(matched)/(len(matched)+len(unmatched))*100:.1f}%"
        }
    }
    
    with open("/Users/mac/Desktop/青葵/foodintelai-site/match_result.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    
    # 输出详细匹配列表
    print(f"\n--- 高匹配度 (>0.8) ---")
    for m in sorted(matched, key=lambda x: -x['score']):
        if m['score'] >= 0.8:
            print(f"  [{m['card_id']}] {m['card_name'][:25]:25s} ↔ {m['recipe_name']:15s} ({m['score']:.2f})")
    
    print(f"\n--- 低置信度 (<0.6, 需人工确认) ---")
    for m in low_conf:
        print(f"  [{m['card_id']}] {m['card_name'][:25]:25s} ↔ {m['recipe_name']:15s} ({m['score']:.2f})")
    
    print(f"\n--- 未匹配卡片 (需补充数据) ---")
    un_by_cat = defaultdict(list)
    for u in unmatched:
        un_by_cat[u['cat']].append(u['id'])
    for cat in sorted(un_by_cat.keys()):
        ids = un_by_cat[cat]
        print(f"  {cat} ({len(ids)}张): {', '.join(ids[:15])}{'...' if len(ids) > 15 else ''}")
    
    print(f"\n结果已保存: match_result.json")
    
    return matched, unmatched

if __name__ == '__main__':
    main()
