#!/usr/bin/env python3
"""给三个案例页面添加FoodIntelAI页面样式"""
import os

cases = {
    "冷吃推车案例.html": {"title": "冷吃推车真实案例 · FoodIntelAI"},
    "王大哥炒鸡案例.html": {"title": "王大哥炒鸡真实案例 · FoodIntelAI"},
    "产供销一体化案例.html": {"title": "产供销一体化真实案例 · FoodIntelAI"},
}

base_dir = "/Users/mac/Desktop/青葵/foodintelai-site/cases"

page_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#f7f5f0;font-family:'Inter','Noto Serif SC','PingFang SC','Microsoft YaHei',serif;color:#2a2218;display:flex;justify-content:center;-webkit-font-smoothing:antialiased;padding:24px 12px}}
.page{{max-width:720px;width:100%}}

/* 返回 */
.back{{display:inline-block;font-size:11px;color:#8b6914;text-decoration:none;font-family:'Inter',sans-serif;letter-spacing:1px;margin-bottom:14px;padding:4px 12px;background:#fff;border:1px solid #e8e3db;border-radius:6px;transition:all .2s}}
.back:hover{{background:#faf8f5;border-color:#c4a35a}}

/* 案例卡片 */
.case-box{{background:#fff;border:1px solid #e8e3db;border-radius:12px;padding:28px 24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}}
.cb-badge{{display:inline-block;font-size:10px;padding:3px 10px;border-radius:4px;background:#fcf8f2;color:#8b6914;letter-spacing:1px;margin-bottom:10px}}
.cb-title{{font-size:18px;font-weight:700;color:#1a1a1a;line-height:1.4;margin-bottom:6px;letter-spacing:1px}}
.cb-sub{{font-size:13px;color:#6a5a3a;line-height:1.7;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid #f0ece4}}

/* 数据指标 */
.cb-stats{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:14px 0}}
.cb-stat{{background:#faf8f5;border:1px solid #e8e3db;border-radius:8px;padding:12px;text-align:center}}
.cb-stat .num{{font-size:20px;font-weight:700;color:#8b6914;font-family:'Inter',sans-serif}}
.cb-stat .num .unit{{font-size:13px;font-weight:400;color:#b5aaa0}}
.cb-stat .label{{font-size:11px;color:#8a7a6a;margin-top:2px;line-height:1.4}}

.cb-divider{{border:none;border-top:1px solid #f0ece4;margin:16px 0}}

/* 区块标题 */
.cb-section-title{{font-size:14px;font-weight:600;color:#7a5a04;margin-bottom:10px;letter-spacing:1px;padding-left:8px;border-left:3px solid #c4a35a}}

/* 产品/阶段列表 */
.cb-products{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:4px}}
.cb-product{{background:#faf8f5;border:1px solid #ede8e0;border-radius:8px;padding:10px 12px;display:flex;align-items:flex-start;gap:8px}}
.cb-product .emoji{{font-size:16px;margin-top:1px}}
.cb-product .info{{flex:1;min-width:0}}
.cb-product .info .name{{font-size:12px;font-weight:600;color:#2a2218;margin-bottom:1px}}
.cb-product .info .desc{{font-size:11px;color:#6a5a3a;line-height:1.5}}
.cb-product .price-tag{{font-size:9px;padding:1px 6px;border-radius:3px;background:#f0eee8;color:#8a7a6a;white-space:nowrap;margin-top:2px}}

/* 工艺链 */
.cb-process{{background:#faf8f5;border:1px solid #e8e3db;border-radius:8px;padding:12px 14px;margin-bottom:4px}}
.cb-process .steps{{display:flex;flex-wrap:wrap;align-items:center;gap:2px;font-size:12px}}
.cb-process .steps .step{{background:#fff;border:1px solid #e0ddd5;border-radius:4px;padding:3px 8px;color:#5a4a3a}}
.cb-process .steps .arrow{{color:#c4a35a;font-size:10px}}

/* CTA */
.cb-cta{{display:block;text-align:center;padding:10px 20px;background:#8b6914;color:#fff;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600;letter-spacing:2px;margin:16px 0 10px;transition:background .2s}}
.cb-cta:hover{{background:#7a5a04}}
.cb-cta .arrow{{font-size:16px;margin-left:4px}}

.cb-footer{{text-align:center;font-size:10px;color:#b5aaa0;padding-top:10px;font-family:'Inter',sans-serif}}

@media(max-width:600px){{
  .page{{padding:0}}
  .case-box{{padding:20px 16px}}
  .cb-stats{{grid-template-columns:1fr}}
  .cb-products{{grid-template-columns:1fr}}
  .cb-stat .num{{font-size:17px}}
}}
</style>
</head>
<body>
<div class="page">

<a href="../stall.html" class="back">← 返回产品机会库</a>

{content}

</div>
</body>
</html>'''

for fname, info in cases.items():
    path = os.path.join(base_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Strip any existing wrapper if present (detect by looking for DOCTYPE)
    if '<!DOCTYPE' in content:
        # Already has a wrapper, extract the inner content between page divs
        import re
        m = re.search(r'<div class="page">(.*?)</div>\s*</body>', content, re.DOTALL)
        if m:
            content = m.group(1)
        else:
            # Try to get everything after <body>
            m = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
            if m:
                content = m.group(1)
    
    full = page_template.format(title=info["title"], content=content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full)
    print(f"  ✅ {fname}")

print(f"\n完成！")
