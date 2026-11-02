#!/usr/bin/env python3
"""Builds the static site: src/pages + src/partials -> index.html, <slug>/index.html, sitemap.xml.

Edit content in src/pages/*.html (page bodies) and src/partials/*.html (head, nav, footer, banner),
styles in assets/site.css, behavior in assets/site.js, then run:  python3 build.py
"""
import datetime
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://photosbyalexandralynn.com'

# slug ('' = home) -> title, description, nav highlight
PAGES = {
    '': dict(file='home', nav='home',
             title='Photos by Alexandra Lynn | Tri-Cities, WA Photographer',
             desc='Wedding, portrait & family photographer in Tri-Cities, WA. Warm, romantic, real. Available to travel anywhere.'),
    'services': dict(file='services', nav='services',
             title='Photography Services in Tri-Cities, WA | Alexandra Lynn',
             desc='Wedding, portrait, family and maternity photography in Richland and the Tri-Cities, WA. See what I offer and book your session.'),
    'weddings': dict(file='weddings', nav='services',
             title='Tri-Cities Wedding Photographer | Photos by Alexandra Lynn',
             desc='Wedding and engagement photography in Richland and the Tri-Cities, WA. Packages from $1,200, with a private online gallery and travel within 50 miles included.'),
    'portraits': dict(file='portraits', nav='services',
             title='Tri-Cities Senior & Portrait Photographer | Alexandra Lynn',
             desc='Senior, couples and individual portrait sessions in Richland and the Tri-Cities, WA. Sessions from $125, with a private online gallery.'),
    'family': dict(file='family', nav='services',
             title='Tri-Cities Family & Maternity Photographer | Alexandra Lynn',
             desc='Relaxed family and maternity photography in Richland and the Tri-Cities, WA. Sessions from $125, with a private online gallery.'),
    'investment': dict(file='investment', nav='investment',
             title='Investment & Pricing | Photos by Alexandra Lynn',
             desc='Photography pricing in the Tri-Cities, WA: weddings from $1,200, portrait and family sessions from $125. See what is included and how booking works.'),
    'galleries': dict(file='galleries', nav='galleries',
             title='Galleries | Photos by Alexandra Lynn',
             desc='Browse wedding, portrait and family photography galleries from Photos by Alexandra Lynn in the Tri-Cities, WA.'),
    'about': dict(file='about', nav='about',
             title='About Alexandra Lynn | Tri-Cities Photographer',
             desc='Meet Alexandra Lynn, a Richland, WA photographer capturing real, unposed moments for weddings, portraits and families across the Tri-Cities.'),
    'contact': dict(file='contact', nav=None,
             title='Contact | Photos by Alexandra Lynn',
             desc='Tell Alexandra Lynn about your wedding, portrait or family session in the Tri-Cities, WA. Replies within 24 to 48 hours.'),
    'privacy': dict(file='privacy', nav=None,
             title='Privacy Policy | Photos by Alexandra Lynn',
             desc='How Photos by Alexandra Lynn collects, uses and protects information submitted through this website.'),
    'terms': dict(file='terms', nav=None,
             title='Terms of Service | Photos by Alexandra Lynn',
             desc='Terms of use, booking, retainer and refund information for Photos by Alexandra Lynn.'),
}

NAV_URLS = {'home': '/', 'services': '/services/', 'galleries': '/galleries/', 'about': '/about/', 'investment': '/investment/'}


PHOTOS = {}
PHOTO_ORDER = []
CATEGORIES = [('wedding', 'Weddings'), ('portrait', 'Portraits'), ('family', 'Family &amp; Maternity')]


def load_photos():
    with open(os.path.join(ROOT, 'src/photos.json'), encoding='utf-8') as f:
        for p in json.load(f)['photos']:
            PHOTOS[p['id']] = p
            PHOTO_ORDER.append(p['id'])


def img_tag(pid, sizes, eager=False):
    p = PHOTOS[pid]
    ws = p['widths']
    srcset = ', '.join('/assets/photos/%s-%d.jpg %dw' % (pid, w, w) for w in ws)
    src = '/assets/photos/%s-%d.jpg' % (pid, ws[len(ws) // 2])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return '<img src="%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s" %s>' % (
        src, srcset, sizes, p['w'], p['h'], esc(p['alt']), load)


def hero_html(desktop, mobile):
    m = PHOTOS[mobile]
    msrc = ', '.join('/assets/photos/%s-%d.jpg %dw' % (mobile, w, w) for w in m['widths'])
    return '<picture><source media="(max-width: 768px)" srcset="%s" sizes="100vw">%s</picture>' % (msrc, img_tag(desktop, '100vw', True))


def gallery_html():
    present = [(k, label) for k, label in CATEGORIES if any(PHOTOS[i]['category'] == k for i in PHOTO_ORDER)]
    out = ''
    if len(present) > 1:
        out += '<div class="gallery-filter">\n    <button class="gfilter-btn active" aria-pressed="true" onclick="filterGallery(\'all\',this)">All</button>\n'
        for k, label in present:
            out += '    <button class="gfilter-btn" aria-pressed="false" onclick="filterGallery(\'%s\',this)">%s</button>\n' % (k, label)
        out += '  </div>\n\n  '
    out += '<div class="gallery-grid" id="gallery-grid">\n'
    for pid in PHOTO_ORDER:
        out += '    <div class="gallery-cell" data-cat="%s">%s<div class="gallery-cell-overlay"></div></div>\n' % (
            PHOTOS[pid]['category'], img_tag(pid, '(min-width:900px) 33vw, 50vw'))
    return out + '  </div>\n'


def render_tags(html):
    html = html.replace('{{gallery}}', gallery_html())
    html = re.sub(r'\{\{hero:([\w-]+)\|([\w-]+)\}\}', lambda m: hero_html(m.group(1), m.group(2)), html)
    html = re.sub(r'\{\{photo:([\w-]+)\|([^|}]*)(\|eager)?\}\}',
                  lambda m: img_tag(m.group(1), m.group(2), bool(m.group(3))), html)
    if '{{' in html:
        raise SystemExit('Unrendered tag: ' + html[html.index('{{'):html.index('{{') + 60])
    return html


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def esc(t):
    return t.replace('&', '&amp;').replace('"', '&quot;')


def build_nav(nav_html, key, home):
    if not home:
        nav_html = nav_html.replace('<nav id="site-nav"', '<nav id="site-nav" class="solid"', 1)
    if key:
        url = NAV_URLS[key]
        nav_html = re.sub(r'<a href="%s"\s+data-page="%s">' % (re.escape(url), key),
                          '<a href="%s" data-page="%s" class="active-page" aria-current="page">' % (url, key), nav_html)
        nav_html = re.sub(r'<a href="%s">' % re.escape(url), '<a href="%s" aria-current="page">' % url, nav_html)
    return nav_html


def build_page(slug, meta):
    head = read('src/partials/head.html')
    url = SITE + '/' + (slug + '/' if slug else '')
    head = (head.replace('{{title}}', esc(meta['title'])).replace('{{desc}}', esc(meta['desc']))
                .replace('{{url}}', url)
                .replace('{{jsonld}}', read('src/partials/jsonld-home.html') if slug == '' else ''))
    body = render_tags(read('src/pages/%s.html' % meta['file']))
    nav = build_nav(read('src/partials/nav.html'), meta['nav'], slug == '')
    skip = '<a class="skip-link" href="#main">Skip to main content</a>\n'
    html = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n' + head + '</head>\n<body>\n'
            + read('src/partials/gtm-noscript.html') + skip + nav
            + '\n<main id="main" tabindex="-1">\n' + body + '</main>\n\n'
            + render_tags(read('src/partials/footer.html')) + '\n' + read('src/partials/banner.html')
            + '\n<script src="/assets/site.js" defer></script>\n</body>\n</html>\n')
    out = os.path.join(ROOT, slug, 'index.html') if slug else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    return url


def build_sitemap(urls):
    today = datetime.date.today().isoformat()
    rows = ''.join('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>\n' % (u, today) for u in urls)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n')


if __name__ == '__main__':
    load_photos()
    urls = [build_page(slug, meta) for slug, meta in PAGES.items()]
    build_sitemap(urls)
    print('Built %d pages + sitemap.xml' % len(urls))
