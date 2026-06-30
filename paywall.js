/**
 * 食品决策库 · 付费墙
 * 静态网站保护方案：CSS blur + localStorage + 微信人工确认
 * 依赖：paywall.css
 * 
 * v2 - 简化版：仅模糊内容，不弹窗
 */
(function(){
  'use strict';

  var PW_STORAGE_KEY = 'foodintelai_unlocked';
  var MASTER_CODES = ['canglin2026', 'food2026', 'vip2026'];

  function init() {
    // 总纲/教材卡免费开放
    var title = document.title || '';
    if (title.indexOf('总纲') >= 0 || title.indexOf('T01') >= 0 || title.indexOf('教材卡') >= 0 || title.indexOf('textbook') >= 0) {
      return;
    }

    var targets = document.querySelectorAll(
      '.fold-content, .recipe-box, .cost-grid, .pw-protect, .pay-content'
    );
    if (targets.length === 0) return;

    targets.forEach(function(el) {
      if (el.closest('.paywall-blur')) return;
      wrapWithBlur(el);
    });

    // 检查是否已解锁
    var cardId = getCardId();
    if (cardId && isUnlocked(cardId)) {
      unlockCard(cardId);
    }
  }

  function wrapWithBlur(el) {
    var wrapper = document.createElement('div');
    wrapper.className = 'paywall-blur';

    // 如果包裹的是pay-content容器，标记最小高度（防塌陷）
    if (el.classList && el.classList.contains('pay-content')) {
      wrapper.classList.add('pw-has-pay-content');
    }

    var contentDiv = document.createElement('div');
    contentDiv.className = 'pw-content';
    el.parentNode.insertBefore(wrapper, el);
    contentDiv.appendChild(el);
    wrapper.appendChild(contentDiv);
  }

  function getCardId() {
    var title = document.querySelector('.ph-name');
    if (title) return title.textContent.trim();
    var meta = document.querySelector('title');
    if (meta) return meta.textContent.trim();
    return window.location.pathname;
  }

  function isUnlocked(id) {
    try {
      var data = JSON.parse(localStorage.getItem(PW_STORAGE_KEY) || '{}');
      return data[id] === true || data['_master'] === true;
    } catch(e) { return false; }
  }

  function unlockCard(id) {
    document.querySelectorAll('.paywall-blur').forEach(function(w) {
      w.classList.add('pw-unlocked');
    });
  }

  // 暴露解锁函数给控制台/调试用
  window._unlockAll = function() {
    try {
      var data = JSON.parse(localStorage.getItem(PW_STORAGE_KEY) || '{}');
      data['_master'] = true;
      localStorage.setItem(PW_STORAGE_KEY, JSON.stringify(data));
    } catch(e) {}
    document.querySelectorAll('.paywall-blur').forEach(function(w) {
      w.classList.add('pw-unlocked');
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
