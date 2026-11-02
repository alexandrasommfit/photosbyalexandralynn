#!/usr/bin/env python3
"""Creates web-sized copies of portfolio photos (macOS only, uses sips).

Photo details (id, category, alt text, sizes) live in src/photos.json and are safe to publish.
Where the original files live on this Mac goes in tools/sources.local.json (git-ignored, never published):
    {"autumn-01": "/path/to/original.jpg", ...}
Run:  python3 tools/photos.py          (then python3 build.py)
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'src', 'photos.json')
SOURCES = os.path.join(ROOT, 'tools', 'sources.local.json')
OUT = os.path.join(ROOT, 'assets', 'photos')
DEFAULT_WIDTHS = [480, 800, 1200]
QUALITY = '60'


def sips_dims(path):
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path], capture_output=True, text=True).stdout
    vals = {l.split(':')[0].strip(): int(l.split(':')[1]) for l in out.splitlines() if ':' in l and 'pixel' in l}
    return vals['pixelWidth'], vals['pixelHeight']


def main():
    manifest = json.load(open(MANIFEST))
    sources = json.load(open(SOURCES)) if os.path.exists(SOURCES) else {}
    os.makedirs(OUT, exist_ok=True)
    for p in manifest['photos']:
        src = sources.get(p['id'])
        if not src:
            continue
        if not os.path.exists(src):
            sys.exit('Missing original for %s: %s' % (p['id'], src))
        ow, oh = sips_dims(src)
        widths = [w for w in p.get('widths', DEFAULT_WIDTHS) if w <= ow] or [ow]
        for w in widths:
            dest = os.path.join(OUT, '%s-%d.jpg' % (p['id'], w))
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', QUALITY,
                            '--resampleWidth', str(w), src, '--out', dest], capture_output=True, check=True)
        p['widths'] = widths
        p['w'], p['h'] = widths[-1], round(oh * widths[-1] / ow)
        print('%-10s %dx%d  -> %s' % (p['id'], p['w'], p['h'], widths))
    json.dump(manifest, open(MANIFEST, 'w'), indent=2, ensure_ascii=False)
    open(MANIFEST, 'a').write('\n')


if __name__ == '__main__':
    main()
