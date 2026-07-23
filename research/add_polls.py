#!/usr/bin/env python3
"""给所有研究文章添加可点击投票组件（localStorage计数）"""
import re, os, hashlib

base_dir = "/Users/mac/Desktop/青葵/foodintelai-site/research"
files = [
    "炸鸡_炸鸡门派.html","炸鸡_六大门派.html","炸鸡_九步法.html","炸鸡_产品架构.html",
    "炸鸡_利益函数.html","炸鸡_五种生存路径.html","炸鸡_六维模型总纲.html",
    "卤味_卤味是什么产业.html","卤味_全国化困局.html","卤味_四维定位模型.html",
    "卤味_资本流向.html","卤味_三红利消失.html","卤味_万店失效.html","卤味_产业认知.html",
    "面食_三条路.html","面食_肉夹馍.html","面食_凉皮三姐妹.html","面食_泡馍四门生意.html",
    "面食_陕西的面.html","面食_三张底牌.html","面食_手工vs机器.html",
]

poll_css = '''
/* 投票组件 */
.poll{background:#fff;border:1px solid #e8e3db;border-radius:10px;padding:20px 24px;margin:24px 0}
.poll .pq{font-size:14px;font-weight:600;color:#2a2218;margin-bottom:12px;text-align:center}
.poll .po{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
.poll .po-btn{font-size:12px;padding:8px 16px;border:1.5px solid #d4c8b0;border-radius:20px;background:#faf8f5;color:#3a322a;cursor:pointer;transition:all .25s;user-select:none;font-family:inherit;line-height:1.4}
.poll .po-btn:hover{border-color:#c4a35a;background:#fcfaf7;transform:translateY(-1px)}
.poll .po-btn.voted{border-color:#8b6914;background:#fcf8f2;color:#7a5a04;font-weight:600}
.poll .po-btn.voted::after{content:' ✓';color:#8b6914}
.poll .po-btn:disabled{cursor:default;opacity:.8}
.poll .po-btn:disabled:hover{transform:none;border-color:#d4c8b0;background:#faf8f5}
.poll .results{margin-top:12px;display:none}
.poll .results.show{display:block}
.poll .rr{margin-bottom:6px}
.poll .rr .rl{display:flex;justify-content:space-between;font-size:11px;color:#6a5a3a;margin-bottom:2px}
.poll .rr .rl .rpct{font-weight:600;color:#8b6914}
.poll .rr .rb{height:6px;border-radius:3px;background:#f0ece4;overflow:hidden}
.poll .rr .rb .rf{height:100%;border-radius:3px;background:linear-gradient(90deg,#c4a35a,#8b6914);transition:width .6s ease;width:0}
.poll .poll-total{font-size:10px;color:#b5aaa0;text-align:center;margin-top:8px;font-family:'Inter',sans-serif}
'''

poll_js = '''
<script>
document.querySelectorAll('.poll').forEach(function(poll){
    var qid = poll.dataset.qid;
    var opts = poll.querySelectorAll('.po-btn');
    var resultsDiv = poll.querySelector('.results');
    var totalSpan = poll.querySelector('.poll-total');

    function loadResults(){
        var raw = localStorage.getItem('poll_'+qid);
        var votes = raw ? JSON.parse(raw) : {};
        var total = 0;
        opts.forEach(function(b){
            var v = votes[b.dataset.val] || 0;
            b._count = v;
            total += v;
        });
        return {votes:votes, total:total};
    }

    function renderResults(){
        var d = loadResults();
        var total = d.total;
        var bars = resultsDiv.querySelectorAll('.rf');
        opts.forEach(function(b,i){
            var pct = total>0 ? Math.round(b._count/total*100) : 0;
            bars[i].style.width = pct+'%';
        });
        var rls = resultsDiv.querySelectorAll('.rpct');
        opts.forEach(function(b,i){
            var pct = total>0 ? Math.round(b._count/total*100) : 0;
            rls[i].textContent = pct+'%';
        });
        totalSpan.textContent = '共 '+total+' 票';
    }

    // 检查是否已投
    var voted = localStorage.getItem('poll_voted_'+qid);
    if(voted){
        opts.forEach(function(b){
            b.disabled = true;
            if(b.dataset.val===voted){b.classList.add('voted');}
        });
        resultsDiv.classList.add('show');
        renderResults();
    }

    opts.forEach(function(b){
        b.addEventListener('click',function(){
            if(localStorage.getItem('poll_voted_'+qid)) return;
            var val = this.dataset.val;
            var raw = localStorage.getItem('poll_'+qid);
            var votes = raw ? JSON.parse(raw) : {};
            votes[val] = (votes[val]||0)+1;
            localStorage.setItem('poll_'+qid,JSON.stringify(votes));
            localStorage.setItem('poll_voted_'+qid,val);
            opts.forEach(function(bb){bb.disabled=true;if(bb.dataset.val===val)bb.classList.add('voted');});
            resultsDiv.classList.add('show');
            renderResults();
        });
    });
});
</script>'''

def extract_poll_data(html):
    """从现有的interact块提取问题和选项"""
    m = re.search(r'<div class="interact">\s*<div class="iq">(.*?)</div>\s*<div class="iopts">(.*?)</div>\s*</div>', html, re.DOTALL)
    if not m:
        return None
    question = m.group(1).strip()
    opts_html = m.group(2)
    options = re.findall(r'<span>(.*?)</span>', opts_html)
    return question, options, m.group(0)

def make_qid(filename, question):
    """生成唯一问题ID"""
    return hashlib.md5((filename + question[:20]).encode()).hexdigest()[:12]

def make_poll_html(question, options, qid):
    """生成投票HTML"""
    opt_btns = '\n'.join([f'<button class="po-btn" data-val="{chr(65+i)}">{o}</button>' for i,o in enumerate(options)])
    opt_bars = '\n'.join([f'<div class="rr"><div class="rl"><span>{o}</span><span class="rpct">0%</span></div><div class="rb"><div class="rf"></div></div></div>' for o in options])
    return f'''<div class="poll" data-qid="{qid}">
<div class="pq">💬 {question}</div>
<div class="po">{opt_btns}</div>
<div class="results"><div class="results-inner">{opt_bars}</div></div>
<div class="poll-total">共 0 票</div>
</div>'''

def inject_poll_css(html):
    if '.poll' in html:
        return html  # already has it
    # insert after the closing </style> tag
    return html.replace('</style>', poll_css + '\n</style>')

def inject_poll_js(html):
    if 'poll_' in html:
        return html
    # Insert before </body>
    return html.replace('</body>', poll_js + '\n</body>')

for fname in files:
    path = os.path.join(base_dir, fname)
    if not os.path.exists(path):
        print(f"  ❌ 不存在: {fname}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    data = extract_poll_data(html)
    if not data:
        print(f"  ⚠️ 未找到interact: {fname}")
        continue
    
    question, options, old_html = data
    qid = make_qid(fname, question)
    new_poll = make_poll_html(question, options, qid)
    
    html = html.replace(old_html, new_poll)
    html = inject_poll_css(html)
    html = inject_poll_js(html)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✅ {fname} → {qid}")

print(f"\n共处理 {len(files)} 篇文章")
