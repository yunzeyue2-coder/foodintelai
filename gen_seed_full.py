#!/usr/bin/env python3
"""生成21篇文章完整SQL seed文件（纯正文，无JS，日期格式修正）"""
import re, os, datetime

base_dir = "/Users/mac/Desktop/青葵/foodintelai-site/research"

files = [
    ("炸鸡_炸鸡门派.html", "炸鸡", "沧林食品技术"),
    ("炸鸡_六大门派.html", "炸鸡", "VORA"),
    ("炸鸡_九步法.html", "炸鸡", "沧林食品技术"),
    ("炸鸡_产品架构.html", "炸鸡", "沧林食品技术"),
    ("炸鸡_利益函数.html", "炸鸡", "VORA"),
    ("炸鸡_五种生存路径.html", "炸鸡", "VORA"),
    ("炸鸡_六维模型总纲.html", "炸鸡", "VORA"),
    ("卤味_卤味是什么产业.html", "卤味", "沧林食品技术"),
    ("卤味_全国化困局.html", "卤味", "VORA"),
    ("卤味_四维定位模型.html", "卤味", "VORA"),
    ("卤味_资本流向.html", "卤味", "沧林食品技术"),
    ("卤味_三红利消失.html", "卤味", "沧林食品技术"),
    ("卤味_万店失效.html", "卤味", "沧林食品技术"),
    ("卤味_产业认知.html", "卤味", "沧林食品技术"),
    ("面食_三条路.html", "面食", "沧林食品技术"),
    ("面食_肉夹馍.html", "面食", "沧林食品技术"),
    ("面食_凉皮三姐妹.html", "面食", "沧林食品技术"),
    ("面食_泡馍四门生意.html", "面食", "沧林食品技术"),
    ("面食_陕西的面.html", "面食", "沧林食品技术"),
    ("面食_三张底牌.html", "面食", "沧林食品技术"),
    ("面食_手工vs机器.html", "面食", "沧林食品技术"),
]

def esc(s):
    return s.replace("'", "''").replace("\\", "\\\\")

def extract(html):
    title = ""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m: title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    
    date = ""
    m = re.search(r'📅\s*(\d{4})\.(\d{2})\.(\d{2})', html)
    if m: date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    
    summary = ""
    m = re.search(r'<div class="ct">(.*?)</div>', html, re.DOTALL)
    if m: summary = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if not summary or len(summary) < 30:
        m = re.search(r'<div class="highlight">(.*?)</div>', html, re.DOTALL)
        if m: summary = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    summary = summary[:200].rsplit(' ', 1)[0] if len(summary) > 200 else summary
    
    # 正文：取.page内到<hr>前，去掉<script>块
    body = ""
    m = re.search(r'<div class="page">(.*?)<hr>', html, re.DOTALL)
    if m:
        body_html = m.group(1)
        # 去掉所有<script>...</script>
        body_html = re.sub(r'<script[^>]*>.*?</script>', '', body_html, flags=re.DOTALL)
        # 去掉所有<style>...</style>
        body_html = re.sub(r'<style[^>]*>.*?</style>', '', body_html, flags=re.DOTALL)
        # 去掉HTML标签
        body_text = re.sub(r'<[^>]+>', '\n', body_html)
        body_text = re.sub(r'\n\s*\n', '\n\n', body_text)
        body = body_text.strip()
    
    return title, summary, date, body

rows = []
for fname, cat, author in files:
    with open(os.path.join(base_dir, fname), 'r') as f:
        title, summary, date, body = extract(f.read())
    rows.append((title, summary, body, cat, author, date))

# 输出
out = []
out.append("""// ============================================================
// FoodIntelAI · 21篇产业分析文章 seed 数据
// 生成时间: 2026-07-23
// 品类ID占位符: XXX_炸鸡, XXX_卤味, XXX_面食
// 使用前替换为实际categoryId
// ============================================================\n""")

for i, (title, summary, body, cat, author, date) in enumerate(rows):
    title_clean = title.replace("'", "''")
    out.append(f"// {i+1}. {title_clean}")
    out.append(f"// 品类: {cat} | 作者: {author} | 日期: {date}")
    out.append("await prisma.article.create({")
    out.append("  data: {")
    out.append(f"    title: '{esc(title)}',")
    out.append(f"    summary: '{esc(summary)}',")
    out.append(f"    content: `{esc(body)}`,")
    out.append(f"    categoryId: 'XXX_{cat}',")
    out.append("    articleType: 'industry_analysis',")
    out.append(f"    author: '{author}',")
    out.append(f"    publishedAt: new Date('{date}'),")
    out.append("    status: 'published',")
    out.append("  },")
    out.append("});")
    out.append("")

out.append("// ✅ 共21条 seed 数据")

with open("/Users/mac/Desktop/foodintelai_articles_seed.sql", "w", encoding='utf-8') as f:
    f.write("\n".join(out))

total_kb = os.path.getsize("/Users/mac/Desktop/foodintelai_articles_seed.sql") / 1024
print(f"✅ 生成完成: ~{total_kb:.0f}KB, {len(rows)} 条记录")
