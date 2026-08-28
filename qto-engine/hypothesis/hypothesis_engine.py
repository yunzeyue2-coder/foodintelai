#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hypothesis Engine-Lite
======================
青藤OS 假设驱动引擎（最小可运行版）

咨询和研究最大的分水岭：
  研究: 数据 → 洞察
  咨询: 问题 → 假设 → 验证 → 判断

本引擎管理假设对象的完整生命周期：
  proposed → testing → validated / rejected / uncertain

Hypothesis Schema:
{
  "id": "H001",
  "statement": "郑州炸鸡存在低成本进入窗口",
  "type": "market",           # market/competition/demand/business/risk
  "source": "FCS问题定义派生",
  "evidence_for": ["E001", "E003"],     # 支持证据
  "evidence_against": ["E007"],         # 反证（允许存在！）
  "status": "validated",                # proposed/testing/validated/rejected/uncertain
  "confidence": "B",                    # A/B/C/D
  "decision_effect": "support_entry"    # support_entry/support_avoid/neutral
}

关键纪律：
- 必须允许 evidence_against（反证）——否则只是"证明自己"
- 没有反证且状态永远是 validated 的假设系统是自欺
"""
import json, datetime

VALID_TYPES = ["market", "competition", "demand", "business", "risk"]
VALID_STATUS = ["proposed", "testing", "validated", "rejected", "uncertain"]
VALID_EFFECT = ["support_entry", "support_avoid", "neutral"]


class HypothesisEngine:
    def __init__(self, project_id, hypotheses=None):
        self.project_id = project_id
        self.hypotheses = hypotheses or {}

    # ---- 核心操作 ----
    def propose(self, hid, statement, htype="market", source="", decision_effect="neutral"):
        """提出新假设"""
        if hid in self.hypotheses:
            return False, f"假设 {hid} 已存在"
        self.hypotheses[hid] = {
            "id": hid,
            "statement": statement,
            "type": htype if htype in VALID_TYPES else "market",
            "source": source,
            "evidence_for": [],
            "evidence_against": [],
            "status": "proposed",
            "confidence": "C",
            "decision_effect": decision_effect if decision_effect in VALID_EFFECT else "neutral",
        }
        return True, f"假设 {hid} 已提出"

    def add_evidence(self, hid, evidence_id, support="for"):
        """绑定证据（for=支持 / against=反证）"""
        if hid not in self.hypotheses:
            return False, f"假设 {hid} 不存在"
        key = "evidence_for" if support == "for" else "evidence_against"
        if evidence_id not in self.hypotheses[hid][key]:
            self.hypotheses[hid][key].append(evidence_id)
        return True, f"{hid} 绑定证据 {evidence_id} ({support})"

    def update_status(self, hid, status, confidence=None):
        """更新假设状态（validated/rejected/uncertain）"""
        if hid not in self.hypotheses:
            return False, f"假设 {hid} 不存在"
        if status not in VALID_STATUS:
            return False, f"非法状态 {status}"
        h = self.hypotheses[hid]
        h["status"] = status
        if confidence:
            h["confidence"] = confidence
        h["updated"] = datetime.datetime.now().isoformat()
        return True, f"{hid} → {status} (置信度 {confidence or h['confidence']})"

    # ---- 验证逻辑 ----
    def evaluate(self, hid):
        """自动评估假设（基于证据 for/against 数量与等级）"""
        if hid not in self.hypotheses:
            return None
        h = self.hypotheses[hid]
        n_for = len(h["evidence_for"])
        n_against = len(h["evidence_against"])
        if n_for == 0 and n_against == 0:
            return {"verdict": "insufficient", "note": "无证据，无法评估"}
        ratio = n_for / (n_for + n_against)
        if n_against > 0 and n_for > 0:
            # 有正反证据：需要人工判断，标 uncertain
            return {"verdict": "uncertain", "note": f"正{n_for}/反{n_against}，存在冲突需人工判定", "ratio": round(ratio, 2)}
        if n_for > 0 and n_against == 0:
            return {"verdict": "supported", "note": f"{n_for}条支持证据，无反证", "ratio": 1.0}
        return {"verdict": "contradicted", "note": f"{n_against}条反证，无支持", "ratio": 0.0}

    def report(self):
        """输出假设审计报告（防止'证明自己'）"""
        lines = [f"=== 假设审计: {self.project_id} ==="]
        for hid, h in self.hypotheses.items():
            ev = self.evaluate(hid)
            lines.append(f"  {hid} [{h['status']}] {h['statement']}")
            lines.append(f"    支持: {h['evidence_for']} | 反证: {h['evidence_against']}")
            lines.append(f"    评估: {ev['verdict']} ({ev['note']}) 置信度{h['confidence']}")
        return "\n".join(lines)

    # ---- 自检 ----
    def self_test(self):
        """回归测试：完整假设生命周期 + 反证约束"""
        r = []
        r.append(self.propose("H001", "郑州炸鸡存在20-30元社区消费窗口", "market", "FCS", "support_entry"))
        r.append(self.add_evidence("H001", "E001", "for"))
        r.append(self.add_evidence("H001", "E003", "for"))
        r.append(self.add_evidence("H001", "E007", "against"))  # 关键：允许反证
        r.append(self.update_status("H001", "uncertain", "B"))
        ev = self.evaluate("H001")
        return r, ev


if __name__ == "__main__":
    eng = HypothesisEngine("FDR-ZZ-FRIED-001")
    results, ev = eng.self_test()
    print("=== Hypothesis Engine-Lite 自检 ===")
    for ok, msg in results:
        print(f"  {'✅' if ok else '❌'} {msg}")
    print(f"\nH001 评估: {ev['verdict']} — {ev['note']}")
    print("\n" + eng.report())
    print("\n✅ 反证约束验证: evidence_against 允许存在（不'证明自己'）")
