/**
 * 分享按钮 · 向网站引流
 * 在所有卡片页添加浮动分享按钮
 * 点击复制卡片链接+推荐语到剪贴板
 */
(function(){
  'use strict';

  // 获取卡片信息
  var pageTitle = document.title || '';
  var pageUrl = window.location.href;
  var cardName = pageTitle.replace(/[•··].*$/, '').trim(); // 去掉版本号
  var siteName = 'FoodIntelAI · 食品决策库';
  
  // 分享文案
  var shareText = '我在' + siteName + '看了《' + cardName + '》的创业决策分析，数据很扎实，推荐做餐饮的朋友看看 → ' + pageUrl;

  // 创建分享按钮
  var btn = document.createElement('div');
  btn.innerHTML = '<div style="position:fixed;bottom:80px;right:16px;z-index:9999;display:flex;flex-direction:column;gap:8px;align-items:center">' +
    '<div id="fdShareBtn" style="width:44px;height:44px;border-radius:50%;background:#C0392B;color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer;box-shadow:0 2px 12px rgba(192,57,43,0.3);transition:transform 0.2s" title="分享此卡片">' +
    '📤</div>' +
    '<div id="fdShareTip" style="display:none;background:#1a1a1a;color:#fff;font-size:11px;padding:6px 12px;border-radius:6px;white-space:nowrap">已复制，去分享吧</div>' +
    '</div>';
  document.body.appendChild(btn);

  // 分享逻辑
  document.getElementById('fdShareBtn').onclick = function() {
    // 复制到剪贴板
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(shareText).then(function() {
        showTip('✅ 已复制');
      }).catch(function() {
        fallbackCopy(shareText);
      });
    } else {
      fallbackCopy(shareText);
    }
  };

  // 兼容方案
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      showTip('✅ 已复制');
    } catch(e) {
      showTip('⚠️ 复制失败，请手动复制链接');
    }
    document.body.removeChild(ta);
  }

  // 提示动画
  function showTip(msg) {
    var tip = document.getElementById('fdShareTip');
    if (!tip) return;
    tip.textContent = msg;
    tip.style.display = 'block';
    setTimeout(function() { tip.style.display = 'none'; }, 2000);
  }

  // 按钮悬停效果
  document.getElementById('fdShareBtn').onmouseenter = function() {
    this.style.transform = 'scale(1.1)';
  };
  document.getElementById('fdShareBtn').onmouseleave = function() {
    this.style.transform = 'scale(1)';
  };

})();

/* 2026-10-23 D-60：卡片页「📋 复制微信号」按钮只写了 onclick="copyWx()"，
   页面本身却没有定义 copyWx（全站 32 页如此）→ 点击抛 ReferenceError、复制不了。
   在卡片页通用脚本里补一份全局实现；页面自带实现的（首页、VC 系列）以页面为准。 */
if (typeof window.copyWx !== 'function') {
  window.copyWx = function () {
    var WX = 'canglin1985';
    function showTip() {
      var tip = document.createElement('div');
      tip.textContent = '✅ 微信号已复制：' + WX;
      tip.style.cssText = 'position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);' +
        'background:#1a1a1a;color:#fff;font-size:14px;line-height:1.6;padding:14px 20px;' +
        'border-radius:10px;z-index:10000;box-shadow:0 6px 24px rgba(0,0,0,.35);' +
        'max-width:80vw;text-align:center';
      document.body.appendChild(tip);
      setTimeout(function () { if (tip.parentNode) tip.parentNode.removeChild(tip); }, 2200);
    }
    function execCopy() {
      var ta = document.createElement('textarea');
      ta.value = WX;
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;top:-1000px;left:-1000px';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      if (ta.parentNode) ta.parentNode.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(WX).then(showTip, function () { execCopy(); showTip(); });
    } else {
      execCopy();
      showTip();
    }
  };
}
