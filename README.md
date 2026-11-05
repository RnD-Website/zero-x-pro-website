# Zero X Pro

Scroll-driven product website for the Zero X Pro drone, plus the earlier 40-second film version. Everything here is source; nothing needs a bundler.

## Folder map

| Path | What it is |
| --- | --- |
| `site/site.html` | **The website source.** One HTML file with inline CSS and JS. This is the editable version, with the DialKit control panel. |
| `site/*.mp4`, `site/*.jpg` | Media the site uses (hero video, tab videos, footer video, hero and snow images). |
| `site/dialkit.js`, `site/dialkit.css` | DialKit 2.1.0 (MIT), the live-tweaking panel. Loaded only by `site.html`. |
| `site/vendor/lenis.min.js` | Lenis 1.1.20 (MIT), the smooth-scroll library. Licences are beside it. |
| `site/archive/` | Clips and stills that earlier versions used and the site no longer references. |
| `build/build.py` | Builds the two production versions below. |
| `dist/` | **Production folder to publish.** DialKit removed, Lenis bundled, `netlify.toml` included. |
| `zero-x-pro.single-file.html` | **One self-contained file** (13 MB): everything embedded, DialKit removed. |
| `film/` | The 40-second film: `index.html` (timeline animation), `render.js` (frames), `shot.js` (stills), `zero-x-pro.mp4` (result). |
| `originals/` | Files the client supplied: 4 logo/icon SVGs, 5 source videos (including the reference screen recording), 2 product images. |

## Work on the site

Open `site/site.html` in a browser. Opening it from a local web server is more reliable for video:

```bash
cd site && python3 -m http.server 8000
```

Then visit http://localhost:8000/site.html. Click the round button at the bottom right for the DialKit panel (copy, colours, motion, images and video slots).
All copy also lives in the `CFG` object at the top of the script in `site.html`.

## Build the production versions

```bash
python3 build/build.py
```

This rewrites `dist/` and `zero-x-pro.single-file.html`. Both have the DialKit panel removed completely (no script, stylesheet or toggle).
Rebuilding the current source reproduces the files that were tested and delivered, byte for byte.

## Deploy

- **Netlify (drag and drop):** drag the `dist` folder onto the site's Deploys page. A Netlify site named `zero-x-pro` was created in the account (https://app.netlify.com/projects/zero-x-pro); nothing has been uploaded to it yet.
- **Any static host:** upload the contents of `dist/`.
- **Single file:** `zero-x-pro.single-file.html` can be opened by double-clicking, or uploaded as `index.html`.

## Render the film

Needs Node with Playwright, and ffmpeg.

```bash
cd film
node render.js 4 ./frames          # 1200 frames, 4 workers
ffmpeg -framerate 30 -i frames/f_%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 17 zero-x-pro.mp4
```

## Notes

- Specs (4K/60, 1 inch, 46 min, 12 km, 249 g, 3-axis) and most copy are placeholders. Replace them with the client's real figures.
- The site is designed at 1920×1080 and scales to fit the window. It has no separate phone layout.
- The preview copy on claude.ai (https://claude.ai/artifact/7A6hgmQVf3KV3uCtRMs3pG) is private to the owner unless shared.
