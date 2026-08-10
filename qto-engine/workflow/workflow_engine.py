#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workflow Engine-Lite
====================
青藤OS 生产流程状态机（最小可运行版）

作用：让系统知道"现在项目走到哪里"——每个咨询项目有一个 workflow_state，
     状态机约束合法流转，每一步记录 input/output/validator/next_step。

状态链:
01_PROJECT_DEFINED → 02_FRAMEWORK_READY → 03_DATA_READY → 04_ANALYSIS_RUNNING
→ 05_EVIDENCE_BOUND → 06_DECISION_GENERATED → 07_FQA_PASSED → 08_DELIVERED

用法:
  from workflow_engine import WorkflowEngine
  wf = WorkflowEngine.load("workflow_state.json")
  wf.advance(output={"artifact": "..."})   # 前进到下一步（校验通过才走）
  wf.state()                                # 查看当前状态
  wf.log()                                  # 查看流转日志
"""
import json, datetime, os

# ---- 状态定义 ----
STATES = [
    "01_PROJECT_DEFINED",      # Project Charter 已产出
    "02_FRAMEWORK_READY",      # FAS 分析框架已生成
    "03_DATA_READY",           # 数据已调用/清洗完成
    "04_ANALYSIS_RUNNING",     # 模型计算中
    "05_EVIDENCE_BOUND",       # 证据已绑定
    "06_DECISION_GENERATED",   # Decision Memo 已生成
    "07_FQA_PASSED",           # FQA 质量闸通过
    "08_DELIVERED",            # 已交付
]

# ---- 状态机转移表：state -> {required_output, validator, next} ----
# validator 可以是内置校验名（如 "has_evidence"）或 None（仅检查 output 存在）
TRANSITIONS = {
    "01_PROJECT_DEFINED": {
        "required_output": ["charter"],
        "validator": "has_charter",
        "next": "02_FRAMEWORK_READY",
    },
    "02_FRAMEWORK_READY": {
        "required_output": ["framework"],
        "validator": "has_framework",
        "next": "03_DATA_READY",
    },
    "03_DATA_READY": {
        "required_output": ["dataset"],
        "validator": "has_dataset",
        "next": "04_ANALYSIS_RUNNING",
    },
    "04_ANALYSIS_RUNNING": {
        "required_output": ["metrics"],
        "validator": "has_metrics",
        "next": "05_EVIDENCE_BOUND",
    },
    "05_EVIDENCE_BOUND": {
        "required_output": ["evidence"],
        "validator": "has_evidence",
        "next": "06_DECISION_GENERATED",
    },
    "06_DECISION_GENERATED": {
        "required_output": ["decision_memo"],
        "validator": "has_decision",
        "next": "07_FQA_PASSED",
    },
    "07_FQA_PASSED": {
        "required_output": ["fqa_report"],
        "validator": "fqa_passed",
        "next": "08_DELIVERED",
    },
    "08_DELIVERED": {
        "required_output": [],
        "validator": None,
        "next": None,
    },
}

# ---- 内置校验器 ----
VALIDATORS = {
    "has_charter": lambda o: isinstance(o.get("charter"), dict) and "decision_question" in o.get("charter", {}),
    "has_framework": lambda o: isinstance(o.get("framework"), dict) and len(o.get("framework", {})) > 0,
    "has_dataset": lambda o: o.get("dataset") is not None and str(o.get("dataset", "")).endswith((".csv", ".json")),
    "has_metrics": lambda o: isinstance(o.get("metrics"), dict) and len(o.get("metrics", {})) > 0,
    "has_evidence": lambda o: isinstance(o.get("evidence"), dict) and len(o.get("evidence", {})) > 0,
    "has_decision": lambda o: isinstance(o.get("decision_memo"), dict) and "decision" in o.get("decision_memo", {}),
    "fqa_passed": lambda o: isinstance(o.get("fqa_report"), dict) and o.get("fqa_report", {}).get("score", 0) >= 75,
}


class WorkflowEngine:
    def __init__(self, project_id, state=None, log=None):
        self.project_id = project_id
        self.state = state or STATES[0]
        self.log = log or []

    # ---- 加载/保存 ----
    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return cls(d["project_id"], d.get("state"), d.get("log", []))

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def to_dict(self):
        return {"project_id": self.project_id, "state": self.state, "log": self.log}

    # ---- 核心：前进 ----
    def advance(self, output=None):
        """尝试前进到下一步。output 必须满足当前状态的 validator。"""
        output = output or {}
        trans = TRANSITIONS.get(self.state)
        if not trans:
            return False, "已是终态 08_DELIVERED"

        # 1. 校验必需产物
        for req in trans["required_output"]:
            if req not in output:
                return False, f"缺必需产物: {req}"

        # 2. 跑校验器
        v = trans["validator"]
        if v:
            if not VALIDATORS[v](output):
                return False, f"校验失败: {v}"

        # 3. 流转
        old = self.state
        self.state = trans["next"]
        self.log.append({
            "from": old,
            "to": self.state,
            "timestamp": datetime.datetime.now().isoformat(),
            "output_keys": list(output.keys()),
            "validator": v,
        })
        return True, f"{old} → {self.state}"

    # ---- 安全：受限推进（防止死循环）----
    def run_to_terminal(self, output_provider, max_steps=20):
        """带步数上限的状态机推进。output_provider(state) -> output dict。
        失败或超限即停止并返回结果——咨询系统不允许无限重试。"""
        results = []
        step = 0
        while not self.is_terminal() and step < max_steps:
            out = output_provider(self.get_state()) or {}
            ok, msg = self.advance(out)
            results.append((self.get_state(), ok, msg))
            if not ok:
                break  # 校验失败：停止，不无限重试
            step += 1
        return results

    def get_state(self):
        return self.state

    def is_terminal(self):
        return self.state == "08_DELIVERED"

    def progress(self):
        """返回当前进度百分比"""
        idx = STATES.index(self.state) if self.state in STATES else 0
        return round(idx / (len(STATES) - 1) * 100)

    def log(self):
        return self.log

    # ---- 测试 ----
    def self_test(self):
        """回归测试：完整走一遍 8 步"""
        results = []
        step_outputs = {
            "01_PROJECT_DEFINED": {"charter": {"decision_question": "20万创业者在郑州进入炸鸡？"}},
            "02_FRAMEWORK_READY": {"framework": {"market": ["规模", "结构"]}},
            "03_DATA_READY": {"dataset": "label_table.csv"},
            "04_ANALYSIS_RUNNING": {"metrics": {"hhi": 2405.9}},
            "05_EVIDENCE_BOUND": {"evidence": {"E001": {}}},
            "06_DECISION_GENERATED": {"decision_memo": {"decision": "R2"}},
            "07_FQA_PASSED": {"fqa_report": {"score": 100}},
        }
        while not self.is_terminal():
            out = step_outputs.get(self.state, {})
            ok, msg = self.advance(out)
            results.append((self.state, ok, msg))
        return results


if __name__ == "__main__":
    # 自检
    wf = WorkflowEngine("SELF-TEST")
    results = wf.self_test()
    all_ok = all(ok for _, ok, _ in results)
    print("=== Workflow Engine-Lite 自检 ===")
    for state, ok, msg in results:
        print(f"  {'✅' if ok else '❌'} {state}: {msg}")
    print(f"\n自检结果: {'全部通过' if all_ok else '存在失败'}")
    print(f"最终状态: {wf.get_state()} | 进度: {wf.progress()}%")
