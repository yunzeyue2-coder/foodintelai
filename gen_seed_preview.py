#!/usr/bin/env python3
"""从21篇HTML文章中提取数据，输出SQL seed文件格式"""
import re, os

base_dir = "/Users/mac/Desktop/青葵/foodintelai-site/research"

files = [
    # (filename, category, author)
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

def extract_meta(html):
    """提取标题、摘要、日期、正文"""
    # 标题
    title_m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = title_m.group(1).strip() if title_m else ""
    title = re.sub(r'<[^>]+>', '', title).strip()
    
    # 日期
    date_m = re.search(r'<span>📅\s*(\d{4}\.\d{2}\.\d{2})', html)
    date = date_m.group(1) if date_m else ""
    
    # 摘要 - 找.meta后面的第一个<p>或者.highlight
    summary = ""
    # 尝试找core statement
    core_m = re.search(r'<div class="ct">(.*?)</div>', html, re.DOTALL)
    if core_m:
        summary = re.sub(r'<[^>]+>', '', core_m.group(1)).strip()
    if not summary or len(summary) < 20:
        # 找第一个highlight
        hl_m = re.search(r'<div class="highlight">(.*?)</div>', html, re.DOTALL)
        if hl_m:
            summary = re.sub(r'<[^>]+>', '', hl_m.group(1)).strip()
    summary = summary[:150].replace("'", "''")
    
    # 正文全文 - 去除HTML标签，保留文本
    # 找到.page开始到.footer之前
    body_m = re.search(r'<div class="page">(.*?)<hr>', html, re.DOTALL)
    body = body_m.group(1) if body_m else html
    # 去除所有HTML标签
    body_text = re.sub(r'<[^>]+>', '', body)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    body_text = body_text.replace("'", "''")
    
    return title, summary, date, body_text

entries = []
for fname, cat, author in files:
    path = os.path.join(base_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    title, summary, date, body = extract_meta(html)
    entries.append((fname, cat, author, title, summary, date, body))

# 输出SQL
print("-- FoodIntelAI 21篇文章 seed 数据")
print("-- 需要先在 categories 表确认: 炸鸡(id), 卤味(id), 面食(id)")
print("-- 将下面 XXX_炸鸡, XXX_卤味, XXX_面食 替换为实际categoryId\n")

for i, (fname, cat, author, title, summary, date, body) in enumerate(entries):
    cat_id = f"XXX_{cat}"
    
    # 摘要截取前100字左右
    short_summary = summary[:150] if len(summary) > 150 else summary
    
    # 正文取前500字做演示，实际灌数据时去掉 LIMIT
    preview = body[:500]
    
    print(f"""
-- {i+1}. {title}
-- 文件: {fname}
-- 品类: {cat} | 作者: {author} | 日期: {date}
INSERT INTO "articles" ("title", "summary", "content", "categoryId", "articleType", "author", "publishedAt", "status")
VALUES (
  '{title}',
  '{short_summary}',
  '{preview}',  -- ⚠️ 完整正文见完整版seed文件，此处仅前500字
  '{cat_id}',
  'industry_analysis',
  '{author}',
  '{date}',
  'published'
);
""")

print("-- ⬆️ 以上为预览版（正文仅500字）。完整版(21篇全文)需生成完整seed文件")
