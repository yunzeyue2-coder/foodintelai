#!/usr/bin/env python3
"""重建index.html：保留前1130行+新品类区+备份的footer"""

# 读取当前文件（保留前1130行）
with open("/Users/mac/Desktop/青葵/foodintelai-site/index.html", "r") as f:
    current = f.read()
current_lines = current.split("\n")
header = "\n".join(current_lines[:1130]) + "\n"

# 从备份读取footer部分
with open("/Users/mac/Desktop/青葵/foodintelai-site/index.html.bak.pre8cleanup", "r") as f:
    bak = f.read()
bak_lines = bak.split("\n")

# 找到wechat-box行
footer_start = None
for i, line in enumerate(bak_lines):
    if 'class="wechat-box"' in line:
        footer_start = i
        break

footer_html = "\n".join(bak_lines[footer_start:])

# ===== 新品类内容 =====
stall_content = """  <!-- ===== 热门项目（点击率排序） ===== -->
  <div class="section-header" id="hotProjects"><h2>🔥 热门项目</h2><span class="more">点击即看</span></div>
  <div class="hot-projects">
    <a class="hot-card" href="cards/HZ_001.html">
      <div class="hc-icon">🍗</div>
      <div class="hc-info">
        <div class="hc-name">韩式炸鸡</div>
        <div class="hc-tags"><span class="htag hot">🔥 抖音热门</span><span class="htag money">💰 3000元起</span><span class="htag rep">🏆 高复购</span></div>
      </div>
      <div class="hc-price">¥39</div>
    </a>
    <a class="hot-card" href="cards/韩式辣炒年糕杯.html">
      <div class="hc-icon">🍢</div>
      <div class="hc-info">
        <div class="hc-name">辣炒年糕杯</div>
        <div class="hc-tags"><span class="htag hot">🔥 夏季热门</span><span class="htag solo">👤 一人可做</span><span class="htag money">💰 2000元起</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="cards/韩式芝士热狗棒.html">
      <div class="hc-icon">🧀</div>
      <div class="hc-info">
        <div class="hc-name">芝士热狗棒</div>
        <div class="hc-tags"><span class="htag hot">🔥 夜市热门</span><span class="htag money">💰 1500元起</span><span class="htag solo">👤 一人可做</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="cards/车轮饼（创新馅料）.html">
      <div class="hc-icon">🧇</div>
      <div class="hc-info">
        <div class="hc-name">车轮饼</div>
        <div class="hc-tags"><span class="htag hot">🔥 夜市热门</span><span class="htag money">💰 1000元起</span><span class="htag solo">👤 一人可做</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="cards/韩式鱼饼串.html">
      <div class="hc-icon">🐟</div>
      <div class="hc-info">
        <div class="hc-name">韩式鱼饼串</div>
        <div class="hc-tags"><span class="htag money">💰 低投资</span><span class="htag solo">👤 一人可做</span><span class="htag rep">🏆 高复购</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="cards/厚切炒酸奶.html">
      <div class="hc-icon">🧊</div>
      <div class="hc-info">
        <div class="hc-name">厚切炒酸奶</div>
        <div class="hc-tags"><span class="htag hot">🔥 夏季热门</span><span class="htag money">💰 3000元起</span><span class="htag solo">👤 一人可做</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="cards/芋泥啵啵冰.html">
      <div class="hc-icon">🟣</div>
      <div class="hc-info">
        <div class="hc-name">芋泥啵啵冰</div>
        <div class="hc-tags"><span class="htag hot">🔥 抖音热门</span><span class="htag money">💰 2000元起</span><span class="htag rep">🏆 高毛利</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="cards/QS_002.html">
      <div class="hc-icon">🦆</div>
      <div class="hc-info">
        <div class="hc-name">紫苏鸭腿</div>
        <div class="hc-tags"><span class="htag hot">🔥 B站爆款</span><span class="htag money">💰 5000元起</span><span class="htag rep">🏆 高复购</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="cards/QS_001.html">
      <div class="hc-icon">🐮</div>
      <div class="hc-info">
        <div class="hc-name">喷泉牛杂</div>
        <div class="hc-tags"><span class="htag hot">🔥 抖音热门</span><span class="htag money">💰 8000元起</span><span class="htag rep">🏆 高复购</span></div>
      </div>
      <div class="hc-price">¥39.9</div>
    </a>
    <a class="hot-card" href="#xc">
      <div class="hc-icon">🌮</div>
      <div class="hc-info">
        <div class="hc-name">小吃炸物</div>
        <div class="hc-tags"><span class="htag hot">🔥 夜市热门</span><span class="htag money">💰 2000元起</span><span class="htag solo">👤 一人可做</span></div>
      </div>
      <div class="hc-price">¥39</div>
    </a>
    <a class="hot-card" href="#sk">
      <div class="hc-icon">🍢</div>
      <div class="hc-info">
        <div class="hc-name">烧烤串串</div>
        <div class="hc-tags"><span class="htag rep">🏆 高复购</span><span class="htag hot">🌙 夜市刚需</span><span class="htag money">💰 3000元起</span></div>
      </div>
      <div class="hc-price">¥39</div>
    </a>
    <a class="hot-card" href="#lb">
      <div class="hc-icon">🥗</div>
      <div class="hc-info">
        <div class="hc-name">凉拌卤味</div>
        <div class="hc-tags"><span class="htag rep">🏆 高毛利</span><span class="htag hot">🏠 社区型</span><span class="htag money">💰 1500元起</span></div>
      </div>
      <div class="hc-price">¥39</div>
    </a>
  </div>

  <!-- ===== 分类区：小吃类 ===== -->
  <div class="section-header" id="snacks"><h2>🍗 小吃类</h2><span class="more">摆摊热门</span></div>

  <!-- 韩式炸鸡 hz -->
  <div class="section-header" id="hz" style="margin-top:0;border-bottom:none"><h2>🍗 韩式炸鸡</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 香酥炸鸡排 jp -->
  <div class="section-header" id="jp"><h2>🍗 香酥炸鸡排</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 小吃炸物 xc -->
  <div class="section-header" id="xc"><h2>🌮 小吃炸物</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 烧烤串串 sk -->
  <div class="section-header" id="sk"><h2>🍢 烧烤串串</h2><span class="more">即将上线</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 凉拌卤味 lb -->
  <div class="section-header" id="lb"><h2>🥗 凉拌卤味</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 傣舂凉菜 lj -->
  <div class="section-header" id="lj"><h2>🥬 傣舂凉菜</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 车轮饼 clb -->
  <div class="section-header" id="clb"><h2>🧇 车轮饼</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 炒饭炒面 cf -->
  <div class="section-header" id="cf"><h2>🍳 炒饭炒面</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- ===== 分类区：饮品类 ===== -->
  <div class="section-header" id="drinks" style="margin-top:20px"><h2>🥤 饮品类</h2><span class="more">摆摊饮品</span></div>

  <!-- 手打柠檬茶 yl -->
  <div class="section-header" id="yl" style="margin-top:0;border-bottom:none"><h2>🍋 手打柠檬茶</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 新式茶饮 cs -->
  <div class="section-header" id="cs"><h2>🍵 新式茶饮</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 手搓咖啡 cd -->
  <div class="section-header" id="cd"><h2>☕ 手搓咖啡</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 冰品甜品 tp -->
  <div class="section-header" id="tp"><h2>🍧 冰品甜品</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 传统糖水 tg -->
  <div class="section-header" id="tg"><h2>🧊 传统糖水</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 大桶糖水 dt -->
  <div class="section-header" id="dt"><h2>🧊 大桶糖水</h2><span class="more">¥9.9 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- ===== 分类区：主食/其他类 ===== -->
  <div class="section-header" style="margin-top:20px"><h2>🍜 主食·其他</h2><span class="more">刚需项目</span></div>

  <!-- 卤炸帮 lzb -->
  <div class="section-header" id="lzb" style="margin-top:0;border-bottom:none"><h2>🍗 卤炸帮</h2><span class="more">即将上线</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 包子蒸点 bz -->
  <div class="section-header" id="bz"><h2>🥟 包子蒸点</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 灌汤包 gt -->
  <div class="section-header" id="gt"><h2>🥟 灌汤包</h2><span class="more">即将上线</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 早餐粥品 zc -->
  <div class="section-header" id="zc"><h2>🥣 早餐粥品</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 汤面米线 lt -->
  <div class="section-header" id="lt"><h2>🍜 汤面米线</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 螺蛳粉酸辣粉 lsf -->
  <div class="section-header" id="lsf"><h2>🍜 螺蛳粉酸辣粉</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 馄饨水饺 hj -->
  <div class="section-header" id="hj"><h2>🥟 馄饨水饺</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 韩式烤肉 kr -->
  <div class="section-header" id="kr"><h2>🥩 韩式烤肉</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 日式烧鸟 rb -->
  <div class="section-header" id="rb"><h2>🍢 日式烧鸟</h2><span class="more">¥39 解锁完整配方</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

  <!-- 麻辣烫冒菜 mlt -->
  <div class="section-header" id="mlt"><h2>🍢 麻辣烫冒菜</h2><span class="more">即将上线</span></div>
  <div class="cat-fold">
  <div class="jingpin-grid cat-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0">
    <!-- 待填充 -->
  </div>
  </div>

</div><!-- end main -->

"""

# 组合并写入
new_content = header + stall_content + footer_html

with open("/Users/mac/Desktop/青葵/foodintelai-site/index.html", "w") as f:
    f.write(new_content)

print(f"Written! Total: {len(new_content)} chars")
print(f"Header: {len(header)} chars")
print(f"Stall: {len(stall_content)} chars")
print(f"Footer: {len(footer_html)} chars")
print(f"\nEnds with: ...{new_content[-100:]}")
