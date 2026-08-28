#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Registry（模型注册中心）
==============================
青藤OS 模型治理的执行层：版本管理 / 参数记录 / 预测记录 / 回测入口。

作用（GPT 审计 D-003 落地）:
- 模型可以解释（Model Card 已做）
- 现在：模型可以被验证（注册预测 → 等待真实结果 → 回测）

回测流程:
1. 注册模型预测（predict）
2. 真实结果落地（record_outcome）
3. 回测（backtest）：比较预测 vs 实际，输出偏差
"""
import json, datetime, os


class ModelRegistry:
    def __init__(self, registry_path=None):
        self.registry_path = registry_path
        self.models = {}          # model_id -> model card
        self.predictions = []     # 预测记录（待回测）
        self.outcomes = {}        # 预测ID -> 真实结果

    # ---- 注册模型 ----
    def register(self, model_id, name, version, params, input_schema, output_schema,
                 limitations="", evidence_status=""):
        """注册模型（含参数与Schema）"""
        self.models[model_id] = {
            "model_id": model_id, "name": name, "version": version,
            "params": params, "input_schema": input_schema, "output_schema": output_schema,
            "limitations": limitations, "evidence_status": evidence_status,
            "registered": datetime.datetime.now().isoformat(),
            "predictions": 0, "backtests": 0,
        }
        return True, f"模型 {model_id} v{version} 已注册"

    # ---- 预测记录 ----
    def predict(self, model_id, project_id, inputs, prediction, confidence="C"):
        """记录一次预测（等待真实结果回测）"""
        if model_id not in self.models:
            return False, f"模型 {model_id} 未注册"
        pid = f"{model_id}-{project_id}-{len(self.predictions)+1}"
        self.predictions.append({
            "prediction_id": pid, "model_id": model_id, "project_id": project_id,
            "inputs": inputs, "prediction": prediction, "confidence": confidence,
            "predicted_at": datetime.datetime.now().isoformat(),
            "outcome": None,
        })
        self.models[model_id]["predictions"] += 1
        return True, f"预测 {pid} 已记录（等待回测）"

    # ---- 结果落地 ----
    def record_outcome(self, prediction_id, actual, actual_at=None):
        """真实结果落地"""
        for p in self.predictions:
            if p["prediction_id"] == prediction_id:
                p["outcome"] = actual
                p["actual_at"] = actual_at or datetime.datetime.now().isoformat()
                return True, f"结果已落地: {prediction_id} 实际={actual}"
        return False, f"预测 {prediction_id} 不存在"

    # ---- 回测 ----
    def backtest(self, model_id=None):
        """回测：比较预测 vs 实际"""
        results = []
        for p in self.predictions:
            if model_id and p["model_id"] != model_id:
                continue
            if p["outcome"] is None:
                continue
            # 预测 vs 实际偏差
            pred = p["prediction"]
            actual = p["outcome"]
            if isinstance(pred, (int, float)) and isinstance(actual, (int, float)):
                err = round(abs(pred - actual) / actual * 100, 1) if actual else None
            else:
                err = None  # 分类型：匹配/不匹配
            hit = pred == actual if not isinstance(pred, (int, float)) else (err is not None and err <= 15)
            results.append({
                "prediction_id": p["prediction_id"], "model": p["model_id"],
                "pred": pred, "actual": actual, "error_pct": err, "hit": hit,
            })
            if p["model_id"] in self.models:
                self.models[p["model_id"]]["backtests"] += 1
        return results

    def backtest_summary(self):
        """回测汇总（按模型）"""
        results = self.backtest()
        by_model = {}
        for r in results:
            by_model.setdefault(r["model"], []).append(r)
        lines = []
        for mid, rs in by_model.items():
            hits = sum(1 for r in rs if r["hit"])
            lines.append(f"  {mid}: {hits}/{len(rs)} 命中 ({round(hits/len(rs)*100)}%)")
        return "\n".join(lines) if lines else "  （暂无回测数据）"

    # ---- 持久化 ----
    def to_json(self, path=None):
        d = {"models": self.models, "predictions": self.predictions}
        s = json.dumps(d, ensure_ascii=False, indent=2)
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(s)
        return s

    def self_test(self):
        """回归测试：注册→预测→结果→回测 全流程"""
        r = ModelRegistry()
        r.register("FDE-V0.3", "FDE决策评分", "V0.3",
                   {"weights": {"market": 0.25, "competition": 0.20, "operation": 0.20, "resource": 0.25, "timing": 0.10}},
                   ["行业五维"], ["decision_score", "R等级"])
        r.predict("FDE-V0.3", "FDR-ZZ-FRIED-001", {"industry": 78, "personal": 70}, 76, "B")
        r.record_outcome("FDE-V0.3-FDR-ZZ-FRIED-001-1", 80)  # 假设实际项目结果80
        r.predict("FDE-V0.3", "FDR-ZZ-TEST-002", {"industry": 60, "personal": 55}, 58, "B")
        r.record_outcome("FDE-V0.3-FDR-ZZ-TEST-002-2", 61)
        return r


if __name__ == "__main__":
    reg = ModelRegistry().self_test()
    print("=== Model Registry 自检 ===")
    for mid, m in reg.models.items():
        print(f"  📦 {mid} v{m['version']} | 参数: {list(m['params'].keys())} | 预测{m['predictions']}次")
    print("\n=== 回测结果 ===")
    for r in reg.backtest():
        hit = "✅" if r["hit"] else "❌"
        print(f"  {hit} {r['prediction_id']}: 预测{r['pred']} vs 实际{r['actual']} (偏差{r['error_pct']}%)")
    print("\n回测汇总:")
    print(reg.backtest_summary())
    print("\n✅ Model Registry: 版本/参数/预测/回测全流程可用")
