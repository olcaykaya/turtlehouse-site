# Turtle House site — handoff notes (for any future Claude session)

Live: https://turtlehouseproductions.com (Netlify project "rainbow-brioche-85b823", auto-deploys from `main`).
Repo: github.com/olcaykaya/turtlehouse-site. Domain registered at Wix (DNS edited there: A @ 75.2.60.5, CNAME www -> rainbow-brioche-85b823.netlify.app; Zoho MX/SPF/DKIM untouched).

## How it works
- `python3 build.py` -> `dist/` (Netlify runs this). Pages: home, 5 services, 3 areas (NJ/NYC/DC), work, about, contact, blog, thanks, 404.
- Content: `content/*.json` (home, services, areas, work, site) and `content/blog/*.md`. Media: `media/` (reels in `media/reels/`, blog photos in `media/blog/`).
- Design: `assets/style.css`, `assets/main.js` (GSAP + ScrollTrigger + Lenis from CDN; WebGL lens hero; reels carousel; lightbox).
- Panel: `/admin` (GitHub token in browser localStorage, commits to `main`).
- Contact form: Netlify Forms (`name="contact"`) -> email notification to hi@turtlehouseproductions.com (set in Netlify UI).
- Redirects for old Wix URLs: generated `_redirects` in build.py.

## Rules from Olcay
- No prices on the site. No invented clients, numbers or quotes. Phone 407 470 9303. Mobile first (90% of visitors).
- Copy direction: plain, specific, studio voice (see commit "Apply revised website copy").
- Blog: weekly, real-project posts first. Mac agent publishes via `TurtleHouseAgent/tools/site_post.py` (GITHUB_TOKEN in agent/.env).

## Next ideas
- Google Search Console: verify domain + submit /sitemap.xml; weekly ranking report in the Mac agent.
- Project/case-study pages per real shoot (VideoObject schema).
- Google Business Profile: service-area business, address hidden, reviews.
