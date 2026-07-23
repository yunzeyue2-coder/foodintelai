#!/usr/bin/env python3
"""
给炸鸡六维模型和卤味七维模型添加章节导航（TOC）
注入位置：第一个h2之前
同时给每个h2/h3添加id锚点
"""
import re
import os

base_dir = "/Users/mac/Desktop/青葵/foodintelai-site/frameworks"

toc_style = '''
/* 章节导航 */
.toc-wrap{background:linear-gradient(135deg,#faf8f5,#f5f0e8);border:1.5px solid #c4a35a;border-radius:10px;padding:16px 20px;margin:24px 0 32px}
.toc-title{font-size:11px;color:#8b6914;font-weight:600;letter-spacing:2px;margin-bottom:10px}
.toc-list{list-style:none;padding:0;margin:0}
.toc-list li{font-size:12px;line-height:1.8;padding:2px 0}
.toc-list li a{color:#3a322a;text-decoration:none;transition:color .2s}
.toc-list li a:hover{color:#8b6914}
.toc-list li.toc-h2{font-weight:600}
.toc-list li.toc-h3{padding-left:16px;font-weight:400;color:#6a5a3a}
'''

def slugify(text):
    """从中文文本生成ID"""
    # 去掉HTML标签和特殊字符
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[：，。！？、""''【】《》（）\s]+', '-', text)
    text = text.strip('-')
    # 保持中文，只去掉特殊符号
    return 's-' + text[:40]

def add_toc(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 先提取所有h2/h3的文本和位置
    headings = []
    for match in re.finditer(r'<(h[23])([^>]*)>(.*?)</\1>', content, re.DOTALL):
        tag = match.group(1)
        attrs = match.group(2)
        text = match.group(3)
        # 去掉text中的HTML标签
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        pos = match.start()
        end = match.end()
        
        # 检查是否有id
        existing_id = re.search(r'id=[\'"]([^\'"]+)[\'"]', attrs)
        if existing_id:
            hid = existing_id.group(1)
        else:
            hid = slugify(clean_text)
        
        headings.append((pos, end, tag, clean_text, hid))
    
    if not headings:
        print(f"  ⚠️  {filepath}: 未找到h2/h3")
        return
    
    # 生成TOC HTML
    toc_items = []
    for pos, end, tag, text, hid in headings:
        cls = 'toc-h2' if tag == 'h2' else 'toc-h3'
        toc_items.append(f'<li class="{cls}"><a href="#{hid}">{text}</a></li>')
    
    toc_html = f'''<style>{toc_style}</style>
<div class="toc-wrap">
<div class="toc-title">📑 本章导读</div>
<ol class="toc-list">
{"".join(toc_items)}
</ol>
</div>'''
    
    # 给每个heading添加id（如果没有的话）
    replacements = []
    for pos, end, tag, text, hid in headings:
        old_heading = content[pos:end]
        # 检查是否已有id
        if f'id="{hid}"' in old_heading or f"id='{hid}'" in old_heading:
            continue
        # 检查是否有其他id
        if re.search(r'id=[\'"][^\'"]+[\'"]', old_heading):
            continue
        # 添加id
        new_heading = re.sub(r'^<' + tag, f'<{tag} id="{hid}"', old_heading)
        replacements.append((old_heading, new_heading))
    
    # 从后往前替换，保持位置不变
    for old, new in reversed(replacements):
        content = content.replace(old, new, 1)
    
    # 找到第一个h2的位置，在它前面插入TOC
    # 先检查是否已经有toc-wrap
    if 'toc-wrap' in content:
        print(f"  ⚠️  {filepath}: 已有TOC，跳过")
        return
    
    first_h2 = content.find('<h2')
    if first_h2 > 0:
        content = content[:first_h2] + toc_html + content[first_h2:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ {os.path.basename(filepath)}: 添加 {len(headings)} 个章节导航")

# 处理两个文件
for fname in ['炸鸡六维模型.html', '卤味七维模型.html']:
    path = os.path.join(base_dir, fname)
    if os.path.exists(path):
        add_toc(path)
    else:
        print(f"  ❌ 文件不存在: {path}")

print("\n完成！")
