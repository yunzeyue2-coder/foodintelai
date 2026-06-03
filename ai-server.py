#!/usr/bin/env python3
"""AI 问答 API Server — 本地版"""
import json, os, http.server, urllib.request

DEEPSEEK_KEY = "sk-ff7f67875649458cb8336e81502f1915"
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
CARDS_JSON = "cards-data.json"
PORT = 8766

SYSTEM_PROMPT = """你是「沧林食品工作站」的AI助手，由20年酱卤实战经验的食品工程师「沧林」创立。

你的定位：帮摆摊 / 开店 / 做工厂的人快速找到产品方案。

知识库：覆盖1049张产品卡，分12个门店品类 + 大量摆摊单品。

回答规则：
1. 简洁务实，做食品的人没时间看废话
2. 根据问题推荐适合的场景（摆摊/门店/工厂）
3. 诚实——不知道就说不知道，不编配方
4. 语气像老师傅聊天，专业但不学术
5. 给出具体品类/产品建议"""

def load_card_context():
    try:
        with open(CARDS_JSON, 'r') as f:
            data = json.load(f)
        by_cat = {}
        for cid, card in data.items():
            cat = card.get('category', '其他')
            by_cat.setdefault(cat, []).append(cid)
        lines = []
        for cat, items in sorted(by_cat.items(), key=lambda x: -len(x[1])):
            samples = ", ".join(items[:5])
            lines.append("  %s (%d个): %s%s" % (cat, len(items), samples, "..." if len(items) > 5 else ""))
        return "\n".join(lines)
    except:
        return "（卡片索引加载失败）"

def ask_ai(question):
    card_context = load_card_context()
    system = SYSTEM_PROMPT + "\n\n当前知识库品类分布：\n" + card_context
    
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": question}
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
    }).encode()
    
    req = urllib.request.Request(DEEPSEEK_URL, data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + DEEPSEEK_KEY,
        })
    
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]

class AIHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        question = body.get("question", "").strip()
        if not question:
            self._json({"error": "请输入问题"}, 400)
            return
        try:
            answer = ask_ai(question)
            self._json({"answer": answer})
        except Exception as e:
            self._json({"error": "服务暂时不可用"}, 500)
    
    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), AIHandler)
    print("AI API Server running on http://0.0.0.0:%d" % PORT)
    print("Test: curl -X POST http://localhost:%d/ask -H 'Content-Type: application/json' -d '{\"question\":\"摆摊卖卤鸡爪要准备什么\"}'" % PORT)
    server.serve_forever()
