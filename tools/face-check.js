// Face-safety test for photo crops. Run it in the browser console (or via Claude Code's browser tools)
// while the site is served locally (python3 -m http.server 8000), on any page of that server.
// For each page and screen size it loads the page and checks that every face area listed in src/photos.json
// (the "focus" boxes) stays fully inside every photo slot. Hero photos must also fit above the fold.
//
//   await faceTest([[375, 812], [1440, 900]], ['/', '/galleries/'])
//   -> { checked, fails: [...] }   (fails should be empty)
//
// Test in small batches (about 6 screen sizes x 8 pages per call) to avoid browser timeouts.
window.faceTest = async function (viewports, pages) {
  const manifest = await (await fetch('/src/photos.json')).json();
  const byId = {}; manifest.photos.forEach(p => byId[p.id] = p);
  const res = { fails: [], checked: 0 };
  const idOf = u => u.split('/').pop().replace(/-\d+\.jpg.*/, '');
  for (const page of pages) for (const [vw, vh] of viewports) {
    const f = document.createElement('iframe');
    f.style.cssText = 'position:fixed;left:-9000px;top:0;border:0;width:' + vw + 'px;height:' + vh + 'px';
    f.src = page; document.body.appendChild(f);
    await new Promise(r => f.onload = r);
    const d = f.contentDocument, w = f.contentWindow;
    d.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
    const st = d.createElement('style'); st.textContent = '*{transition:none!important;animation:none!important}'; d.head.appendChild(st);
    await new Promise(r => setTimeout(r, 350));
    d.querySelectorAll('img[data-ctx]').forEach(img => {
      const r = img.getBoundingClientRect();
      if (r.width < 2 || r.height < 2 || w.getComputedStyle(img).display === 'none') return;
      const pic = img.closest('picture'); let id = idOf(img.src);
      if (pic) { const s = pic.querySelector('source'); if (s && w.matchMedia(s.media).matches) id = idOf(s.srcset); }
      const p = byId[id]; if (!p) return;
      const cw = r.width, ch = r.height, scale = Math.max(cw / p.w, ch / p.h), rw = p.w * scale, rh = p.h * scale;
      const pos = w.getComputedStyle(img).objectPosition.split(' ').map(parseFloat);
      const ox = (cw - rw) * pos[0] / 100, oy = (ch - rh) * pos[1] / 100;
      const [x0, y0, x1, y1] = p.focus;
      const fx0 = x0 * rw + ox, fx1 = x1 * rw + ox, fy0 = y0 * rh + oy, fy1 = y1 * rh + oy;
      const visH = pic ? Math.min(ch, vh) : ch;
      const ix = Math.max(0, Math.min(fx1, cw) - Math.max(fx0, 0)), iy = Math.max(0, Math.min(fy1, visH) - Math.max(fy0, 0));
      const vis = (ix * iy) / ((fx1 - fx0) * (fy1 - fy0)); res.checked++;
      if (vis < 0.985) res.fails.push(page + ' @' + vw + 'x' + vh + ' ' + img.dataset.ctx + ' ' + id + ' visible=' + Math.round(vis * 100) + '%');
    });
    f.remove();
  }
  return res;
};
