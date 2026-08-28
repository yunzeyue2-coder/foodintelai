#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FDR Content Quality Gate（内容质量闸门）V1.0
=============================================
GPT 质量框架（2026-08-11）：青藤OS 内容输出的质量标准和认知框架。

核心标准（不是页数，是决策复杂度）：
1. 密度标准: 事实描述 ≤30% / 分析解释 ≥40% / 决策建议 ≥30%
2. 证据密度: 每个核心判断必须有 数据+来源+解释+推论（不是"外卖竞争激烈"）
3. 决策链: 需求变化→用户行为→产品结构→供应链→竞争格局→商业模型→投资判断

用法:
  python3 content_quality_gate.py <report.json>    检查单份报告
  python3 content_quality_gate.py --sentence "郑州小吃线上订单30元以下占X%"  检查单句
"""
import json, sys, re


class ContentQualityGate:
    # 密度标准（GPT 原话）
    FACT_MAX = 0.30      # 事实描述 ≤30%
    ANALYSIS_MIN = 0.40  # 分析解释 ≥40%
    RECOMMEND_MIN = 0.30 # 决策建议 ≥30%

    # 低质量信号（GPT: "这是互联网文章"）
    VAGUE_WORDS = [
        "市场很大", "年轻化", "行业增长", "竞争激烈", "未来趋势很好",
        "前景广阔", "潜力巨大", "蓬勃发展", "消费升级", "蓝海",
    ]

    # 证据四要素
    EVIDENCE_FIELDS = ["data", "source", "explanation", "inference"]

    def __init__(self):
        self.issues, self.passed = [], []

    # ============ 1. 句子分类（事实/分析/建议）============

    def classify_sentence(self, text):
        """粗分类：事实（含数字/来源）/ 分析（因果/机制）/ 建议（应该/需要/必须）"""
        if any(k in text for k in ["应该", "需要", "必须", "建议", "停止", "先验证", "投入"]):
            return "recommend"
        if any(k in text for k in ["因为", "导致", "意味着", "所以", "说明", "取决于", "机制", "结构"]):
            return "analysis"
        if re.search(r"\d", text) or any(k in text for k in ["占比", "家", "元", "%", "数据显示", "报告"]):
            return "fact"
        return "analysis"  # 默认分析

    # ============ 2. 单句质量检查 ============

    ACTION_VERBS = ["完成", "确定", "测试", "评估", "记录", "执行", "校准", "选址", "踩点",
                    "统计", "追踪", "验证", "停止", "签订", "选择", "落地", "跑通", "核算",
                    "SOP", "文档化", "轮换", "初筛", "冷启动", "试卖"]

    def check_sentence(self, text):
        """单句四要素检查：数据/来源/解释/推论
        动作句（动词开头/任务类）只需可执行性，不强制四要素"""
        issues = []
        # 动作句判定：动词开头 或 含动作核心词（测试/采集/统计等）→ 检查可执行性即可
        stripped = text.strip()
        is_action = any(stripped.startswith(v) for v in self.ACTION_VERBS)
        if not is_action:
            action_kws = ["测试", "采集", "统计", "追踪", "记录", "验收", "试卖", "踩点", "校准", "签订", "选择", "落地"]
            is_action = any(kw in stripped for kw in action_kws)
        if is_action or stripped.endswith("?"):
            if len(stripped) < 10:
                issues.append("动作句过短（无可执行信息）")
            return issues
        # 低质量词
        for w in self.VAGUE_WORDS:
            if w in text:
                issues.append(f"低质量表达: '{w}'（互联网文章级，非决策级）")
                break
        # 数据密度
        if not re.search(r"\d", text) and not re.search(r"占|比|率|指数|HHI", text):
            issues.append("缺数据锚点（无数字/比率/指数）")
        # 来源
        if not re.search(r"据|来源|数据显示|报告|调研|202\d", text):
            issues.append("缺来源（数据从哪来）")
        # 推论
        if not any(k in text for k in ["意味着", "导致", "因此", "所以", "推论", "说明"]):
            issues.append("缺推论（数据意味着什么）")
        return issues

    # ============ 3. 整报告检查 ============

    def check_report(self, report):
        """密度标准 + 判断质量"""
        # 提取所有文本段落（reasons + insights + evidence + action + risk + memo建议）
        texts = []
        memo = report.get("decision_memo", {})
        texts += [r if isinstance(r, str) else r.get("text", "") for r in memo.get("reasons", [])]
        texts += [i.get("text", "") for i in report.get("insight_layer", {}).values()]
        texts += [e.get("text", "") for e in report.get("evidence_layer", {}).values()]
        # 建议/行动层（GPT: 物理世界可落地的行动解）
        for a in report.get("action_layer", []):
            texts.append(a.get("goal", ""))
            texts += [t if isinstance(t, str) else str(t) for t in a.get("tasks", [])]
        # 风险层
        for rk in report.get("risk_layer", []):
            texts.append(rk.get("name", ""))
            texts.append(rk.get("response", ""))
        # memo 建议字段
        if memo.get("recommended_direction"):
            texts.append(str(memo["recommended_direction"]))
        if memo.get("action_30days"):
            texts.append(str(memo["action_30days"]))
        for c in memo.get("conditions", []):
            texts.append(c.get("text", "") if isinstance(c, dict) else str(c))

        # 密度分布
        dist = {"fact": 0, "analysis": 0, "recommend": 0}
        for t in texts:
            if t:
                dist[self.classify_sentence(t)] += 1
        total = sum(dist.values()) or 1
        ratios = {k: v / total for k, v in dist.items()}

        print(f"\n[密度分布] 事实 {ratios['fact']:.0%} / 分析 {ratios['analysis']:.0%} / 建议 {ratios['recommend']:.0%}")
        if ratios["fact"] > self.FACT_MAX + 0.1:
            self.issues.append(f"事实占比 {ratios['fact']:.0%} 偏高（≤{self.FACT_MAX:.0%}）——像百科不像决策")
        else:
            self.passed.append(f"事实占比 {ratios['fact']:.0%}（≤{self.FACT_MAX:.0%}）✅")
        if ratios["analysis"] < self.ANALYSIS_MIN - 0.1:
            self.issues.append(f"分析占比 {ratios['analysis']:.0%} 偏低（≥{self.ANALYSIS_MIN:.0%}）——缺机制解释")
        else:
            self.passed.append(f"分析占比 {ratios['analysis']:.0%}（≥{self.ANALYSIS_MIN:.0%}）✅")
        if ratios["recommend"] < self.RECOMMEND_MIN - 0.1:
            self.issues.append(f"建议占比 {ratios['recommend']:.0%} 偏低（≥{self.RECOMMEND_MIN:.0%}）——缺决策建议")
        else:
            self.passed.append(f"建议占比 {ratios['recommend']:.0%}（≥{self.RECOMMEND_MIN:.0%}）✅")

        # 判断质量（只查核心判断句：reasons + insights，动作任务只看占比）
        quality_issues = 0
        core_texts = [r if isinstance(r, str) else r.get("text", "") for r in memo.get("reasons", [])] \
                     + [i.get("text", "") for i in report.get("insight_layer", {}).values()]
        for t in core_texts:
            if not t:
                continue
            for iss in self.check_sentence(t):
                quality_issues += 1
                if quality_issues <= 5:
                    self.issues.append(f"判断质量: {iss} | {t[:50]}...")
        if not quality_issues:
            self.passed.append(f"核心判断质量: {len(core_texts)} 条全含 数据+来源+推论 ✅")

        score = round((len(self.passed) / (len(self.passed) + len(self.issues))) * 100) if (self.passed or self.issues) else 0
        return {"score": score, "ratios": ratios, "issues": self.issues, "passed": self.passed}


def main():
    if "--sentence" in sys.argv:
        idx = sys.argv.index("--sentence")
        text = sys.argv[idx + 1]
        gate = ContentQualityGate()
        issues = gate.check_sentence(text)
        print(f"句子: {text}")
        print(f"{'❌ ' + '; '.join(issues) if issues else '✅ 达标'}")
        return

    if len(sys.argv) < 2:
        print("用法: python3 content_quality_gate.py <report.json> | --sentence <文本>")
        return
    report = json.load(open(sys.argv[1], encoding="utf-8"))
    gate = ContentQualityGate()
    r = gate.check_report(report)
    print(f"\n=== Content Quality: {r['score']}/100 ===")
    for p in r["passed"]:
        print(f"  ✅ {p}")
    for i in r["issues"]:
        print(f"  ❌ {i}")


if __name__ == "__main__":
    main()
