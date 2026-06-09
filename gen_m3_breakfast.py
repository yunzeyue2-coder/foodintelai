#!/usr/bin/env python3
"""追加早餐店M3卡"""
import os, sys
sys.path.insert(0, '/Users/mac/Desktop/青葵/foodintelai-site')
from gen_m3_stores import STORES, CARDS_DIR, DELIVERY_DIR, DE_FILE, M3_TPL, update_de

# 追加
new_store = {
    'id': 'MD_BZ_000', 'name': '早餐/包子店', 'color': '#F39C12',
    'desc': '包子粥品完整方案 · 40+款单品SOP · 早高峰翻台率制胜',
    'sop_count': '40+', 'score1': '6.5', 'score2': '8.5', 'score3': '7.5', 'score4': '6.0',
    'funds': '¥3-8万', 'daily': '¥1,000-2,500', 'margin': '55-65%', 'payback': '4-8个月',
    'staff': '1-2人', 'area': '10-25㎡',
    'note': '早餐店',
    'products': '<div class="product-item"><span class="label">🥟 包子系列</span><br>灌汤包/蟹黄汤包/酱肉包/猪肉包/咖喱牛肉包/青菜包/豆沙包/麻辣粉丝包(11+款)</div>'
               '<div class="product-item"><span class="label">🥣 粥品系列</span><br>皮蛋瘦肉粥/南瓜粥/小米粥/滑蛋牛肉粥/紫薯燕麦粥/猪肝粥/香菇瘦肉粥/海带绿豆粥(13+款)</div>'
               '<div class="product-item"><span class="label">🥟 早餐系列</span><br>千层饼/鸡蛋饼/京东肉饼/糍粑油条/菜角/武汉三鲜豆皮/油条/葱香茄子饼(9+款)</div>'
               '<div class="product-item"><span class="label">🥣 胡辣汤系列</span><br>逍遥镇胡辣汤/羊肉胡辣汤/肉丁胡辣汤/面筋胡辣汤/大料粉配方(5+款)</div>'
               '<div class="product-item"><span class="label">🧂 配套酱料</span><br>灌汤包馅料/皮冻配方/包子馅料6种/万能母馅</div>'
               '<div class="product-item"><span class="label">📊 经营数据</span><br>翻台率决定生死·出餐≤7分钟/笼·早午双品类互补</div>',
    'delivery': '<strong>一、包子SOP（11+款）</strong><br>'
               '灌汤包·蟹黄汤包·酱肉包·猪肉包·咖喱牛肉包·香菇青菜包·豆沙包·麻辣粉丝包<br>'
               '皮冻配方·发面包子面皮（冬/夏两版）·馅料6种配方(酱肉熟鲜·咖喱牛肉·麻辣粉丝·豆沙·青菜·猪肉)<br><br>'
               '<strong>二、粥品SOP（13+款）</strong><br>'
               '皮蛋瘦肉粥·南瓜粥·小米粥·滑蛋牛肉粥·紫薯燕麦粥·猪肝粥·香菇瘦肉粥·红枣小米粥·海带绿豆粥·鸡肉粥·窝蛋牛肉粥·芋头粥等<br><br>'
               '<strong>三、早餐面点（9+款）</strong><br>'
               '千层饼·鸡蛋饼·京东肉饼·糍粑油条·菜角·武汉三鲜豆皮<br><br>'
               '<strong>四、胡辣汤（5+款）</strong><br>'
               '逍遥镇胡辣汤·羊肉胡辣汤·肉丁胡辣汤·面筋胡辣汤·大料粉配方<br><br>'
               '<strong>五、设备清单+开店指南</strong><br>'
               '蒸包炉/粥桶/电饼铛/保温柜·早高峰动线设计·前夜备料方案',
}

html = M3_TPL.format(**new_store)
path = os.path.join(CARDS_DIR, f"{new_store['id']}_{new_store['name']}.html")
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"[M3] {new_store['id']} {new_store['name']}")

update_de(new_store['id'], new_store)
print("✅ 早餐/包子店完成")
