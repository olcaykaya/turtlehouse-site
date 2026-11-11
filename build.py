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
    links = [("Work",p+"work.html"),("Services",p+"services/index.html"),("Areas",p+"areas/index.html"),("About",p+"about.html")]
    li = "".join(f'<li><a href="{h}">{t}</a></li>' for t,h in links)
    mi = "".join(f'<a href="{h}">{t}</a>' for t,h in links+[("Contact",p+"contact.html")])
    return f'''<header class="nav"><a class="logo" href="{p}index.html" aria-label="Turtle House Productions home"><img src="{p}media/logo-black.png" alt="Turtle House Productions" width="103" height="22"></a>
<nav aria-label="Main"><ul>{li}</ul></nav><a class="btn" href="{p}contact.html">Start a project {ARR}</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button></header>
<div class="menu" aria-label="Mobile menu">{mi}<span class="mono">{PHONE} · {EMAIL}</span></div><main>'''

def foot(p):
    s = "".join(f'<li><a href="{p}services/{x["slug"]}.html">{x["short"]}</a></li>' for x in SERVICES)
    a = "".join(f'<li><a href="{p}areas/{x["slug"]}.html">{x["name"]}</a></li>' for x in AREAS)
    return f'''</main><div class="lb" hidden><div class="lb-stage"></div><p class="lb-cap mono"></p><button class="lb-x glass" aria-label="Close">✕</button><button class="lb-p glass" aria-label="Previous">←</button><button class="lb-n glass" aria-label="Next">→</button></div><div class="shutter" aria-hidden="true"><i></i><i></i></div><nav class="mbar" aria-label="Quick contact"><a href="tel:{TEL}" class="mb-call"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>Call</a><a href="{IG}" rel="noopener" class="mb-ig">Reels</a><a href="{p}contact.html" class="mb-go">Start a project {ARR}</a></nav><footer><div class="wrap"><div class="foot"><div><img src="{p}media/logo-black.png" alt="Turtle House Productions" width="103" height="22" style="height:22px;width:auto;margin-bottom:16px"><p style="max-width:34ch">Video and photography for places and brands. Based in Weehawken, NJ. Working across New York, New Jersey and DC.</p></div>
<div><h4>Services</h4><ul>{s}</ul></div><div><h4>Areas</h4><ul>{a}</ul></div>
<div><h4>Contact</h4><ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG}" rel="noopener">Instagram</a></li><li><a href="{p}contact.html">Start a project</a></li></ul></div></div>
<div class="foot-base"><span>© 2026 Turtle House Productions</span><span class="mono">Weehawken, NJ · 40.769° N</span></div></div></footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script><script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="{p}assets/main.js"></script></body></html>'''

def h1(lines, cls="h-xxl"):
    return f'<h1 class="{cls}">' + "".join(f'<span class="ln"><span>{l}</span></span>' for l in lines) + "</h1>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faq) + "</div>"

def faq_schema(faq):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

def crumbs_schema(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}

def closing(p, line="Have a place <em>worth</em> filming?"):
    return f'''<section class="close"><div class="wrap"><p class="mono eyebrow">Next scene</p><h2 class="h-xxl"><a href="{p}contact.html">{line}</a></h2>
<div class="contact-grid"><div><span class="mono">Call</span><a href="tel:{TEL}">{PHONE}</a></div><div><span class="mono">Write</span><a href="mailto:{EMAIL}">{EMAIL}</a></div><div><span class="mono">Watch</span><a href="{IG}" rel="noopener">@turtlehouseprod</a></div></div></div></section>'''

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
    lux = "".join(f'<a href="services/luxury-brand-video-production.html"><span class="mono dim">{n}</span><div><h3>{t}</h3><p>{d}</p></div></a>' for n,t,d in [
        ("I","Fine jewelry","Boutiques, collections and private viewings. Light that behaves on gold and stone."),
        ("II","Private aviation","Cabins, ramps and departures for charter and sales teams."),
        ("III","Residences","Cinematic films for $5M+ homes and new developments."),
        ("IV","Yachts & clubs","On-water films, members' spaces, evenings worth remembering.")])
    areas = "".join(f'<a class="area rv" href="areas/{a["slug"]}.html"><span class="mono">0{i+1} — Area</span><h3>{a["name"]}</h3><p>{a["towns"]}</p></a>' for i,a in enumerate(AREAS))
    s = head(p, "Turtle House Productions | Video Production NJ & NYC — Real Estate, Luxury, Hospitality",
             "Cinematic video and photography for real estate, luxury brands, hotels and restaurants. Based in Weehawken, NJ, filming across Jersey City, Hoboken, Manhattan, Brooklyn and Washington DC.",
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

<section class="statement"><div class="wrap"><div class="mono eyebrow">01 — The problem</div>
<p>{H["statement"]}</p></div></section>

<section class="film" aria-label="Showreel"><div class="film-sticky"><div class="film-frame"><video src="media/{F(H['film_video'])}" poster="media/k1.jpg" muted loop playsinline autoplay preload="metadata" aria-label="Kitchen film excerpt"></video></div>
<p class="film-cap mono">{H["film_caption"]}</p></div></section>

<section class="reels sec" aria-label="Reels"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">02 — Reels</p><h2 class="h-xl">Made for the<br><em>vertical</em> scroll.</h2></div>
<p class="lead">Most of what we make lives on a phone. Short vertical films with a hook in the first second, cut for Instagram, TikTok and Shorts.</p></div></div>
<div class="phones" data-group>{phones}</div><div class="wrap reels-cta"><button class="rbtn glass-l" data-dir="-1" aria-label="Previous reels">←</button><button class="rbtn glass-l" data-dir="1" aria-label="Next reels">→</button><a class="btn" href="{IG}" rel="noopener">More on Instagram {ARR}</a></div></section>

<section class="sec" id="services"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">03 — What we make</p><h2 class="h-xl">Five ways<br>to be <em>seen.</em></h2></div>
<a class="btn ghost" href="services/index.html">All services {ARR}</a></div>
<ul class="svc-list">{svc_rows(p)}</ul></div><div class="peek" aria-hidden="true"><img alt=""></div></section>

<section class="sec stack-sec" aria-label="Photography"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">04 — Photos</p><h2 class="h-xl">Frames people<br><em>save.</em></h2></div><a class="btn ghost" href="work.html">Full portfolio {ARR}</a></div>
<div class="stack" data-group>{stack}</div></div></section>

<section class="night sec"><i class="blob b1"></i><i class="blob b2"></i><div class="wrap" style="position:relative"><p class="mono eyebrow">05 — The quiet end of the market</p>
<h2 class="h-xl">For brands that<br>don't do <em>discounts.</em></h2>
<p class="lead" style="margin-top:var(--s4)">Fine jewelry, private aviation, yachts, residences. Expensive things are hard to film. Reflections, tight cabins, rooms that have to feel calm. That is the work we like most.</p>
<div class="lux-grid">{lux}</div></div></section>

<section class="sec"><div class="wrap proof"><div class="m rv"><video src="media/{F(H['testimonial_video'])}" poster="media/k4.jpg" controls playsinline preload="metadata" aria-label="Client testimonial video"></video></div>
<div class="rv"><p class="mono eyebrow">06 — In their words</p><h2 class="h-l">The homeowner says it <em>better</em> than we could.</h2>
<p class="lead" style="margin:var(--s3) 0 var(--s4)">A real client, in her finished kitchen, filmed for a New Jersey remodeler. No script. Just questions, good light and enough time to forget the camera.</p>
<a class="btn ghost" href="services/testimonial-video-production.html">Testimonial films {ARR}</a></div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">07 — How it works</p><h2 class="h-xl" style="margin-bottom:var(--s6)">Planned like<br>a <em>film.</em></h2>
<div class="steps swipe"><div class="step rv"><span class="mono">01 / Plan</span><h3>One call, one shot list</h3><p>Where it runs, who it is for, what the one shot is. You approve the plan before we arrive.</p></div>
<div class="step rv"><span class="mono">02 / Shoot</span><h3>Small crew, right light</h3><p>Scheduled around the best light and your hours. Video and photos in the same visit.</p></div>
<div class="step rv"><span class="mono">03 / Deliver</span><h3>Every screen</h3><p>Graded films, edited photos, and vertical cuts for Reels, Stories and TikTok.</p></div></div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><div><p class="mono eyebrow">08 — Where</p><h2 class="h-xl">Across the <em>river,</em><br>and beyond it.</h2></div></div>
<div class="areas">{areas}</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">09 — Questions</p>{faq_html(HOME_FAQ)}</div></section>
''' + closing(p) + foot(p)
    write("index.html", s)

# ---------------- SERVICE PAGES ----------------
def service(sv):
    p = "../"; path = f"/services/{sv['slug']}.html"
    others = "".join(f'<a href="{x["slug"]}.html">{x["name"]}</a>' for x in SERVICES if x is not sv)
    areas = "".join(f'<a href="../areas/{a["slug"]}.html">{sv["short"]} in {a["name"]}</a>' for a in AREAS)
    strip = "".join(f'<div class="m"><img data-par src="{p}media/{f}" alt="{esc(sv["name"])} by Turtle House Productions" loading="lazy"></div>' for f in [sv["img"]]+sv["strip"][:2])
    deliv = "".join(f'<li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a,b in sv["deliv"])
    svc_schema = {"@context":"https://schema.org","@type":"Service","name":sv["name"],"serviceType":sv["name"],"provider":{"@id":BASE+"/#org"},
                  "areaServed":["New Jersey","New York City","Washington DC"],"description":sv["desc"],"url":BASE+path}
    s = head(p, sv["title"]+" | Turtle House", sv["desc"], path,
             [ORG, svc_schema, faq_schema(sv["faq"]), crumbs_schema([("Home","/"),("Services","/services/"),(sv["name"],path)])]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / <a href="index.html">Services</a> / {sv["short"]}</p>
{h1(sv["h1"])}<p class="lead">{sv["lead"]}</p><div class="cta-row"><a class="btn" href="../contact.html">Plan a shoot {ARR}</a><a class="btn ghost" href="tel:{TEL}">{PHONE}</a></div></div></section>
<div class="strip">{strip}</div>
<section class="sec"><div class="wrap two"><div><p class="mono eyebrow">What you get</p><h2 class="h-l">One shoot.<br>Every <em>screen.</em></h2></div><ul class="deliv rv">{deliv}</ul></div></section>
<section class="sec" style="padding-top:0"><div class="wrap two"><div><p class="mono eyebrow">Why it works</p></div><div class="prose rv"><h2 class="h-l">{esc(sv["name"])}, <em>done properly.</em></h2>{"".join(f"<p>{esc(b)}</p>" for b in sv["body"])}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">How it works</p><div class="steps"><div class="step rv"><span class="mono">01 / Plan</span><h3>Call &amp; shot list</h3><p>We agree where it runs, who it is for and what the hero shot is.</p></div><div class="step rv"><span class="mono">02 / Shoot</span><h3>Small crew</h3><p>Scheduled around the light and your hours, video and photo together.</p></div><div class="step rv"><span class="mono">03 / Deliver</span><h3>Every format</h3><p>Graded, edited and cut for web, listings and social.</p></div></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">Questions</p>{faq_html(sv["faq"])}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">Where we film this</p><div class="related" style="margin-bottom:var(--s5)">{areas}</div><p class="mono eyebrow">Other services</p><div class="related">{others}</div></div></section>
''' + closing(p) + foot(p)
    write(f"services/{sv['slug']}.html", s)

def services_index():
    p = "../"
    s = head(p, "Services | Video Production & Photography NJ, NYC | Turtle House", "Real estate video, luxury brand films, hotel and restaurant content, and client testimonial videos across New Jersey, New York City and DC.", "/services/",
             [ORG, crumbs_schema([("Home","/"),("Services","/services/")])]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / Services</p>{h1(["Five ways","to be <em>seen.</em>"])}
<p class="lead">Every service starts the same way: a plan, a shot list and a clear idea of where the content will live. Pick the one closest to what you need.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><ul class="svc-list">{svc_rows(p)}</ul></div><div class="peek" aria-hidden="true"><img alt=""></div></section>''' + closing(p) + foot(p)
    write("services/index.html", s)

# ---------------- AREA PAGES ----------------
def area(a):
    p = "../"; path = f"/areas/{a['slug']}.html"
    svc = "".join(f'<a href="../services/{x["slug"]}.html">{x["short"]} in {a["name"]}</a>' for x in SERVICES)
    others = "".join(f'<a href="{x["slug"]}.html">{x["name"]}</a>' for x in AREAS if x is not a)
    faq = [(f"Do you have a crew in {a['name']}?", f"Yes. Our base is Weehawken, NJ, and we work in {a['name']} regularly with the same small crew and plan-first approach."),
           ("What do you film?", "Real estate, luxury brands, hotels and resorts, restaurants and client testimonials, as video and photography together.")]
    s = head(p, a["title"], a["desc"], path, [ORG, faq_schema(faq), crumbs_schema([("Home","/"),("Areas","/areas/"),(a["name"],path)])]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / <a href="index.html">Areas</a> / {a["name"]}</p>
{h1(a["h1"])}<p class="lead">{a["lead"]}</p><p class="mono" style="margin-top:var(--s3);color:var(--ink-2)">{a["towns"]}</p>
<div class="cta-row"><a class="btn" href="../contact.html">Plan a shoot {ARR}</a></div></div></section>
<div class="strip"><div class="m"><img data-par src="{p}media/{a["img"]}" alt="Video production in {esc(a["name"])}" loading="lazy"></div><div class="m"><img data-par src="{p}media/f6.jpg" alt="Restaurant photography" loading="lazy"></div><div class="m"><img data-par src="{p}media/h1.jpg" alt="Hotel video production" loading="lazy"></div></div>
<section class="sec"><div class="wrap two"><div><p class="mono eyebrow">Local, on purpose</p></div><div class="prose rv">{"".join(f"<p>{esc(b)}</p>" for b in a["body"])}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><p class="mono eyebrow">What we film in {a["name"]}</p><div class="related" style="margin-bottom:var(--s6)">{svc}</div>{faq_html(faq)}
<p class="mono eyebrow" style="margin-top:var(--s6)">Other areas</p><div class="related">{others}</div></div></section>
''' + closing(p) + foot(p)
    write(f"areas/{a['slug']}.html", s)

def areas_index():
    p = "../"
    cards = "".join(f'<a class="area rv" href="{a["slug"]}.html"><span class="mono">0{i+1}</span><h3>{a["name"]}</h3><p>{a["towns"]}</p></a>' for i,a in enumerate(AREAS))
    s = head(p, "Areas We Serve | New Jersey, NYC, Washington DC | Turtle House", "Video and photo production across New Jersey, New York City and Washington DC from our base in Weehawken, NJ.", "/areas/",
             [ORG]) + nav(p) + f'''<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="../index.html">Home</a> / Areas</p>{h1(["Across the <em>river,</em>","and beyond it."])}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="areas">{cards}</div></div></section>''' + closing(p) + foot(p)
    write("areas/index.html", s)

# ---------------- WORK / ABOUT / CONTACT ----------------
def work():
    p = ""
    figs = "".join(f'<figure data-c="{c}" class="rv">{media_tag(p,f,cap)}</figure>' for f,c,cap in WORK)
    btn = "".join(f'<button data-f="{k}" class="{"on" if k=="all" else ""}">{t}</button>' for k,t in [("all","All"),("homes","Homes & interiors"),("hotels","Hotels & resorts"),("food","Restaurants"),("set","On set")])
    s = head(p, "Work | Video & Photography Portfolio | Turtle House Productions", "Selected video and photography by Turtle House Productions: homes and interiors, hotels and resorts, restaurants, and behind the scenes.", "/work.html", [ORG]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="index.html">Home</a> / Work</p>{h1(["Proof, not","<em>promises.</em>"])}<div class="filter" style="margin-top:var(--s5)">{btn}</div></div></section>
<div class="masonry" data-group>{figs}</div>''' + closing(p) + foot(p)
    write("work.html", s)

def about():
    p = ""
    s = head(p, "About | Turtle House Productions, Weehawken NJ", "Turtle House Productions is a video and photography studio in Weehawken, NJ, making films for places and brands across New Jersey, New York and DC.", "/about.html", [ORG]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="index.html">Home</a> / About</p>{h1(["A small studio","with a <em>big</em> view."])}
<p class="lead">Turtle House Productions is a video and photography studio based in Weehawken, New Jersey, looking straight at Midtown. We make films and photographs for places and the brands that live in them.</p></div></section>
<div class="strip"><div class="m"><img data-par src="media/b1.jpg" alt="Turtle House Productions on set" loading="lazy"></div><div class="m"><img data-par src="media/b3.jpg" alt="Behind the scenes" loading="lazy"></div><div class="m"><img data-par src="media/b2.jpg" alt="Camera setup" loading="lazy"></div></div>
<section class="sec"><div class="wrap two"><div><p class="mono eyebrow">How we think</p><h2 class="h-l">Plan like a film.<br>Deliver like a <em>feed.</em></h2></div>
<div class="prose rv"><p>Every project starts with where the content will live and who will see it. Then we plan the shots that matter, light them properly and cut them for every screen.</p>
<p>We keep crews small. It is faster, quieter and easier on homeowners, hotel guests and boutique staff. It also means the person who plans your shoot is the person on set.</p>
<p>We are slow about the parts that matter, like light, reflections and the first three seconds, and fast about everything else.</p></div></div></section>''' + closing(p) + foot(p)
    write("about.html", s)

def contact():
    p = ""
    s = head(p, "Contact | Book a Shoot | Turtle House Productions", f"Book video or photo production in New Jersey, NYC or DC. Call {PHONE} or email {EMAIL}.", "/contact.html", [ORG]) + nav(p) + f'''
<section class="page-hero"><div class="wrap"><p class="crumbs mono"><a href="index.html">Home</a> / Contact</p>{h1(["Tell us about","the <em>place.</em>"])}
<p class="lead">The place, the date you have in mind and where the content will run. We reply with a plan and a quote.</p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap two"><div class="contact-grid" style="grid-template-columns:1fr;margin-top:0;border:0;padding:0">
<div><span class="mono">Call</span><a href="tel:{TEL}">{PHONE}</a></div><div><span class="mono">Write</span><a href="mailto:{EMAIL}">{EMAIL}</a></div><div><span class="mono">Studio</span><span>Weehawken, NJ</span></div></div>
<form class="form" action="mailto:{EMAIL}" method="post" enctype="text/plain"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>What are we filming?<select name="type"><option>Real estate</option><option>Luxury brand</option><option>Hotel or resort</option><option>Restaurant</option><option>Testimonial</option><option>Something else</option></select></label>
<label>Tell us more<textarea name="message"></textarea></label><button class="btn" type="submit">Send {ARR}</button><p class="note">Opens your email app. Or call {PHONE}.</p></form></div></section>''' + foot(p)
    write("contact.html", s)

def seo_files():
    urls = ["/","/services/","/areas/","/work.html","/about.html","/contact.html"]+[f"/services/{s['slug']}.html" for s in SERVICES]+[f"/areas/{a['slug']}.html" for a in AREAS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls)+"</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    return len(urls)

home(); services_index(); areas_index(); work(); about(); contact()
for s in SERVICES: service(s)
for a in AREAS: area(a)
for d in ("assets", "media"):
    shutil.copytree(os.path.join(SRC, d), os.path.join(OUT, d), dirs_exist_ok=True)
print("pages:", seo_files(), "->", OUT)
