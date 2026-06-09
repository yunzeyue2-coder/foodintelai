#!/usr/bin/env python3
"""Add 大桶糖水 navigation link and card zone to index.html"""
from pathlib import Path
import re

wd = Path('/Users/mac/Desktop/青葵/foodintelai-site')
idx_path = wd / 'index.html'
idx = idx_path.read_text('utf-8')

# === 1. Add nav link ===
nav_close = idx.find('</div>', idx.find('cat-tags'))
last_link = idx.rfind('<a href=', idx.find('cat-tags'), nav_close)
new_nav = '<a href="#dt" style="display:inline-block;padding:4px 12px;font-size:11px;background:var(--card);border-radius:6px;text-decoration:none;color:var(--text);box-shadow:var(--shadow);transition:.15s">🧊 大桶糖水</a>\n    '
idx = idx[:last_link] + new_nav + idx[last_link:]

# === 2. Add DT card zone after TS (传统糖水) zone ===
# Find TG zone end
tg_pos = idx.find('id="tg"')
catfold_start = idx.find('cat-fold', tg_pos)
# Find the closing of cat-fold (3 nested div closes: grid + cat-fold)
close1 = idx.find('</div>', catfold_start + 50)
close2 = idx.find('</div>', close1 + 5)
close3 = idx.find('</div>', close2 + 5)
# Next section header
next_section = idx.find('<!--', close3 + 10)

# Generate DT cards
emoji_map = {
    '绿豆':'🫘','西米':'🥥','椰奶':'🥥','椰子':'🥥','芭乐':'🍈','草莓':'🍓',
    '桃胶':'🍑','桂花':'🌸','藕粉':'🌸','玉米':'🌽','杨梅':'🍒','芋头':'🍠',
    '酸梅':'🫙','米酒':'🍶','玫瑰':'🌹','菠萝':'🍍','柠檬':'🍋','茉莉':'🌸',
    '豆浆':'🥛','斑斓':'🌿','珍珠':'🟤','雪梨':'🍐','银耳':'🍄','红豆':'🫘',
    '红枣':'🔴','红薯':'🍠','抹茶':'🍵','海底椰':'🥥','西瓜':'🍉','芒果':'🥭',
    '板栗':'🌰','芝麻':'🫘','凤梨':'🍍','薄荷':'🌿','紫薯':'🍠','布丁':'🍮',
    '清补凉':'🥥','烧仙草':'🟤','奶茶':'🧋','杨枝甘露':'🥭','话梅':'🫙',
    '百香果':'🍈','马蹄':'🌰','火龙果':'🍈','冰':'🧊','糖水':'🧊','水果':'🍑'
}

dt_cards_html = ''
for i in range(1, 47):
    fname = f'DT_{i:03d}.html'
    card_path = wd / 'cards' / fname
    if not card_path.exists():
        continue
    content = card_path.read_text('utf-8', errors='ignore')
    ts = content.find('DT-')
    te = content.find('· 大桶糖水')
    title = content[ts:te].strip() if ts >= 0 and te >= 0 else fname
    
    emoji = '🧊'
    for kw, e in emoji_map.items():
        if kw in title:
            emoji = e
            break
    
    dt_cards_html += f'''  <!-- {fname} -->
  <a class="jingpin-card" href="cards/{fname}" style="display:flex;align-items:center;gap:8px;padding:12px;background:var(--card);border-radius:12px;text-decoration:none;color:var(--text);box-shadow:var(--shadow)">
    <div style="font-size:24px">{emoji}</div>
    <div style="flex:1;min-width:0">
      <div style="font-size:13px;font-weight:700">{title[:30]}</div>
    </div>
    <div style="font-size:14px;font-weight:700;color:var(--accent)">¥9.9</div>
  </a>

'''

dt_zone = f'''
<!-- ===== 大桶糖水专区 ===== -->
<div class="section-header" id="dt"><h2>🧊 大桶糖水 · 46款爆品</h2><span class="more">¥9.9 解锁完整配方</span></div>
<div class="cat-fold">
<div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">

{dt_cards_html}</div>
</div>

'''

idx = idx[:next_section] + dt_zone + idx[next_section:]

# Verify
print(f"✅ 首页更新完成")
print(f"   大小: {len(idx)} 字符")
print(f"   #tg: {idx.count('id=\"tg\"')} (导航1+专区1)")
print(f"   #dt: {idx.count('id=\"dt\"')} (导航1+专区1)")
print(f"   DT卡: {idx.count('DT_')} 张")

# Write
idx_path.write_text(idx, encoding='utf-8')
print("   已写入文件")
