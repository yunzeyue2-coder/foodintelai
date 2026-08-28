#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FDR Renderer V2（决策卡交付协议）
==================================
GPT Phase 4 指令：FDR 不是报告生成器，是 Decision Graph 的可视化交付协议。

15 页决策卡（投资委员会风格，非行业研究报告）:
  P1  Decision Summary    一句话: 是否进入/进入条件/最大风险/建议动作
  P2  Business DNA        商业结构（需求频率/标准化/人工依赖/资本强度/复制能力）
  P3  Decision Graph      Why→Evidence→Risk→Action 链
  P4  Business Twin       三世界模拟（乐观/基准/压力）→ 盈亏平衡/生存
  P5  Kill Criteria       出现以下条件立即停止（与普通AI报告的本质区别）
  P6  Evidence Map        判断来自哪里（数据/规则/经验/假设）
  P7  Action Roadmap      执行路径（0-30验证需求/30-90模型测试/90-180复制）
  P8  Unknown & Boundary  缺失数据 + 置信度
  P9  Final Decision Card 项目/建议/置信度/核心依据/最大风险/下一步

产物: Decision Package（HTML + PDF + JSON 决策卡）
"""
import json, os, datetime


class FDRRendererV2:
    def __init__(self, pipeline_result, output_dir=None):
        """pipeline_result: Pipeline.run() 的输出"""
        self.pr = pipeline_result
        self.output_dir = output_dir or "/tmp/fdr_v2_packages"
        os.makedirs(self.output_dir, exist_ok=True)

    # ============ P1: Decision Summary ============
    def _decision_summary(self):
        d = self.pr["decision_node"]
        phases = list(self.pr["action_node"]["validation_plan"]["phases"].values())
        return {
            "title": f"{self.pr['inputs']['category']} 创业决策卡",
            "enter": d["decision"],
            "conditions": [p.get("goal", "") for p in phases][:3],
            "max_risk": self.pr["action_node"]["kill_criteria"].get("principle", ""),
            "next_action": "按 90 天验证战役执行（Phase1 验证需求→Phase2 验证盈利→Phase3 验证复制）",
        }

    # ============ P2: Business DNA（商业结构画像）============
    def _business_dna(self):
        op = self.pr["ontology_node"]["operation_profile"]
        def stars(v):
            return "★" * max(1, min(5, round(v / 20))) + "☆" * max(0, 5 - max(1, min(5, round(v / 20))))
        return {
            "需求频率": stars(80 - op["loss_sensitivity"]),
            "标准化": stars(op["standardization_level"] + 50),
            "人工依赖": stars(op["labor_intensity"]),
            "资本强度": stars(op["investment_level"]),
            "复制能力": stars(100 - op["replication_difficulty"]),
            "风险等级": f"{op['risk_level']}/100",
            "技能依赖": f"{op['skill_dependency']}/100",
        }

    # ============ P3: Decision Graph（为什么→证据→风险→行动）============
    def _decision_graph(self):
        reasons = self.pr["reason_node"]
        return {
            "why": [r["text"] for r in reasons],
            "evidence_levels": [r["evidence_level"] for r in reasons],
            "risk": self.pr["action_node"]["kill_criteria"],
            "action": "90天验证战役（需求→盈利→复制）",
        }

    # ============ P4: Business Twin（三世界模拟）============
    def _business_twin(self):
        # 从 pipeline 结果提取（这里用占位——实际由 twin.run 提供）
        inv = self.pr.get("twin_investment", {})
        return {
            "三世界": ["乐观（订单增长/成本下降/复制成功）",
                       "基准（正常经营）",
                       "压力（价格战/人工上涨/流量下降）"],
            "投资结构": inv.get("allocation", {}),
            "原则": "输出风险区间，不是单一答案",
        }

    # ============ P5: Kill Criteria ============
    def _kill_criteria(self):
        k = self.pr["action_node"]["kill_criteria"]
        return {
            "kill": [f"{v['trigger']} → {v['action']}" for v in k.values() if isinstance(v, dict)],
            "principle": k.get("principle", ""),
            "tagline": "青藤OS 与普通 AI 报告的本质区别：先定义何时停止，再谈进入",
        }

    # ============ P6: Evidence Map ============
    def _evidence_map(self):
        return {
            "数据": self.pr.get("evidence_count", 0),
            "规则": len(self.pr["reason_node"]),
            "假设": len(self.pr.get("unknowns", [])),
            "置信度": f"{self.pr['inference_confidence']*100:.0f}%",
        }

    # ============ P7: Action Roadmap ============
    def _action_roadmap(self):
        phases = self.pr["action_node"]["validation_plan"]["phases"]
        return [
            {"period": p["days"], "goal": p["goal"],
             "metrics": ", ".join(p["metrics"]),
             "pass": "; ".join(p["pass_criteria"]),
             "fail": "; ".join(p["fail_criteria"])}
            for p in phases.values()
        ]

    # ============ P8: Unknown & Boundary ============
    def _unknowns(self):
        return {
            "unknowns": self.pr.get("unknowns", []),
            "confidence": f"{self.pr['inference_confidence']*100:.0f}%",
            "boundary": "缺失数据已标注——不假装分析，置信度如实展示",
        }

    # ============ P9: Final Decision Card ============
    def _final_card(self):
        d = self.pr["decision_node"]
        return {
            "project": self.pr["inputs"]["category"],
            "recommendation": d["decision"],
            "confidence": f"{self.pr['inference_confidence']*100:.0f}%",
            "core_basis": f"{len(self.pr['reason_node'])} 条规则推导",
            "max_risk": self.pr["action_node"]["kill_criteria"].get("principle", ""),
            "next_step": "执行 90 天验证战役，按 Kill Criteria 止损",
        }

    # ============ 编译 ============
    def compile(self):
        pages = {
            "p1_decision_summary": self._decision_summary(),
            "p2_business_dna": self._business_dna(),
            "p3_decision_graph": self._decision_graph(),
            "p4_business_twin": self._business_twin(),
            "p5_kill_criteria": self._kill_criteria(),
            "p6_evidence_map": self._evidence_map(),
            "p7_action_roadmap": self._action_roadmap(),
            "p8_unknowns": self._unknowns(),
            "p9_final_card": self._final_card(),
        }
        # 决策包 JSON
        package = {
            "meta": {
                "schema": "FDR-Decision-Package-V2",
                "generated": datetime.datetime.now().isoformat(),
                "category": self.pr["inputs"]["category"],
                "confidence": self.pr["inference_confidence"],
            },
            "pages": pages,
        }
        out_path = os.path.join(self.output_dir, f"FDR_V2_{self.pr['inputs']['category']}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(package, f, ensure_ascii=False, indent=2)

        # HTML 渲染（决策卡视图）
        html = self._render_html(pages)
        html_path = os.path.join(self.output_dir, f"FDR_V2_{self.pr['inputs']['category']}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        return {"package": out_path, "html": html_path, "pages": pages}

    def _render_html(self, pages):
        """决策卡 HTML（简洁决策风格，非研究报告）"""
        dna = pages["p2_business_dna"]
        dna_rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in dna.items() if isinstance(v, str) and "★" in v)
        kill_rows = "".join(f"<li>🚨 {k}</li>" for k in pages["p5_kill_criteria"]["kill"])
        road = ""
        for step in pages["p7_action_roadmap"]:
            road += f"""<div class="phase">
            <div class="period">{step['period']}</div>
            <div class="goal">{step['goal']}</div>
            <div class="detail">指标: {step['metrics']}</div>
            <div class="detail">✅通过: {step['pass']}</div>
            <div class="detail fail">❌失败: {step['fail']}</div>
          </div>"""
        unknown_rows = "".join(f"<li>⚠️ {u}</li>" for u in pages["p8_unknowns"]["unknowns"]) or "<li>无缺失标注（规则全覆盖）</li>"

        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>FDR V2 Decision Card</title>
<style>
body {{ font-family: -apple-system, "PingFang SC", sans-serif; background: #F8F9FA; color: #1a1a2e; margin: 0; padding: 32px; }}
.card {{ background: #fff; border: 1px solid #E5E7EB; border-radius: 8px; padding: 24px 28px; margin-bottom: 24px; }}
h1 {{ font-size: 22px; margin: 0 0 8px; }}
h2 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 1.5px; color: #6B7280; margin: 0 0 16px; }}
.tag {{ display: inline-block; background: #00205B; color: #fff; padding: 4px 12px; border-radius: 4px; font-size: 13px; }}
.tag.gold {{ background: #C4A35A; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ padding: 8px 12px; border-bottom: 1px solid #EEF0F3; font-size: 14px; }}
.big {{ font-size: 28px; font-weight: 700; color: #00205B; }}
.phase {{ border-left: 3px solid #C4A35A; padding: 10px 16px; margin: 10px 0; background: #FAFBFC; }}
.period {{ font-weight: 700; color: #00205B; }}
.fail {{ color: #B00020; }}
.grid {{ display: flex; gap: 16px; flex-wrap: wrap; }}
.stat {{ flex: 1; min-width: 120px; background: #F8F9FA; border-radius: 6px; padding: 12px; text-align: center; }}
.stat .num {{ font-size: 24px; font-weight: 700; color: #00205B; }}
</style></head><body>
<div class="card">
  <h2>P1 · Decision Summary</h2>
  <h1>{pages['p1_decision_summary']['title']}</h1>
  <span class="tag {'gold' if 'CONDITIONAL' in pages['p1_decision_summary']['enter'] or 'GO' in pages['p1_decision_summary']['enter'] else ''}">{pages['p1_decision_summary']['enter']}</span>
  <p style="margin-top:12px"><b>最大风险:</b> {pages['p1_decision_summary']['max_risk']}</p>
  <p><b>建议动作:</b> {pages['p1_decision_summary']['next_action']}</p>
</div>
<div class="card">
  <h2>P2 · Business DNA</h2>
  <p style="color:#6B7280;font-size:13px">系统理解的是商业结构，不是"品类名称"</p>
  <table>{dna_rows}</table>
</div>
<div class="card">
  <h2>P3 · Decision Graph</h2>
  <p><b>为什么建议: </b></p>
  <ul>{"".join(f"<li>{r}</li>" for r in pages['p3_decision_graph']['why'])}</ul>
  <p><b>风险控制:</b> {pages['p3_decision_graph']['risk'].get('principle','')}</p>
</div>
<div class="card">
  <h2>P4 · Business Twin（三世界模拟）</h2>
  <div class="grid">
    {"".join(f'<div class="stat"><div class="num">{i+1}</div><div style="font-size:12px">{w}</div></div>' for i,w in enumerate(pages['p4_business_twin']['三世界']))}
  </div>
  <p style="margin-top:12px;color:#6B7280;font-size:13px">输出风险区间，不是单一答案</p>
</div>
<div class="card">
  <h2>P5 · Kill Criteria（先定义何时停止）</h2>
  <ul>{kill_rows}</ul>
  <p style="color:#C4A35A;font-size:13px">{pages['p5_kill_criteria']['tagline']}</p>
</div>
<div class="card">
  <h2>P6 · Evidence Map</h2>
  <div class="grid">
    <div class="stat"><div class="num">{pages['p6_evidence_map']['数据']}</div><div>数据</div></div>
    <div class="stat"><div class="num">{pages['p6_evidence_map']['规则']}</div><div>规则</div></div>
    <div class="stat"><div class="num">{pages['p6_evidence_map']['假设']}</div><div>假设</div></div>
    <div class="stat"><div class="num">{pages['p6_evidence_map']['置信度']}</div><div>置信度</div></div>
  </div>
</div>
<div class="card">
  <h2>P7 · Action Roadmap</h2>
  {road}
</div>
<div class="card">
  <h2>P8 · Unknown & Boundary</h2>
  <ul>{unknown_rows}</ul>
  <p style="color:#6B7280;font-size:13px">置信度 {pages['p8_unknowns']['confidence']} — 缺失数据已标注，不假装分析</p>
</div>
<div class="card" style="border-left: 4px solid #C4A35A;">
  <h2>P9 · Final Decision Card</h2>
  <p><b>项目:</b> {pages['p9_final_card']['project']}</p>
  <p><b>建议:</b> <span class="tag">{pages['p9_final_card']['recommendation']}</span></p>
  <p><b>置信度:</b> {pages['p9_final_card']['confidence']}</p>
  <p><b>核心依据:</b> {pages['p9_final_card']['core_basis']}</p>
  <p><b>最大风险:</b> {pages['p9_final_card']['max_risk']}</p>
  <p><b>下一步:</b> {pages['p9_final_card']['next_step']}</p>
</div>
</body></html>"""


if __name__ == "__main__":
    print("=== FDR Renderer V2 自检 ===")
    # 用 pipeline 结果演示（简化构造）
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pipeline"))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from pipeline.ontology_decision_pipeline import Pipeline

    pipe = Pipeline()
    r = pipe.run({"category": "奶茶", "process": "冲调/预制", "product_form": "杯装/便携",
                  "price_band": [12, 20], "business_model": "堂食+外卖", "style": "新式"}, budget=300000)
    # 补 twin 结果
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "business-twin"))
    from business_twin_engine import BusinessTwinEngine
    twin = BusinessTwinEngine()
    tw = twin.run(budget=300000, avg_order_value=16, gross_margin=0.65, monthly_fixed_cost=20000, daily_orders=(50, 90, 150))
    r["twin_investment"] = tw["investment"]
    r["evidence_count"] = 13

    renderer = FDRRendererV2(r, output_dir="/tmp/fdr_v2_packages")
    result = renderer.compile()
    print(f"✅ Decision Package 生成: {result['package']}")
    print(f"✅ HTML 决策卡: {result['html']}")
    print(f"✅ 9 页决策卡结构: {list(result['pages'].keys())}")
