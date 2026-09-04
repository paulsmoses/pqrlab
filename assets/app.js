/* Lightning + grid overlay for every banner (hero and page-head).
   Injected here so all pages share one definition; styling lives in the CSS. */
(function () {
  var svg =
    '<svg viewBox="0 0 1200 600" preserveAspectRatio="xMidYMin slice">' +
    '<path class="bolt bolt-1" d="M842 -40 L806 150 L850 160 L792 322 L824 330 L748 512" />' +
    '<path class="bolt bolt-1" d="M824 330 L770 402" />' +
    '<path class="bolt bolt-2" d="M372 -40 L346 128 L382 136 L336 268 L366 276 L316 400" />' +
    '</svg>';
  document.querySelectorAll('.hero, .page-head').forEach(function (banner) {
    if (banner.querySelector('.hero-lightning')) return;
    var wrap = document.createElement('div');
    wrap.className = 'hero-lightning';
    wrap.setAttribute('aria-hidden', 'true');
    wrap.innerHTML = '<div class="hero-flash"></div>' + svg;
    banner.insertBefore(wrap, banner.firstChild);
  });
})();

/* Nav toggle */
document.addEventListener('click', function (e) {
  var t = e.target.closest('.nav-toggle');
  if (t) {
    document.querySelector('.menu').classList.toggle('open');
    return;
  }
  var rm = e.target.closest('.readmore-btn');
  if (rm) {
    var card = rm.closest('.collapsible');
    var open = card.classList.toggle('open');
    var lbl = rm.querySelector('.rm-label');
    if (lbl) lbl.textContent = open ? 'Read less' : 'Read more';
  }
});

/* Deterministic gradient avatars from initials */
(function () {
  var palettes = [
    ['#1a4d8f', '#2f6fd0'],
    ['#0f766e', '#22b8cf'],
    ['#7c3a00', '#f4a531'],
    ['#3b2f8f', '#6d5fd0'],
    ['#0b1f3a', '#1a4d8f'],
    ['#9a3412', '#f97316'],
    ['#155e75', '#06b6d4'],
    ['#4a1d6e', '#a855f7'],
    ['#134e2f', '#2fb673']
  ];
  function hash(s) {
    var h = 0;
    for (var i = 0; i < s.length; i++) { h = (h * 31 + s.charCodeAt(i)) >>> 0; }
    return h;
  }
  document.querySelectorAll('.avatar[data-name]').forEach(function (el) {
    var name = el.getAttribute('data-name').trim();
    var parts = name.split(/\s+/);
    var initials = (parts[0][0] || '') + (parts.length > 1 ? parts[parts.length - 1][0] : '');
    el.textContent = initials.toUpperCase();
    var p = palettes[hash(name) % palettes.length];
    el.style.background = 'linear-gradient(135deg,' + p[0] + ',' + p[1] + ')';

    // Render photo when available; fall back to the monogram if it fails to load.
    var src = el.getAttribute('data-img');
    if (src) {
      var img = new Image();
      img.className = 'avatar-photo';
      img.alt = name;
      img.decoding = 'async';
      img.onload = function () { el.classList.add('has-photo'); el.appendChild(img); };
      img.onerror = function () { /* keep monogram */ };
      img.src = src;
    }
  });
})();

/* De-spam email links: the address is split across two data attributes
   so it never appears as plain text (not even once JS runs) in either the
   page source or the rendered page -- only inside the mailto: href, which
   basic scrapers/crawlers generally don't parse. The visible label stays
   the obscured "user 'at' domain" text already in the HTML. */
(function () {
  document.querySelectorAll('[data-email-user]').forEach(function (el) {
    var user = el.getAttribute('data-email-user');
    var domain = el.getAttribute('data-email-domain');
    if (!user || !domain) return;
    el.setAttribute('href', 'mailto:' + user + '@' + domain);
  });
})();
