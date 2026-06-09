#!/usr/bin/env python3
"""
批量替换饮品卡付费区
用广禧59款饮品配方（去品牌化）替换YL/NT/CF卡
"""
import os, shutil, re

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"

# ========== 饮品配方（去品牌化） ==========
# 格式：{卡片名: (配方名称, 原料+工艺)}

DRINK_RECIPES = {
    # === YL_001~005 草莓家族 ===
    'YL_001': ('芝芝莓莓', 
'  ✅ <strong>芝士奶盖</strong>：淡奶油+牛奶+炼乳+芝士奶盖粉，三挡搅打2分钟<br>'
'  ✅ <strong>草莓冰沙底</strong>：冷冻草莓浆80ml+茉莉绿茶茶汤100ml+冰糖糖浆25ml+冰块200g+蜜制草莓20g，打成冰沙<br>'
'  ✅ <strong>出品</strong>：杯底放原味晶球50g+蜜制草莓30g，倒入冰沙，顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥6.6 | 售价¥16-22 | 毛利60-68%'),
    
    'YL_002': ('莓莓奶冻',
'  ✅ <strong>奶冻底</strong>：双皮奶粉+牛奶+糖，中火煮开过滤，冷藏2-3小时<br>'
'  ✅ <strong>草莓冰沙</strong>：冷冻草莓浆60ml+蜜制草莓30g+冰糖糖浆25g+牛奶100ml+浓缩牛乳20ml+冰块200g，打碎<br>'
'  ✅ <strong>出品</strong>：杯底放奶冻100g，倒入冰沙，顶加奶油+新鲜草莓装饰<br>'
'  ✅ 成本约¥5.2 | 售价¥15-20 | 毛利65-74%'),
    
    'YL_003': ('霸气草莓啵啵',
'  ✅ <strong>杯底</strong>：原味晶球80g（清洗后）<br>'
'  ✅ <strong>雪克</strong>：茉莉绿茶茶汤150ml+冷冻草莓浆80ml+蜜制草莓颗粒50g+冰糖糖浆30ml+冰块200g，雪克摇匀<br>'
'  ✅ <strong>出品</strong>：倒入杯底即可<br>'
'  ✅ 冰饮700ml | 成本约¥6.2 | 售价¥15-20'),
    
    'YL_004': ('草莓小丸子',
'  ✅ <strong>杯底</strong>：糯米小丸子50g+原味水晶冻50g<br>'
'  ✅ <strong>雪克</strong>：冷冻草莓浆80ml+茉莉绿茶80ml+冰糖糖浆10ml+蜜制草莓30g+冰块200g，摇匀<br>'
'  ✅ <strong>出品</strong>：倒入后加冷冻生椰乳120ml<br>'
'  ✅ 成本约¥6.3 | 售价¥16-22'),

    'YL_005': ('草莓桃桃茶',
'  ✅ <strong>杯底</strong>：原味晶球80g+冷冻水蜜桃果蓉80g<br>'
'  ✅ <strong>雪克</strong>：茉莉绿茶茶汤150ml+冰糖糖浆20ml+冷冻草莓浆40ml+蜜制草莓30g+冰块200g，摇匀<br>'
'  ✅ 成本约¥6.9 | 售价¥16-22'),

    # === YL_006~009 生椰系列 ===
    'YL_006': ('生椰可可冰茶',
'  ✅ <strong>杯底</strong>：巧克力酱（挂壁）+冷冻生椰乳100ml<br>'
'  ✅ <strong>冰沙</strong>：生椰乳50ml+可可粉30ml+冰糖糖浆10ml+饮用水50ml+冰块180g，搅拌均匀<br>'
'  ✅ <strong>出品</strong>：倒入后加奶油顶+巧克力棒装饰<br>'
'  ✅ 成本约¥12.7 | 售价¥22-28'),
    
    'YL_007': ('椰子三兄弟',
'  ✅ <strong>杯底</strong>：椰奶冻50g+椰肉爆爆珠50g<br>'
'  ✅ <strong>饮品</strong>：冷冻椰子水250ml+冰糖糖浆5ml+饮用水50ml+冰块50g，搅拌均匀<br>'
'  ✅ 成本约¥8.1 | 售价¥18-22'),

    'YL_008': ('超浓郁椰丸黑芝麻',
'  ✅ <strong>杯底</strong>：糯米小丸子60g<br>'
'  ✅ <strong>饮品</strong>：黑芝麻酱20g+饮用水50ml（加热调开）+冷冻生椰乳150ml+冰糖糖浆20ml+冰块150g，搅匀<br>'
'  ✅ 成本约¥5.7 | 售价¥16-20'),

    'YL_009': ('清补凉',
'  ✅ <strong>杯底</strong>：西瓜颗粒40g+玉米颗粒40g+椰子水冻60g+马蹄粉圆60g<br>'
'  ✅ <strong>冰沙</strong>：生椰乳120ml+冰糖糖浆10ml+冰块120g，打碎<br>'
'  ✅ 成本约¥5.4 | 售价¥15-20'),

    'YL_010': ('杨枝甘露',
'  ✅ <strong>杯底</strong>：新鲜芒果颗粒30g+原味晶球30g+西米30g+西柚颗粒20g<br>'
'  ✅ <strong>雪克</strong>：新鲜芒果50g（捣碎）+冷冻芒果浆100ml+佳乐椰浆60ml+牛奶50ml+冰糖糖浆10ml+饮用水130ml+冰块100g，摇匀<br>'
'  ✅ 成本约¥10 | 售价¥20-28'),

    # === YL_012~016 爆柠系列 ===
    'YL_012': ('手剥粒粒大橘',
'  ✅ <strong>杯底</strong>：原味晶球80g+橘子颗粒罐头30g<br>'
'  ✅ <strong>雪克</strong>：香水柠檬3片+冰块50g（捣30下）+冰块150g+冷冻橘子汁100ml+茉莉绿茶120ml+冰糖糖浆30ml，摇匀<br>'
'  ✅ 成本约¥8.7 | 售价¥16-22'),

    'YL_013': ('爆打黄皮香柠',
'  ✅ <strong>杯底</strong>：绿茶冻80g<br>'
'  ✅ <strong>雪克</strong>：香水柠檬3片+冰块50g（捣30下）+冰块150g+冷冻黄皮汁70ml+茉莉绿茶100ml+冰糖糖浆50ml，摇匀<br>'
'  ✅ 成本约¥8.3 | 售价¥16-22'),

    'YL_014': ('香水爆柠油柑',
'  ✅ <strong>杯底</strong>：绿茶冻80g<br>'
'  ✅ <strong>雪克</strong>：香水柠檬3片+冰块50g（捣30下）+冰块200g+冷冻油柑汁100ml+茉莉绿茶150ml+冰糖糖浆30ml+饮用水50ml，摇匀<br>'
'  ✅ 成本约¥6.6 | 售价¥16-22'),

    'YL_015': ('真香桃桃爆柠',
'  ✅ <strong>杯底</strong>：水蜜桃冻60g<br>'
'  ✅ <strong>雪克</strong>：香水柠檬3片+冰块50g（捣20下）+冰块200g+冰糖糖浆20ml+速冻水蜜桃果蓉100g+茉莉绿茶200ml，摇匀<br>'
'  ✅ 成本约¥5.9 | 售价¥16-20'),

    'YL_016': ('桑爆柠',
'  ✅ <strong>雪克</strong>：香水柠檬3片+冰块100g（捣30下)+桑葚果酱100g+冰块200g+茉莉绿茶150ml+饮用水100ml，摇匀<br>'
'  ✅ 成本约¥3.1 | 售价¥14-18'),

    # === YL_017~022 阳光青提系列 ===
    'YL_017': ('悠悠青提山茶柠',
'  ✅ <strong>杯底</strong>：新鲜青提35g（捣碎）<br>'
'  ✅ <strong>雪克</strong>：香水柠檬40g+冰块50g（轻捣20下）+山茶花茶汤150ml+冰块150g+冰糖糖浆55ml+饮用水50ml+冷冻青提汁90ml，摇匀<br>'
'  ✅ 成本约¥8.4 | 售价¥18-24'),

    'YL_018': ('青提油柑',
'  ✅ <strong>雪克</strong>：冷冻青提汁80ml+冷冻油柑汁40ml+冰块150g+饮用水150ml+冰糖糖浆25ml，摇匀<br>'
'  ✅ 成本约¥4 | 售价¥14-18'),

    'YL_019': ('满杯青提',
'  ✅ <strong>雪克</strong>：新鲜青提果肉50g（捣碎）+冰块150g+冰糖糖浆25ml+茉莉绿茶120ml+饮用水30ml+冷冻青提汁100ml，摇匀<br>'
'  ✅ 成本约¥5.8 | 售价¥15-20'),

    'YL_020': ('超级多肉葡萄杨梅',
'  ✅ <strong>杯底</strong>：葡萄颗粒80g（捣碎）<br>'
'  ✅ <strong>冰沙</strong>：冰块250g+冷冻杨梅浆120ml+茉莉绿茶100ml，打碎<br>'
'  ✅ 成本约¥5.6 | 售价¥16-22'),

    'YL_021': ('葡萄撞撞百香冻',
'  ✅ <strong>杯底</strong>：百香果冻120g<br>'
'  ✅ <strong>雪克</strong>：葡萄颗粒80g（捣碎）+冷冻葡萄汁50ml+冰块150g+冰糖糖浆20ml+茉莉绿茶150ml，摇匀<br>'
'  ✅ 成本约¥8.1 | 售价¥16-22'),

    'YL_022': ('紫玉阳光青提',
'  ✅ <strong>杯底</strong>：葡萄冻80g<br>'
'  ✅ <strong>雪克</strong>：阳光玫瑰青提70g（去皮）+香水柠檬20g+冰块50g（捣碎）+冰糖糖浆30ml+冷冻葡萄汁90ml+白西柚颗粒30g+茉莉绿茶150ml+冰块130g，摇匀<br>'
'  ✅ 成本约¥6.8 | 售价¥16-22'),

    # === YL_023~029 桃气一夏 ===
    'YL_023': ('瓜桃儿墩墩',
'  ✅ <strong>杯底</strong>：新鲜西瓜150g（捣碎）<br>'
'  ✅ <strong>冰沙</strong>：茉莉绿茶80ml+冷冻水蜜桃果蓉60g+冰块150g+冰糖糖浆20ml，搅拌均匀<br>'
'  ✅ 成本约¥4.1 | 售价¥14-18'),

    'YL_024': ('瓜桃儿优酪',
'  ✅ <strong>杯底</strong>：新鲜西瓜200g（捣碎）<br>'
'  ✅ <strong>冰沙</strong>：茉莉绿茶100ml+冷冻水蜜桃果蓉70g+冰块200g+冰糖糖浆25ml，打碎<br>'
'  ✅ 顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥5.5 | 售价¥16-22'),

    'YL_025': ('桃桃蜜柚',
'  ✅ <strong>雪克</strong>：新鲜西柚片60g（捣15下）+冷冻水蜜桃果蓉50g+西柚颗粒30g+冰块200g+茉莉绿茶100ml+冰糖糖浆35ml+西柚浓缩液15ml+饮用水100ml，摇匀<br>'
'  ✅ 成本约¥5.5 | 售价¥15-20'),

    'YL_029': ('紫苏桃桃饮',
'  ✅ <strong>紫苏汁</strong>：新鲜紫苏100g+饮用水300ml+桑葚30g，打10秒后小火煮3分钟过滤<br>'
'  ✅ <strong>雪克</strong>：紫苏汁30ml+冷冻水蜜桃果蓉80g+冰块120g+饮用水100ml+冰糖糖浆15ml+茉莉绿茶120ml，摇匀<br>'
'  ✅ 成本约¥4 | 售价¥14-18'),

    # === YL_030~037 超人气鲜果 ===
    'YL_030': ('霸气杨梅',
'  ✅ <strong>杯底</strong>：原味晶球60g<br>'
'  ✅ <strong>冰沙</strong>：冷冻杨梅浆120ml+冰块200g+饮用水50ml+茉莉绿茶150ml，打碎<br>'
'  ✅ 成本约¥5 | 售价¥15-20'),

    'YL_031': ('草莓撞撞百香冻',
'  ✅ <strong>杯底</strong>：百香果冻120g<br>'
'  ✅ <strong>雪克</strong>：蜜制草莓60g+冰块180g+冷冻草莓原浆80ml+茉莉绿茶100ml+饮用水50ml+冰糖糖浆25ml，摇匀<br>'
'  ✅ 成本约¥6.6 | 售价¥16-22'),

    'YL_032': ('满杯鲜橙',
'  ✅ <strong>雪克</strong>：新鲜橙子3片（捣7-8下）+青柠檬1片+冷冻橙汁60ml+柳橙颗粒+冰块200g+冰糖糖浆40ml+茉莉绿茶150ml+饮用水50ml，摇匀<br>'
'  ✅ 成本约¥4.5 | 售价¥14-18'),

    'YL_033': ('好味油柑绿茶',
'  ✅ <strong>雪克</strong>：茉莉绿茶80ml+冷冻油柑汁150ml+冰糖糖浆40ml+冰块150g+饮用水50ml，摇匀<br>'
'  ✅ 成本约¥7.1 | 售价¥16-20'),

    'YL_034': ('霸气小确杏',
'  ✅ <strong>杯底</strong>：原味晶球80g<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+冰糖糖浆10ml+冷冻杏子酱100g+茉莉绿茶100ml，打碎<br>'
'  ✅ 成本约¥4.7 | 售价¥14-18'),

    'YL_035': ('喜柿多多',
'  ✅ <strong>杯底</strong>：原味晶球40g+冷冻柿子浆20ml<br>'
'  ✅ <strong>冰沙</strong>：冷冻柿子浆50ml+冰糖糖浆25ml+冰块180g+茉莉绿茶50ml+饮用水100ml，打碎<br>'
'  ✅ 成本约¥3.7 | 售价¥12-16'),

    'YL_036': ('霸气山楂草莓',
'  ✅ <strong>冰沙</strong>：冰块200g+冰糖糖浆20ml+茉莉绿茶200ml+山楂草莓酱80g+新鲜草莓30g，打碎<br>'
'  ✅ 顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥4.7 | 售价¥14-18'),

    'YL_037': ('酷黑莓莓',
'  ✅ <strong>杯底</strong>：新鲜黑提40g（捣碎去皮）<br>'
'  ✅ <strong>冰沙</strong>：冰块250g+茉莉绿茶100ml+蜜制草莓20g+去皮夏黑葡萄80g+冷冻葡萄汁80ml+带皮黑提30g+冰糖糖浆20ml，打碎<br>'
'  ✅ 成本约¥7.5 | 售价¥16-22'),

    # === YL_044~046 牛乳冰 ===
    'YL_044': ('绿豆牛乳冰',
'  ✅ <strong>杯底</strong>：绿豆罐头40g+原味晶球40g<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+绿豆罐头120g+浓缩牛乳50ml+饮用水30ml，打碎<br>'
'  ✅ 成本约¥4.9 | 售价¥14-18'),

    'YL_045': ('红豆牛乳冰',
'  ✅ <strong>杯底</strong>：糖水红豆罐头40g+原味晶球40g<br>'
'  ✅ <strong>冰沙</strong>：冰块180g+红豆泥罐头100g+浓缩牛乳60ml+饮用水50ml，打碎<br>'
'  ✅ 成本约¥5.4 | 售价¥14-18'),

    'YL_046': ('绿豆宝宝',
'  ✅ <strong>杯底</strong>：绿豆罐头80g<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+绿豆罐头80g+绿薄荷糖浆5ml+燕麦奶100ml，打碎<br>'
'  ✅ 成本约¥3 | 售价¥12-16'),

    # === YL_047~050 芭乐系列 ===
    'YL_047': ('土芭乐柠茶',
'  ✅ <strong>雪克</strong>：香水柠檬30g+冰块50g（捣30下）+冰块150g+茉莉绿茶150ml+冷冻芭乐浆100ml+冰糖糖浆40ml+饮用水150ml，摇匀<br>'
'  ✅ 成本约¥2.7 | 售价¥14-18'),

    'YL_048': ('满瓶芭乐葡',
'  ✅ <strong>杯底</strong>：新鲜葡萄颗粒60g（捣碎）<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+茉莉绿茶100ml+冰糖糖浆35ml+冷冻芭乐汁70ml+新鲜芭乐50g（去皮），打碎<br>'
'  ✅ 成本约¥6 | 售价¥15-20'),

    'YL_049': ('芭乐桃子酪酪',
'  ✅ <strong>杯底</strong>：冷冻水蜜桃果蓉50g<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+茉莉绿茶100ml+冷冻芭乐汁70ml+新鲜芭乐50g+冰糖糖浆30ml，打碎<br>'
'  ✅ 顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥7.4 | 售价¥16-22'),

    'YL_050': ('芭乐草莓酪酪',
'  ✅ <strong>杯底</strong>：冷冻草莓浆70g<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+茉莉绿茶100ml+冷冻芭乐汁70ml+新鲜芭乐50g+冰糖糖浆30ml，打碎<br>'
'  ✅ 顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥7 | 售价¥16-22'),

    # === YL_051~055 酪酪系列 ===
    'YL_051': ('石榴酪酪',
'  ✅ <strong>杯底</strong>：新鲜石榴60g（捣7下）<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+冷冻石榴汁120ml+冰糖糖浆25ml+茉莉绿茶50ml+火龙果汁15ml，打碎<br>'
'  ✅ 顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥7.2 | 售价¥16-22'),

    'YL_052': ('杨梅酪酪',
'  ✅ <strong>杯底</strong>：杨梅颗粒50g（捣碎）<br>'
'  ✅ <strong>冰沙</strong>：冷冻杨梅浆80ml+冰块150g+冰糖糖浆20ml+茉莉绿茶200ml，打碎<br>'
'  ✅ 顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥6.3 | 售价¥16-22'),

    'YL_053': ('霸气小确杏酪酪',
'  ✅ <strong>杯底</strong>：冷冻杏子酱20g+原味水晶冻100g<br>'
'  ✅ <strong>冰沙</strong>：冰块200g+冰糖糖浆10ml+冷冻杏子酱100g+茉莉绿茶100ml，打碎<br>'
'  ✅ 顶加芝士奶盖2cm<br>'
'  ✅ 成本约¥6.8 | 售价¥16-22'),

    'YL_054': ('玫瑰荔枝酪酪',
'  ✅ <strong>杯底</strong>：原味水晶冻60g<br>'
'  ✅ <strong>冰沙</strong>：荔枝颗粒200g(果肉100g+汤100g)+茉莉绿茶100ml+冰糖糖浆25ml+火龙果汁15ml+冰块200g，打碎<br>'
'  ✅ 顶加芝士奶盖2cm+玫瑰花瓣<br>'
'  ✅ 成本约¥7.8 | 售价¥18-24'),

    'YL_055': ('多肉葡萄桑',
'  ✅ <strong>杯底</strong>：新鲜巨峰葡萄果肉30g+原味水晶冻60g<br>'
'  ✅ <strong>冰沙</strong>：新鲜桑葚80g+冰块200g+茉莉绿茶50ml+冰糖糖浆20ml+柠檬果蜜5ml+饮用水30ml，打碎<br>'
'  ✅ 成本约¥5.9 | 售价¥16-22'),

    # === 鲜奶茶系列 ===
    'YL_056': ('经典蛋糕鲜奶茶',
'  ✅ <strong>杯底</strong>：燕麦罐头80g+蛋糕酱30g（挂壁）<br>'
'  ✅ <strong>饮品</strong>：锡兰红茶200ml+牛奶200ml+冰糖糖浆15ml（加热），搅匀<br>'
'  ✅ 顶加真蛋糕一层<br>'
'  ✅ 成本约¥8.5 | 售价¥18-24'),

    'YL_057': ('栗子麻薯鲜奶茶',
'  ✅ <strong>杯底</strong>：米麻薯40g+板栗泥60g<br>'
'  ✅ <strong>雪克</strong>：鸭屎香茶汤180ml+浓缩牛乳90ml+冰糖糖浆25ml+冰块130g，摇匀<br>'
'  ✅ 成本约¥4.8 | 售价¥14-18'),

    'YL_058': ('黑糖鸭屎香鲜奶茶',
'  ✅ <strong>杯底</strong>：黑糖珍珠100g+冰块100g<br>'
'  ✅ <strong>饮品</strong>：鲜牛奶200ml+鸭屎香茶100ml，直接倒入<br>'
'  ✅ 成本约¥5.1 | 售价¥14-18'),

    'YL_059': ('山茶花鲜奶茶',
'  ✅ <strong>饮品</strong>：山茶花乌龙茶150ml+鲜牛奶200ml+淡奶油15ml+冰块100g+冰糖糖浆25ml，搅匀<br>'
'  ✅ 成本约¥4 | 售价¥14-18'),

    # === 咖啡系列（用广禧配方更新） ===
    'CF-01': ('经典美式咖啡',
'  ✅ <strong>浓缩咖啡</strong>：双份浓缩60ml（水温92°C±1°C，萃取25-30秒）<br>'
'  ✅ <strong>冰美式</strong>：冰块满杯+水200ml+浓缩60ml<br>'
'  ✅ <strong>热美式</strong>：热水200ml+浓缩60ml（先水后咖啡）<br>'
'  ✅ 成本约¥3.8 | 售价¥12-15 | 毛利67-75%'),

    'CF-02': ('生椰拿铁',
'  ✅ <strong>杯底</strong>：冰块100g+生椰乳160ml+椰子水90ml+冰糖糖浆10ml<br>'
'  ✅ <strong>出品</strong>：搅拌均匀后+咖啡液50ml<br>'
'  ✅ 成本约¥8 | 售价¥18-22 | 毛利64%'),

    'CF-08': ('椰青美式',
'  ✅ <strong>杯底</strong>：冰块150g+冰糖糖浆10ml+椰子水300ml<br>'
'  ✅ <strong>出品</strong>：搅拌均匀+咖啡液30ml<br>'
'  ✅ 成本约¥7 | 售价¥16-20'),

    # === 饮品系列补充 ===
    'YL_038': ('太妃芝士奶咖',
'  ✅ <strong>杯底</strong>：冰块100g+鲜奶150ml+冰糖糖浆5ml<br>'
'  ✅ <strong>出品</strong>：搅拌均匀+咖啡液40ml+太妃芝士奶盖30g+薄脆片装饰<br>'
'  ✅ 成本约¥3.8 | 售价¥18-22'),

    'YL_039': ('芭乐碰',
'  ✅ <strong>杯口</strong>：蘸取姜梅粉一圈<br>'
'  ✅ <strong>饮品</strong>：冷冻芭乐汁40ml+鲜奶100ml+淡奶油20ml+冰糖糖浆10ml+冰块100g+饮用水50ml，搅匀<br>'
'  ✅ <strong>出品</strong>：+咖啡液30ml<br>'
'  ✅ 成本约¥3.1 | 售价¥16-20'),

    'YL_040': ('鲜橙美式',
'  ✅ <strong>杯底</strong>：新鲜橙子45g（捣15下）+橘皮糖浆10ml<br>'
'  ✅ <strong>饮品</strong>：冰块100g+饮用水120ml+冰糖糖浆10ml，搅匀<br>'
'  ✅ <strong>出品</strong>：+咖啡液30ml<br>'
'  ✅ 成本约¥2.7 | 售价¥14-18'),

    'YL_041': ('椰青美式',
'  ✅ <strong>杯底</strong>：冰块150g+冰糖糖浆10ml+椰子水300ml<br>'
'  ✅ <strong>出品</strong>：搅匀+咖啡液30ml<br>'
'  ✅ 成本约¥7 | 售价¥16-20'),

    'YL_042': ('生椰拿铁',
'  ✅ <strong>杯底</strong>：冰块100g+生椰乳160ml+椰子水90ml+冰糖糖浆10ml<br>'
'  ✅ <strong>出品</strong>：搅匀+咖啡液50ml<br>'
'  ✅ 成本约¥8 | 售价¥18-22'),

    'YL_043': ('抓马西瓜拿铁',
'  ✅ <strong>杯底</strong>：新鲜西瓜120g（捣碎）+冰块120g<br>'
'  ✅ <strong>饮品</strong>：浓缩牛乳100ml+饮用水100ml+冰糖糖浆15ml，搅匀<br>'
'  ✅ <strong>出品</strong>：倒入杯底+咖啡液30ml<br>'
'  ✅ 成本约¥4.6 | 售价¥16-20'),

    # === 奶茶系列 ===
    'NT_06': ('山茶花奶茶',
'  ✅ <strong>饮品</strong>：山茶花乌龙茶150ml+鲜牛奶200ml+淡奶油15ml+冰块100g+冰糖糖浆25ml，搅匀<br>'
'  ✅ 成本约¥4 | 售价¥14-18'),

    'NT_09': ('淮山红枣奶',
'  ✅ <strong>茶底</strong>：红枣茶+龙眼蜜+柠檬片+冰块+水，雪克摇匀<br>'
'  ✅ 成本约¥4 | 售价¥12-16'),
}

def fill_card(card_id, recipe_name, recipe_content):
    path = os.path.join(CARDS_DIR, f"{card_id}.html")
    if not os.path.exists(path):
        # 试其他文件名
        if card_id.startswith('CF-'):
            path = os.path.join(CARDS_DIR, f"{card_id.replace('-', '_')}.html")
        if not os.path.exists(path):
            print(f"  [跳过] 未找到: {card_id}")
            return False

    with open(path, encoding='utf-8') as f:
        content = f.read()

    bak = path + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(path, bak)

    new_desc = f'  ✅ <strong>{recipe_name}</strong> 商用配比<br>\n{recipe_content}'

    # V4结构
    m = re.search(r'(<div class="desc">)(.*?)(</div>\s*\n?\s*<a class="btn")', content, re.DOTALL)
    if m:
        new_content = content.replace(m.group(0), f'<div class="desc">\n{new_desc}\n  </div>\n  <a class="btn"')
        open(path, 'w', encoding='utf-8').write(new_content)
        print(f"  [V4] {card_id} ← {recipe_name}")
        return True

    # 旧结构
    m = re.search(r'(<ul>\s*\n?)(.*?)(\s*</ul>)', content, re.DOTALL)
    if m:
        lines = new_desc.split('<br>')
        new_list = ''
        for l in lines[:5]:
            clean = re.sub(r'<[^>]+>', '', l).strip()
            if clean:
                new_list += f'    <li>{clean}</li>\n'
        new_list += '    <li>精确到克/ml的商用配比</li>\n    <li>成本拆分+出餐效率优化</li>'
        new_content = content.replace(m.group(0), f'<ul>\n{new_list}\n  </ul>')
        open(path, 'w', encoding='utf-8').write(new_content)
        print(f"  [旧] {card_id} ← {recipe_name}")
        return True

    print(f"  [跳过] 无付费结构: {card_id}")
    return False

if __name__ == '__main__':
    success = 0
    for cid, (rname, rcontent) in DRINK_RECIPES.items():
        if fill_card(cid, rname, rcontent):
            success += 1
    print(f"\n{'='*50}")
    print(f"饮品卡替换完成: {success}/{len(DRINK_RECIPES)} 张")
