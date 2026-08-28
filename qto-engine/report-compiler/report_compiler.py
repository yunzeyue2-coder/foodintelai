#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Compiler（报告编译闭环）
===============================
让最后链路闭合：
  旧: JSON → 人工生成PDF
  新: Decision Object → Report JSON → FQA → PDF → Delivery Package

步骤:
  1. ingest: 读取 REPORT JSON（含 decision_memo/executive_summary）
  2. fqa: 跑 FQA 质量闸（score<75 拒绝编译）
  3. render: 生成 HTML（复用 fdr_render_v2）
  4. pdf: Playwright 转 PDF
  5. package: 生成 Delivery Package（PDF + 摘要 + 数据源 + 模型分 + 更新记录）

产物 6 件套:
  FDR_XX.pdf / summary.md / action_page.md / sources.md / model_scores.md / update_log.md
"""
import json, os, subprocess, datetime, shutil


class ReportCompiler:
    def __init__(self, render_script="/tmp/fdr_render_v2.py", output_dir=None):
        self.render_script = render_script
        self.output_dir = output_dir or "/tmp/fdr_delivery"

    # ---- 1. 校验 FQA ----
    def check_fqa(self, report_path, min_score=75):
        """跑 FQA，质量闸"""
        try:
            import sys
            sys.path.insert(0, os.path.dirname(self.render_script) if os.path.dirname(self.render_script) else "/tmp")
            from fqa_check import main as fqa_main
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                score, issues = fqa_main(report_path)
            ok = score >= min_score
            return ok, score, issues, buf.getvalue()
        except Exception as e:
            return False, 0, -1, f"FQA 运行失败: {e}"

    # ---- 2. 渲染 ----
    def render_html(self, report_path):
        """渲染 HTML（复用渲染脚本）"""
        r = subprocess.run(["python3", self.render_script], capture_output=True, text=True, timeout=120)
        return r.returncode == 0, r.stdout, r.stderr

    # ---- 3. PDF ----
    def render_pdf(self, html_path, pdf_path):
        script = f'''
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("file://{html_path}", wait_until="networkidle")
        await page.pdf(path="{pdf_path}", prefer_css_page_size=True,
                       print_background=True, margin={{"top": "0", "bottom": "0", "left": "0", "right": "0"}})
        await browser.close()
        print("PDF done")
asyncio.run(main())
'''
        r = subprocess.run(["python3", "-c", script], capture_output=True, text=True, timeout=180)
        return r.returncode == 0 and os.path.exists(pdf_path), r.stdout, r.stderr

    # ---- 4. Delivery Package ----
    def build_package(self, report, pdf_path, out_dir):
        """生成 6 件套"""
        os.makedirs(out_dir, exist_ok=True)
        rid = report["report_metadata"]["report_id"]
        ver = report["report_metadata"]["version"]
        # PDF
        pdf_dst = os.path.join(out_dir, f"{rid}_{ver}.pdf")
        shutil.copy(pdf_path, pdf_dst)
        # Summary
        with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as f:
            f.write(f"# {rid} {ver} 摘要\n\n{report.get('executive_summary', {}).get('headline', '')}\n")
            for k in report.get('executive_summary', {}).get('key_findings', []):
                f.write(f"- {k}\n")
            f.write(f"\n**决策**: {report['decision_memo']['decision']}\n")
            f.write(f"**方向**: {report['decision_memo']['recommended_direction']}\n")
        # Action page
        with open(os.path.join(out_dir, "action_page.md"), "w", encoding="utf-8") as f:
            f.write(f"# {rid} 行动页\n\n")
            for a in report.get("action_layer", []):
                f.write(f"## {a.get('period', '')} {a.get('goal', '')}\n")
                for task in a.get("tasks", []):
                    f.write(f"- {task}\n")
        # Sources
        with open(os.path.join(out_dir, "sources.md"), "w", encoding="utf-8") as f:
            f.write(f"# {rid} 数据源\n\n")
            for eid, e in report.get("evidence_layer", {}).items():
                f.write(f"- {eid}: {e.get('metric', '')} | 来源:{e.get('source', '')} | 等级:{e.get('evidence_status', '')} | 置信度:{e.get('confidence', '')}\n")
        # Model scores
        with open(os.path.join(out_dir, "model_scores.md"), "w", encoding="utf-8") as f:
            f.write(f"# {rid} 模型分\n\n")
            s = report.get("score_engine", {}).get("score", {})
            f.write(f"- FDE-V0.3: 行业{s.get('industry_score')} / 个人{s.get('personal_match')} / 综合{s.get('decision_score')} / {s.get('r_level')}\n")
        # Update log
        with open(os.path.join(out_dir, "update_log.md"), "w", encoding="utf-8") as f:
            f.write(f"# {rid} 更新记录\n\n")
            for u in report.get("update_policy", {}).get("items", []):
                f.write(f"- {u}\n")
            f.write(f"\n*生成时间: {datetime.datetime.now().isoformat()}*\n")
        return pdf_dst, os.listdir(out_dir)

    # ---- 全流程 ----
    def compile(self, report_path, html_path=None, pdf_path=None, out_dir=None):
        """完整编译：FQA → HTML → PDF → Package"""
        print("=== Report Compiler ===")
        # 1. FQA
        ok, score, issues, detail = self.check_fqa(report_path)
        print(f"[1/4] FQA: {'✅' if ok else '❌'} score={score} (≥75)")
        if not ok:
            print("  编译中止：质量闸未过")
            return {"status": "BLOCKED", "fqa_score": score, "issues": issues}
        # 2. HTML
        ok_html, out, err = self.render_html(report_path)
        print(f"[2/4] HTML: {'✅' if ok_html else '❌'} {out.strip()[:60]}")
        # 3. PDF
        html_path = html_path or "/tmp/fdr_zz_v2/FDR-ZZ-FRIED-001_V2.0.html"
        pdf_path = pdf_path or "/tmp/fdr_zz_v2/FDR-ZZ-FRIED-001_compiled.pdf"
        ok_pdf, out_pdf, err_pdf = self.render_pdf(html_path, pdf_path)
        print(f"[3/4] PDF: {'✅' if ok_pdf else '❌'} {out_pdf.strip()[:40]}")
        # 4. Package
        with open(report_path, encoding="utf-8") as f:
            report = json.load(f)
        out_dir = out_dir or os.path.join(self.output_dir, f"{report['report_metadata']['report_id']}_{report['report_metadata']['version']}")
        pdf_dst, files = self.build_package(report, pdf_path, out_dir)
        print(f"[4/4] Package: ✅ {len(files)} 件 → {out_dir}")
        return {"status": "COMPILED", "fqa_score": score, "package_dir": out_dir, "files": files}


if __name__ == "__main__":
    # 全流程编译测试
    compiler = ReportCompiler(render_script="/tmp/fdr_render_v2.py")
    result = compiler.compile("/tmp/FDR-ZZ-FRIED-001_REPORT_JSON_V2.1.json")
    if result["status"] == "COMPILED":
        print("\n✅ Report Compiler: JSON→FQA→HTML→PDF→6件套 全链路闭合")
