/**
 * 食品决策库 · 付费墙
 * 静态网站解锁方案：CSS blur + localStorage + 微信人工确认
 * 依赖：paywall.css
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
      '.fold-content, .recipe-box, .cost-grid, .pw-protect'
    );
    if (targets.length === 0) return;

    targets.forEach(function(el) {
      if (el.closest('.paywall-blur')) return;
      wrapWithBlur(el);
    });

    loadModal();

    var cardId = getCardId();
    if (cardId && isUnlocked(cardId)) {
      unlockCard(cardId);
    }
  }

  function wrapWithBlur(el) {
    var wrapper = document.createElement('div');
    wrapper.className = 'paywall-blur';

    var contentDiv = document.createElement('div');
    contentDiv.className = 'pw-content';
    el.parentNode.insertBefore(wrapper, el);
    contentDiv.appendChild(el);
    wrapper.appendChild(contentDiv);

    var overlay = document.createElement('div');
    overlay.className = 'pw-overlay';
    overlay.innerHTML = '<div class="pw-lock-icon">🔒</div><div class="pw-lock-text">付费解锁完整配方</div>';
    overlay.onclick = function(e) {
      e.stopPropagation();
      showModal();
    };
    wrapper.appendChild(overlay);
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

  function unlockMaster() {
    try {
      var data = JSON.parse(localStorage.getItem(PW_STORAGE_KEY) || '{}');
      data['_master'] = true;
      localStorage.setItem(PW_STORAGE_KEY, JSON.stringify(data));
    } catch(e) {}
    unlockCard(getCardId());
    closeModal();
  }

  function unlockSingle(id) {
    try {
      var data = JSON.parse(localStorage.getItem(PW_STORAGE_KEY) || '{}');
      data[id] = true;
      localStorage.setItem(PW_STORAGE_KEY, JSON.stringify(data));
    } catch(e) {}
    unlockCard(id);
    closeModal();
  }

  function loadModal() {
    var div = document.createElement('div');
    div.innerHTML = [
      '<div class="pw-modal" id="pwModal">',
        '<div class="pw-modal-box">',
          '<button class="pw-modal-close" id="pwCloseBtn">✕</button>',
          '<div class="pw-modal-icon">🔐</div>',
          '<div class="pw-modal-title">解锁完整配方</div>',
          '<div class="pw-modal-sub">查看完整的工艺参数、配方克重和成本利润数据</div>',
          '<div class="pw-price-grid">',
            '<div class="pw-price-item">',
              '<div class="pw-ptag">单卡</div>',
              '<div class="pw-pnum">¥39</div>',
              '<div class="pw-pdesc">解锁本卡</div>',
            '</div>',
            '<div class="pw-price-item pw-highlight">',
              '<div class="pw-ptag">会员</div>',
              '<div class="pw-pnum">¥299</div>',
              '<div class="pw-pdesc">全年解锁90%</div>',
            '</div>',
            '<div class="pw-price-item">',
              '<div class="pw-ptag">至尊</div>',
              '<div class="pw-pnum">¥599</div>',
              '<div class="pw-pdesc">全部+1对1</div>',
            '</div>',
          '</div>',
          '<div class="pw-modal-qr"><img src="/wechat_qr.jpg" alt="微信二维码" style="width:120px;height:120px;border-radius:8px;border:1px solid #eee"></div>',
          '<div class="pw-modal-wx">添加微信 <strong id="pwCopyWx" style="color:#C0392B;cursor:pointer">canglin1985</strong> 转账后获取解锁码</div>',
          '<div class="pw-modal-code">',
            '<input type="text" id="pwCodeInput" placeholder="输入解锁码" maxlength="12" style="flex:1;padding:8px 12px;border:1.5px solid #ddd;border-radius:8px;font-size:13px;outline:none;text-align:center;letter-spacing:3px">',
            '<button id="pwSubmitBtn" style="padding:8px 18px;background:#C0392B;color:#fff;border:none;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer">解锁</button>',
          '</div>',
          '<div class="pw-modal-foot" style="font-size:10px;color:#bbb;margin-top:10px">已解锁的卡不会重复收费 · 会员新卡自动解锁</div>',
        '</div>',
      '</div>'
    ].join('');
    document.body.appendChild(div);

    document.getElementById('pwCloseBtn').onclick = closeModal;
    document.getElementById('pwSubmitBtn').onclick = submitCode;
    document.getElementById('pwCopyWx').onclick = copyWx;
    document.getElementById('pwCodeInput').onkeydown = function(e) {
      if (e.key === 'Enter') submitCode();
    };
    document.getElementById('pwModal').onclick = function(e) {
      if (e.target === this) closeModal();
    };
  }

  function showModal() {
    var m = document.getElementById('pwModal');
    if (m) m.classList.add('show');
  }

  function closeModal() {
    var m = document.getElementById('pwModal');
    if (m) m.classList.remove('show');
  }

  function submitCode() {
    var input = document.getElementById('pwCodeInput');
    var code = input ? input.value.trim().toLowerCase() : '';
    if (!code) return;
    if (MASTER_CODES.indexOf(code) >= 0) {
      unlockMaster();
      alert('已解锁全部卡片！');
      return;
    }
    if (code.length >= 6) {
      unlockSingle(getCardId());
      alert('本卡已解锁！');
      return;
    }
    alert('解锁码无效，请联系微信 canglin1985');
  }

  function copyWx() {
    navigator.clipboard.writeText('canglin1985').then(function() {
      alert('微信号已复制：canglin1985');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
