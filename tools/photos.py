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


def detect_faces(paths):
    """Runs Apple Vision face detection (macOS). Returns {filename: [[x, y, w, h], ...]} or {}."""
    try:
        r = subprocess.run(['swift', os.path.join(ROOT, 'tools', 'faces.swift')] + paths, capture_output=True, text=True, timeout=600)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else {}
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return {}


def focus_from_faces(boxes):
    """Face area plus room for hair and ears, as [x0, y0, x1, y1] (0-1, from the top-left)."""
    x0 = y0 = 1.0
    x1 = y1 = 0.0
    for x, y, w, h in boxes:
        x0, x1 = min(x0, x - 0.35 * w), max(x1, x + 1.35 * w)
        y0, y1 = min(y0, y - 0.8 * h), max(y1, y + 1.15 * h)
    clamp = lambda v: round(max(0.0, min(1.0, v)), 3)
    return [clamp(x0), clamp(y0), clamp(x1), clamp(y1)]


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
    # Where the faces are, so crops never cut them off (a "focus_manual" entry overrides detection)
    biggest = {p['id']: os.path.join(OUT, '%s-%d.jpg' % (p['id'], p['widths'][-1])) for p in manifest['photos'] if p.get('widths')}
    found = detect_faces(list(biggest.values()))
    for p in manifest['photos']:
        if p.get('focus_manual'):
            p['focus'] = p['focus_manual']
        elif p['id'] in biggest and os.path.basename(biggest[p['id']]) in found:
            p['focus'] = focus_from_faces(found[os.path.basename(biggest[p['id']])])
    json.dump(manifest, open(MANIFEST, 'w'), indent=2, ensure_ascii=False)
    open(MANIFEST, 'a').write('\n')


if __name__ == '__main__':
    main()
