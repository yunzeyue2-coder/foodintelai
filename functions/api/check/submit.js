// POST /api/check/submit — 收集极速开店体检数据
export async function onRequest(context) {
  const { request, env } = context;
  
  // 只接受POST
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ ok: false, msg: '仅支持POST' }), {
      status: 405, headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const body = await request.json();
    
    // 补充服务端信息
    const record = {
      ...body,
      ts: Date.now(),
      date: new Date().toISOString(),
      cf: request.cf?.country || 'unknown',
      ua: request.headers.get('User-Agent')?.slice(0, 80) || ''
    };

    // 1. 尝试写入KV（如果已绑定CHECK_DATA命名空间）
    if (env && env.CHECK_DATA) {
      const key = `check_${Date.now()}`;
      await env.CHECK_DATA.put(key, JSON.stringify(record), {
        expirationTtl: 86400 * 90  // 保留90天
      });
      // 维护最近100条索引
      const indexKey = 'check_recent';
      const raw = await env.CHECK_DATA.get(indexKey);
      const recent = raw ? JSON.parse(raw) : [];
      recent.unshift(key);
      if (recent.length > 100) recent.pop();
      await env.CHECK_DATA.put(indexKey, JSON.stringify(recent));
    }

    // 2. 总是打日志（Cloudflare控制台可见）
    console.log('CHECK_DATA:', JSON.stringify(record));

    return new Response(JSON.stringify({ ok: true }), {
      status: 200, headers: { 'Content-Type': 'application/json' }
    });
  } catch (e) {
    console.error('CHECK_DATA_ERROR:', e.message);
    return new Response(JSON.stringify({ ok: false, msg: e.message }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }
}
