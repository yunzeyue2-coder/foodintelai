// 评分系统 · 产品卡验证评分
(async function(){
  try{
    const r = await fetch('../scores.json');
    const SCORES = await r.json();
    const id = window.location.pathname.split('/').pop().replace('.html','');
    const d = SCORES[id];
    if(!d || !d.s) return;

    const labels = ['市场热度','复购潜力','操作难度','利润空间','成本优势'];
    const colors = ['#E8652D','#07C160','#8B5CF6','#F59E0B','#3B82F6'];
    const avg = (d.s.reduce((a,b)=>a+b,0)/d.s.length).toFixed(1);
    const marginMap = {A:'高毛利 🟢',B:'中毛利 🟡',C:'低毛利 🔴'};
    const costMap = {low:'低成本 ✅',mid:'中成本',high:'高成本 ⚠️'};
    const riskMap = {low:'低风险 🟢',mid:'中风险 🟡',high:'高风险 🔴'};

    const stars = '★'.repeat(Math.round(avg/2)) + '☆'.repeat(Math.max(0,5-Math.round(avg/2)));

    let html = '<div style="margin:16px 24px;padding:16px 20px;background:#fff8f5;border:1px solid #f5e0d0;border-radius:12px">';
    html += `<div style="font-size:15px;color:#C0392B;margin-bottom:10px">${stars} <strong>综合 ${avg}/10</strong></div>`;
    html += '<div style="display:flex;flex-direction:column;gap:7px">';
    d.s.forEach((v,i)=>{
      const pct = v/10*100;
      html += `<div style="display:flex;align-items:center;gap:8px;font-size:12px">
        <span style="width:65px;flex-shrink:0;color:#7a7269">${labels[i]}</span>
        <div style="flex:1;height:6px;background:#f0e9e2;border-radius:3px;overflow:hidden">
          <div style="height:100%;width:${pct}%;background:${colors[i]};border-radius:3px;transition:width .4s"></div>
        </div>
        <span style="width:28px;text-align:right;font-weight:600;color:#3a322a">${v}/10</span>
      </div>`;
    });
    html += '</div>';
    html += '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">';
    if(marginMap[d.m]) html += `<span style="font-size:10px;padding:2px 8px;background:#f5ede5;border-radius:4px;color:#5a4f44">${marginMap[d.m]}</span>`;
    if(costMap[d.c]) html += `<span style="font-size:10px;padding:2px 8px;background:#f5ede5;border-radius:4px;color:#5a4f44">${costMap[d.c]}</span>`;
    if(riskMap[d.r]) html += `<span style="font-size:10px;padding:2px 8px;background:#f5ede5;border-radius:4px;color:#5a4f44">${riskMap[d.r]}</span>`;
    if(d.b && d.b.length){
      const sceneMap = {stall:'🛵摆摊',small_shop:'🏪门店',workshop:'🏭工坊'};
      html += `<div style="font-size:10px;color:#7a7269;margin-top:4px;width:100%">适合：${d.b.map(x=>sceneMap[x]||x).join(' · ')}</div>`;
    }
    html += '</div></div>';

    // Insert after story section
    const story = document.querySelector('.story') || document.querySelector('.card > :first-child');
    if(story) story.insertAdjacentHTML('afterend', html);
  }catch(e){}
})();
