// GET /api/check/data — 查看收集的体检数据
export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const limit = parseInt(url.searchParams.get('limit') || '20');
  
  // 尝试从KV获取
  if (env && env.CHECK_DATA) {
    const raw = await env.CHECK_DATA.get('check_recent');
    if (raw) {
      const keys = JSON.parse(raw).slice(0, limit);
      const records = [];
      for (const key of keys) {
        const val = await env.CHECK_DATA.get(key);
        if (val) records.push(JSON.parse(val));
      }
      return Response.json({ ok: true, total: records.length, records, kv: true });
    }
  }

  // 无KV时返回空
  return Response.json({
    ok: true,
    total: 0,
    records: [],
    kv: false,
    note: 'KV未绑定，请在Cloudflare Pages > 设置 > KV命名空间绑定中添加 CHECK_DATA'
  });
}
