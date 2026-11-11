#!/usr/bin/env python3
"""Turtle House site generator. Edit the CONTENT below, run `python3 build.py`, done.
Photos/videos: drop files into /media and change the file names here."""
import json, os, html, re, shutil
BASE = "https://www.turtlehouseproductions.com"
PHONE, TEL, EMAIL, IG = "407 470 9303", "+14074709303", "hi@turtlehouseproductions.com", "https://instagram.com/turtlehouseprod"
SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, "dist")
def J(n): return json.load(open(os.path.join(SRC, "content", n + ".json")))
def F(x): x = (x or "").lstrip("/"); return x[6:] if x.startswith("media/") else x   # path inside /media
_S = J("site"); PHONE, EMAIL, IG = _S["phone"], _S["email"], _S["instagram"]; TEL = "+1" + re.sub(r"\D", "", PHONE)[-10:]

ARR = '<svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.5"/></svg>'

SERVICES = [
  dict(slug="real-estate-video-photography", short="Real estate", name="Real Estate Video & Photography",
       line="Listing films, photo sets and agent intros for homes that should sell on the first scroll.",
       img="k1.jpg", strip=["k3.jpg","k5.jpg","h2.jpg"],
       title="Real Estate Video & Photography in NJ & NYC",
       desc="Listing films, real estate photography, drone and agent intro videos across Jersey City, Hoboken, Manhattan and Brooklyn. Turtle House Productions, Weehawken NJ.",
       h1=["Listings that", "sell on the", "<em>first</em> scroll."],
       lead="A buyer decides in about the time it takes to swipe. We shoot homes for that moment: a vertical film for Reels, a horizontal cut for the MLS and YouTube, and a photo set that holds up on a phone and a 27-inch screen.",
       deliv=[("Listing film","Horizontal and vertical cuts, color graded, music licensed"),("Photo set","Wide, detail and twilight frames, edited for MLS and print"),("Drone","Exterior, street and neighborhood context, where airspace allows"),("Agent intro","A short on-camera piece that sells you, not just the house"),("Social package","Reels, Stories and carousel frames cut from the same shoot")],
       body=["Hudson County and Manhattan listings compete in the same feed. A buyer looking in Hoboken is also looking at Long Island City and the Upper West Side, so the listing has to read as the best version of the home in the first three seconds.",
             "We plan the walk-through before we film it: which room opens the film, where the light is best and when, and what the one shot is that people remember. That plan is why our listings feel like a place, not a slideshow."],
       faq=[("Do you shoot both video and photos in one visit?","Yes. One crew, one visit, one plan. Photo and video are scheduled around the same light so the set feels consistent."),
            ("Do you make vertical videos for Instagram and TikTok?","Every listing film is planned for both 16:9 and 9:16, so the vertical cut is framed for phones instead of cropped from the wide version."),
            ("Which areas do you cover?","We are based in Weehawken, NJ and shoot across Hudson County, North Jersey, Manhattan, Brooklyn and Queens, plus Washington DC and Northern Virginia.")]),
  dict(slug="luxury-brand-video-production", short="Luxury & brands", name="Luxury Brand Video Production",
       line="Fine jewelry, private aviation, yachts and $5M+ residences. Quiet, expensive, exact.",
       img="h3.jpg", strip=["r1.jpg","h4.jpg","r3.jpg"],
       title="Luxury Brand Video Production NYC | Jewelry, Aviation, Residences",
       desc="Cinematic video and photography for luxury brands in New York and New Jersey: fine jewelry boutiques, private aviation, yachts and high-end residences.",
       h1=["For brands that", "don't do", "<em>discounts.</em>"],
       lead="Luxury is mostly what you leave out. We shoot jewelry, aircraft, yachts and residences with slow light, controlled reflections and very few words, so the object does the talking.",
       deliv=[("Product films","Macro and motion-control style shots for jewelry and watches"),("Aviation & yacht","Cabin, ramp and on-water films for charter and sales teams"),("Residence films","Cinematic tours for $5M+ homes and new developments"),("Campaign stills","Editorial photography for web, print and paid social"),("Event coverage","Launches, private viewings and client evenings")],
       body=["Expensive objects are hard to film. Gold and diamonds mirror everything in the room, aircraft cabins are tight, and a residence at this level has to feel calm rather than staged. Most of our time goes into light and reflections before the camera rolls.",
             "We work discreetly. Shoots can be scheduled outside opening hours, crews are small, and nothing is posted to our channels without your written approval."],
       faq=[("Can you film in our boutique before or after opening hours?","Yes. Most boutique and showroom shoots are scheduled outside client hours so the space is clear and the light is controlled."),
            ("Do you work at Teterboro and other private terminals?","We plan aviation shoots with the operator and FBO in advance and follow their access and safety rules on the ramp."),
            ("Will you post our project on your social media?","Only with your written approval. Many luxury clients prefer private work, and that is fine.")]),
  dict(slug="hotel-resort-video-production", short="Hotels & resorts", name="Hotel & Resort Video Production",
       line="Rooms, lobbies, the pool at golden hour. Films that sell the stay before the booking page.",
       img="h1.jpg", strip=["r2.jpg","h3.jpg","r4.jpg"],
       title="Hotel & Resort Video Production | NYC, NJ, DC",
       desc="Hotel and resort films, room photography and social content that sell the stay. Turtle House Productions shoots hospitality across New York, New Jersey and DC.",
       h1=["Sell the stay", "before the", "<em>booking</em> page."],
       lead="Guests book a feeling, then check the price. We film the feeling: the first look at the room, the light in the lobby at five, the pool when nobody is in it yet.",
       deliv=[("Brand film","A 60 to 90 second hero film for the website and OTA listings"),("Room library","Photography for every room category, consistent across the set"),("Social content","Reels and Stories built from one shoot, ready to schedule"),("F&B","Restaurant, bar and room service frames"),("Events & weddings","Venue films for sales teams")],
       body=["A hotel's photos live on its own site, on booking platforms and on every guest's phone. We build a library that stays consistent across all of them, shot on a plan so each room category looks like the same hotel.",
             "We schedule around occupancy and housekeeping so the shoot does not get in the way of guests."],
       faq=[("Can you shoot while the hotel is open?","Yes. We plan room access with housekeeping and work around guests, usually in small blocks across one or two days."),
            ("Do you deliver content for booking platforms?","We export to the sizes and ratios your booking channels and website need, along with vertical cuts for social.")]),
  dict(slug="restaurant-food-video-photography", short="Restaurants", name="Restaurant Video & Food Photography",
       line="Plates, pours and the room at night. Content that fills tables, not just feeds.",
       img="f2.jpg", strip=["f6.jpg","f1.jpg","f5.jpg"],
       title="Restaurant Video & Food Photography | NYC & New Jersey",
       desc="Food photography, restaurant Reels and menu shoots in Manhattan, Brooklyn, Jersey City and Hoboken. Content built to fill tables.",
       h1=["Content that", "fills <em>tables,</em>", "not just feeds."],
       lead="People choose dinner on their phone. We shoot the plate, the pour and the room at night so the reservation happens before they finish scrolling.",
       deliv=[("Menu photography","Every dish, lit to look like it does at the table"),("Reels","Short vertical films with sound, built for Instagram and TikTok"),("The room","Interior and atmosphere shots for Google, Resy and OpenTable"),("Launch content","New menu, new location, opening night")],
       body=["A restaurant's best marketing is a photo a guest saves and sends to a friend. We plan shoots around service so food comes straight from the pass to the lens, and the room is shot when it looks its best.",
             "One shoot gives you a month of posts: plates, process, people and place."],
       faq=[("How long does a restaurant shoot take?","It depends on the menu and the room. We plan it with you beforehand and schedule around service so the kitchen is not slowed down."),
            ("Do you also update our Google Business photos?","We deliver files sized for Google, Resy, OpenTable and your website, so you can update all of them from one shoot.")]),
  dict(slug="testimonial-video-production", short="Testimonials", name="Client Testimonial Video Production",
       line="Real clients, real projects. Testimonial films for remodelers, builders and service brands.",
       img="k4.jpg", strip=["k2.jpg","k1.jpg","b2.jpg"],
       title="Testimonial Video Production NJ | Remodelers, Builders, Brands",
       desc="Client testimonial videos for kitchen remodelers, builders, designers and service businesses in New Jersey and New York. Real stories, filmed well.",
       h1=["Let the client", "say it", "<em>for you.</em>"],
       lead="Nothing sells a remodel like the homeowner standing in the finished kitchen. We film real clients telling real stories, then cut them into a long version for your site and short versions for ads and Reels.",
       deliv=[("Interview","Lit, two-camera, clean audio, in the finished space"),("B-roll","The work itself: details, materials, before and after"),("Cuts","A long story for the website, short versions for ads and social"),("Captions","Burned-in captions so it works with the sound off")],
       body=["Most people are nervous on camera. We keep the crew small, ask questions instead of handing out scripts, and film long enough that people forget the camera is there. That is where the honest lines come from.",
             "We have filmed kitchen and remodel stories in New Jersey with the homeowner in the finished space, and that format works for builders, designers and any service where the result lives in someone's home."],
       faq=[("Do you write a script for the client?","No. We ask questions and let people answer in their own words. Real answers are more convincing than read lines."),
            ("Can you make short ads from the testimonial?","Yes. Every testimonial shoot is cut into a full version and several short vertical versions for ads and social.")]),
]

AREAS = [
  dict(slug="new-jersey", name="New Jersey", towns="Jersey City · Hoboken · Weehawken · Edgewater · Fort Lee · Hudson & Bergen County",
       title="Video Production Company in New Jersey | Jersey City, Hoboken, Weehawken",
       desc="Turtle House Productions is a video and photo production company based in Weehawken, NJ, serving Jersey City, Hoboken, Edgewater and North Jersey.",
       h1=["Video production,", "from <em>across</em>", "the river."],
       lead="We are based in Weehawken, minutes from Hoboken, Jersey City and the Lincoln Tunnel. That means North Jersey clients get a local crew, and Manhattan is one tunnel away.",
       body=["Hudson County has changed fast. Waterfront towers, new restaurants in Jersey City and Hoboken, and remodeled brownstones all compete for the same attention as Manhattan. We shoot real estate, restaurants, hotels and brands here every week.",
             "Being local means we can scout before the shoot, come back for golden hour, and plan around the skyline view that half of the waterfront is selling."],
       img="k5.jpg"),
  dict(slug="new-york-city", name="New York City", towns="Manhattan · Brooklyn · Queens · Long Island City",
       title="NYC Video Production Company | Luxury, Real Estate, Hospitality",
       desc="Video production and photography in Manhattan, Brooklyn and Queens for luxury brands, real estate, hotels and restaurants. Turtle House Productions.",
       h1=["New York,", "filmed like it", "<em>costs</em> what it does."],
       lead="Manhattan clients expect a crew that knows the city: building access, loading docks, permits and how the light falls between towers. We work across Manhattan, Brooklyn and Queens from our base just across the Hudson.",
       body=["In New York the bar is set by the best brands in the world. Jewelry houses on Fifth Avenue, hotels in SoHo and residences on Billionaires' Row all live in the same feed as your work. We shoot for that standard.",
             "We plan around the city: building management, freight elevators, street permits where they are needed, and the hours when a space is quiet."],
       img="h4.jpg"),
  dict(slug="washington-dc", name="Washington DC", towns="Washington DC · Georgetown · Northern Virginia",
       title="Video Production in Washington DC | Turtle House Productions",
       desc="Turtle House Productions films real estate, hospitality and brand content in Washington DC, Georgetown and Northern Virginia.",
       h1=["Washington DC,", "on the", "<em>same</em> standard."],
       lead="We travel to DC and Northern Virginia for real estate, hospitality and brand work, with the same crew and the same plan-first approach we use in New York.",
       body=["DC projects are often planned weeks ahead around events and access, so we scout remotely, confirm locations early and arrive with a shot list that is already approved.",
             "Clients who work in both New York and DC get one consistent look across both markets."],
       img="r2.jpg"),
]

WORK = [  # (file, category, caption)
  ("v_resort.mp4","hotels","Resort film"),("k1.jpg","homes","Kitchen, New Jersey"),("f2.jpg","food","Restaurant"),("h1.jpg","hotels","Hotel"),
  ("k3.jpg","homes","Interior"),("f6.jpg","food","Plate"),("r2.jpg","hotels","Resort"),("k5.jpg","homes","Interior"),("f1.jpg","food","Bar"),
  ("h3.jpg","hotels","Lobby"),("k2.jpg","homes","Detail"),("f5.jpg","food","Plate"),("r1.jpg","hotels","Resort"),("f3.jpg","food","Restaurant"),
  ("h2.jpg","homes","Room"),("r3.jpg","hotels","Resort"),("f8.jpg","food","Plate"),("k4.jpg","homes","Kitchen"),("f4.jpg","food","Plate"),
  ("h4.jpg","hotels","Hotel"),("r4.jpg","hotels","Resort"),("f7.jpg","food","Plate"),("f9.jpg","food","Plate"),("f10.jpg","food","Plate"),
  ("b1.jpg","set","On set"),("b3.jpg","set","On set"),("b2.jpg","set","On set"),
]

ORG = {"@context":"https://schema.org","@type":"ProfessionalService","@id":BASE+"/#org","name":"Turtle House Productions",
  "url":BASE+"/","logo":BASE+"/media/logo-black.png","image":BASE+"/media/k1.jpg","telephone":TEL,"email":EMAIL,
  "description":"Video production and photography for real estate, luxury brands, hotels and restaurants in New Jersey, New York City and Washington DC.",
  "address":{"@type":"PostalAddress","addressLocality":"Weehawken","addressRegion":"NJ","addressCountry":"US"},
  "areaServed":["Weehawken NJ","Hoboken NJ","Jersey City NJ","Edgewater NJ","Hudson County NJ","Bergen County NJ","Manhattan NY","Brooklyn NY","Queens NY","New York City","Washington DC","Northern Virginia"],
  "sameAs":[IG],"knowsAbout":["Real estate video","Luxury brand video","Hotel video production","Food photography","Testimonial video","Drone video"]}

def esc(s): return html.escape(s, quote=True)

def head(p, title, desc, path, schemas):
    sc = "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schemas)
    return f'''<!doctype html><html lang="en" class="js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}/media/k1.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f1ea"><link rel="icon" href="{p}media/logo-black.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/style.css">{sc}</head><body>
<div class="cursor" aria-hidden="true"></div>'''

def nav(p):
    links = [("Work",p+"work.html"),("Services",p+"services/index.html"),("Areas",p+"areas/index.html"),("Blog",p+"blog/index.html"),("About",p+"about.html")]
    li = "".join(f'<li><a href="{h}">{t}</a></li>' for t,h in links)
    mi = "".join(f'<a href="{h}">{t}</a>' for t,h in links+[("Contact",p+"contact.html")])
    return f'''<header class="nav"><a class="logo" href="{p}index.html" aria-label="Turtle House Productions home"><img src="{p}media/logo-black.png" alt="Turtle House Productions" width="103" height="22"></a>
<nav aria-label="Main"><ul>{li}</ul></nav><a class="btn" href="{p}contact.html">Start a project {ARR}</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button></header>
<div class="menu" aria-label="Mobile menu">{mi}<span class="mono">{PHONE} · {EMAIL}</span></div><main>'''

def foot(p):
    s = "".join(f'<li><a href="{p}services/{x["slug"]}.html">{x["name"]}</a></li>' for x in SERVICES)
    a = "".join(f'<li><a href="{p}areas/{x["slug"]}.html">{x["name"]}</a></li>' for x in AREAS)
    return f'''</main><div class="lb" hidden><div class="lb-stage"></div><p class="lb-cap mono"></p><button class="lb-x glass" aria-label="Close">✕</button><button class="lb-p glass" aria-label="Previous">←</button><button class="lb-n glass" aria-label="Next">→</button></div><div class="shutter" aria-hidden="true"><i></i><i></i></div><nav class="mbar" aria-label="Quick contact"><a href="tel:{TEL}" class="mb-call"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>Call</a><a href="{IG}" rel="noopener" class="mb-ig">Reels</a><a href="{p}contact.html" class="mb-go">Start a project {ARR}</a></nav><footer><div class="wrap"><div class="foot"><div><img src="{p}media/logo-black.png" alt="Turtle House Productions" width="103" height="22" style="height:22px;width:auto;margin-bottom:16px"><p style="max-width:34ch">Video production and photography for real estate, hospitality, restaurants and brands. Based in Weehawken, New Jersey, serving NJ and NYC.</p></div>
<div><h4>Services</h4><ul>{s}</ul></div><div><h4>Areas</h4><ul>{a}</ul></div>
<div><h4>Contact</h4><ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG}" rel="noopener">Instagram</a></li><li><a href="{p}contact.html">Start a project</a></li></ul></div></div>
<div class="foot-base"><span>© 2026 Turtle House Productions</span><span class="mono">Weehawken, New Jersey</span></div></div></footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script><script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="{p}assets/main.js"></script></body></html>'''

def h1(lines, cls="h-xl"):
    return f'<h1 class="{cls}">' + "".join(f'<span class="ln"><span>{l}</span></span>' for l in lines) + "</h1>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faq) + "</div>"

def faq_schema(faq):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

def crumbs_schema(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}

def closing(p, h2="Have a project<br>in <em>mind?</em>", text="Tell us what you are looking to create. We’ll help you plan the shoot.", third=None):
    lbl, href = third or ("View our work", p + "work.html")
    return f'''<section class="close"><div class="wrap"><p class="mono eyebrow">Contact</p><h2 class="h-xl"><a href="{p}contact.html">{h2}</a></h2><p class="lead" style="margin-top:var(--s3)">{text}</p>
<div class="contact-grid"><div><span class="mono">Call us</span><a href="tel:{TEL}">{PHONE}</a></div><div><span class="mono">Email us</span><a href="mailto:{EMAIL}">{EMAIL}</a></div><div><span class="mono">See more</span><a href="{href}">{lbl} →</a></div></div></div></section>'''

def write(path, s):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(s)

def svc_rows(p):
    return "".join(f'<li><a href="{p}services/{s["slug"]}.html" data-img="{p}media/{s["img"]}"><span class="mono n">0{i+1}</span><img class="th" src="{p}media/{s["img"]}" alt="" loading="lazy"><h3>{s["short"]}</h3><p>{s["line"]}</p><span class="arr">{ARR}</span></a></li>' for i,s in enumerate(SERVICES))

def media_tag(p, f, alt):
    if f.endswith(".mp4"): return f'<video src="{p}media/{f}" muted loop playsinline autoplay preload="metadata" aria-label="{esc(alt)}"></video>'
    return f'<img src="{p}media/{f}" alt="{esc(alt)}" loading="lazy">'

# ---- content from the panel (content/*.json) overrides the defaults above ----
H = J("home")
SERVICES = [dict(s, img=F(s["img"]), strip=[F(x) for x in s["strip"]], deliv=[(d["title"], d["text"]) for d in s["deliv"]], faq=[(f["q"], f["a"]) for f in s["faq"]]) for s in J("services")["items"]]
AREAS = [dict(a, img=F(a["img"])) for a in J("areas")["items"]]
WORK = [(F(w["file"]), w["category"], w["caption"]) for w in J("work")["items"]]

# ---------------- HOME ----------------
HOME_FAQ = [(f["q"], f["a"]) for f in H["faq"]]
def home():
    p = ""
    REELS = H["reels"]
    ico = {"h":'<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',"c":'<path d="M20 12a8 8 0 1 1-3.2-6.4L20 4v5h-5"/>',"s":'<path d="M21 3 3 10l7 3 3 7z"/>'}
    side = "".join(f'<span class="gb glass"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">{v}</svg></span>' for v in ico.values())
    phones = "".join(f'''<figure class="phone" style="--i:{i}"><video data-src="media/{F(r['video'])}" poster="media/{F(r.get('poster',''))}" muted loop playsinline preload="none" aria-label="{esc(r['caption'])}"></video>
<div class="ph-ui"><span class="chip glass"><i class="dot"></i>@turtlehouseprod</span><div class="ph-side">{side}</div><figcaption class="glass">{esc(r['caption'])}</figcaption></div></figure>''' for i,r in enumerate(REELS))
    STK = [(F(x["image"]), x["title"], x["text"]) for x in H["photos"]]
    stack = "".join(f'<figure class="card" style="--i:{i}"><img src="media/{f}" alt="{esc(t)} photography by Turtle House Productions" loading="lazy"><figcaption class="glass"><span class="mono">0{i+1} / 0{len(STK)}</span><b>{t}</b><span>{d}</span></figcaption></figure>' for i,(f,t,d) in enumerate(STK))
    reel = "".join(f'<figure class="reel-item"><div class="m">{media_tag(p,f,c)}</div><figcaption class="cap mono"><span>{c}</span><span>{i+1:02d}</span></figcaption></figure>' for i,(f,_,c) in enumerate([WORK[i] for i in (1,0,3,2,4,6,5,9,8,12)]))
    lux = "".join(f'<a href="services/luxury-brand-video-production.html"><span class="mono dim">0{i+1}</span><div><h3>{esc(x["title"])}</h3><p>{esc(x["text"])}</p></div></a>' for i,x in enumerate(H["lux_items"]))
    steps = "".join(f'<div class="step rv"><span class="mono">0{i+1} / {esc(x["title"])}</span><h3>{esc(x["title"])}</h3><p>{esc(x["text"])}</p></div>' for i,x in enumerate(H["steps"]))
    areas = "".join(f'<a class="area rv" href="areas/{a["slug"]}.html"><span class="mono">0{i+1} — Area</span><h3>{a["name"]}</h3><p>{a["summary"]}</p></a>' for i,a in enumerate(AREAS))
    s = head(p, H["seo_title"],
             H["seo_desc"],
             "/", [ORG, faq_schema(HOME_FAQ)]) + '<div class="intro" aria-hidden="true"><span class="mono"><span class="intro-t"><i class="dot"></i>Turtle House Productions — Scene 01</span></span><span class="intro-n">00</span></div>' + nav(p) + f'''
<section class="hero2" aria-label="Intro">
<video class="hero-src" data-d="media/{F(H['hero_video'])}" data-m="media/{F(H['hero_video_mobile'])}" poster="media/{F(H['hero_poster'])}" muted loop playsinline autoplay preload="auto" aria-hidden="true"></video>
<canvas class="lens-gl" aria-hidden="true"></canvas><div class="hero2-shade"></div>
<div class="hero2-ui" aria-hidden="true"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i>
<span class="chip glass k1"><i class="dot"></i>REC <b data-tc>00:00:00:00</b></span><span class="chip glass k2">24mm · f/1.4 · ISO 800</span><span class="chip glass k3 hint">Move to focus · click to pull</span></div>
<div class="hero2-text wrap"><p class="mono hero2-eyebrow">Turtle House Productions — Weehawken, NJ</p>
{h1(H["hero_lines"])}
<div class="hero2-row"><p class="lead">{H["hero_lead"]}</p>
<div class="cta-row"><a class="btn" href="contact.html">Start a project {ARR}</a><a class="btn ghost" href="work.html">See the work</a></div></div></div>
<div class="ticker" aria-hidden="true"><div class="ticker-in"><span>Reels</span><i>✦</i><span>Real estate</span><i>✦</i><span>Fine jewelry</span><i>✦</i><span>Hotels</span><i>✦</i><span>Restaurants</span><i>✦</i><span>Private aviation</span><i>✦</i><span>Reels</span><i>✦</i><span>Real estate</span><i>✦</i><span>Fine jewelry</span><i>✦</i><span>Hotels</span><i>✦</i><span>Restaurants</span><i>✦</i><span>Private aviation</span><i>✦</i></div></div>
</section>

<section class="statement"><div class="wrap"><div class="mono eyebrow">01 — What we do</div>
<p>{H["statement"]}</p></div></section>

<section class="film" aria-label="Showreel"><div class="film-sticky"><div class="film-frame"><video src="media/{F(H['film_video'])}" poster="media/k1.jpg" muted loop playsinline autoplay preload="metadata" aria-label="Kitchen film excerpt"></video></div>
<p class="film-cap mono">{H["film_caption"]}</p></div></section>

<section class="reels sec" aria-label="Reels"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">02 — Short-form video</p><h2 class="h-xl">{H["reels_h2"]}</h2></div>
<p class="lead">{H["reels_text"]}</p></div></div>
<div class="phones" data-group>{phones}</div><div class="wrap reels-cta"><button class="rbtn glass-l" data-dir="-1" aria-label="Previous reels">←</button><button class="rbtn glass-l" data-dir="1" aria-label="Next reels">→</button><a class="btn" href="{IG}" rel="noopener">More on Instagram {ARR}</a></div></section>

<section class="sec" id="services"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">03 — Services</p><h2 class="h-xl">{H["services_h2"]}</h2></div>
<a class="btn ghost" href="services/index.html">All services {ARR}</a></div>
<ul class="svc-list">{svc_rows(p)}</ul></div><div class="peek" aria-hidden="true"><img alt=""></div></section>

<section class="sec stack-sec" aria-label="Photography"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">04 — Photography</p><h2 class="h-xl">{H["photos_h2"]}</h2></div><a class="btn ghost" href="work.html">Full portfolio {ARR}</a></div>
<div class="stack" data-group>{stack}</div></div></section>

<section class="night sec"><i class="blob b1"></i><i class="blob b2"></i><div class="wrap" style="position:relative"><p class="mono eyebrow">05 — Luxury brands</p>
<h2 class="h-xl">{H["lux_h2"]}</h2>
{"".join(f'<p class="lead" style="margin-top:var(--s3)">{t}</p>' for t in H["lux_text"])}
<div class="lux-grid">{lux}</div></div></section>

<section class="sec"><div class="wrap proof"><div class="m rv"><video src="media/{F(H['testimonial_video'])}" poster="media/k4.jpg" controls playsinline preload="metadata" aria-label="Client testimonial video"></video></div>
<div class="rv"><p class="mono eyebrow">06 — Client stories</p><h2 class="h-l">{H["stories_h2"]}</h2>
<p class="lead" style="margin:var(--s3) 0 var(--s4)">{H["stories_text"]}</p>
<a class="btn ghost" href="services/testimonial-video-production.html">Client testimonial videos {ARR}</a></div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">07 — Our process</p><h2 class="h-xl" style="margin-bottom:var(--s6)">{H["process_h2"]}</h2>
<div class="steps swipe">{steps}</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">08 — Service areas</p><h2 class="h-xl">{H["areas_h2"]}</h2></div></div>
<div class="areas">{areas}</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">09 — FAQ</p>{faq_html(HOME_FAQ)}</div></section>
''' + closing(p, H["cta_h2"], H["cta_text"]) + foot(p)
    write("index.html", s)

# ---------------- SERVICE PAGES ----------------
def service(sv):
    p = "../"; path = f"/services/{sv['slug']}.html"
    others = "".join(f'<a href="{x["slug"]}.html">{x["name"]}</a>' for x in SERVICES if x is not sv)
    areas = "".join(f'<a href="../areas/{a["slug"]}.html">{a["name"]}</a>' for a in AREAS)
    strip = "".join(f'<div class="m"><img data-par src="{p}media/{f}" alt="{esc(sv["name"])} by Turtle House Productions" loading="lazy"></div>' for f in [sv["img"]]+sv["strip"][:2])
    deliv = "".join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a,b in sv["deliv"])
    steps = "".join(f'<div class="step rv"><span class="mono">0{i+1} / {esc(x["title"])}</span><h3>{esc(x["title"])}</h3><p>{esc(x["text"])}</p></div>' for i,x in enumerate(sv["steps"]))
    svc_schema = {"@context":"https://schema.org","@type":"Service","name":sv["name"],"serviceType":sv["name"],"provider":{"@id":BASE+"/#org"},
                  "areaServed":["New Jersey","New York City","Washington DC"],"description":sv["desc"],"url":BASE+path}
    s = head(p, sv["title"], sv["desc"], path,
             [ORG, svc_schema, faq_schema(sv["faq"]), crumbs_schema([("Home","/"),("Services","/services/"),(sv["name"],path)])]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / <a href="index.html">Services</a> / {sv["short"]}</p>
{h1(sv["h1"])}<p class="lead">{sv["lead"]}</p><div class="cta-row"><a class="btn" href="../contact.html">Start a project {ARR}</a><a class="btn ghost" href="tel:{TEL}">{PHONE}</a></div></div></section>
<div class="strip">{strip}</div>
<section class="sec"><div class="wrap two"><div><p class="mono eyebrow">Deliverables</p><h2 class="h-l">What we <em>produce.</em></h2></div><ul class="deliv rv">{deliv}</ul></div></section>
<section class="sec" style="padding-top:0"><div class="wrap two"><div><p class="mono eyebrow">Why work with us</p></div><div class="prose rv"><h2 class="h-l">{sv["why_h2"]}</h2>{"".join(f"<p>{esc(x)}</p>" for x in sv["body"])}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">Our process</p><div class="steps swipe">{steps}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">FAQ</p>{faq_html(sv["faq"])}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">Related services</p><div class="related" style="margin-bottom:var(--s5)">{others}</div><p class="mono eyebrow">Service areas</p><div class="related">{areas}</div></div></section>
''' + closing(p, sv["cta_h2"], sv["cta_text"]) + foot(p)
    write(f"services/{sv['slug']}.html", s)

def services_index():
    p = "../"
    rows = "".join(f'<li><a href="{p}services/{s["slug"]}.html" data-img="{p}media/{s["img"]}"><span class="mono n">0{i+1}</span><img class="th" src="{p}media/{s["img"]}" alt="" loading="lazy"><h3>{s["name"]}</h3><p>{s["index_line"]}</p><span class="arr">{ARR}</span></a></li>' for i,s in enumerate(SERVICES))
    s = head(p, "Video Production & Photography Services | Turtle House", "Explore video production and photography services for real estate, luxury brands, hotels, restaurants and client testimonials in NJ and NYC.", "/services/",
             [ORG, crumbs_schema([("Home","/"),("Services","/services/")])]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / Services</p>{h1(["Video production","and photography <em>services.</em>"])}
<p class="lead">We produce video and photography for businesses, properties and hospitality brands. Whether you need a property listing film, a restaurant content shoot or a brand video, every project starts with a conversation about your goals and how the content will be used.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><ul class="svc-list">{rows}</ul></div><div class="peek" aria-hidden="true"><img alt=""></div></section>''' + closing(p, "Let’s talk about<br>your <em>project.</em>", "Share a few details about the location, timing and content you need. We’ll be in touch to discuss the production.") + foot(p)
    write("services/index.html", s)

# ---------------- AREA PAGES ----------------
def area(a):
    p = "../"; path = f"/areas/{a['slug']}.html"
    others = "".join(f'<a href="{x["slug"]}.html">{x["name"]}</a>' for x in AREAS if x is not a)
    what = "".join(f'<li><b>{esc(x["title"])}</b><span>{esc(x["text"])}</span></li>' for x in a["what"])
    svc = "".join(f'<a href="../services/{x["slug"]}.html">{x["name"]}</a>' for x in SERVICES)
    faq = [(f["q"], f["a"]) for f in a["faq"]]
    s = head(p, a["title"], a["desc"], path, [ORG, faq_schema(faq), crumbs_schema([("Home","/"),("Areas","/areas/"),(a["name"],path)])]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / <a href="index.html">Areas</a> / {a["name"]}</p>
{h1(a["h1"])}<p class="lead">{a["lead"]}</p><p class="lead" style="margin-top:var(--s2)">{a["lead2"]}</p><p class="mono" style="margin-top:var(--s3);color:var(--ink-2)">{a["towns"]}</p>
<div class="cta-row"><a class="btn" href="../contact.html">Start a project {ARR}</a></div></div></section>
<div class="strip"><div class="m"><img data-par src="{p}media/{a["img"]}" alt="Video production in {esc(a["name"])}" loading="lazy"></div><div class="m"><img data-par src="{p}media/f6.jpg" alt="Restaurant photography" loading="lazy"></div><div class="m"><img data-par src="{p}media/h1.jpg" alt="Hotel photography" loading="lazy"></div></div>
<section class="sec"><div class="wrap two"><div><p class="mono eyebrow">Why work with us</p></div><div class="prose rv"><h2 class="h-l">{a["why_h2"]}</h2>{"".join(f"<p>{esc(x)}</p>" for x in a["body"])}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap two"><div><p class="mono eyebrow">Services</p><h2 class="h-l">What we film in {a["name"]}</h2></div><ul class="deliv rv">{what}</ul></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">FAQ</p>{faq_html(faq)}
<p class="mono eyebrow" style="margin-top:var(--s6)">Services</p><div class="related" style="margin-bottom:var(--s5)">{svc}</div><p class="mono eyebrow">Other service areas</p><div class="related">{others}</div></div></section>
''' + closing(p, a["cta_h2"], a["cta_text"]) + foot(p)
    write(f"areas/{a['slug']}.html", s)

def areas_index():
    p = "../"
    cards = "".join(f'<a class="area rv" href="{a["slug"]}.html"><span class="mono">0{i+1}</span><h3>{a["name"]}</h3><p>{a["summary"]}</p></a>' for i,a in enumerate(AREAS))
    s = head(p, "Service Areas | Video Production in NJ, NYC & DC | Turtle House", "Turtle House Productions is based in Weehawken, NJ, providing video production and photography across New Jersey and New York City, with selected projects in DC.", "/areas/",
             [ORG]) + nav(p) + f'''<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / Areas</p>{h1(["Video production across","New Jersey and New York <em>City.</em>"])}
<p class="lead">Turtle House Productions is based in Weehawken, New Jersey, just across the Hudson River from Manhattan. We work with businesses, property professionals and hospitality brands throughout the region, and travel for selected projects farther afield.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="areas">{cards}</div></div></section>''' + closing(p, "Planning a shoot<br>in the <em>area?</em>", "Get in touch with the location, project type and timing.") + foot(p)
    write("areas/index.html", s)

# ---------------- WORK / ABOUT / CONTACT ----------------
def work():
    p = ""
    figs = "".join(f'<figure data-c="{c}" class="rv">{media_tag(p,f,cap)}</figure>' for f,c,cap in WORK)
    btn = "".join(f'<button data-f="{k}" class="{"on" if k=="all" else ""}">{t}</button>' for k,t in [("all","All"),("homes","Real estate"),("hotels","Hotels & resorts"),("food","Restaurants"),("set","Behind the scenes")])
    s = head(p, "Video & Photography Portfolio | Turtle House Productions", "Explore selected real estate, hospitality, restaurant, brand and testimonial video and photography projects by Turtle House Productions.", "/work.html", [ORG]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="index.html">Home</a> / Work</p>{h1(["Selected video","and photography <em>projects.</em>"])}<p class="lead">A selection of our work across real estate, hospitality, restaurants and brands. Each project is shaped around the subject, location and intended audience.</p><div class="filter" style="margin-top:var(--s5)">{btn}</div></div></section>
<div class="masonry" data-group>{figs}</div>''' + closing(p, "Have a project you’d like<br>us to <em>film?</em>", "Tell us what you have in mind and where the shoot will take place.", ("View our services", "services/index.html")) + foot(p)
    write("work.html", s)

def about():
    p = ""
    s = head(p, "About Turtle House Productions | Video Production in NJ & NYC", "Meet Turtle House Productions, a Weehawken-based video and photography studio working with real estate, hospitality businesses and brands across NJ and NYC.", "/about.html", [ORG]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="index.html">Home</a> / About</p>{h1(["A focused video","and photography <em>studio.</em>"])}
<p class="lead">Turtle House Productions is an independent video and photography studio based in Weehawken, New Jersey. We work with property professionals, restaurants, hotels and brands across New Jersey and New York City.</p>
<p class="lead" style="margin-top:var(--s2)">Our work ranges from real estate listing films and food photography to hotel content, brand videos and client stories. We keep production focused, communicate clearly and pay attention to the details that make each project different.</p></div></section>
<div class="strip"><div class="m"><img data-par src="media/b1.jpg" alt="Turtle House Productions on set" loading="lazy"></div><div class="m"><img data-par src="media/b3.jpg" alt="Behind the scenes on a video shoot" loading="lazy"></div><div class="m"><img data-par src="media/b2.jpg" alt="Camera setup on location" loading="lazy"></div></div>
<section class="sec"><div class="wrap two"><div><p class="mono eyebrow">How we work</p><h2 class="h-l">A thoughtful approach to every <em>shoot.</em></h2></div>
<div class="prose rv"><p>We start by understanding what the client needs and where the content will be used. From there, we plan the shots, schedule the production and decide what needs to be captured on location.</p>
<p>We keep crews small when the project allows. It makes communication simpler and helps us work comfortably in homes, restaurants, hotels and other active spaces.</p>
<p>We care about lighting, composition, sound and editing—but just as importantly, we want the finished content to feel appropriate for the business and the people behind it.</p></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap two"><div><p class="mono eyebrow">Process</p><h2 class="h-l">From planning to final <em>delivery.</em></h2></div>
<div class="prose rv"><p>Every project has a clear production plan. We coordinate the shoot with the client, capture the agreed video and photography, then edit and prepare the final files for the intended platforms.</p></div></div></section>''' + closing(p, "Let’s talk about what<br>you’re <em>working on.</em>", "Share a little about your business and the project you have in mind.") + foot(p)
    write("about.html", s)

def contact():
    p = ""
    s = head(p, "Contact Turtle House Productions | Book a Video Shoot", f"Contact Turtle House Productions to discuss video production or photography in New Jersey, New York City or Washington, DC. Call {PHONE} or email us.", "/contact.html", [ORG]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="index.html">Home</a> / Contact</p>{h1(["Tell us about","your <em>project.</em>"])}
<p class="lead">What are you looking to create? Share the location, your preferred timing and the type of video or photography you need. We’ll get back to you to discuss the project and provide a quote.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap two"><div class="contact-grid" style="grid-template-columns:1fr;margin-top:0;border:0;padding:0">
<div><span class="mono">Phone</span><a href="tel:{TEL}">{PHONE}</a></div><div><span class="mono">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div><div><span class="mono">Studio location</span><span>Weehawken, NJ</span></div></div>
<form class="form" name="contact" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="company"><input type="hidden" name="form-name" value="contact"><p hidden><label>Company<input name="company"></label></p><label>Name<input name="name" required autocomplete="name"></label><label>Email<input type="email" name="email" required autocomplete="email"></label><label>Phone (optional)<input type="tel" name="phone" autocomplete="tel"></label>
<label>Project type<select name="type"><option>Real estate</option><option>Luxury brand</option><option>Hotel or resort</option><option>Restaurant</option><option>Client testimonial</option><option>Other</option></select></label>
<label>Tell us about your project<textarea name="message"></textarea></label><button class="btn" type="submit">Send project inquiry {ARR}</button><p class="note">Prefer email? Write to {EMAIL}. You can also call us at {PHONE}.</p></form></div></section>''' + foot(p)
    write("contact.html", s)


# ---------------- BLOG (content/blog/*.md) ----------------
def md_inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", t)
    def link(m):
        href = m.group(2).replace("&amp;", "&")
        if href.startswith("/") and not href.startswith("/media"): href = href.rstrip("/") or "/"
        ext = href.startswith("http") and "turtlehouseproductions.com" not in href
        return f'<a href="{href}"' + (' rel="noopener" target="_blank"' if ext else "") + f'>{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)

def md_html(md, root):
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    out, para, lst, ltype = [], [], [], None
    def flush():
        nonlocal para, lst, ltype
        if para: out.append("<p>" + md_inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"<{ltype}>" + "".join(f"<li>{md_inline(x)}</li>" for x in lst) + f"</{ltype}>"); lst = []; ltype = None
    for line in md.split("\n"):
        s = line.strip()
        if not s: flush(); continue
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", s)
        if m:
            flush(); out.append(f'<figure class="bf"><img src="{root}{m.group(2).lstrip("/")}" alt="{esc(m.group(1))}" loading="lazy"></figure>'); continue
        if re.match(r"^\*[^*].*\*$", s) and out and out[-1].startswith('<figure class="bf">') and not para:
            out[-1] = out[-1].replace("</figure>", f"<figcaption>{md_inline(s[1:-1])}</figcaption></figure>"); continue
        m = re.match(r"(#{2,4})\s+(.*)", s)
        if m: flush(); n = len(m.group(1)); out.append(f"<h{n}>{md_inline(m.group(2))}</h{n}>"); continue
        if s == "---": flush(); out.append("<hr>"); continue
        m = re.match(r"[-*]\s+(.*)", s)
        if m:
            if para or ltype == "ol": flush()
            ltype = "ul"; lst.append(m.group(1)); continue
        m = re.match(r"\d+[.)]\s+(.*)", s)
        if m:
            if para or ltype == "ul": flush()
            ltype = "ol"; lst.append(m.group(1)); continue
        if lst: flush()
        para.append(s)
    flush()
    return "\n".join(out)

def load_posts():
    posts = []
    d = os.path.join(SRC, "content", "blog")
    for fn in sorted(os.listdir(d), reverse=True):
        if not fn.endswith(".md"): continue
        raw = open(os.path.join(d, fn), encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        meta = {}
        for ln in m.group(1).split("\n"):
            if ":" in ln: k, v = ln.split(":", 1); meta[k.strip()] = v.strip().strip('"')
        meta["date"] = meta.get("date") or fn[:10]
        meta["body"] = m.group(2)
        meta["slug"] = meta.get("slug") or fn[11:-3]
        meta["cover"] = (meta.get("cover") or "").replace("photos/blog/", "media/blog/")
        posts.append(meta)
    return posts

def blog():
    posts = load_posts()
    import datetime
    nice = lambda d: datetime.date.fromisoformat(d).strftime("%B %-d, %Y")
    for i, po in enumerate(posts):
        p = "../"; path = f"/blog/{po['slug']}"
        art = {"@context":"https://schema.org","@type":"BlogPosting","headline":po["title"],"datePublished":po["date"],"dateModified":po["date"],
               "author":{"@type":"Organization","name":"Turtle House Productions"},"publisher":{"@id":BASE+"/#org"},
               "image":BASE+"/"+po["cover"] if po["cover"] else None,"mainEntityOfPage":BASE+path,"description":po.get("seo_description","")}
        more = "".join([f'<a href="{x["slug"]}.html">{esc(x["title"])}</a>' for x in posts if x is not po][:3])
        s = head(p, po.get("seo_title") or po["title"], po.get("seo_description") or po.get("excerpt",""), path,
                 [ORG, art, crumbs_schema([("Home","/"),("Blog","/blog/"),(po["title"],path)])]) + nav(p) + f'''
<article><section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / <a href="index.html">Blog</a></p>
<p class="mono" style="color:var(--ink-2);margin-bottom:var(--s2)">{nice(po["date"])}</p><h1 class="h-l post-h1">{esc(po["title"])}</h1>
<p class="lead">{esc(po.get("excerpt",""))}</p></div></section>
{f'<div class="post-cover wrap"><img src="{p}{po["cover"]}" alt="{esc(po["title"])}"></div>' if po["cover"] else ""}
<section class="sec" style="padding-top:var(--s5)"><div class="wrap"><div class="post">{md_html(po["body"], p)}</div></div></section></article>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">More from the blog</p><div class="related">{more}</div></div></section>
''' + closing(p) + foot(p)
        write(f"blog/{po['slug']}.html", s)
    p = "../"
    cards = "".join(f'''<a class="pcard rv" href="{po["slug"]}.html">{f'<div class="m"><img src="{p}{po["cover"]}" alt="" loading="lazy"></div>' if po["cover"] else ""}<span class="mono">{nice(po["date"])}</span><h2>{esc(po["title"])}</h2><p>{esc(po.get("excerpt",""))}</p></a>''' for po in posts)
    s = head(p, "Blog | Video & Photography Tips for NJ & NYC | Turtle House", "Practical guides on real estate, restaurant, hotel and testimonial video and photography from Turtle House Productions in Weehawken, NJ.", "/blog/", [ORG]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / Blog</p>{h1(["Notes from","the <em>shoot.</em>"])}
<p class="lead">Practical guides on real estate, restaurant, hotel and testimonial video and photography in New Jersey and New York City.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="pgrid">{cards}</div></div></section>''' + closing(p) + foot(p)
    write("blog/index.html", s)
    return [f"/blog/{po['slug']}" for po in posts]

def notfound():
    p = "/"
    s = head(p, "Page not found | Turtle House Productions", "This page has moved.", "/404.html", [ORG]).replace('<link rel="canonical"','<meta name="robots" content="noindex"><link rel="canonical"') + nav(p) + f'''
<section class="page-hero"><div class="wrap">{h1(["This page","has <em>moved.</em>"])}<p class="lead">Our website has a new home. Try one of these instead:</p>
<div class="related" style="margin-top:var(--s4)"><a href="/work">Our work</a><a href="/services/">Services</a><a href="/blog/">Blog</a><a href="/contact">Contact</a></div></div></section>''' + foot(p)
    write("404.html", s)

def thanks():
    p = ""
    s = head(p, "Thank you | Turtle House Productions", "Your message has been sent.", "/thanks.html", [ORG]).replace('<link rel="canonical"','<meta name="robots" content="noindex"><link rel="canonical"') + nav(p) + f'''
<section class="page-hero"><div class="wrap">{h1(["Thank you.","We got your <em>message.</em>"])}<p class="lead">We’ll get back to you shortly to talk about your project. If it’s urgent, call us at {PHONE}.</p>
<div class="cta-row"><a class="btn" href="work.html">View our work {ARR}</a><a class="btn ghost" href="index.html">Back to home</a></div></div></section>''' + foot(p)
    write("thanks.html", s)

def seo_files():
    urls = ["/","/services/","/areas/","/work.html","/about.html","/contact.html"]+[f"/services/{s['slug']}.html" for s in SERVICES]+[f"/areas/{a['slug']}.html" for a in AREAS]+["/blog/"]+BLOG_URLS
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls)+"</urlset>")
    write("_redirects", "\n".join(["/post/:slug  /blog/:slug  301", "/blog-1  /blog/  301", "/portfolio  /work  301", "/works  /work  301", "/our-work  /work  301",
        "/scantoconnect  /contact  301", "/contact-us  /contact  301", "/about-us  /about  301", "/home  /  301"]) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {BASE}/sitemap.xml\n")
    return len(urls)

BLOG_URLS = blog(); notfound(); thanks(); home(); services_index(); areas_index(); work(); about(); contact()
for s in SERVICES: service(s)
for a in AREAS: area(a)
for d in ("assets", "media", "admin"):
    shutil.copytree(os.path.join(SRC, d), os.path.join(OUT, d), dirs_exist_ok=True)
print("pages:", seo_files(), "->", OUT)
