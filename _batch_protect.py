#!/usr/bin/env python3
"""
第一层防护 · 批量转换V5.1卡片（防小白版）

作用：
- 把配方数据从HTML里抽出来，放到独立JS数据文件
- HTML只留"加载完整出摊包"按钮，无内联配方
- 数据文件路径经base64编码，不在HTML里明文出现
- 加右键菜单禁用+F12快捷键拦截
- 保留paywall.js模糊保护

虾哥说：现在最要紧的不是防扒，是让更多人点进来。
"""

import os
import re
import base64
import json
import time

SITE_ROOT = os.path.expanduser("~/Desktop/青葵/foodintelai-site")
CATALOG_DIR = os.path.join(SITE_ROOT, "catalog")
DATA_DIR = os.path.join(SITE_ROOT, "data")

# 各类统计
stats = {"processed": 0, "skipped_no_v51": 0, "skipped_done": 0, "errors": []}


def sanitize_filename(card_id):
    """把卡片ID处理成安全文件名"""
    # 替换特殊字符
    s = card_id
    for ch in [' ', '·', '．', '：', '（', '）', '!', '！', '，', '。', '、', '；', '？', '—', '–', '"', '"', "'", "'", '/', '\\']:
        s = s.replace(ch, '_')
    # 只保留安全字符
    s = re.sub(r'[^a-zA-Z0-9_\-\u4e00-\u9fff]', '_', s)
    # 合并连续下划线
    s = re.sub(r'_+', '_', s).strip('_')
    # 限制长度
    if len(s) > 80:
        s = s[:80]
    return s


def extract_pay_content(html_content):
    """从HTML中提取pay-content区域的innerHTML"""
    pattern = r'<div\s+id="payContent"\s+class="pay-content">(.*?)</div>\s*\n?\s*(?:<div\s+class="badge")'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def get_card_id(html_content):
    """从HTML的title标签提取卡片ID"""
    m = re.search(r'<title>(.*?)</title>', html_content)
    return m.group(1).strip() if m else None


def has_v51_button(html_content):
    """检查是否含V5.1解锁按钮"""
    return '展开完整出摊包' in html_content


def has_been_processed(html_content):
    """检查是否已被本脚本处理过"""
    return 'loadRecipeData' in html_content


def insert_before_closing(html, marker, snippet):
    """在指定标记前插入代码"""
    idx = html.find(marker)
    if idx >= 0:
        return html[:idx] + snippet + html[idx:]
    return html


def process_card(filepath):
    """处理单张卡片"""
    rel_path = os.path.relpath(filepath, SITE_ROOT)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
        content = raw
    
    # 跳过非V5.1
    if not has_v51_button(content):
        stats["skipped_no_v51"] += 1
        return None
    
    # 跳过已处理的
    if has_been_processed(content):
        stats["skipped_done"] += 1
        return None
    
    # 提取配方数据
    recipe_data = extract_pay_content(content)
    if not recipe_data:
        stats["errors"].append(f"未找到配方数据: {rel_path}")
        return None
    
    # 提取卡片ID
    card_id = get_card_id(content)
    if not card_id:
        card_id = os.path.splitext(os.path.basename(filepath))[0]
    
    safe_id = sanitize_filename(card_id)
    data_filename = f"recipe_{safe_id}.js"
    data_filepath = os.path.join(DATA_DIR, data_filename)
    encoded_path = base64.b64encode(f"data/{data_filename}".encode()).decode()
    
    # ---------- 1. 生成配方数据JS文件 ----------
    escaped_html = json.dumps(recipe_data)
    js_content = f'''(function() {{
  if (!window._RD) window._RD = {{}};
  window._RD[{json.dumps(card_id)}] = {escaped_html};
}})();
'''
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(data_filepath, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # ---------- 2. 替换pay-area ----------
    # 找到旧的pay-area区域（从pay-area开始到badge的</div>结束）
    old_pay = re.search(
        r'<div class="pay-area">.*?<div class="badge"[^>]*>.*?</div>\s*</div>',
        content, re.DOTALL
    )
    
    if not old_pay:
        # 尝试更宽松的匹配
        old_pay = re.search(
            r'<div class="pay-area">.*?</div>\s*(?:\n\s*)?</div>(?:\s*\n)?',
            content, re.DOTALL
        )
    
    if not old_pay:
        stats["errors"].append(f"无法定位pay-area: {rel_path}")
        return None
    
    new_pay = f'''<div class="pay-area">
  <div class="lock-icon">[保护]</div>
  <h3>📦 完整出摊包 · 数据全开</h3>
  <div class="p-sub">7大模块：精确配方 · 精确克数 · 温度曲线 · 批量SOP · 翻车处理 · 变体方案 · 规模化方案</div>
  <div class="price-tag">¥68 <small>永久解锁</small></div>
  <button class="btn" onclick="loadRecipeData({json.dumps(card_id)})">🔓 加载完整出摊包</button>
  <div class="note">配方数据经保护处理，点击加载</div>
  <div id="payContent" class="pay-content" style="display:none;min-height:100px">
    <div style="text-align:center;padding:20px;color:#b5aaa0;font-size:12px">⏳ 数据加载中...</div>
  </div>
</div>'''
    
    content = content.replace(old_pay.group(0), new_pay)
    
    # ---------- 3. 添加数据加载脚本 ----------
    loader_script = f'''
<script>
(function(){{
  // 配方数据动态加载器（保护层）
  window.RECIPE_CACHE = window.RECIPE_CACHE || {{}};
  window.loadRecipeData = function(cardId) {{
    var btn = document.querySelector('.pay-area .btn');
    var pc = document.getElementById('payContent');
    if (!pc) return;
    if (pc.dataset.loaded === '1') {{
      var show = pc.style.display === 'none';
      pc.style.display = show ? 'block' : 'none';
      if (btn) btn.textContent = show ? '收起' : '🔓 加载完整出摊包';
      return;
    }}
    var f = atob('{encoded_path}');
    var s = document.createElement('script');
    s.src = f;
    s.onload = function() {{
      var d = window._RD && window._RD[cardId];
      if (d) {{
        pc.innerHTML = d;
        pc.style.display = 'block';
        pc.dataset.loaded = '1';
        if (btn) btn.textContent = '收起';
      }} else {{
        pc.innerHTML = '<div style="text-align:center;padding:20px;color:#b53b3b">数据加载失败，请刷新页面重试</div>';
      }}
    }};
    s.onerror = function() {{
      pc.innerHTML = '<div style="text-align:center;padding:20px;color:#b53b3b">数据加载失败，请刷新页面重试</div>';
    }};
    document.body.appendChild(s);
  }};
}})();
</script>'''
    
    content = content.replace('<script src="../../paywall.js"></script>',
                               loader_script + '\n<script src="../../paywall.js"></script>')
    
    # ---------- 4. 添加右键禁用 ----------
    block_script = '''
<script>
// 防顺手复制：禁用右键菜单 + F12/开发者工具快捷键
document.addEventListener('contextmenu',function(e){e.preventDefault()});
document.addEventListener('keydown',function(e){
  if(e.key==='F12'||(e.ctrlKey&&e.shiftKey&&(e.key==='I'||e.key==='J'||e.key==='C'))||(e.ctrlKey&&e.key==='U'))
    e.preventDefault();
});
</script>'''
    content = content.replace('</head>', block_script + '\n</head>')
    
    # ---------- 5. 写回文件 ----------
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    stats["processed"] += 1
    print(f"  ✅ {card_id[:40]}... → data/{data_filename}")
    return card_id


def main():
    print("=" * 55)
    print("  第一层防护 · 批量转换V5.1卡片")
    print("  数据 → 从HTML抽到独立JS文件")
    print("  路径 → Base64编码")
    print("  右键/F12 → 拦截")
    print("=" * 55)
    
    start = time.time()
    
    # 扫描所有HTML卡片
    for root, dirs, files in os.walk(CATALOG_DIR):
        # 跳过已处理过的目录
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            filepath = os.path.join(root, fname)
            process_card(filepath)
    
    elapsed = time.time() - start
    
    # 统计
    print(f"\n{'='*55}")
    print(f"  转换完成!")
    print(f"  ✅ 已处理: {stats['processed']} 张")
    print(f"  ⏭️  跳过(非V5.1): {stats['skipped_no_v51']} 张")
    print(f"  ⏭️  跳过(已处理): {stats['skipped_done']} 张")
    if stats['errors']:
        print(f"  ❌ 错误: {len(stats['errors'])} 个")
        for e in stats['errors'][:5]:
            print(f"     - {e}")
    print(f"  ⏱️  耗时: {elapsed:.1f}秒")
    print(f"  📁 数据目录: data/")
    print(f"\n  部署：git add -A && git commit -m '第一层防护' && git push")
    print(f"{'='*55}")


if __name__ == '__main__':
    main()
