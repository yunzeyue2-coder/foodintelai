#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recipe Engine（配方引擎）V1.0 —— 生成端升级
=============================================
单点打穿（Vertical Spike）：把工业级 SOP 战术链注入 FDR 报告，
让报告从"市场分析"变成"物理世界可落地的行动解"。

数据纪律（沧林铁律）：工业参数不编造——写成
  "参数框架（假设区间）→ 实验校准 → 达标线" 的可执行验证方案。

SOP 战术链（炸鸡案例）:
  工艺: 温控曲线 / 克重配比 / 废油率（生炸关键参数）
  选址: 流量租金比模型（替代"竞争少"模糊判断）
  验证: 90天战役的具体动作 + 达标线

输出: 注入 action_layer + reason_layer 的文本（供 Content Quality Gate 打分）
"""
import json, datetime


class RecipeEngine:
    """配方引擎：为决策报告注入可执行的工业级战术链"""

    # ============ 工艺参数框架（假设区间 + 校准方法，不编数字）============

    def process_parameters(self, process):
        """工艺参数框架——每个参数: 假设区间 + 校准方法 + 达标线"""
        params = {
            "生炸": [
                {"param": "油温曲线", "assumption": "170-180℃起炸，出锅前升温逼油",
                 "calibrate": "记录不同温度段出品差异（每10℃一组，各测10次）",
                 "pass_line": "皮脆度/含油量双指标稳定波动<10%"},
                {"param": "克重配比", "assumption": "整鸡600-900g/鸡腿120-180g/鸡架200-400g",
                 "calibrate": "按克重分档炸制，记录成熟时间与出品一致性",
                 "pass_line": "同规格出品时间差<1分钟"},
                {"param": "废油率", "assumption": "裸炸废油率5-15%（区间，依裹粉/裸炸而异）",
                 "calibrate": "每日测油色/油味/换油记录，追踪废油周期",
                 "pass_line": "废油周期稳定，单日废油成本≤毛利X%（实测校准）"},
                {"param": "良率", "assumption": "稳定出品良率≥90%（熟而不焦/皮脆肉嫩）",
                 "calibrate": "试营业期每日统计废弃与返工",
                 "pass_line": "连续7天良率≥90%才进入正式营业"},
            ],
            "小锅现煮": [
                {"param": "汤底保鲜", "assumption": "汤底当日制当日用，冷藏≤12h",
                 "calibrate": "记录风味衰减与售罄率",
                 "pass_line": "晚市售罄率>80%且无投诉"},
                {"param": "出餐节拍", "assumption": "单碗出餐90-150秒（现煮）",
                 "calibrate": "高峰时段计时测产",
                 "pass_line": "高峰翻台率≥X桌/时"},
            ],
        }
        return params.get(process, [])

    # ============ 选址模型：流量租金比（替代"竞争少"）============

    def site_model(self, demand_index, rent_pressure):
        """流量租金比模型——选址判断从模糊变可计算"""
        if rent_pressure <= 0:
            return {"status": "NO_DATA", "advice": "缺租金数据——须实地采集"}
        ratio = demand_index / rent_pressure
        if ratio >= 2.5:
            grade, advice = "A", "需求/租金比高——优先考虑（仍需实地核验人流时段）"
        elif ratio >= 1.5:
            grade, advice = "B", "需求/租金比中等——可作为备选，压低租金再谈"
        else:
            grade, advice = "C", "需求/租金比低——租金吃掉毛利，谨慎"
        return {"ratio": round(ratio, 2), "grade": grade, "advice": advice}

    # ============ 90天验证动作（物理世界可落地）============

    def validation_actions(self, process_params, site_advice):
        """把工艺参数+选址模型组装成 90 天可执行动作"""
        actions = []
        # Phase 1: 需求验证（0-30天）
        p1 = ["冷启动试卖（不挂牌，试营业摆摊测客流）",
              "按 {site_advice} 初筛 3 个候选点位，实地踩点 3 个时段（早/中/晚各1h）"]
        if site_advice:
            p1[1] = f"按「{site_advice}」初筛 3 个候选点位，实地踩点 3 个时段"
        actions.append({"phase": "0-30天", "goal": "验证需求", "actions": p1})

        # Phase 2: 工艺验证（31-60天）——注入 SOP 参数
        p2 = ["工艺参数校准（逐项执行，每项≥10次采样）:"]
        for p in process_params:
            p2.append(f"  - {p['param']}: {p['assumption']} → 校准: {p['calibrate']} → 达标: {p['pass_line']}")
        p2.append("完整记账（收入/成本/损耗分日），算真实毛利率")
        actions.append({"phase": "31-60天", "goal": "验证盈利+工艺稳定", "actions": p2})

        # Phase 3: 复制验证（61-90天）
        p3 = ["SOP 文档化（把校准后的参数写成标准作业卡）",
              "人员轮换测试（请假/换人仍能稳定出品）",
              "按 Kill Criteria 复核：达标→决定扩店/维持单店；不达标→止损退出"]
        actions.append({"phase": "61-90天", "goal": "验证可复制性", "actions": p3})
        return actions

    # ============ 生成建议层文本（注入报告）============

    def build_recommendation_texts(self, process, demand_index, rent_pressure):
        """生成建议层文本（供 Quality Gate 的 recommend 分类）"""
        params = self.process_parameters(process)
        site = self.site_model(demand_index, rent_pressure)
        actions = self.validation_actions(params, site["advice"])

        texts = []
        # 选址建议
        texts.append(f"选址建议: {site['advice']}（需求/租金比 {site.get('ratio', '待采集')}）")
        # 工艺建议
        for p in params:
            texts.append(f"工艺建议: {p['param']} 参数框架 {p['assumption']}，须按「{p['calibrate']}」校准，达标线 {p['pass_line']}")
        # 90天动作
        for a in actions:
            texts.append(f"{a['phase']} {a['goal']}: {'；'.join(a['actions'][:3])}")
        return texts

    def inject(self, report, process, demand_index, rent_pressure):
        """把建议层注入报告（action_layer 扩展 + reason 补充）"""
        texts = self.build_recommendation_texts(process, demand_index, rent_pressure)

        # 注入 action_layer
        actions = report.setdefault("action_layer", [])
        for t in texts[:5]:
            actions.append({
                "period": "90天战役", "goal": t.split(":")[0],
                "tasks": [t], "source": "recipe_engine",
            })
        return report


if __name__ == "__main__":
    print("=== Recipe Engine V1.0 自检 ===")
    re_ = RecipeEngine()

    print("\n[生炸工艺参数框架]")
    for p in re_.process_parameters("生炸"):
        print(f"  {p['param']}: {p['assumption']}")

    print("\n[选址流量租金比]")
    for d, r in [(85, 30), (60, 40), (40, 30)]:
        s = re_.site_model(d, r)
        print(f"  需求{d}/租金{r} → {s['grade']}级 ({s.get('ratio', '?')}) {s['advice']}")

    print("\n[90天验证动作（含SOP注入）]")
    texts = re_.build_recommendation_texts("生炸", 85, 30)
    for t in texts[:4]:
        print(f"  • {t[:80]}")
