# 内容分发生成器
# 输入：卡片HTML文件路径
# 输出：公众号文章/小红书笔记/知乎回答/知乎专栏 四种格式

import os, re

CARDS_DIR = '/Users/mac/Desktop/青葵/foodintelai-site/cards'

def extract_card_data(filepath):
    """从V4卡片HTML提取关键数据"""
    with open(filepath) as f:
        html = f.read()
    
    data = {}
    
    # 标题
    m = re.search(r'<h1>([^<]+)</h1>', html)
    data['title'] = m.group(1) if m else ''
    
    # 副标题
    m = re.search(r'<div class="sub">([^<]+)</div>', html)
    data['sub'] = m.group(1) if m else ''
    
    # 品类标签
    m = re.search(r'<span class="badge">([^<]+)</span>', html)
    data['badge'] = m.group(1) if m else ''
    
    # 启动资金/日营收/毛利率/回本（去掉前缀标签）
    levels = re.findall(r'<span class="level-item[^"]*">([^<]+)</span>', html)
    data['invest_raw'] = levels[0] if len(levels) > 0 else ''
    data['income_raw'] = levels[1] if len(levels) > 1 else ''
    data['gross_raw'] = levels[2] if len(levels) > 2 else ''
    data['roi_raw'] = levels[3] if len(levels) > 3 else ''
    # 去掉前缀（如"启动资金："只保留数值部分）
    data['invest'] = re.sub(r'^[^：]*：', '', data['invest_raw'])
    data['income'] = re.sub(r'^[^：]*：', '', data['income_raw'])
    data['gross'] = data['gross_raw']  # 毛利率通常直接是数值
    data['roi'] = re.sub(r'^[^：]*：', '', data['roi_raw'])
    
    # 产品说（第一个story块）
    stories = re.findall(r'<div class="story">(.*?)</div>', html, re.DOTALL)
    data['desc'] = stories[0].strip() if stories else ''
    # 第二个story是工艺流程
    data['process'] = stories[1].strip().replace('<br>', '\n') if len(stories) > 1 else ''
    
    # 风险
    risks = re.findall(r'<div class="risk-item"><span>([^<]+)</span>', html)
    data['risks'] = risks
    
    # 场景
    scenes = re.findall(r'<span class="scene-item">([^<]+)</span>', html)
    data['scenes'] = scenes
    
    # 搭配
    pairs = re.findall(r'<span class="p-name">([^<]+)</span>.*?<span class="p-price">([^<]+)</span>', html)
    data['pairs'] = pairs
    
    # 话术
    m = re.search(r'<div class="talk">(.*?)</div>', html, re.DOTALL)
    data['talk'] = m.group(1).strip() if m else ''
    
    # 避坑
    tips = re.findall(r'<div class="tip-item">([^<]*)</div>', html)
    data['tips'] = tips
    
    # 配方内容
    m = re.search(r'<div class="recipe-box">(.*?)</div>', html, re.DOTALL)
    data['recipe'] = m.group(1).strip() if m else ''
    
    # 成本行
    cost_rows = re.findall(r'<div class="row[^"]*"><span>([^<]+)</span><span class="v">([^<]+)</span></div>', html)
    data['costs'] = [(r[0], r[1]) for r in cost_rows if '总成本' not in r[0] and '建议售价' not in r[0]]
    
    # 编号
    m = re.search(r'产品编号 ([A-Z]+_\d+)', html)
    data['card_id'] = m.group(1) if m else ''
    
    return data


def gen_wechat(data):
    """生成公众号文章"""
    title = f'{data["title"]}：摆摊到开店，这份配方够你赚回房租'
    
    body = f'''# {title}

> {data['sub']}

---

## 一、这个产品是什么

{data['desc'][:200]}...

**启动资金**：{data['invest']}
**日营收**：{data['income']}
**毛利率**：{data['gross']}
**回本周期**：{data['roi']}

---

## 二、成本利润拆解

| 项目 | 成本 |
|------|------|
'''
    for name, price in data['costs']:
        body += f'| {name} | {price} |\n'
    
    body += f'''
**毛利率**：{data['gross']}

这是一个摆摊级别的利润模型，日营收{data['income']}，一个人就能干。

---

## 三、核心工艺

{data['process'][:300]}...

---

## 四、风险提示

'''
    for r in data['risks']:
        body += f'- ❗ {r}\n'
    
    body += f'''
---

## 五、适合谁干

'''
    for s in data['scenes']:
        body += f'- ✅ {s}\n'
    
    body += f'''
---

## 六、搭配销售提升客单价

'''
    for name, price in data['pairs'][:3]:
        body += f'- {name}：{price}\n'
    
    body += f'''
---

## 💰 完整配方获取

完整配方含精确到克的配比、详细工艺参数、运营方案。
添加微信获取：**备注「{data["card_id"]}」**

---

*本文由 FoodIntel AI 食品创业决策系统生成*
*{data["card_id"]} · 沧林食品*
'''
    return body


def gen_xiaohongshu(data):
    """生成小红书笔记"""
    title = f'🔥{data["title"]}｜{data["sub"][:30]}'
    
    body = f'''{title}

---

💡 **产品说**
{data['desc'][:150]}...

💰 **利润模型**
启动资金：{data['invest']}
日营收：{data['income']}
毛利率：{data['gross']}
回本周期：{data['roi']}

成本拆解：
'''
    for name, price in data['costs']:
        body += f'• {name}：{price}\n'
    
    body += f'''
🔬 **核心工艺**
{data['process'][:200]}...

⚠️ **三大风险**
'''
    for r in data['risks'][:3]:
        body += f'• {r}\n'
    
    body += f'''
🎯 **适合场景**
{' · '.join(data['scenes'][:4])}

💬 **卖货话术**
{data['talk'][:100]}...

---

完整配方📩 加微信备注「{data["card_id"]}」
#摆摊创业 #餐饮创业 #{data["title"]} #配方分享 #小本创业
'''
    return title, body


def gen_zhihu(data):
    """生成知乎回答"""
    title = f'{data["title"]}值得做吗？真实利润和风险分析'
    
    body = f'''**问题：** {data["title"]}值得做吗？

**回答：**

先说结论：**可以做，但前提是你得搞清楚下面几件事。**

---

### 1. 这个产品赚不赚钱？

启动资金{data['invest']}，日营收{data['income']}，毛利率{data['gross']}，{data['roi']}回本。

成本拆解：
'''
    for name, price in data['costs']:
        body += f'- {name}：{price}\n'
    
    body += f'''
### 2. 核心壁垒在哪？

{data['desc'][:200]}...

### 3. 最大风险是什么？

'''
    for r in data['risks']:
        body += f'- {r}\n'
    
    body += f'''
### 4. 什么样的人适合干？

'''
    for s in data['scenes']:
        body += f'- {s}\n'
    
    body += f'''
---

**总结：** {data["title"]}这个品类{data["roi"]}能回本，适合{data["invest"]}预算的创业者。核心是做好成本和品控。

---

*数据来源：FoodIntel AI 食品创业决策系统 · 卡片编号 {data["card_id"]}*
'''
    return title, body


def gen_zhihu_column(data):
    """生成知乎专栏（更深度内容）"""
    title = f'深度拆解{data["title"]}：从配方到利润，一篇讲透'
    
    body = f'''# {title}

## 前言

{data["sub"]}

这篇文章将从**产品定位、成本利润、核心工艺、风险控制、运营策略**五个维度，完整拆解{data["title"]}这个品类。

---

## 一、产品定位

{data["desc"]}

**关键数据：**
- 启动资金：{data['invest']}
- 日营收：{data['income']}
- 毛利率：{data['gross']}
- 回本周期：{data['roi']}

---

## 二、成本利润深度拆解

'''
    for name, price in data['costs']:
        body += f'| {name} | {price} |\n'
    
    body += f'''
从成本结构看，这个品类的毛利率在{data['gross']}，属于餐饮行业中等偏上的水平。

---

## 三、核心工艺要点

{data['process']}

---

## 四、风险控制

'''
    for r in data['risks']:
        body += f'### {r}\n\n'
    
    body += f'''
---

## 五、适合场景与运营策略

**适合场景：**
'''
    for s in data['scenes']:
        body += f'- {s}\n'
    
    body += f'''
**搭配销售：**
'''
    for name, price in data['pairs'][:5]:
        body += f'- {name}：{price}\n'
    
    body += f'''
---

## 完整配方获取

本文内容为配方框架。精确到克的完整配方、工艺参数、运营方案，请添加微信获取。

备注：**「{data["card_id"]}」**

---

*本文由 FoodIntel AI 内容分发系统生成 · {data["card_id"]}*
'''
    return title, body


def generate_all(card_id):
    """生成所有平台内容"""
    # 支持两种输入：纯ID（如BM_001）或路径
    if '/' in card_id or '\\' in card_id:
        filepath = card_id
    else:
        filepath = os.path.join(CARDS_DIR, f'{card_id}.html')
    
    if not os.path.exists(filepath):
        # 尝试cards/cards/目录
        filepath2 = os.path.join(CARDS_DIR, 'cards', f'{card_id}.html')
        if os.path.exists(filepath2):
            filepath = filepath2
        else:
            print(f'❌ 未找到卡片: {card_id}')
            return None
    
    data = extract_card_data(filepath)
    if not data['title']:
        print(f'❌ 无法解析卡片内容: {card_id}')
        return None
    
    print(f'\n{"="*60}')
    print(f'  {data["card_id"]} · {data["title"]}')
    print(f'  {data["sub"]}')
    print(f'{"="*60}')
    
    # 公众号
    wechat = gen_wechat(data)
    print(f'\n{"="*60}')
    print(f'📢 公众号文章')
    print(f'{"="*60}')
    print(wechat)
    
    # 小红书
    xhs_title, xhs_body = gen_xiaohongshu(data)
    print(f'\n{"="*60}')
    print(f'📕 小红书笔记')
    print(f'  标题: {xhs_title}')
    print(f'{"="*60}')
    print(xhs_body)
    
    # 知乎回答
    zh_title, zh_body = gen_zhihu(data)
    print(f'\n{"="*60}')
    print(f'❓ 知乎回答')
    print(f'  标题: {zh_title}')
    print(f'{"="*60}')
    print(zh_body)
    
    # 知乎专栏
    zc_title, zc_body = gen_zhihu_column(data)
    print(f'\n{"="*60}')
    print(f'📝 知乎专栏')
    print(f'  标题: {zc_title}')
    print(f'{"="*60}')
    print(zc_body)
    
    return {
        'card_id': data['card_id'],
        'title': data['title'],
        'wechat': wechat,
        'xiaohongshu': xhs_body,
        'zhihu': zh_body,
        'zhihu_column': zc_body,
    }


def batch_generate(card_ids):
    """批量生成"""
    results = {}
    for cid in card_ids:
        result = generate_all(cid)
        if result:
            results[cid] = result
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        generate_all(sys.argv[1])
    else:
        # 默认测试一张卡
        print("用法: python3 content_generator.py <卡片ID>")
        print("例如: python3 content_generator.py BM_001")
        print("\n测试生成 BM_001:\n")
        generate_all('BM_001')
