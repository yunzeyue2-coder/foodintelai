#!/usr/bin/env python3
"""
V4标准卡批量生成 - 韩式衍生品+炸鸡系统+小料卡
从DeepSeek韩式炸鸡技术文档提取真实配方数据
去品牌化，精确到克，分类清晰
"""
import os, re

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"
DATA_FILE = "/Users/mac/Desktop/青葵/foodintelai-site/cards-data.js"

HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{id} · {name} · 沧林食品</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f0e9e2;color:#3a322a;padding:28px 16px;line-height:1.7}}
.card{{max-width:540px;margin:0 auto;background:#faf6f0;border-radius:18px;overflow:hidden}}
.meta{{padding:20px 22px 14px;background:#fdf8f0;border-bottom:1px solid #eee5d8}}
.meta .badge{{display:inline-block;font-size:10px;font-weight:700;color:#C0392B;background:#fef2ee;padding:2px 10px;border-radius:4px}}
.meta h1{{font-size:20px;font-weight:700;color:#3a322a;line-height:1.3}}
.meta .sub{{font-size:12px;color:#b5aaa0}}
.level-banner{{display:flex;gap:8px;padding:10px 22px;background:#fef9f2;flex-wrap:wrap}}
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
.free-badge{{display:inline-block;font-size:10px;background:#27ae60;color:#fff;padding:1px 8px;border-radius:3px}}
</style></head>
<body><div class="card">
<div class="meta">
  <div class="badge">{id} · {cat_label} · ¥{cost_est}</div>
  <h1>{name}</h1>
  <div class="sub">{desc}</div>
</div>
<div class="level-banner"><span class="level-item high">{hot}</span><span class="level-item">难度 {diff}</span></div>
<div class="section">
  <div class="s-title"><span class="free-badge">免费</span> 📖 产品说</div>
  <div class="story">{story}</div>
</div>
<div class="paywall">
  <div class="price">¥{price}</div>
  <div class="desc">{paid}</div>
  <a class="btn" href="https://foodintelai.com">加微信 canglin1985 获取</a>
  <div class="up">包含{id} · {name} · 完整商用方案</div>
</div>
</div></body></html>'''

CARDS = [
    # ===== 1. 韩式炸鸡衍生品 =====
    {
        'id': 'HZ-021', 'name': '韩式年糕无骨炸鸡（蜜汁）',
        'cat': '🍗 韩式炸鸡', 'cat_label': '韩式炸鸡', 'price': '39', 'cost_est': '39',
        'desc': '年糕+无骨鸡块 · 双倍咀嚼 · 韩式炸鸡店招牌',
        'hot': '🔥 韩式经典', 'diff': '★★★',
        'story': '年糕无骨炸鸡在韩国炸鸡店基本上是人手一份——外酥里嫩的鸡块配软糯Q弹的年糕，再裹上韩式甜辣酱。一份里有肉有碳水，吃一份顶一餐。年糕先用冷水泡1小时再焯水，口感更弹。',
        'paid': '✅ 蜜汁年糕无骨炸鸡·商用标准<br>✅ 鸡胸肉200g切1.5cm块，原味腌料10g+水25g+姜葱汁10g腌4小时<br>✅ 年糕70g冷水泡1小时→焯水沥干<br>✅ 1号粉(小伙炸粉:玉米淀粉=1:1)拍粉→挂糊(1号粉:水=1:1.5)→200°C下锅转160°C炸3分钟<br>✅ 平底锅120°C→鸡块+韩国炸鸡酱90g快速翻炒挂汁→撒花生碎+熟芝麻<br>✅ 蜜汁版本：VC蜜汁酱(橙汁400g+麦芽糖400g+蜂蜜100g)<br>✅ 成本约¥12/份 | 售价¥25-35 | 毛利55-65%',
    },
    {
        'id': 'HZ-022', 'name': '韩式起司棒棒鸡（原味）',
        'cat': '🍗 韩式炸鸡', 'cat_label': '韩式炸鸡', 'price': '39', 'cost_est': '39',
        'desc': '鸡胸肉卷芝士+培根 · 拉丝起司 · 小孩最爱',
        'hot': '🔥 拉丝爆款', 'diff': '★★★',
        'story': '起司棒棒鸡把鸡胸肉片成薄片，包进芝士和培根，卷成棒状裹面包糠炸。咬开拉丝效果拔群——芝士融化后拉出长长的丝，小孩和年轻女生看到就走不动路。',
        'paid': '✅ 韩式起司棒棒鸡·商用标准(5根)<br>✅ 鸡胸肉片9cm×7cm薄片(松肉锤砸松，力度均匀)<br>✅ 原味腌料10g+鸡粉5g+水100g腌制10分钟<br>✅ 每片放芝士20g+培根10g+青红椒米3g→卷成棒状<br>✅ 拍薄淀粉→沾蛋液→裹白色面包糠→竹签插入<br>✅ 150-160°C油炸至熟透(约5-6分钟)→挤番茄酱+沙拉酱+柠檬汁<br>✅ 其他变体：水果起司(草莓/苹果)、坚果起司(花生/核桃)、海鲜起司(鱿鱼/虾仁)、什锦起司(香菇/胡萝卜/香肠)<br>✅ 成本约¥15/5根 | 售价¥28-38 | 毛利55-60%',
    },
    {
        'id': 'HZ-023', 'name': '韩式脆皮炸鸡（蒜香酱油）',
        'cat': '🍗 韩式炸鸡', 'cat_label': '韩式炸鸡', 'price': '39', 'cost_est': '39',
        'desc': '特制脆皮炸鸡粉 · 双炸工艺 · 外卖也不软',
        'hot': '🔥 脆度升级', 'diff': '★★★',
        'story': '脆皮炸鸡和普通韩式炸鸡的区别在于裹粉——脆皮炸鸡粉加了木薯淀粉和小苏打，炸出来皮更酥脆。外卖放半小时也不回软。蒜香酱油酱刷在表面不拌，保持脆弱的口感。',
        'paid': '✅ 韩式脆皮炸鸡·商用标准(整只)<br>✅ 脆皮粉配方：中筋粉350g+玉米淀粉150g+土豆淀粉150g+玉米粉100g+黑胡椒5g+白胡椒10g+洋葱粉10g+蒜粉10g+味精10g+奶粉3g<br>✅ 堂食版调比例：玉米淀粉+50g，土豆淀粉-50g<br>✅ 腌鸡剂：水1000g+腌鸡剂40g，冷藏12小时以上<br>✅ 炸鸡浆：粉:水=1:1 → 腌鸡入浆拌匀 → 脆皮粉滚匀<br>✅ 170°C一次炸10分钟→捞出放凉→出品前170°C复炸10分钟<br>✅ 蒜香酱油酱配方：浓香酱油60g+咸味酱油60g+赤砂糖80g+低聚糖100g+水40g+蒜末60g+味精2g（不加热，发酵3小时刷涂）<br>✅ 成本约¥22/整只 | 售价¥45-58 | 毛利55-60%',
    },
    {
        'id': 'HZ-024', 'name': '韩式炸鸡大饭团',
        'cat': '🍗 韩式炸鸡', 'cat_label': '韩式炸鸡', 'price': '39', 'cost_est': '39',
        'desc': '炸鸡块+大饭团 · 韩式炸鸡店定食风 · 一份管饱',
        'hot': '🔥 定食套餐', 'diff': '★★',
        'story': '炸鸡大饭团是把韩式炸鸡定食化——炸鸡块单独炸好，饭团用拌饭汁调味，再配上酸甜脆萝卜。客人买一份有肉有饭有菜，比单买炸鸡满足感高很多。',
        'paid': '✅ 韩式炸鸡大饭团·商用标准<br>✅ 鸡腿肉180g+原味腌料→裹糊→180°C炸4分钟<br>✅ 饭团：米饭300g+沙拉酱25g+香油6g+拌饭汁25g+脆萝卜丁+黄瓜丁+玉米粒共50g+海苔碎6g+芝麻2g<br>✅ 所有配料搅拌均匀→抓出弹性→手上抹香油揉成大饭团<br>✅ 出品：饭团入盒+炸鸡块+挤客户喜欢的酱料+黑白芝麻<br>✅ 配酸甜脆萝卜一份<br>✅ 炸鸡拌饭汁配方：清净园糖稀100g+酱油15g+烧汁30g+苹果醋13g<br>✅ 成本约¥12/份 | 售价¥25-35 | 毛利58-65%',
    },
    {
        'id': 'HZ-025', 'name': '韩式鸡腿汉堡',
        'cat': '🍗 韩式炸鸡', 'cat_label': '韩式炸鸡', 'price': '39', 'cost_est': '39',
        'desc': '现炸鸡腿肉+汉堡坯 · 比炸鸡店卖的还好吃',
        'hot': '🔥 汉堡系列', 'diff': '★★★',
        'story': '韩式鸡腿汉堡用腌制好的去骨鸡腿肉（180g/个），裹起鳞粉炸出鳞片效果。鸡腿肉比鸡胸肉多汁得多，咬开汁水直冒。加生菜+沙拉酱，比快餐店的美式鸡腿堡更有韩式风味。',
        'paid': '✅ 韩式鸡腿汉堡·商用标准<br>✅ 鸡腿肉180g/个(腌鸡剂腌12小时)<br>✅ 起鳞工艺：腌鸡控干→裹起鳞粉3遍→180°C下锅前抖粉→炸5-6分钟定型<br>✅ 汉堡组装：包装纸→下半汉堡坯→生菜→沙拉酱→炸鸡腿→上半汉堡坯→打包<br>✅ 起鳞粉：中筋粉+玉米淀粉+小苏打+调味料配比<br>✅ 成本约¥8/个(含面包坯+包装) | 售价¥18-25 | 毛利60-68%',
    },
    # ===== 2. 韩式周边主食 =====
    {
        'id': 'KR-007', 'name': '韩式辣炒年糕',
        'cat': '🍗 韩式小吃', 'cat_label': '韩式小吃', 'price': '29', 'cost_est': '29',
        'desc': '手指年糕+韩式辣酱 · 韩剧同款 · 摆摊爆品',
        'hot': '🔥 韩剧同款', 'diff': '★★',
        'story': '韩式辣炒年糕在夜市出镜率极高——红彤彤的酱汁裹着Q弹的年糕，辣中带甜。手指年糕一定要冷水泡1小时再煮，不然咬不动。辣酱可以提前批量预制，出餐不到3分钟。',
        'paid': '✅ 韩式辣炒年糕·商用标准<br>✅ 手指年糕500g冷水泡1小时→洗净沥水<br>✅ 韩式辣酱90g+白砂糖30g+粗辣椒面10g+海鲜酱油20g+水100g调匀<br>✅ 热油炒香洋葱1/3个→放年糕+水350g中火煮2-3分钟→倒酱汁大火收汁<br>✅ 收好加青红椒丝炒匀→盛盘撒白芝麻<br>✅ 成本约¥8/份 | 售价¥18-25 | 毛利60-68%',
    },
    {
        'id': 'KR-008', 'name': '韩式紫菜包饭（原味）',
        'cat': '🍗 韩式小吃', 'cat_label': '韩式小吃', 'price': '29', 'cost_est': '29',
        'desc': '韩式经典 · 米饭+紫菜+五彩馅料 · 冷吃热吃都行',
        'hot': '🔥 韩式经典', 'diff': '★★',
        'story': '韩式紫菜包饭和日式寿司卷不一样——米饭调了盐和香油，馅料更丰富（胡萝卜、黄瓜、火腿、鸡蛋、黄萝卜条）。卷好后切1cm的片，配辣白菜或腌萝卜一起吃，一份能吃饱。',
        'paid': '✅ 韩式紫菜包饭·商用标准(3条)<br>✅ 米饭500g趁热+盐3g+香油5g+熟芝麻10g拌匀<br>✅ 馅料预制：胡萝卜条+黄瓜条盐腌→火腿切条→鸡蛋摊饼切条<br>✅ 竹帘包保鲜膜→紫菜铺上→米饭铺平压实(前端留2cm不铺)<br>✅ 放入胡萝卜+黄瓜+火腿+鸡蛋+黄萝卜→卷实→封口朝下<br>✅ 刀沾水切1cm片<br>✅ 其他变体：泡菜紫菜包饭(加辣白菜)、彩虹紫菜包饭(五色原料表面装饰)、金枪鱼寿司、紫薯三文鱼寿司<br>✅ 成本约¥6/条 | 售价¥15-22/条 | 毛利68-72%',
    },
    {
        'id': 'KR-009', 'name': '韩式石锅拌饭',
        'cat': '🍗 韩式小吃', 'cat_label': '韩式小吃', 'price': '29', 'cost_est': '29',
        'desc': '石锅滋滋响 · 锅巴焦香+拌饭酱 · 韩餐经典必学',
        'hot': '🔥 必学经典', 'diff': '★★★',
        'story': '石锅拌饭的魅力在锅巴——石锅涂香油后加热，米饭底部煎出金黄色的锅巴，焦香酥脆。豆芽焯水、西葫芦和胡萝卜丝分别烫熟码在饭上，中间放糖心煎蛋+拌饭酱，吃的时候拌匀。',
        'paid': '✅ 韩式石锅拌饭·商用标准<br>✅ 配菜：菠菜200g+胡萝卜30g+豆芽100g+鸡蛋1个+角瓜60g<br>✅ 豆芽开水焯(加小苏打+油提亮)→冷水过凉+盐+牛肉粉拌匀<br>✅ 西葫芦丝/胡萝卜丝/香菇/角瓜分别开水烫熟+盐+牛肉粉<br>✅ 鸡蛋煎一面金黄一面糖心→边缘修圆<br>✅ 石锅涂香油→米饭盛入压实→码上蔬菜→放回火上小火加热至滋滋响<br>✅ 上层加拌饭酱料100g+糖心煎蛋→撒芝麻+紫菜碎<br>✅ 鱿鱼石锅拌饭变体：鱿鱼烫熟→明太鱼酱炒制→同法码放<br>✅ 成本约¥8/份 | 售价¥22-30 | 毛利65-73%',
    },
    {
        'id': 'KR-010', 'name': '韩式炸酱面',
        'cat': '🍗 韩式小吃', 'cat_label': '韩式小吃', 'price': '29', 'cost_est': '29',
        'desc': '春酱黑炸酱 · 洋葱肉丁浓香 · 韩剧中出镜率第一',
        'hot': '🔥 电视剧同款', 'diff': '★★',
        'story': '韩式炸酱面用的是春酱（黑豆酱），和北京炸酱面不一样——颜色黑亮、味道偏甜。五花肉切丁先炒出油，加土豆丁、洋葱丁、春酱小火炖煮。面煮好浇上黑亮的炸酱，撒黄瓜丝。',
        'paid': '✅ 韩式炸酱面·商用标准(1份)<br>✅ 五花肉丁150g+土豆丁80g+洋葱丁150g+包菜80g+春酱200g<br>✅ 五花肉下锅+料酒10g翻炒变色→蚝油8g+土豆丁炒1-2分钟→葱蒜出香<br>✅ 加春酱200g+水180ml+白糖稀10g+牛肉粉3g→搅匀→小火炖至酱稠<br>✅ 加洋葱丁+包菜微翻拌即关火(保持洋葱脆度)<br>✅ 拉面煮熟过水→浇酱+黄瓜丝<br>✅ 注意：五花肉选肥一点炒出来更香<br>✅ 成本约¥10/份 | 售价¥22-28 | 毛利60-64%',
    },
    # ===== 3. 炸鸡系统基础卡 =====
    {
        'id': 'HZ-SYS-01', 'name': '韩式核心腌制料粉（原味）',
        'cat': '🧂 炸鸡系统', 'cat_label': '炸鸡系统', 'price': '19', 'cost_est': '19',
        'desc': '韩式炸鸡的基础料粉 · 精确配比 · 统一风味标准',
        'hot': '🔥 基础必备', 'diff': '★',
        'story': '韩式炸鸡的腌制料粉是所有口味的起点。盐100g+糖80g+牛肉粉20g+蒜粉8g+肉桂粉4g+姜粉5g+黑胡椒粉6g——七种粉混合，可腌制500-1000g鸡肉。批量打好粉密封保存，3-4个月不变质。',
        'paid': '✅ 韩式核心腌料粉·商用配方<br>✅ 原味料粉(总重223g)：盐100g+白砂糖80g+牛肉粉20g+蒜粉8g+肉桂粉4g+姜粉5g+黑胡椒粉6g<br>✅ 所有材料一起打成粉末→密封阴凉保存<br>✅ 腌制比例：腌料30g+水500g+鸡肉500-1000g<br>✅ 操作：料粉和水搅匀→放入鸡肉→扎孔入味→冷藏12小时后可用<br>✅ 辣味版：原味料粉30g+水500g+小米辣4g<br>✅ 注意：腌制料水不可反复使用；鸡肉可冷藏泡3-4天<br>✅ 批量预制可放大10倍(水按比例)',
    },
    {
        'id': 'HZ-SYS-02', 'name': '韩式核心炸粉配比',
        'cat': '🧂 炸鸡系统', 'cat_label': '炸鸡系统', 'price': '19', 'cost_est': '19',
        'desc': '堂食版+外卖版双配方 · 脆度可控 · 成本可见',
        'hot': '🔥 核心配方', 'diff': '★',
        'story': '韩式炸鸡的炸粉和腌料同样重要——好的炸粉决定外壳的脆度和口感。外卖版增加土豆淀粉、减少玉米淀粉，放半小时也不回软。堂食版追求刚出锅的极致脆感。',
        'paid': '✅ 韩式核心炸粉·商用配方(总量305g)<br>✅ 玉米淀粉120g+大米粉50g+土豆淀粉60g+中筋面粉50g+玉米粉20g+小苏打5g<br>✅ 所有材料搅匀→密封保存(常温30天)<br>✅ 外卖炸粉比例：土豆淀粉+30g(+50%)→小苏打+1g→外卖半小时仍酥脆<br>✅ 核心炸粉适用：韩式甜辣炸鸡、蜂蜜芥末、蒜香等所有风味<br>✅ 炸鸡糊：核心炸粉260g+水180g+油20g＝调匀→鸡肉控干入糊→180°C炸7分钟<br>✅ 注意：粉料可用厨师机最小转速打半小时更均匀',
    },
    {
        'id': 'HZ-SYS-03', 'name': '香辣/原味/奥尔良腌制系统',
        'cat': '🧂 炸鸡系统', 'cat_label': '炸鸡系统', 'price': '19', 'cost_est': '19',
        'desc': '三大腌制体系完整配比 · 低中高辣三档可调',
        'hot': '🔥 系统方案', 'diff': '★★',
        'story': '炸鸡的腌制决定了肉的风味和汁水感。香辣、原味、奥尔良是三大主流——香辣分低中高三档，原味做韩式炸鸡打底，奥尔良做烤鸡版。腌好后冷藏12小时风味最好。',
        'paid': '✅ 三大腌制系统·商用标准<br>✅ 香辣(推荐:妙利香辣腌料)：<br>  翅中/翅根：肉100：腌料4.5-5.5：水10(低/中/高辣)<br>  童子鸡/腿肉：肉100：腌料4.5-5.5：水12<br>✅ 原味(推荐:妙利原味腌料·韩式专用)：<br>  翅中/翅根：肉100：腌料4：水12<br>  童子鸡/腿肉：肉100：腌料4：水12<br>✅ 奥尔良(推荐:妙利奥尔良烤鸡腌料)：<br>  翅中/翅根：肉100：腌料8：水8<br>✅ 注意事项：水温不超过25°C(最好冰水)；推荐隔夜腌制第二天用；最多第三天用完；腌料过多会咸<br>✅ 适用：鸡翅中、翅根、琵琶腿、去骨腿肉、童子鸡',
    },
    {
        'id': 'HZ-SYS-04', 'name': '美式炸鸡粉水粉/浆粉工艺SOP',
        'cat': '🧂 炸鸡系统', 'cat_label': '炸鸡系统', 'price': '29', 'cost_est': '29',
        'desc': 'KFC同款工艺 · 鳞片起酥技巧 · 标准化操作流程',
        'hot': '🔥 工艺标准', 'diff': '★★★',
        'story': '美式炸鸡的鳞片效果靠的是\"粉水粉\"工艺——裹粉→沾水→再裹粉，反复3次。裹粉时手不能直接碰肉，靠\"按压3次+左右翻动8-10次\"的手法起鳞。裹好1分钟内必须下锅。',
        'paid': '✅ 美式炸鸡·完整工艺SOP<br>✅ 粉水粉工艺(KFC中国做法)：<br>  腌鸡→裹粉(按压3次+翻动8-10次→重复3次)→过筛去浮粉<br>  入水抖5-8次→再裹粉(同方法3次)→过筛→1分钟内油炸<br>✅ 浆粉工艺(KFC韩国做法)：<br>  调浆(粉:水=1:1.6)→腌鸡入浆→裹粉(按压3+翻10→重复3)→过筛→1分钟油炸<br>✅ 油炸参数：<br>  翅中/翅根：175-180°C，6分30秒<br>  去骨腿肉：175-180°C，4-5分钟<br>  童子鸡：175-180°C，10-12分钟<br>✅ 判断标准：中心温度80°C/牙签插入无血水<br>✅ 裹粉品牌推荐：妙利炸鸡粉',
    },
    {
        'id': 'HZ-SYS-05', 'name': '韩式酸甜脆萝卜',
        'cat': '🧂 炸鸡系统', 'cat_label': '炸鸡系统', 'price': '9.9', 'cost_est': '9.9',
        'desc': '炸鸡店黄金配菜 · 酸甜解腻 · 72h发酵风味最佳',
        'hot': '🔥 必备配菜', 'diff': '★',
        'story': '韩式炸鸡萝卜是吃炸鸡的灵魂配菜——酸甜微辣的萝卜块在嘴里嘎嘣脆，刚好中和炸鸡的油腻。黄栀子调出天然黄色，72小时发酵后风味最醇。韩式炸鸡店一个月能消耗几十斤。',
        'paid': '✅ 韩式酸甜脆萝卜·商用配方<br>✅ 白萝卜1000g去皮切1×1cm方块<br>✅ 酸甜汁：水300g+黄栀子10g+盐35g+白砂糖350g煮开→滤掉栀子→晾凉<br>✅ 加入苹果醋100g+白醋185g调匀<br>✅ 萝卜块入料理盒→倒酸甜汁→冷藏发酵<br>✅ 最少48小时后食用→72小时最佳→可保存1个月<br>✅ 小米辣20g+小葱50g可同时加入增香<br>✅ 注意：汁水不循环使用；萝卜上色程度由栀子量决定<br>✅ 成本约¥5/1000g萝卜 | 出15-20份',
    },
    # ===== 4. 韩式小料/预制卡 =====
    {
        'id': 'HZ-PREP-01', 'name': '韩式炸鸡酱系列（基础6款）',
        'cat': '🧂 炸鸡系统', 'cat_label': '炸鸡系统', 'price': '29', 'cost_est': '29',
        'desc': '韩式炸鸡6款核心酱料 · 预制15天冷藏 · 出餐即用',
        'hot': '🔥 酱料大全', 'diff': '★★',
        'story': '韩式炸鸡的灵魂在酱料。甜辣酱、蜂蜜芥末、嗨辣酱、琥珀酱、奶香芝士、蒜香酱油——这6款覆盖了95%的韩式炸鸡口味。每款配方都是精确到克的商业配比，熬好冷藏可用15天。',
        'paid': '✅ 韩式炸鸡基础6酱·商用配方<br>✅ ①经典甜辣酱：蒜末20g+洋葱末35g+白糖稀200g+番茄沙司85g+黑胡椒2g+赤砂糖50g+韩细辣椒面15g+酱油20g+盐3g+牛肉粉5g+白葡萄酒50g→大火烧开转小火熬10分钟<br>✅ ②韩式蜂蜜芥末酱：黄芥末酱100g+沙拉酱250g+白糖40g+苹果醋10g+蜂蜜30g+黄芥末粉4g→搅匀→冷藏3小时使用<br>✅ ③韩式嗨辣酱：白糖稀200g+番茄酱300g+酱油30g+烧汁30g+蒜末30g+赤砂糖65g+黑胡椒1g+辣椒素15-20g→熬10分钟<br>✅ ④韩式琥珀酱：酱油140g+赤砂糖225g+照烧汁15g+洋葱末135g+白糖稀150g+水280g+土豆淀粉15g→熬10分钟<br>✅ ⑤奶香芝士酱：卡夫芝士粉40g+沙拉酱200g+香甜沙拉酱50g+奶粉10g+淡奶油100g+炼乳85g+苹果醋20g→搅匀<br>✅ ⑥蒜香酱油酱：酱油180g+水180g+糖160g+蒜末50g+蒜粉6g+洋葱粉4g+黑胡椒1.5g+水怡40g→熬出蒜味(约2分钟)关火',
    },
]

def generate(data):
    path = os.path.join(CARDS_DIR, f"{data['id']}.html")
    html = HEAD.format(**data)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  [生成] {data['id']} {data['name']}")

def update_data(cards):
    with open(DATA_FILE, encoding='utf-8') as f:
        content = f.read()
    
    # 按品类分组
    groups = {}
    for c in cards:
        g = c['cat']
        if g not in groups:
            groups[g] = []
        groups[g].append(c)
    
    # 处理已有品类
    for cat, cat_cards in groups.items():
        import re
        # 找品类块
        escaped = re.escape(cat)
        m = re.search(r'("' + escaped + r'"\s*:\s*\[)(.*?)(\]\s*,?\s*(?:"|$))', content, re.DOTALL)
        if m:
            existing = m.group(2)
            new = ''
            for c in cat_cards:
                new += f'\n    {{e:"📄", n:"{c["name"]} · 沧林食品", d:"", f:"cards/{c["id"]}.html"}},'
            content = content.replace(m.group(0), f'"{cat}": [{existing}{new}\n  ]')
            print(f"  [数据] {cat}: 添加{len(cat_cards)}张")
        else:
            # 新品类插在最后一个品类前
            new_section = f'\n  "{cat}": [\n'
            for c in cat_cards:
                new_section += f'    {{e:"📄", n:"{c["name"]} · 沧林食品", d:"", f:"cards/{c["id"]}.html"}},\n'
            new_section += '  ],\n'
            # 插在最后一个右大括号前
            insert_pos = content.rfind('}')
            content = content[:insert_pos] + new_section + content[insert_pos:]
            print(f"  [数据] 新品类 {cat}: {len(cat_cards)}张")
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  [数据] cards-data.js 更新完成")

if __name__ == '__main__':
    print(f"生成 {len(CARDS)} 张V4标准卡...")
    for c in CARDS:
        generate(c)
    update_data(CARDS)
    print(f"\n全部完成! 共生成 {len(CARDS)} 张")
