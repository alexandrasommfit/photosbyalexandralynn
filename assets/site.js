// Old single-page links (e.g. /#investment) redirect to the new pages
(function () {
  if (location.pathname !== '/' || !location.hash) return;
  var parts = location.hash.replace('#', '').split('/');
  var pages = { services: '/services/', investment: '/investment/', about: '/about/', galleries: '/galleries/', contact: '/contact/', privacy: '/privacy/', terms: '/terms/' };
  var services = { weddings: '/weddings/', portraits: '/portraits/', family: '/family/' };
  var target = pages[parts[0]];
  if (parts[0] === 'services' && services[parts[1]]) target = services[parts[1]];
  if (parts[0] === 'investment' && parts[1]) target = '/investment/#inv-' + parts[1];
  if (target) location.replace(target);
})();

// Mobile nav
function toggleMobileNav() {
  var ham = document.getElementById('nav-ham');
  var mob = document.getElementById('nav-mobile');
  ham.classList.toggle('open');
  mob.classList.toggle('open');
  ham.setAttribute('aria-expanded', mob.classList.contains('open') ? 'true' : 'false');
  document.body.style.overflow = mob.classList.contains('open') ? 'hidden' : '';
}

// Investment sticky nav + scroll spy
function scrollInv(id, el) {
  document.querySelectorAll('.inv-nav-item').forEach(function (i) { i.classList.remove('active'); });
  if (el) el.classList.add('active');
  var sec = document.getElementById(id);
  if (sec) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
(function () {
  var navItems = document.querySelectorAll('.inv-nav-item');
  if (!navItems.length || !('IntersectionObserver' in window)) return;
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      navItems.forEach(function (item) { item.classList.toggle('active', item.dataset.section === entry.target.id); });
    });
  }, { rootMargin: '-10% 0px -60% 0px', threshold: 0 });
  ['inv-weddings', 'inv-seniors', 'inv-family'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) observer.observe(el);
  });
})();

// FAQ accordion
function toggleFaq(btn) {
  var item = btn.closest('.faq-item');
  var isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(function (i) { i.classList.remove('open'); });
  document.querySelectorAll('.faq-q').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
  if (!isOpen) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
}

// Gallery filter
function filterGallery(cat, btn) {
  document.querySelectorAll('.gfilter-btn').forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
  if (btn) { btn.classList.add('active'); btn.setAttribute('aria-pressed', 'true'); }
  document.querySelectorAll('.gallery-cell').forEach(function (cell) {
    cell.style.display = (cat === 'all' || cell.dataset.cat === cat) ? 'block' : 'none';
  });
}

// Nav turns solid on scroll (home page only)
(function () {
  var nav = document.getElementById('site-nav');
  if (!nav || !document.getElementById('home-hero')) return;
  window.addEventListener('scroll', function () { nav.classList.toggle('scrolled', window.scrollY > 60); });
})();

// Contact forms (Netlify Forms)
async function submitForm(e, form) {
  e.preventDefault();
  var btn = form.querySelector('.csub');
  var status = form.querySelector('.form-status');
  if (!status) {
    status = document.createElement('p');
    status.className = 'form-status sr-only';
    status.setAttribute('role', 'status');
    form.appendChild(status);
  }
  btn.textContent = 'Sending…';
  btn.disabled = true;
  var encoded = new URLSearchParams(new FormData(form)).toString();
  try {
    var res = await fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: encoded
    });
    if (res.ok) {
      btn.textContent = 'Sent! I\'ll be in touch soon.';
      btn.style.background = 'var(--navy)';
      btn.style.color = 'white';
      status.textContent = 'Your inquiry was sent. I\'ll be in touch soon.';
    } else {
      btn.textContent = 'Something went wrong — email me directly.';
      status.textContent = 'Something went wrong sending your inquiry. Please email me directly.';
      btn.disabled = false;
    }
  } catch (err) {
    btn.textContent = 'Something went wrong — email me directly.';
    status.textContent = 'Something went wrong sending your inquiry. Please email me directly.';
    btn.disabled = false;
  }
}

// Cookie consent (analytics stays off until accepted)
function showCookieBanner() {
  var b = document.getElementById('cookie-banner');
  if (b) { b.hidden = false; b.querySelector('.cookie-accept').focus(); }
}
function setConsent(value) {
  try { localStorage.setItem('pbal-consent', value); } catch (e) {}
  gtag('consent', 'update', { analytics_storage: value });
  var b = document.getElementById('cookie-banner');
  if (b) b.hidden = true;
}
(function () {
  var saved = null;
  try { saved = localStorage.getItem('pbal-consent'); } catch (e) {}
  if (saved !== 'granted' && saved !== 'denied') {
    var b = document.getElementById('cookie-banner');
    if (b) b.hidden = false;
  }
})();
