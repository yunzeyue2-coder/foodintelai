#!/usr/bin/env python3
"""
韩式炸鸡门店配方替换脚本
用咖吃客韩式炸鸡技术教学的9个配方
替换HZ炸鸡卡和JL酱料卡的付费区内容
"""
import os, shutil, re

CARDS_DIR = "/Users/mac/Desktop/青葵/foodintelai-site/cards"

# ========== 韩式配方数据 ==========

# 1. 甘梅地瓜
GANMEI = """
  ✅ <strong>面糊</strong>：面粉150g 糯米粉75g 酵母1g 蛋黄1个 色拉油10g 水适量<br>
  ✅ <strong>地瓜</strong>：红薯500g，去皮切1×1×6cm长条<br>
  ✅ <strong>炸制</strong>：油温145-175°C，炸至浮起金黄，捞出撒甘梅粉<br>
  ✅ 关键：面糊搅拌至表面起小泡（约5-8分钟），地瓜裹糊均匀<br>
  ✅ 成本：地瓜约¥3+粉料约¥1+油约¥0.5=¥4.5，售价¥12-15，毛利65-70%
"""

# 2. 秘酱火辣
MIJIANG_HOLA = """
  ✅ <strong>白糖稀</strong>200g+<strong>番茄酱</strong>80g+<strong>赤砂糖</strong>50g+<strong>白葡萄酒</strong>50g+<strong>蒜末</strong>20g+<strong>洋葱末</strong>30g<br>
  ✅ <strong>调味</strong>：黑胡椒粉2g 辣椒面(细)6g 清净园酱油12g 细盐2g CJ牛肉粉4g 桂皮粉0.2g 青友液体辣椒素3g<br>
  ✅ <strong>制作</strong>：全部材料混合后中火烧开，小火冒泡，发酵3小时以上可用<br>
  ✅ <strong>保存</strong>：最长15天，建议5-7天用完<br>
  ✅ 品牌：清净园糖稀+亨氏番茄酱+小伙子辣椒面
"""

# 3. 酸奶酱
YOGURT = """
  ✅ <strong>酸奶</strong>45g（固体酸奶）+<strong>柠檬酱</strong>25g（美谈彩）+<strong>芝士沙拉酱</strong>10g（味好美）<br>
  ✅ <strong>制作</strong>：所有材料混合均匀即可<br>
  ✅ <strong>保存</strong>：密封2-4°C冷藏，最长15天<br>
  ✅ 用途：炸鸡蘸酱、蔬菜沙拉酱<br>
  ✅ 口感：酸甜清爽，中和炸鸡油腻感
"""

# 4. 韩式脆萝卜
PICKLED_RADISH = """
  ✅ <strong>主料</strong>：白萝卜1000g（去皮切1×1cm方块）<br>
  ✅ <strong>酸甜汁</strong>：白砂糖300g 大麦醋300g 大粒盐20g 水800g 小米辣20g(椒圈) 小葱50g(10cm段)<br>
  ✅ <strong>香料</strong>：酸黄瓜料5g 栀子3g（调色）<br>
  ✅ <strong>制作</strong>：糖醋汁煮开放入萝卜块+香料，常温冷却后冷藏<br>
  ✅ <strong>发酵</strong>：72小时后使用，最多存储30天<br>
  ✅ 成本：萝卜约¥3+糖醋调料约¥5=¥8，可出15-20份
"""

# 5. 经典甜辣炸鸡酱 —— 核心配方！
SWEET_SPICY = """
  ✅ <strong>核心酱底</strong>：<br>
  &nbsp;&nbsp;• 韩式辣酱120g（CJ好餐得）<br>
  &nbsp;&nbsp;• 番茄酱240g（亨氏）<br>
  &nbsp;&nbsp;• 糖稀250g（清净园）<br>
  &nbsp;&nbsp;• 赤砂糖90g（CJ）<br>
  ✅ <strong>调味料</strong>：<br>
  &nbsp;&nbsp;• 蒜末60g 洋葱末30g 水100g<br>
  &nbsp;&nbsp;• 泰式甜辣酱30g（潘泰诺华星）<br>
  &nbsp;&nbsp;• 伍斯特酱25g（亨氏）<br>
  &nbsp;&nbsp;• 草莓酱75g（不倒翁）<br>
  ✅ <strong>制作</strong>：全部材料入锅，大火烧开转小火加热1分钟<br>
  ✅ <strong>发酵</strong>：常温冷却后冷藏，发酵6小时后使用<br>
  ✅ <strong>保存</strong>：2-4°C冷藏，最多存放15天<br>
  ✅ 成本：酱料成本约¥8/500g，每份鸡翅用酱约50g=¥0.8
"""

# 6. 雪翼芝士粉
CHEESE_POWDER = """
  ✅ <strong>基底</strong>：全脂奶粉100g（雀巢） 帕玛森芝士粉50g（卡雷） 橘黄芝士粉50g（飞驼） 巧达芝士粉20g（宝尔）<br>
  ✅ <strong>调味</strong>：黄砂糖70g（CJ） 熟黄豆粉10g 盐5g 咖喱粉3g（不倒翁） 洋葱粉5g（玉友） 欧芹碎1g<br>
  ✅ <strong>制作</strong>：除欧芹碎外所有材料入破壁机打碎，最后加欧芹碎拌匀<br>
  ✅ <strong>保存</strong>：密封阴凉干燥处保存<br>
  ✅ 用途：炸鸡出锅后趁热裹粉，雪翼风格
"""

# 7. 盐酥鸡腌料
SALT_CRISPY = """
  ✅ <strong>主料</strong>：鸡腿肉500g（去骨）<br>
  ✅ <strong>腌料</strong>：酱油膏30g（金兰） 啤酒120g 蒜泥16g 姜泥2g 五香粉3g（海堤） 白胡椒粉2g（麦味宝）<br>
  ✅ <strong>调味</strong>：盐2g 白砂糖3g 味精3g 玉米淀粉14g<br>
  ✅ <strong>制作</strong>：所有材料混合均匀，放入鸡块用手按摩5分钟<br>
  ✅ <strong>腌制</strong>：2-4°C冷藏，腌制12小时后使用<br>
  ✅ 成本：鸡腿肉约¥15+腌料约¥2=¥17，出4-5份
"""

# 8. 黄芥末酱
MUSTARD = """
  ✅ <strong>基底</strong>：黄芥末酱300g（旗牌） 糖稀1000g（清净园） 酸奶400g 蛋黄酱100g（不倒翁）<br>
  ✅ <strong>调味</strong>：白砂糖250g（CJ） 苹果醋150g（不倒翁） 生抽75g（清净园） 黄芥末粉10g（不倒翁）<br>
  ✅ <strong>制作</strong>：所有材料放入干净无油盆中，手动打蛋器搅拌均匀<br>
  ✅ <strong>发酵</strong>：冷藏发酵6小时后使用<br>
  ✅ <strong>保存</strong>：2-4°C冷藏约15天<br>
  ✅ 用途：炸鸡蘸酱、汉堡酱
"""

# 9. 芝士芥末酱
CHEESE_MUSTARD = """
  ✅ <strong>基底</strong>：芝士沙拉酱1000g（百利）+200g（味好美） 芝士酱100g（百吉福）<br>
  ✅ <strong>调味</strong>：糖稀700g（清净园） 芝士粉10g（宝尔） 黄芥末酱40g（旗牌）<br>
  ✅ <strong>制作</strong>：所有材料放入干净无油盆中，手动打蛋器搅拌均匀<br>
  ✅ <strong>发酵</strong>：冷藏发酵6小时后使用<br>
  ✅ <strong>保存</strong>：2-4°C冷藏约15天<br>
  ✅ 用途：炸鸡蘸酱、芝士控首选
"""

RECIPES = {
    # HZ炸鸡系列
    'HZ_001': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_002': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_003': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_004': ('韩式甜辣炸鸡', SWEET_SPICY),
    'HZ_005': ('蜂蜜芥末炸鸡', MUSTARD),  # 黄芥末酱
    'HZ_006': ('琥珀酱油炸鸡', MIJIANG_HOLA),  # 秘酱火辣 接近琥珀酱油
    'HZ_007': ('奶香芝士炸鸡/雪翼', CHEESE_POWDER),  # 雪翼芝士粉
    'HZ_008': ('奶香芝士炸鸡', CHEESE_MUSTARD),  # 芝士芥末酱
    'HZ_009': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_010': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_011': ('米粉炸鸡', SWEET_SPICY),
    'HZ_012': ('蒜香黄金炸鸡', MIJIANG_HOLA),  # 秘酱火辣+蒜香
    'HZ_013': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_014': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_015': ('琥珀酱油炸鸡', MIJIANG_HOLA),
    'HZ_016': ('调味酱油鸡块', MIJIANG_HOLA),
    'HZ_017': ('经典甜辣炸鸡', SWEET_SPICY),
    'HZ_018': ('甘梅地瓜', GANMEI),
    'HZ_019': ('韩式炸鸡拌饭', SWEET_SPICY),
    'HZ_020': ('经典甜辣炸鸡', SWEET_SPICY),
    
    # JL酱料系列
    'JL_051': ('韩式甜辣酱（熬制版）', SWEET_SPICY),
    'JL_052': ('韩式嗨辣酱（爆辣）', MIJIANG_HOLA),  # 秘酱火辣+辣椒素
    'JL_053': ('韩式琥珀酱', MIJIANG_HOLA),
    'JL_054': ('蜂蜜芥末酱', MUSTARD),
    'JL_055': ('奶香芝士酱', CHEESE_MUSTARD),
    'JL_056': ('蒜香酱油酱', MIJIANG_HOLA),  # 秘酱火辣调咸口
    'JL_057': ('香辣酱', MIJIANG_HOLA),
    'JL_058': ('VC蜜汁酱', SWEET_SPICY),
    'JL_059': ('糖醋蜜汁酱', SWEET_SPICY),
    'JL_060': ('果味蜜汁酱', SWEET_SPICY),
    'JL_063': ('杰克丹尼酱', SWEET_SPICY),
    'JL_064': ('四川炸鸡酱', SWEET_SPICY),
    'JL_065': ('葱丝炸鸡酱', SWEET_SPICY),
    'JL_066': ('米粉炸鸡蘸料', SWEET_SPICY),
    'JL_067': ('甜辣炸鸡酱', SWEET_SPICY),
    'JL_068': ('蜂蜜炸鸡酱', MUSTARD),  # 蜂蜜+黄芥末
    'JL_069': ('椒香炸鸡酱', SWEET_SPICY),
    'JL_070': ('果酱炸鸡酱', SWEET_SPICY),
    'JL_071': ('酱油炸鸡酱', MIJIANG_HOLA),
    'JL_072': ('秘酱炸鸡酱', MIJIANG_HOLA),
    'JL_073': ('甜蒜炸鸡酱', SWEET_SPICY),
    'JL_074': ('雪花芝士炸鸡酱', CHEESE_POWDER),
    'JL_075': ('黄芥末酸奶酱', MUSTARD),  # 黄芥末+酸奶
    'JL_076': ('韩式炸鸡基础酱（草莓酱版）', SWEET_SPICY),
    'JL_077': ('泡菜炸鸡酱', SWEET_SPICY),
    'JL_078': ('芝士炸鸡酱', CHEESE_MUSTARD),
    'JL_079': ('芝士牛乳酱', CHEESE_MUSTARD),
    'JL_080': ('辣芝士炸鸡酱', CHEESE_MUSTARD),
    'JL_081': ('美式香草沙拉酱', MUSTARD),
    'JL_082': ('原味炸鸡酱', SWEET_SPICY),
    'JL_083': ('韩式辣白菜酱', SWEET_SPICY),
    'JL_084': ('韩式甜辣酱（冷调版）', SWEET_SPICY),
    'JL_085': ('蜂蜜黄油炸鸡酱', MUSTARD),
    'JL_086': ('炸鸡拌饭汁', SWEET_SPICY),
}

def update_card(card_id, recipe_name, recipe_content):
    """更新单张卡"""
    path = os.path.join(CARDS_DIR, f"{card_id}.html")
    if not os.path.exists(path):
        print(f"  [跳过] 未找到: {card_id}")
        return False
    
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    bak = path + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    
    # 构建新的付费区desc
    new_desc = f'  ✅ <strong>配方来源</strong>：韩式连锁店标准工艺<br>\n  ✅ <strong>配方</strong>：{recipe_name}<br>\n{recipe_content}'
    
    # 替换V4结构
    m = re.search(r'(<div class="desc">)(.*?)(</div>\s*\n?\s*<a class="btn")', content, re.DOTALL)
    if m:
        new_content = content.replace(m.group(0), f'<div class="desc">\n{new_desc}\n  </div>\n  <a class="btn"')
        open(path, 'w', encoding='utf-8').write(new_content)
        print(f"  [V4] {card_id} ← {recipe_name}")
        return True
    
    # 替换旧结构
    m = re.search(r'(<ul>\s*\n?)(.*?)(\s*</ul>)', content, re.DOTALL)
    if m:
        lines = new_desc.split('<br>')
        new_list = ''
        for l in lines[:5]:
            clean = re.sub(r'<[^>]+>', '', l).strip()
            if clean:
                new_list += f'    <li>{clean}</li>\n'
        new_list += '    <li>韩式连锁店标准工艺配方</li>\n    <li>精确到克的商用配比+品牌推荐</li>'
        new_content = content.replace(m.group(0), f'<ul>\n{new_list}\n  </ul>')
        open(path, 'w', encoding='utf-8').write(new_content)
        print(f"  [旧] {card_id} ← {recipe_name}")
        return True
    
    print(f"  [跳过] 无付费结构: {card_id}")
    return False

if __name__ == '__main__':
    success = 0
    for cid, (rname, rcontent) in RECIPES.items():
        if update_card(cid, rname, rcontent):
            success += 1
    
    print(f"\n{'='*50}")
    print(f"韩式配方替换完成: {success}/{len(RECIPES)} 张")
    print(f"HZ炸鸡卡20张 + JL酱料卡{len(RECIPES)-20}张")
