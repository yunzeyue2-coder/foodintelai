#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Business Twin Engine（商业数字孪生）V1.0
=========================================
青藤OS 护城河：输入 城市+品类+预算+经验+目标
→ 输出 投资结构 + 风险区间 + 生存压力测试（不是给一个答案）

核心能力：
1. 投资结构模拟（启动资金怎么分配）
2. 单店经济框架（收入/成本/盈亏平衡，用假设区间不编数字）
3. 三场景生存压力测试（低/中/理想销量 → 现金能撑多久）
4. Kill Criteria 前置（先定义退出条件再入场）

原则（Schema V2.0）：
- no_fake_precision: 无数据时用假设区间，不编造精确数字
- survival_first: 先证明能活过90天，再谈复制
- kill_before_enter: 入场前先定义止损线
"""
import json


class BusinessTwinEngine:
    def __init__(self, category_config=None):
        # 品类默认配置（可被项目级 config 覆盖）
        self.category_config = category_config or {}
        self.last_simulation = None

    # ============ 1. 投资结构 ============

    def simulate_investment_structure(self, budget, model_preset="档口/小店", ratios=None):
        """启动资金结构模拟。
        默认分配比（档口/小店模型，可覆盖）：
          设备 25% / 装修 15% / 租金押金 20% / 首批物料+运营 15% / 试错缓冲 25%
        """
        default_ratios = {
            "设备": 0.25, "装修": 0.15, "租金押金": 0.20,
            "首批物料+运营": 0.15, "试错缓冲": 0.25,
        }
        ratios = ratios or self.category_config.get("investment_ratios", default_ratios)
        # 校验总和 ≤ 1
        total = sum(ratios.values())
        if total > 1.0:
            return {"status": "INVALID", "error": f"分配比总和 {total:.2f} > 1.0"}

        items = {}
        for name, ratio in ratios.items():
            items[name] = round(budget * ratio, -2)  # 取整百
        items["预算总额"] = budget
        items["分配余量"] = round(budget * (1 - total), -2)

        # 缓冲占比（关键指标：试错资金够不够）
        buffer_ratio = ratios.get("试错缓冲", 0)
        buffer_status = "充足" if buffer_ratio >= 0.2 else ("紧张" if buffer_ratio >= 0.1 else "危险")

        return {
            "status": "OK",
            "budget": budget,
            "allocation": items,
            "buffer_ratio": round(buffer_ratio, 2),
            "buffer_status": buffer_status,
            "warning": "租金押金与设备为沉没成本，试错缓冲决定你能撑多久" if buffer_ratio < 0.2 else "试错缓冲充足",
        }

    # ============ 2. 单店经济框架 ============

    def simulate_unit_economics(self, avg_order_value, gross_margin, monthly_fixed_cost,
                                daily_order_low, daily_order_mid, daily_order_ideal,
                                days_per_month=30):
        """单店经济三场景模拟。
        输入假设区间（不是编数字），输出盈亏平衡点 + 三场景月利润。
        """
        results = {}
        scenarios = {
            "low": daily_order_low,
            "medium": daily_order_mid,
            "ideal": daily_order_ideal,
        }
        for name, daily_orders in scenarios.items():
            monthly_revenue = daily_orders * avg_order_value * days_per_month
            monthly_gross = monthly_revenue * gross_margin
            monthly_profit = monthly_gross - monthly_fixed_cost
            survival = "存活" if monthly_profit >= 0 else f"月亏 {-monthly_profit:.0f}元"
            results[name] = {
                "daily_orders": daily_orders,
                "monthly_revenue": round(monthly_revenue),
                "monthly_gross": round(monthly_gross),
                "monthly_fixed_cost": monthly_fixed_cost,
                "monthly_profit": round(monthly_profit),
                "status": survival,
            }

        # 盈亏平衡点（每日需要多少单）
        # 日单量 = 月固定成本 / 毛利率 / 客单价 / 天数
        if gross_margin > 0 and avg_order_value > 0:
            break_even_daily = monthly_fixed_cost / gross_margin / avg_order_value / days_per_month
        else:
            break_even_daily = None

        self.last_simulation = {
            "unit_economics": results,
            "break_even_daily_orders": round(break_even_daily, 1) if break_even_daily else None,
            "assumptions": {
                "avg_order_value": avg_order_value,
                "gross_margin": gross_margin,
                "monthly_fixed_cost": monthly_fixed_cost,
                "note": "假设区间来自行业基准+品类插件，非真实经营数据（E008 D级）",
            },
        }
        return self.last_simulation

    # ============ 3. 生存压力测试（现金流能撑多久）============

    def survival_pressure_test(self, investment_structure, monthly_fixed_cost, monthly_profit_by_scenario,
                               initial_cash_ratio=0.5):
        """现金流压力测试：启动资金里可动用的现金（缓冲+部分运营资金）
        在低/中/理想场景下分别能撑几个月。
        """
        # 可用现金 = 试错缓冲 + 首批物料运营（近似）
        alloc = investment_structure.get("allocation", {})
        usable_cash = alloc.get("试错缓冲", 0) + alloc.get("首批物料+运营", 0) * initial_cash_ratio

        months = {}
        for scenario, profit in monthly_profit_by_scenario.items():
            # 每月净流出 = 固定成本 - 毛利（负利润时）
            monthly_burn = monthly_fixed_cost - (monthly_profit_by_scenario[scenario] if scenario != "ideal" else 0)
            # 简化：理想场景接近自平衡
            if scenario == "ideal" and monthly_profit_by_scenario[scenario] > 0:
                months[scenario] = "无限（正现金流）"
            elif monthly_burn <= 0:
                months[scenario] = "无限（自平衡）"
            else:
                m = usable_cash / monthly_burn
                months[scenario] = f"{m:.1f}个月"
                if m < 3:
                    months[scenario] += " ⚠️ 危险（<3个月）"

        return {
            "usable_cash": round(usable_cash),
            "months_by_scenario": months,
            "warning": "若低场景撑不过3个月，需要降低固定成本或提高缓冲",
        }

    # ============ 4. Kill Criteria 前置 ============

    def define_kill_criteria(self, budget, max_monthly_loss=None, survival_months=3, financial_stop_ratio=0.5):
        """入场前定义止损线（Schema V2.0: kill_before_enter）"""
        max_loss = max_monthly_loss or budget * financial_stop_ratio / survival_months
        return {
            "financial_stop": f"连续亏损达预算{financial_stop_ratio:.0%}（{budget*financial_stop_ratio:.0f}元）即退出",
            "monthly_loss_limit": f"单月亏损超过 {max_loss:.0f} 元 → 触发复核",
            "survival_floor": f"现金低于 {survival_months} 个月运营成本 → 停止投入",
            "principle": "90天验证期不达标即退（不是硬撑到破产）",
        }

    # ============ 一站式 ============

    def run(self, budget, avg_order_value, gross_margin, monthly_fixed_cost,
            daily_orders=(30, 60, 100), model_preset="档口/小店"):
        """一站式模拟：投资结构 → 单店经济 → 生存压力 → Kill Criteria"""
        inv = self.simulate_investment_structure(budget, model_preset)
        ue = self.simulate_unit_economics(avg_order_value, gross_margin, monthly_fixed_cost,
                                          *daily_orders)
        survival = self.survival_pressure_test(inv, monthly_fixed_cost,
                                               {k: v["monthly_profit"] for k, v in ue["unit_economics"].items()})
        kill = self.define_kill_criteria(budget)
        return {
            "investment": inv,
            "unit_economics": ue,
            "survival": survival,
            "kill_criteria": kill,
        }


if __name__ == "__main__":
    print("=== Business Twin Engine V1.0 自检 ===")
    bt = BusinessTwinEngine()

    # 炸鸡场景（20万预算，档口模型）
    r = bt.run(
        budget=200000,
        avg_order_value=18,      # 15-20元价格带中点
        gross_margin=0.55,       # 餐饮毛利假设区间
        monthly_fixed_cost=15000, # 租金+人工+水电（档口简化）
        daily_orders=(30, 60, 100),
    )
    print("\n[投资结构]")
    for k, v in r["investment"]["allocation"].items():
        print(f"  {k}: {v}")
    print(f"  缓冲: {r['investment']['buffer_ratio']:.0%} ({r['investment']['buffer_status']})")

    print("\n[单店经济三场景]")
    for name, v in r["unit_economics"]["unit_economics"].items():
        print(f"  {name}: 日{ v['daily_orders']}单 → 月利{v['monthly_profit']}元 [{v['status']}]")
    print(f"  盈亏平衡日单量: {r['unit_economics']['break_even_daily_orders']}")

    print("\n[生存压力测试]")
    for k, v in r["survival"]["months_by_scenario"].items():
        print(f"  {k}: {v}")
    print(f"  可用现金: {r['survival']['usable_cash']}")

    print("\n[Kill Criteria]")
    for k, v in r["kill_criteria"].items():
        print(f"  {k}: {v}")
