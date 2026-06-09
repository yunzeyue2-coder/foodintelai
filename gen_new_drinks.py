#!/usr/bin/env python3
"""
批量生成新饮品卡（DeepSeek 75张配方数据中的新品）
V4模板格式，去品牌化
"""
import os, re

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"

# ====== V4卡模板 ======
HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0">
<title>{id} · {name} · 沧林食品</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:#f0e9e2;color:#3a322a;padding:28px 16px;line-height:1.7}}
.card{{max-width:540px;margin:0 auto;background:#faf6f0;border-radius:18px;overflow:hidden;box-shadow:0 2px 20px rgba(0,0,0,.04)}}
.meta{{padding:20px 22px 14px;background:#fdf8f0;border-bottom:1px solid #eee5d8}}
.meta .badge{{display:inline-block;font-size:10px;font-weight:700;color:#C0392B;background:#fef2ee;padding:2px 10px;border-radius:4px;margin-bottom:6px}}
.meta h1{{font-size:20px;font-weight:700;color:#3a322a;line-height:1.3;margin-bottom:2px}}
.meta .sub{{font-size:12px;color:#b5aaa0;margin-bottom:10px}}
.level-banner{{display:flex;gap:8px;padding:10px 22px;background:#fef9f2;border-bottom:1px solid #eee5d8;flex-wrap:wrap}}
.level-item{{font-size:11px;padding:3px 10px;border-radius:6px;background:#f0e9e2;color:#5a4f44}}
.level-item.high{{background:#C0392B;color:#fff}}
.s-title{{font-size:14px;font-weight:700;color:#3a322a;margin-bottom:10px;padding-bottom:4px;border-bottom:2px solid #f0ece6}}
.story{{font-size:13px;line-height:2;color:#5a4f44}}
.section{{padding:20px 22px}}
.paywall{{padding:24px 22px;text-align:center;background:#fdf8f0}}
.paywall .price{{font-size:28px;font-weight:800;color:#C0392B}}
.paywall .desc{{font-size:13px;color:#7a7269;margin:8px 0 16px;line-height:1.6;text-align:left}}
.paywall .btn{{display:inline-block;background:#C0392B;color:#fff;padding:10px 32px;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none}}
.paywall .up{{font-size:10px;color:#b5aaa0;margin-top:10px}}
.free-badge{{display:inline-block;font-size:10px;background:#27ae60;color:#fff;padding:1px 8px;border-radius:3px;margin-right:4px}}
</style>
</head>
<body>
<div class="card">
<div class="meta">
  <div class="badge">{id} · {cat_label} · ¥{cost_est}</div>
  <h1>{name}</h1>
  <div class="sub">{desc}</div>
</div>
<div class="level-banner">
  <span class="level-item high">{hot_label}</span>
  <span class="level-item">摆摊指数 ★★★★☆</span>
  <span class="level-item">复购指数 ★★★★☆</span>
</div>
<div class="section">
  <div class="s-title"><span class="free-badge">免费</span> 📖 产品说</div>
  <div class="story">{story}</div>
</div>
<div class="paywall">
  <div class="price">¥{price}</div>
  <div class="desc">
{paid_desc}
  </div>
  <a class="btn" href="https://foodintelai.com">加微信 canglin1985 获取</a>
  <div class="up">包含{id} · {name} · 商用完整方案</div>
</div>
</div>
</body>
</html>'''

# ====== 新品数据 ======
NEW_CARDS = [
    # === 手打柠檬茶新品 ===
    {
        'id': 'CD-100', 'name': '金桔柠檬', 'cat': '🍋 手打柠檬茶',
        'cat_label': '柠檬茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '经典清爽 · 金桔+柠檬双果香 · 一杯解腻',
        'hot_label': '🔥 经典复刻',
        'story': '金桔柠檬是饮品店的元老级单品。金桔的独特皮香和柠檬的酸爽撞在一起，夏天来一杯直接解暑。做法简单但味道很正——金桔皮香不能靠捶，只能挤汁；柠檬片拍打出香，茶底用茉莉绿茶衬托果味。成本极低，利润空间大。',
        'paid_desc': '  ✅ 金桔柠檬·商用配比<br>  ✅ 原料：金桔2颗+黄柠檬3片+绿茶汤100ml+果糖35g+冰块+水<br>  ✅ 工艺：金桔对半切开挤汁连皮入杯 → 柠檬3片 → 果糖35g+绿茶汤100ml → 冰块满杯+水补满 → 雪克摇匀<br>  ✅ 注意：金桔不要捶打只挤汁，否则籽会苦<br>  ✅ 成本约¥3 | 售价¥10-14 | 毛利65-70%',
    },
    {
        'id': 'CD-101', 'name': '黑加仑柠檬茶', 'cat': '🍋 手打柠檬茶',
        'cat_label': '柠檬茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '紫红色颜值 · 黑加仑果香+香水柠檬 · 酸甜平衡',
        'hot_label': '🔥 新品推荐',
        'story': '黑加仑柠檬茶用黑加仑果酱提供颜色和甜香，黄柠檬和香水柠檬两种柠檬混合捶打出复合柠檬香。紫色渐变的外观拍照特别出片——年轻女生点单率极高。',
        'paid_desc': '  ✅ 黑加仑柠檬茶·商用配比<br>  ✅ 原料：黄柠檬3片+香水柠檬3片+黑加仑果酱20g+茉莉绿茶汤100ml+果糖20ml+冰块<br>  ✅ 工艺：双柠檬+冰块50g捶打8下出香 → 黑加仑果酱20g+果糖20ml+绿茶汤100ml → 补冰至500ml → 雪克摇匀<br>  ✅ 注意：黑加仑果酱含糖，果糖量需减少<br>  ✅ 成本约¥3.5 | 售价¥12-16 | 毛利70-78%',
    },
    {
        'id': 'CD-102', 'name': '青桔鲜柠茶（咸话梅）', 'cat': '🍋 手打柠檬茶',
        'cat_label': '柠檬茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '咸话梅独家风味 · 青金桔+柠檬 · 咸酸甜三重刺激',
        'hot_label': '🔥 独特口味',
        'story': '加了咸话梅的柠檬茶是夏天的开胃神器。咸话梅的咸鲜味中和了柠檬的酸，金桔的皮香做底——咸酸甜在口腔里打转，喝完还想再来一杯。去年摆摊这款的复购率比我预期高很多。',
        'paid_desc': '  ✅ 青桔鲜柠茶(咸话梅)·商用配比<br>  ✅ 原料：青金桔2颗+咸话梅1颗+柠檬2片+金桔浓缩汁20cc+茉莉绿茶汤80ml+果糖20cc+冰块<br>  ✅ 工艺：青金桔挤汁连皮入杯 → 咸话梅捏裂+柠檬2片 → 果糖+金桔汁 → 冰块八分满+绿茶汤 → 水补满 → 雪克摇匀<br>  ✅ 注意：咸话梅提供独特咸鲜，不要省略<br>  ✅ 成本约¥3.2 | 售价¥12-16 | 毛利70-75%',
    },
    {
        'id': 'CD-103', 'name': '芒果柠檬茶', 'cat': '🍋 手打柠檬茶',
        'cat_label': '柠檬茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '芒果泥+柠檬 · 热带水果风暴 · 果肉感十足',
        'hot_label': '🔥 当季推荐',
        'story': '芒果柠檬茶用新鲜小台芒做芒果泥打底，香水柠檬捶打出香，茉莉绿茶衬托。芒果的绵密甜香和柠檬的清爽酸感在嘴里打乒乓球——每口都能吸到芒果肉。',
        'paid_desc': '  ✅ 芒果柠檬茶·商用配比<br>  ✅ 原料：小台芒果肉60g(去核)+香水柠檬50g+茉莉绿茶汤150ml+果糖50ml+冰块<br>  ✅ 工艺：芒果肉+柠檬片+冰块150g捶打12下 → 加果糖+绿茶汤 → 补冰至500ml → 雪克摇匀<br>  ✅ 注意：芒果纤维多，可多捶几下<br>  ✅ 成本约¥4.5 | 售价¥14-18 | 毛利68-75%',
    },
    {
        'id': 'CD-104', 'name': '芭乐柠檬茶', 'cat': '🍋 手打柠檬茶',
        'cat_label': '柠檬茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '台湾土芭乐 · 粉嫩颜值 · 浓郁果香',
        'hot_label': '🔥 颜值爆款',
        'story': '芭乐柠檬茶这两年在小红书上火得不行——粉色的芭乐果肉和柠檬茶混合出自然粉紫色，拍照不用滤镜。芭乐本身香气独特，和香水柠檬是天生一对。',
        'paid_desc': '  ✅ 芭乐柠檬茶·商用配比<br>  ✅ 原料：芭乐块60g(去皮去籽)+香水柠檬50g+茉莉绿茶汤150ml+果糖50ml+冰块<br>  ✅ 工艺：芭乐块+柠檬片+冰块150g捶打10下 → 加果糖+绿茶汤 → 补冰至500ml → 雪克摇匀<br>  ✅ 注意：芭乐籽硬需去除，果皮可保留<br>  ✅ 成本约¥4.2 | 售价¥14-18 | 毛利68-76%',
    },
    {
        'id': 'CD-105', 'name': '好出奇冰柠茶', 'cat': '🍋 手打柠檬茶',
        'cat_label': '柠檬茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '气泡柠檬+奇异果 · 清爽双打 · 最适合夏天',
        'hot_label': '🔥 气泡系列',
        'story': '好出奇冰柠茶用气泡水替代普通水底，气泡在舌尖炸开的刺激感搭配柠檬酸香和奇异果的清甜，喝一口就像在夏天跳进游泳池。摆摊时这款经常卖断。',
        'paid_desc': '  ✅ 好出奇冰柠茶·商用配比(500ml)<br>  ✅ 原料：黄柠檬25g+糖浆10ml+气泡水250ml+奇异果汁60ml+新鲜奇异果肉65g+冰块<br>  ✅ 工艺：柠檬轻压出汁(不捶打) → 糖浆10ml → 冰块八分满 → 气泡水250ml缓慢倒入 → 奇异果汁60ml → 顶部加奇异果肉 → 轻搅拌<br>  ✅ 注意：生奇异果口感更脆不易氧化；气泡水最后加<br>  ✅ 成本约¥5 | 售价¥15-20 | 毛利70-75%',
    },
    # === 饮品系列新品 ===
    {
        'id': 'YL-060', 'name': '百香果凤梨红茶', 'cat': '🥤 饮品系列',
        'cat_label': '饮品', 'price': '9.9', 'cost_est': '9.9',
        'desc': '百香果凤梨双果香 · 红茶打底 · 酸甜解腻',
        'hot_label': '🔥 果茶精选',
        'story': '百香果和凤梨是夏天最搭的水果CP。百香果的浓烈酸香遇到凤梨的甜，红茶做底不抢戏。捶打凤梨出汁后和红茶融合，每一口都有凤梨纤维和百香果籽的咀嚼感。',
        'paid_desc': '  ✅ 百香果凤梨红茶·商用配比(500ml)<br>  ✅ 原料：百香果1个(约40g果肉)+新鲜凤梨块100g+红茶汤100ml+果糖30g+冰块+水<br>  ✅ 工艺：凤梨块捶打8下出汁 → 百香果果肉 → 果糖30g+红茶汤100ml → 冰块八分满 → 水补满 → 雪克摇匀10次<br>  ✅ 注意：凤梨选熟甜的<br>  ✅ 成本约¥4 | 售价¥14-18 | 毛利70-78%',
    },
    {
        'id': 'YL-061', 'name': '柠檬优多冰沙', 'cat': '🥤 饮品系列',
        'cat_label': '饮品', 'price': '12', 'cost_est': '12',
        'desc': '乳酸菌柠檬冰沙 · 酸甜绵密 · 消暑利器',
        'hot_label': '🔥 冰沙系列',
        'story': '柠檬优多冰沙把乳酸菌(优酪多)和柠檬汁打成冰沙，乳酸菌的酸甜中和了柠檬的尖锐酸感。冰沙质地绵密，比柠檬茶更有饱腹感。摆摊时女生很喜欢这款。',
        'paid_desc': '  ✅ 柠檬优多冰沙·商用配比(500ml)<br>  ✅ 原料：柠檬浓缩汁20cc+果糖20cc+优酪多20cc+奶精1平勺+水70ml+冰块约450g+柠檬片装饰<br>  ✅ 工艺：冰沙机放入柠檬汁+果糖+优酪多+奶精+水70ml → 加冰块450g → 打成细腻冰沙 → 倒杯+柠檬片装饰<br>  ✅ 注意：优酪多=乳酸菌饮料，可用可尔必思代替<br>  ✅ 成本约¥3.5 | 售价¥14-18 | 毛利75-80%',
    },
    {
        'id': 'YL-062', 'name': '蓝莓冰摇优酪乳', 'cat': '🥤 饮品系列',
        'cat_label': '饮品', 'price': '9.9', 'cost_est': '9.9',
        'desc': '蓝莓+优酪乳 · 酸甜绵密 · 高颜值渐变紫',
        'hot_label': '🔥 颜值系列',
        'story': '蓝莓的紫色和优酪乳的白色混合出自然的渐变效果，拍视频很上镜。蓝莓酱提供浓郁浆果风味，优酪乳增加醇厚度。是最近两年茶饮店的热门搭配。',
        'paid_desc': '  ✅ 蓝莓冰摇优酪乳·商用配比(500ml)<br>  ✅ 原料：蓝莓酱1勺(20g)+果糖20cc+优酪乳20cc+冰块+水<br>  ✅ 工艺：雪克杯放蓝莓酱+果糖+优酪乳 → 冰块八分满 → 水补满 → 雪克摇匀<br>  ✅ 注意：优酪乳可用浓稠酸奶代替<br>  ✅ 成本约¥3.8 | 售价¥14-18 | 毛利72-79%',
    },
    {
        'id': 'YL-063', 'name': '百香果盐力多', 'cat': '🥤 饮品系列',
        'cat_label': '饮品', 'price': '9.9', 'cost_est': '9.9',
        'desc': '百香果+乳酸菌 · 酸甜微咸 · 解腻刮油',
        'hot_label': '🔥 独特口味',
        'story': '百香果盐力多在日本居酒屋很常见——百香果汁+可尔必思(乳酸菌饮料)的组合，酸中带甜、甜中带咸，喝完后回甘。摆摊和夜市很配，作为解腻饮品。',
        'paid_desc': '  ✅ 百香果盐力多·商用配比(500ml)<br>  ✅ 原料：百香果汁30ml+可尔必思40ml+果糖40ml+茉莉绿茶100ml+冰块+水<br>  ✅ 工艺：雪克杯放百香果汁+可尔必思+果糖+绿茶 → 冰块八分满 → 水补满 → 雪克摇匀<br>  ✅ 注意：可尔必思可用国产优酪多代替<br>  ✅ 成本约¥4.2 | 售价¥14-18 | 毛利70-76%',
    },
    {
        'id': 'YL-064', 'name': '玫瑰咖啡气泡饮', 'cat': '🥤 饮品系列',
        'cat_label': '饮品', 'price': '12', 'cost_est': '12',
        'desc': '玫瑰花香+咖啡+气泡 · 三重刺激 · 夏日特调',
        'hot_label': '🔥 创意特调',
        'story': '玫瑰咖啡气泡饮是我自己琢磨出来的——浓缩咖啡+玫瑰蜜露+气泡水。玫瑰的花香中和了咖啡的苦，气泡的刺激感把两者融合。摆摊时经常有人问\"这是啥\"，好奇式消费。',
        'paid_desc': '  ✅ 玫瑰咖啡气泡饮·商用配比(500ml)<br>  ✅ 原料：浓缩咖啡18ml+玫瑰蜜露10-15ml+果糖25ml+气泡水+冰块<br>  ✅ 工艺：雪克杯放浓缩咖啡+玫瑰蜜露+果糖+冰块 → 雪克摇匀 → 倒入出品杯 → 缓慢倒入气泡水至满杯 → 轻搅匀<br>  ✅ 注意：可用速溶黑咖啡粉2g+20ml热水代替浓缩<br>  ✅ 成本约¥4.5 | 售价¥16-20 | 毛利75-78%',
    },
    # === 奶茶系列新品 ===
    {
        'id': 'NT-13', 'name': '原味奶茶', 'cat': '🧋 奶茶系列',
        'cat_label': '奶茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '经典锡兰红茶+奶精 · 台式奶茶鼻祖 · 百搭百变',
        'hot_label': '🔥 经典款',
        'story': '原味奶茶是奶茶界的白米饭——看起来简单但要做好不容易。锡兰红茶底+奶精粉+果糖，标准三要素。关键在于奶精粉要完全化开、茶汤要够浓。做出好喝的原味奶茶，打底其他口味奶茶就有了根基。',
        'paid_desc': '  ✅ 原味奶茶·商用配比(500ml冰)<br>  ✅ 原料：锡兰红茶汤200ml+奶精粉3勺+果糖35ml+冰块+水<br>  ✅ 工艺：雪克杯放奶精粉3勺+果糖35ml → 温红茶50ml化开奶精粉 → 加剩余红茶150ml → 冰块八分满 → 水补满 → 雪克摇匀10次 → 刮泡沫→ 出品<br>  ✅ 热饮版：奶精3.5勺+果糖35ml+红茶200ml+热水补满<br>  ✅ 成本约¥3 | 售价¥10-14 | 毛利70-78%',
    },
    {
        'id': 'NT-14', 'name': '金钻奶茶', 'cat': '🧋 奶茶系列',
        'cat_label': '奶茶', 'price': '12', 'cost_est': '12',
        'desc': '原味奶茶基底+三种小料 · 咀嚼感十足 · 超值体验',
        'hot_label': '🔥 小料满杯',
        'story': '金钻奶茶就是原味奶茶加三种小料——彩色蒟蒻、寒天、黑糖冻。小料在嘴里嚼着蹦着，一杯奶茶能喝出好几个层次。年轻人特别喜欢这种"一杯吃回本"的感觉。',
        'paid_desc': '  ✅ 金钻奶茶·商用配比(500ml)<br>  ✅ 原料：原味奶茶基底+彩色蒟蒻半勺+寒天半勺+黑糖冻半勺<br>  ✅ 工艺：出品杯放蒟蒻+寒天+黑糖冻 → 做原味奶茶基底 → 倒入混合<br>  ✅ 注意：小料需提前制备冷藏<br>  ✅ 成本约¥4 | 售价¥12-16 | 毛利70-75%',
    },
    {
        'id': 'NT-15', 'name': '奶茶三兄弟', 'cat': '🧋 奶茶系列',
        'cat_label': '奶茶', 'price': '12', 'cost_est': '12',
        'desc': '珍珠+仙草+布丁 · 三料齐下 · 经典台式风味',
        'hot_label': '🔥 经典搭配',
        'story': '奶茶三兄弟是台湾50岚的招牌产品——珍珠的Q弹、仙草的滑嫩、布丁的绵密，三种质地在嘴里打架。原味奶茶做底，不抢小料的风头。一杯下去管饱。',
        'paid_desc': '  ✅ 奶茶三兄弟·商用配比(500ml)<br>  ✅ 原料：原味奶茶基底+珍珠1勺+仙草冻2勺+布丁冻2勺<br>  ✅ 工艺：出品杯放珍珠+仙草冻+布丁冻 → 倒入做好的原味奶茶<br>  ✅ 注意：布丁不能做热饮(遇热融化)<br>  ✅ 成本约¥4.5 | 售价¥12-16 | 毛利68-72%',
    },
    {
        'id': 'NT-16', 'name': '香芋奶茶', 'cat': '🧋 奶茶系列',
        'cat_label': '奶茶', 'price': '9.9', 'cost_est': '9.9',
        'desc': '香芋果粉+奶茶 · 芋香浓郁 · 少女心爆棚的紫色',
        'hot_label': '🔥 人气口味',
        'story': '香芋奶茶是果味奶茶里卖得最好的——香芋特有的浓郁香气和奶精的醇厚特别搭，紫色外观也好拍。草莓、哈密瓜等其他果味同比例替换果粉就行，配方逻辑一样。',
        'paid_desc': '  ✅ 香芋奶茶·商用配比(500ml冰)<br>  ✅ 原料：红茶汤100ml+奶精粉2勺+香芋果粉2勺+果糖15g+冰块+水<br>  ✅ 工艺：雪克杯放奶精粉2勺+香芋果粉2勺+果糖15g → 开水20ml化开粉料 → 红茶汤100ml → 冰块满杯+水补满 → 雪克摇匀<br>  ✅ 热饮版：粉料化开后加红茶100ml+热水补满<br>  ✅ 其他果味(草莓/哈密瓜等)同比例替换果粉<br>  ✅ 成本约¥3.2 | 售价¥10-14 | 毛利70-77%',
    },
    {
        'id': 'NT-17', 'name': '鸳鸯奶茶', 'cat': '🧋 奶茶系列',
        'cat_label': '奶茶', 'price': '12', 'cost_est': '12',
        'desc': '港式奶茶+咖啡 · 提神双倍 · 香港茶餐厅灵魂',
        'hot_label': '🔥 提神利器',
        'story': '鸳鸯奶茶是香港茶餐厅的招牌——港式丝袜奶茶+浓缩咖啡。茶味和咖啡味在嘴里打架但谁也不压倒谁。提神效果翻倍，很多上班族下午一杯顶半天。',
        'paid_desc': '  ✅ 鸳鸯奶茶·商用配比(500ml冷)<br>  ✅ 原料：特浓红茶底250ml+三花淡奶75ml+果糖25ml+浓缩咖啡液25ml+冰块<br>  ✅ 工艺：奶茶缸放红茶+淡奶+果糖+咖啡液 → 搅匀 → 出品杯满冰 → 倒入混合液<br>  ✅ 热饮版：同比例原料加热，咖啡液最后加<br>  ✅ 注意：咖啡可用速溶黑咖啡粉2g+20ml热水化开<br>  ✅ 成本约¥4.5 | 售价¥14-18 | 毛利70-75%',
    },
    # === 霸王杯系列 ===
    {
        'id': 'CD-106', 'name': '招牌霸王杯', 'cat': '🍋 手打柠檬茶',
        'cat_label': '柠檬茶', 'price': '19.9', 'cost_est': '19.9',
        'desc': '1000ml超大容量 · 香水柠檬爆打 · 喝到撑',
        'hot_label': '🔥 霸气超大杯',
        'story': '霸王杯是这两年饮料界的流量密码——1000ml超大杯拿在手上回头率爆表。香水柠檬120g加倍捶打，茶底和糖也相应翻倍。摆摊时霸王杯一出，旁边摊位的客人都被吸引过来看。',
        'paid_desc': '  ✅ 招牌霸王杯·商用配比(1000ml)<br>  ✅ 原料：香水柠檬120g+果糖60ml+锡兰红茶汤250ml+冰块<br>  ✅ 工艺：柠檬120g+冰块250g捶打16下 → 果糖60ml+红茶250ml → 补冰至1000ml → 雪克摇匀<br>  ✅ 注意：雪克杯容量不足可分两次制作后混合<br>  ✅ 成本约¥7 | 售价¥19.9-25 | 毛利70-72%',
    },
]

def generate_card(data):
    """生成单张卡"""
    card_id = data['id']
    path = os.path.join(CARDS_DIR, f"{card_id}.html")
    
    html = HEAD.format(
        id=card_id,
        name=data['name'],
        cat_label=data['cat_label'],
        cost_est=str(data.get('cost_est', '9.9')),
        desc=data['desc'],
        hot_label=data['hot_label'],
        story=data['story'],
        price=data['price'],
        paid_desc=data['paid_desc'],
    )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  [生成] {card_id} {data['name']}")

def update_cards_data(cards, data_file="/Users/mac/Desktop/青葵/foodintelai-site/cards-data.js"):
    """更新cards-data.js"""
    with open(data_file, encoding='utf-8') as f:
        content = f.read()
    
    # 找到每个分类的插入点
    cat_insertions = {}
    for card in cards:
        cat = card['cat']
        if cat not in cat_insertions:
            cat_insertions[cat] = []
        cat_insertions[cat].append(card)
    
    for cat, cat_cards in cat_insertions.items():
        # 找到该分类的最后一个卡片
        import re
        # 找品类区域
        cat_pattern = re.escape(cat)
        cat_match = re.search(r'("' + cat_pattern + r'"\s*:\s*\[)(.*?)(\]\s*,?\s*(?:"|$))', content, re.DOTALL)
        
        if cat_match:
            existing_section = cat_match.group(2)
            new_cards = ''
            for card in cat_cards:
                new_cards += f'\n    {{e:"📄", n:"{card["name"]} · 沧林食品", d:"", f:"cards/{card["id"]}.html"}},'
            # 在最后一个}]前插入
            new_content = content.replace(cat_match.group(0), 
                f'"{cat}": [{existing_section}{new_cards}\n  ]')
            content = new_content
            print(f"  [数据] 已添加 {len(cat_cards)} 张到 {cat}")
        else:
            # 新品类，插入到最前面
            new_section = f'\n  "{cat}": [\n'
            for card in cat_cards:
                new_section += f'    {{e:"📄", n:"{card["name"]} · 沧林食品", d:"", f:"cards/{card["id"]}.html"}},\n'
            new_section += '  ],\n'
            content = content.replace('const ALL_CARDS = {', f'const ALL_CARDS = {{{new_section}')
            print(f"  [数据] 新品类 {cat}: {len(cat_cards)} 张")
    
    with open(data_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  [数据] cards-data.js 更新完成")

if __name__ == '__main__':
    print(f"生成 {len(NEW_CARDS)} 张新卡...")
    for card in NEW_CARDS:
        generate_card(card)
    update_cards_data(NEW_CARDS)
    print("\n全部完成!")
