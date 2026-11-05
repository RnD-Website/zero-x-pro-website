#!/usr/bin/env python3
"""Builds the two production versions of the site from site/site.html.

  python3 build/build.py

Outputs (DialKit panel is removed from both):
  dist/                              folder to publish (Netlify: drag this folder, or set it as the publish directory)
  zero-x-pro.single-file.html        one self-contained file (videos/images/scripts embedded as data URIs)
"""
import base64, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
DIST = os.path.join(ROOT, 'dist')
SINGLE = os.path.join(ROOT, 'zero-x-pro.single-file.html')

MEDIA = ['drone.jpg', 'snow.jpg', 'clip-hero.mp4', 'clip-valley.mp4', 'clip-snow.mp4',
         'clip-aerial.mp4', 'clip-survey.mp4', 'clip-cinema.mp4', 'clip-landscape.mp4']
MIME = {'jpg': 'image/jpeg', 'mp4': 'video/mp4'}
CDN_LENIS = '<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.20/dist/lenis.min.js"></script>'
NETLIFY_TOML = '''[build]
  publish = "."

[[headers]]
  for = "/*.mp4"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.jpg"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
'''

def read(p, mode='r'):
    with open(p, mode) as f:
        return f.read()

def production_html():
    s = read(os.path.join(SITE, 'site.html'))
    # 1) remove DialKit completely (stylesheet, library, panel script)
    link = '<link rel="stylesheet" href="dialkit.css">'
    assert s.count(link) == 1, 'dialkit.css link not found'
    s = s.replace(link + '\n', '').replace(link, '')
    i = s.index('<script src="dialkit.js"></script>')
    s = s[:i].rstrip() + '\n'
    assert 'dialkit' not in s.lower()
    # 2) Lenis from the same site instead of a CDN
    assert s.count(CDN_LENIS) == 1, 'Lenis CDN tag not found'
    s = s.replace(CDN_LENIS, '<script src="lenis.min.js"></script>')
    # 3) standalone document wrapper (the preview host added this before)
    m = re.match(r'\s*<title>.*?</title>\s*', s, re.S)
    assert m, 'title not found'
    s = s[m.end():]
    head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="description" content="Zero X Pro: cinematic aerial imaging, anywhere.">\n'
            '<meta name="theme-color" content="#fbfbfb">\n<title>Zero X Pro</title>\n</head>\n<body>\n')
    return head + s + '\n</body>\n</html>\n'

def build_dist(html):
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    with open(os.path.join(DIST, 'index.html'), 'w') as f:
        f.write(html)
    for name in MEDIA:
        shutil.copy(os.path.join(SITE, name), DIST)
    shutil.copy(os.path.join(SITE, 'vendor', 'lenis.min.js'), DIST)
    with open(os.path.join(DIST, 'netlify.toml'), 'w') as f:
        f.write(NETLIFY_TOML)

def build_single(html):
    s = html
    old = "i.src='drone.jpg'"
    assert s.count(old) == 1
    s = s.replace(old, "i.src=getComputedStyle(document.documentElement).getPropertyValue('--hero').trim().replace(/^url\\([\"']?|[\"']?\\)$/g,'')")
    js = read(os.path.join(SITE, 'vendor', 'lenis.min.js'))
    tag = '<script src="lenis.min.js"></script>'
    assert s.count(tag) == 1 and '</script' not in js
    s = s.replace(tag, '<script>' + js + '</script>')
    for name in MEDIA:
        assert s.count(name) == 1, (name, s.count(name))
        data = base64.b64encode(read(os.path.join(SITE, name), 'rb')).decode()
        s = s.replace(name, 'data:%s;base64,%s' % (MIME[name.rsplit('.', 1)[1]], data))
    with open(SINGLE, 'w') as f:
        f.write(s)

if __name__ == '__main__':
    html = production_html()
    build_dist(html)
    build_single(html)
    size = sum(os.path.getsize(os.path.join(DIST, n)) for n in os.listdir(DIST)) / 1e6
    print('dist/                         %.1f MB (%d files)' % (size, len(os.listdir(DIST))))
    print('single-file html              %.1f MB' % (os.path.getsize(SINGLE) / 1e6))
