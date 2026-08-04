#!/usr/bin/env python3
"""
Category Profile Engine V0.1 · 品类画像引擎
FoodIntelAI Data Layer → 画像层

输入: 品类关键词 (如"米线")
数据源: FID-001 郑州餐饮数据集 (郑州.xlsx)
输出: 统一格式品类画像 (CPE-001 标准)

用法: python3 category_profile_engine.py 米线
"""
import openpyxl, collections, re, statistics, sys, json

DATA_PATH = '/Users/mac/Desktop/郑州.xlsx'

def clean_num(v):
    """Rule-001: 科学计数法异常清理"""
    if isinstance(v, float) and v > 1e10:
        return None
    return v

def extract_score(s):
    """从 '口味:4.4 环境:4.4 服务:4.4' 提取口味分"""
    if isinstance(s, str) and '口味' in s:
        m = re.search(r'口味:([\d.]+)', s)
        if m: return float(m.group(1))
    return None

def brand_of(name):
    """Rule-002: 品牌归一 (店名关键词匹配)"""
    BRANDS = ['蜜雪冰城','瑞幸','霸王茶姬','库迪','沪上阿姨','茶百道','古茗','喜茶','奈雪','华莱士','杨国福','张亮','阿香','米村','塔斯汀','夸父','正新','锅圈','幸运咖','书亦','益禾堂','甜啦啦']
    for b in BRANDS:
        if b in name: return b
    return None

def load_all():
    wb = openpyxl.load_workbook(DATA_PATH, read_only=True, data_only=True)
    ws = wb['美食']
    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    data = []
    for r in rows:
        data.append(r)
    return headers, data

def profile(keyword):
    headers, data = load_all()
    # 匹配: 店名含关键词 OR 三类含关键词
    matched = []
    for r in data:
        nm = str(r[8]) if r[8] else ''
        c3 = str(r[7]) if r[7] else ''
        if keyword in nm or keyword in c3:
            matched.append(r)
    n = len(matched)
    if n == 0:
        print(f'❌ 品类"{keyword}"无匹配门店'); return

    # 覆盖率
    price_n = sum(1 for r in matched if isinstance(r[11], (int,float)))
    score_n = sum(1 for r in matched if extract_score(r[12]) is not None)
    comment_n = sum(1 for r in matched if isinstance(r[10], (int,float)))

    # 品类结构
    cat3 = collections.Counter(str(r[7]) for r in matched if r[7])
    # 区域
    dist = collections.Counter(str(r[19]) for r in matched if r[19])
    biz = collections.Counter(str(r[20]) for r in matched if r[20])
    # 品牌
    brands = collections.Counter()
    for r in matched:
        b = brand_of(str(r[8]) if r[8] else '')
        if b: brands[b] += 1
    # 价格
    prices = sorted(r[11] for r in matched if isinstance(r[11], (int,float)))
    # 评分
    scores = sorted(extract_score(r[12]) for r in matched if extract_score(r[12]) is not None)
    # 营业状态
    state = collections.Counter(str(r[28]) for r in matched if r[28])

    print(f'═══ CPE-001 · {keyword}品类画像 ═══')
    print(f'数据源: FID-001 郑州餐饮数据集 (2025H1快照)')
    print(f'\n【市场规模】')
    print(f'  门店数: {n} 家')
    print(f'  覆盖率: 价格 {price_n/n*100:.0f}% | 评分 {score_n/n*100:.0f}% | 评论 {comment_n/n*100:.0f}%')
    print(f'\n【品类结构】三类 TOP8')
    for k,v in cat3.most_common(8): print(f'  {k}: {v} ({v/n*100:.1f}%)')
    print(f'\n【区域分布】区县 TOP8')
    for k,v in dist.most_common(8): print(f'  {k}: {v} ({v/n*100:.1f}%)')
    print(f'\n【商圈分布】TOP6')
    for k,v in biz.most_common(6): print(f'  {k}: {v}')
    print(f'\n【品牌格局】连锁品牌')
    if brands:
        for k,v in brands.most_common(8): print(f'  {k}: {v} 家')
        print(f'  连锁化率(TOP品牌合计): {sum(brands.values())/n*100:.1f}%')
    else:
        print('  无识别品牌 (高度分散)')
    print(f'\n【价格带】(有价格 {len(prices)} 家)')
    if prices:
        print(f'  中位数: ¥{prices[len(prices)//2]}')
        for lo,hi in [(0,15),(15,25),(25,40),(40,60),(60,10**9)]:
            c = sum(1 for p in prices if lo <= p < hi)
            print(f'  ¥{lo}-{hi}: {c} ({c/len(prices)*100:.1f}%)')
    print(f'\n【评分分布】(有评分 {len(scores)} 家)')
    if scores:
        print(f'  均值: {statistics.mean(scores):.2f} | 中位数: {statistics.median(scores)}')
        for lo,hi in [(4.5,5.1),(4.0,4.5),(3.5,4.0),(0,3.5)]:
            c = sum(1 for s in scores if lo <= s < hi)
            print(f'  {lo}-{hi}: {c} ({c/len(scores)*100:.1f}%)')
    print(f'\n【风险项】')
    print(f'  ⚠️ 评分覆盖率仅 {score_n/n*100:.0f}% (结论须标注覆盖率)')
    if len(biz) <= 5: print('  ⚠️ 商圈分布集中, 密度风险')
    if state.get('暂停营业'): print(f'  ⚠️ 暂停营业 {state["暂停营业"]} 家')
    print(f'\n(CPE V0.1 · 画像为结构性描述, 非商业判断 · FID-001 V1.1 frozen)')

if __name__ == '__main__':
    kw = sys.argv[1] if len(sys.argv) > 1 else '米线'
    profile(kw)
