#!/usr/bin/env python3
"""给所有研究文章添加分享条"""
import os

base_dir = "/Users/mac/Desktop/青葵/foodintelai-site/research"
files = [
    "炸鸡_炸鸡门派.html","炸鸡_六大门派.html","炸鸡_九步法.html","炸鸡_产品架构.html",
    "炸鸡_利益函数.html","炸鸡_五种生存路径.html","炸鸡_六维模型总纲.html",
    "卤味_卤味是什么产业.html","卤味_全国化困局.html","卤味_四维定位模型.html",
    "卤味_资本流向.html","卤味_三红利消失.html","卤味_万店失效.html","卤味_产业认知.html",
    "面食_三条路.html","面食_肉夹馍.html","面食_凉皮三姐妹.html","面食_泡馍四门生意.html",
    "面食_陕西的面.html","面食_三张底牌.html","面食_手工vs机器.html",
]

share_html = '''
<!-- 分享条 -->
<div class="share-bar">
<div class="share-label">分享本文</div>
<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
<button class="share-btn" onclick="copyLink(this)" title="复制链接">
<span class="sb-icon">🔗</span> 复制链接
</button>
<button class="share-btn" onclick="shareWeb()" title="分享给朋友">
<span class="sb-icon">📤</span> 分享
</button>
<button class="share-btn" onclick="window.print()" title="打印/保存为PDF">
<span class="sb-icon">🖨️</span> 打印
</button>
</div>
<div class="share-hint" id="shareHint" style="display:none">链接已复制</div>
</div>

<script>
function copyLink(btn){
    var url = window.location.href.split('?')[0];
    if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){
        showHint('✅ 链接已复制');
    });}else{
        var ta = document.createElement('textarea');ta.value=url;document.body.appendChild(ta);ta.select();
        document.execCommand('copy');document.body.removeChild(ta);showHint('✅ 链接已复制');
    }
}
function shareWeb(){
    if(navigator.share){navigator.share({title:document.title,url:window.location.href.split('?')[0]});}
    else{copyLink();}
}
function showHint(t){
    var h=document.getElementById('shareHint');h.textContent=t;h.style.display='block';
    setTimeout(function(){h.style.display='none';},2000);
}
</script>
'''

share_css = '''
.share-bar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:12px 16px;background:#faf8f5;border:1px solid #e8e3db;border-radius:8px;margin:24px 0 16px}
.share-bar .share-label{font-size:10px;color:#b5aaa0;letter-spacing:2px;font-family:'Inter',sans-serif;font-weight:500}
.share-btn{font-size:11px;padding:6px 12px;border:1px solid #d4c8b0;border-radius:6px;background:#fff;color:#6a5a3a;cursor:pointer;transition:all .2s;font-family:'Inter','PingFang SC',sans-serif;display:flex;align-items:center;gap:4px;line-height:1}
.share-btn:hover{border-color:#c4a35a;background:#fcfaf7;color:#7a5a04}
.share-btn .sb-icon{font-size:13px}
.share-hint{font-size:11px;color:#3A8D5D;width:100%;text-align:center;font-family:'Inter',sans-serif}
'''

def inject_share(html):
    if 'share-bar' in html:
        return html  # already has it
    
    # inject CSS before </style>
    html = html.replace('</style>', share_css + '\n</style>')
    
    # inject share bar before <hr> that precedes the footer
    # Look for the first <hr> that's near the end (before footer)
    # Find the last <hr>
    last_hr = html.rfind('<hr')
    if last_hr > 0:
        html = html[:last_hr] + share_html + html[last_hr:]
    
    return html

for fname in files:
    path = os.path.join(base_dir, fname)
    if not os.path.exists(path):
        print(f"  ❌ 不存在: {fname}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = inject_share(html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✅ {fname}")

print(f"\n共处理 {len(files)} 篇")
