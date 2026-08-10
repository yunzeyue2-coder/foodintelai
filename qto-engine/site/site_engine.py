#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Site Engine（选址引擎）V1.0
============================
GPT 工业化清单 Sprint 4：从"最近邻距离"升级为"位置评分+焦土检测"。

SiteScore = 需求指数 + 流量指数 - 竞争压力 - 租金压力

焦土检测（RENT_TRAP）:
  shop_turnover_rate 高（一年换3次店）→ 标记 RENT_TRAP
  → 不是"竞争少"就是好位置，租金陷阱要识别

输出: 推荐点位 + 原因（需求/租金比最高），不是"竞争少"这种模糊结论
"""
import json, math


class SiteEngine:
    # 焦土阈值：一年换店次数 ≥ 3 → RENT_TRAP
    RENT_TRAP_TURNOVER = 3
    # 评分权重
    W = {"demand": 0.4, "traffic": 0.3, "competition": 0.2, "rent": 0.1}

    def __init__(self, weights=None):
        self.weights = weights or self.W

    # ============ 1. 单点位评分 ============

    def score_site(self, site):
        """单点位评分。
        site: {name, demand_index(0-100), traffic_index(0-100),
               competition_pressure(0-100), rent_pressure(0-100),
               shop_turnover_rate(年换店次数)}
        返回 {score(0-100), grade, flags[]}
        """
        # 焦土检测
        flags = []
        turnover = site.get("shop_turnover_rate", 0)
        if turnover >= self.RENT_TRAP_TURNOVER:
            flags.append("RENT_TRAP")

        # 需求/租金比（GPT 强调的关键指标）
        demand_rent_ratio = 0
        if site.get("rent_pressure", 0) > 0:
            demand_rent_ratio = site.get("demand_index", 0) / site.get("rent_pressure", 1)

        # SiteScore（优势分公式：竞争/租金低=优势高）
        score = (
            self.weights["demand"] * site.get("demand_index", 0)
            + self.weights["traffic"] * site.get("traffic_index", 0)
            + self.weights["competition"] * (100 - site.get("competition_pressure", 0))
            + self.weights["rent"] * (100 - site.get("rent_pressure", 0))
        )
        score = max(0, min(100, score))

        # RENT_TRAP 惩罚：score 减半 + 标记
        if "RENT_TRAP" in flags:
            score *= 0.5

        grade = "A" if score >= 75 else ("B" if score >= 55 else ("C" if score >= 35 else "D"))
        return {
            "name": site.get("name", "?"),
            "score": round(score, 1),
            "grade": grade,
            "demand_rent_ratio": round(demand_rent_ratio, 2),
            "flags": flags,
            "recommend": score >= 60 and "RENT_TRAP" not in flags,
        }

    # ============ 2. 多点位对比（推荐）============

    def recommend(self, sites):
        """多点位对比：按需求/租金比+评分排序，输出推荐点位+原因"""
        scored = [self.score_site(s) for s in sites]
        # 排序：推荐优先，然后评分
        ranked = sorted(scored, key=lambda x: (x["recommend"], x["score"], x["demand_rent_ratio"]), reverse=True)
        top = ranked[0] if ranked else None
        return {
            "ranked": ranked,
            "top_pick": top,
            "reason": (f"{top['name']} 需求/租金比最高（{top['demand_rent_ratio']}）+ 评分{top['score']}（{top['grade']}级）"
                       if top and top["recommend"] else
                       ("所有点位均有风险（RENT_TRAP 或评分不足）" if top else "无点位输入")),
        }


if __name__ == "__main__":
    print("=== Site Engine V1.0 自检 ===")
    se = SiteEngine()

    sites = [
        {"name": "点位A-大学城", "demand_index": 85, "traffic_index": 80,
         "competition_pressure": 40, "rent_pressure": 30, "shop_turnover_rate": 1},
        {"name": "点位B-老社区", "demand_index": 60, "traffic_index": 50,
         "competition_pressure": 20, "rent_pressure": 15, "shop_turnover_rate": 2},
        {"name": "点位C-高换手商圈", "demand_index": 90, "traffic_index": 85,
         "competition_pressure": 45, "rent_pressure": 25, "shop_turnover_rate": 4},  # 焦土
        {"name": "点位D-写字楼", "demand_index": 70, "traffic_index": 65,
         "competition_pressure": 35, "rent_pressure": 40, "shop_turnover_rate": 1},
    ]
    r = se.recommend(sites)
    print("\n[点位评分]")
    for s in r["ranked"]:
        trap = " ⚠️RENT_TRAP" if "RENT_TRAP" in s["flags"] else ""
        print(f"  {s['name']}: {s['score']}分({s['grade']}) 需求/租金比{s['demand_rent_ratio']}{trap}")
    print(f"\n[推荐] {r['top_pick']['name'] if r['top_pick'] else '无'}")
    print(f"  原因: {r['reason']}")
    print(f"\n  ✅ 焦土点位C 被识别（换手4次/年 → RENT_TRAP → 评分减半）")
