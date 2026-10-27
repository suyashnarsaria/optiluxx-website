"""Generates the Optiluxx static site into /home/claude/site from site_data.json + content below."""
import json, html, re
OUT = '/home/claude/site'
D = json.load(open('/home/claude/build/site_data.json'))
CATS, PRODS = D['cats'], D['products']
e = html.escape

PHONE_DISPLAY = '+91 76170 17384'
EMAIL = 'suyash.narsaria@optiluxx.in'
WA = 'https://wa.me/917617017384'
IG = 'https://www.instagram.com/optiluxxlights/'
FB = 'https://www.facebook.com/optiluxxlights'
HO_MAP = 'https://www.google.com/maps/search/?api=1&query=Draupadi+Mansion+11+Brabourne+Road+Kolkata+700001'
EC_MAP = 'https://www.google.com/maps/search/?api=1&query=PS+PACE+Mahendra+Roy+Lane+Halder+Avenue+Topsia+Kolkata'

# ---------- editable content ----------
PROJECTS = [
  dict(title='Khalsa College', place='Amritsar, Punjab', year='2026', type='Heritage façade illumination',
       text='Façade lighting for a 130-year-old Indo-Saracenic landmark. Optiluxx handled the concept design, supply and installation end to end.', images=[]),
  dict(title='Diamond Heritage', place='Strand Road, Kolkata', year='', type='Heritage façade illumination',
       text='Lighting designed by Suyash Narsaria and executed by Optiluxx to bring out the heritage elevation at night.', images=[]),
  dict(title='DPS Ruby', place='Kolkata', year='2026', type='Façade illumination',
       text='Façade lighting for the school campus, including supply and installation, starting with the front elevation.', images=[]),
  dict(title='Art Gallery', place='New Delhi', year='', type='Gallery & art lighting',
       text='Picture Light framing projectors that shape light precisely to each artwork.', images=[]),
]
# Home slideshow. Real project photos (from PROJECTS) are used first; catalogue images fill in until then.
SLIDE_FALLBACK = [
  ('h/facade.webp','Façade lighting','ACUTA architectural façade luminaires','outdoor.html#acuta-facade','50% 35%'),
  ('h/aura.webp','Interior accent lighting','AURA indoor collection','indoor.html','50% 50%'),
  ('h/pool.webp','Pool & water lighting','ACQUA IP68 swimming pool luminaires','outdoor.html#acqua-pool','50% 55%'),
  ('h/curtain.webp','Layered residential lighting','Curtain grazers, magnetic track and wallwashers','indoor.html#curtain-grazer','50% 55%'),
  ('h/street.webp','Campus & street lighting','URBE post-top and street luminaires','outdoor.html#urbe-street','50% 55%'),
  ('h/sera.webp','Entrances & walkways','SERA decorative wall luminaires','outdoor.html#sera-wall','50% 50%'),
]
CLIENTS = [('Hyatt','Hospitality'),('JW Marriott','Hospitality'),('Tarun Tahiliani','Fashion retail'),('Aditya Birla Fashion','Retail'),
           ('BMW','Automotive showroom'),('Harley-Davidson','Automotive showroom'),('Emami Realty','Real estate'),('L&T','Infrastructure'),
           ('Merlin Group','Real estate'),('Bandhan Bank','Banking')]
SECTORS = ['Hospitality','Retail','Corporate offices','Real estate','Automotive showrooms','Healthcare','Education','Government',
           'Clubs','Warehousing','Banking','Residential','Heritage façades']
PROCESS = [
  ('Understand the space','A site visit and brief: how the space is used, what should be seen first, and the mood you want at each hour.'),
  ('Lighting design','A layered concept of ambient, accent and task light, with fixture selection and placement, led by Suyash Narsaria.'),
  ('DIALux simulation','Lux levels, uniformity and glare checked in DIALux reports before a single fixture is bought.'),
  ('Supply & fabrication','Catalogue luminaires with CREE and Bridgelux chips, BIS certified, plus custom profiles and fittings built to your layout.'),
  ('Installation','Our team installs, aims and commissions the lighting, and sets scenes and controls.'),
  ('Service at your site','After handover a technician comes to your premises. You never have to send fixtures back.'),
]

# ---------- shared chrome ----------
NAV = [('indoor.html','Indoor'),('outdoor.html','Outdoor'),('projects.html','Projects'),('clientele.html','Clientele'),('about.html','About'),('contact.html','Contact')]
ICON_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zm0 4.7a5.1 5.1 0 100 10.2 5.1 5.1 0 000-10.2zm0 8.4a3.3 3.3 0 110-6.6 3.3 3.3 0 010 6.6zm5.3-9.8a1.2 1.2 0 100 2.4 1.2 1.2 0 000-2.4z"/></svg>'
ICON_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.3v3.2h2.8V22h3.4z"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4c1.7.7 2.3.8 3.2.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.2-.3-.3-.5-.4z"/></svg>'

def head(title, desc, current):
    links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{t}</a>' for h,t in NAV)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="assets/img/h/aura.webp">
<link rel="icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Mulish:wght@400;600&family=JetBrains+Mono:wght@400&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="site-head"><div class="wrap">
<a class="logo" href="index.html" aria-label="Optiluxx home"><img src="assets/img/logo.png" alt="Optiluxx · Lighting up lives" width="600" height="151"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="{WA}" target="_blank" rel="noopener">Enquire</a></nav>
</div></header>
<main>
'''

def foot(extra_js=''):
    return f'''</main>
<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div><img src="assets/img/logo.png" alt="Optiluxx" width="600" height="151" style="height:34px;width:auto;margin-bottom:18px">
<p>Architectural lighting, from design to installation. Crafting light in Kolkata since 2014.</p>
<div class="social" style="margin-top:18px"><a href="{IG}" target="_blank" rel="noopener">{ICON_IG}Instagram</a><a href="{FB}" target="_blank" rel="noopener">{ICON_FB}Facebook</a></div></div>
<div><h4>Head office</h4><address>Optiluxx Electricals LLP<br>Draupadi Mansion, 2nd Floor<br>11 Brabourne Road<br>Kolkata 700001</address></div>
<div><h4>Experience center</h4><address>Display Wise<br>PS PACE, Unit 401, 4th Floor<br>Mahendra Roy Lane, Halder Avenue<br>Topsia, Kolkata</address></div>
<div><h4>Talk to us</h4><ul><li>{PHONE_DISPLAY}</li><li style="word-break:break-all">{EMAIL}</li><li><a href="{WA}" target="_blank" rel="noopener">WhatsApp us</a></li><li><a href="contact.html">Contact page</a></li></ul></div>
</div>
<div class="foot-base"><span>© Optiluxx Electricals LLP</span><span>Lighting up lives</span></div>
</div></footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ICON_WA}</a>
{extra_js}<script src="assets/site.js"></script>
</body>
</html>
'''

def wrange(p):
    w = p['specs']['watt']
    parts = []
    if w: parts.append(w[0] if len(w)==1 else f'{w[0]} – {w[-1]}')
    if p['specs']['ip']: parts.append(p['specs']['ip'][-1])
    if p['specs']['beam'] and len(parts)<2: parts.append(' / '.join(p['specs']['beam'][:3]))
    return ' · '.join(parts)

def card(p):
    k = (p['name']+' '+' '.join(p['specs']['watt'])+' '+p['cat']).lower()
    return f'<a class="card" href="product.html#{p["slug"]}" data-k="{e(k)}"><div class="im"><img src="assets/img/p/{p["img"][0]}.webp" alt="{e(p["name"])}" loading="lazy" width="909" height="1286"></div><div class="tx"><b>{e(p["name"])}</b><span>{e(wrange(p))}</span></div></a>'

def write(name, s):
    open(f'{OUT}/{name}','w').write(s)

def cats_of(side): return [c for c in CATS if c['side']==side]
def prods_of(cat): return [p for p in PRODS if p['cat']==cat]
def cat_img(c): return c['hero'] or prods_of(c['slug'])[0]['img'][0]

# ---------- home ----------
def tiles(side):
    out=[]
    href = 'indoor.html' if side=='indoor' else 'outdoor.html'
    for c in cats_of(side):
        n=len(prods_of(c['slug']))
        out.append(f'<a class="tile" href="{href}#{c["slug"]}"><div class="im"><img src="assets/img/p/{cat_img(c)}.webp" alt="" loading="lazy"></div><div class="tx"><b>{e(c["name"])}</b><span>{n} {"product" if n==1 else "products"}</span></div></a>')
    return ''.join(out)

steps = ''.join(f'<div class="step"><span class="n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i,(t,d) in enumerate(PROCESS))

def slideshow():
    slides=[]
    for p in PROJECTS:
        for im in p['images'][:2]:
            slides.append((f'projects/{im}', p['title'], ' · '.join(x for x in [p['type'],p['place']] if x), 'projects.html', '50% 50%'))
    if len(slides) < 4: slides += SLIDE_FALLBACK[:6-len(slides)] if slides else SLIDE_FALLBACK
    items=[]; dots=[]
    for i,(img,t,sub,href,pos) in enumerate(slides):
        load = '' if i==0 else ' loading="lazy"'
        items.append(f'<figure class="slide{" is-on" if i==0 else ""}" aria-hidden="{"false" if i==0 else "true"}"><img src="assets/img/{img}" alt="{e(t)}" style="object-position:{pos}"{load}><figcaption><a href="{href}" tabindex="{0 if i==0 else -1}"><b>{e(t)}</b><span>{e(sub)}</span></a></figcaption></figure>')
        dots.append(f'<button type="button" class="dot" aria-label="Show slide {i+1}: {e(t)}" aria-pressed="{"true" if i==0 else "false"}" data-i="{i}"></button>')
    return f'''<section class="show" aria-roledescription="carousel" aria-label="Featured work">
<div class="slides">{"".join(items)}</div>
<div class="show-copy"><div class="wrap">
<p class="eyebrow">Complete lighting solutions · Kolkata · Since 2014</p>
<h1>Light, designed for the space. <em>Then built and installed.</em></h1>
<p class="lede">We design the lighting, simulate it, supply or fabricate every luminaire, and install it, for homes, hotels, retail, offices and heritage façades.</p>
<div class="actions"><a class="btn solid" href="indoor.html">Indoor collection</a><a class="btn" href="outdoor.html">Outdoor collection</a></div>
</div></div>
<div class="show-ctrl"><div class="wrap"><div class="dots">{"".join(dots)}</div><button type="button" class="pause" aria-label="Pause slideshow">Pause</button></div></div>
<div class="show-bar"><i></i></div>
</section>'''

home = head('Optiluxx · Architectural Lighting, Kolkata','Optiluxx designs, supplies and installs complete architectural lighting for homes, hotels, retail and façades. Indoor and outdoor luminaire collections, Kolkata since 2014.','index.html') + f'''
{slideshow()}

<section class="section" style="border-top:0"><div class="wrap split">
<div class="sec-head" style="margin:0"><p class="eyebrow">The 2026 collections</p><hr class="kelvin"><h2>Two catalogues, one standard of light</h2><p>AURA covers interiors: deep-recess COBs, wallwashers, lasers, magnetic track, strips and custom profiles. NOCTURNE covers everything outdoors, from façades and gardens to pools and streets.</p></div>
<div class="collections">
<a class="coll" href="indoor.html"><img src="assets/img/h/aura.webp" alt="Warm wall-grazing light on a curved wall" width="1407" height="1233" loading="lazy"><div class="cap"><span>Indoor collection</span><b>AURA</b></div></a>
<a class="coll" href="outdoor.html"><img src="assets/img/h/nocturne.webp" alt="Residential tower lit with vertical façade beams" width="1406" height="1232" loading="lazy"><div class="cap"><span>Outdoor collection</span><b>NOCTURNE</b></div></a>
</div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><p class="eyebrow">How we work</p><hr class="kelvin"><h2>One team from first sketch to the last fixture aimed</h2><p>Most suppliers sell you fittings. We take responsibility for how the space looks at night, so design, products and installation sit with one team.</p></div>
<div class="process">{steps}</div>
</div></section>

<section class="section"><div class="wrap split">
<div class="photo-frame portrait"><img src="assets/img/suyash.webp" alt="Suyash Narsaria, founder and lead lighting designer of Optiluxx" width="600" height="750" loading="lazy"></div>
<div class="founder-card">
<p class="role">Founder & Lead Lighting Designer</p>
<h3>Suyash Narsaria</h3>
<p class="quote">“Good lighting isn’t noticed. It’s felt in posture, mood and attention.”</p>
<p class="muted">A chartered accountant who chose light over ledgers, Suyash founded Optiluxx in 2014 and leads every design himself, from private residences to heritage façades such as Khalsa College, Amritsar.</p>
<div><a class="btn ghost" href="about.html">About Optiluxx</a></div>
</div>
</div></section>

<section class="section"><div class="wrap">
<div class="cat-head"><div><p class="eyebrow">Aura · Indoor collection</p><h2 style="margin-top:12px">Indoor luminaires</h2></div><a class="btn ghost" href="indoor.html">View all indoor</a></div>
<div class="tiles">{tiles("indoor")}</div>
<div class="cat-head" style="margin-top:64px"><div><p class="eyebrow">Nocturne · Outdoor collection</p><h2 style="margin-top:12px">Outdoor luminaires</h2></div><a class="btn ghost" href="outdoor.html">View all outdoor</a></div>
<div class="tiles">{tiles("outdoor")}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Trusted by</p><hr class="kelvin"><h2>Brands that care how their spaces look</h2></div>
<div class="clients">{"".join(f'<div class="client">{e(n)}<small>{e(s)}</small></div>' for n,s in CLIENTS[:8])}</div>
<div style="margin-top:28px;display:flex;flex-wrap:wrap;gap:12px"><a class="btn ghost" href="clientele.html">Full clientele</a><a class="btn ghost" href="projects.html">See our projects</a></div>
</div></section>

<section class="section"><div class="wrap split">
<div class="sec-head" style="margin:0"><p class="eyebrow">Start a project</p><hr class="kelvin"><h2>Tell us about your space</h2><p>Send a floor plan, a few photos or just a description. We will come back with a lighting approach and the right fixtures.</p></div>
<div style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn solid" href="{WA}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a><a class="btn" href="contact.html">All contact details</a></div>
</div></section>
''' + foot()
write('index.html', home)

# ---------- collections ----------
def collection(side):
    file = f'{side}.html'
    cs = cats_of(side)
    if side=='indoor':
        title, eyebrow, h1 = 'Indoor Collection · Optiluxx', 'Aura · The 2026 indoor collection', 'Indoor architectural lighting'
        lede = 'Deep-recess COB downlights, wallwashers, lasers, magnetic track, strips, neon and custom profiles. High colour fidelity, glare control and 1800K–4000K tunable options across most models.'
        img = 'h/home.webp'
    else:
        title, eyebrow, h1 = 'Outdoor Collection · Optiluxx', 'Nocturne · The 2026 outdoor collection', 'Outdoor architectural lighting'
        lede = 'Seven series for façades, gardens, paths, pools and streets: SERA, VARCO, ORTO, ACUTA, PASSO, ACQUA and URBE. IP65 to IP68, warm 3000K, precise beam control.'
        img = 'h/sera.webp'
    chips = ''.join(f'<a class="chip" href="#{c["slug"]}">{e(c["name"])}</a>' for c in cs)
    secs = []
    for c in cs:
        ps = prods_of(c['slug'])
        secs.append(f'<section class="cat" id="{c["slug"]}"><div class="cat-head"><div><h2>{e(c["name"])}</h2><p>{e(c["intro"])}</p></div><span class="count">{len(ps)} {"product" if len(ps)==1 else "products"}</span></div><div class="grid">{"".join(card(p) for p in ps)}</div></section>')
    n = sum(len(prods_of(c['slug'])) for c in cs)
    s = head(title, lede, file) + f'''
<section class="page-hero"><div class="wrap ph-grid">
<div><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lede">{lede}</p></div>
<div class="ph-img"><img src="assets/img/{img}" alt="" width="1407" height="1094"></div>
</div></section>
<div class="toolbar"><div class="wrap">
<div class="search"><label for="q" class="eyebrow" style="position:absolute;left:-9999px">Search products</label><input id="q" type="search" placeholder="Search {n} products" autocomplete="off"></div>
<nav class="chips" aria-label="Product families">{chips}</nav>
</div></div>
<div class="wrap">{"".join(secs)}<p class="empty" id="noresults" hidden>No products match that search. Try a name like “Pinnacle” or a wattage like “12W”.</p></div>
<div style="height:72px"></div>
''' + foot()
    write(file, s)
collection('indoor'); collection('outdoor')

# ---------- product (rendered client-side from data.js) ----------
write('assets/data.js', 'window.OPX=' + json.dumps({'cats':CATS,'products':PRODS}, ensure_ascii=False, separators=(',',':')) + ';')
write('product.html', head('Product · Optiluxx','Optiluxx luminaire details, specifications and catalogue page.','') +
      '<div id="product-root"><div class="wrap" style="padding-block:80px"><p class="muted">Loading product…</p></div></div>\n' +
      foot('<script src="assets/data.js"></script>\n'))

# ---------- about ----------
about = head('About Optiluxx · Lighting Design, Kolkata','Optiluxx Electricals LLP is a Kolkata architectural lighting company offering lighting design, DIALux simulation, custom fixtures, supply and installation. Founded in 2014 by lead lighting designer Suyash Narsaria.','about.html') + f'''
<section class="page-hero"><div class="wrap ph-grid">
<div><p class="eyebrow">About Optiluxx</p><h1>A lighting company that starts with design</h1>
<p class="lede">Optiluxx Electricals LLP was founded in Kolkata in 2014. We are a complete lighting solutions provider: we design the lighting, prove it in simulation, supply or fabricate the luminaires, install them and service them on site.</p></div>
<div class="ph-img"><img src="assets/img/h/facade.webp" alt="Façade lit with vertical grazing beams" style="object-position:50% 40%"></div>
</div></section>

<section class="section" id="design"><div class="wrap split" style="align-items:start">
<div class="sec-head" style="margin:0"><p class="eyebrow">Lighting design</p><hr class="kelvin"><h2>Every project begins on paper, not in a catalogue</h2></div>
<div class="prose">
<p>We plan light in three layers: <strong>ambient</strong> for comfort, <strong>accent</strong> for meaning, and <strong>task</strong> for clarity. We pick one primary colour temperature for a space and create variety through intensity and beam, not mixed whites.</p>
<p>Before you buy anything, we verify the scheme in <strong>DIALux</strong> simulation reports covering lux levels, uniformity and glare. Then we specify the exact fixture, beam and finish for each position.</p>
<p>When the catalogue does not have the right shape, we <strong>fabricate it</strong>: custom linear profiles, geometric fittings and bespoke luminaires built to your layout.</p>
</div>
</div></section>

<section class="section"><div class="wrap split">
<div class="founder-card">
<p class="role">Founder & Lead Lighting Designer</p>
<h3>Suyash Narsaria</h3>
<p class="muted">Suyash qualified as a Chartered Accountant in 2014 after his articleship at Deloitte, Mumbai, and then chose a different path: light. He founded Optiluxx the same year and has led its design work ever since.</p>
<p class="muted">He personally designs Optiluxx’s schemes, from homes and hotels to heritage façades such as Khalsa College in Amritsar and the Diamond Heritage building on Strand Road, Kolkata. The financial discipline stays: clients get a design that is beautiful and a bill of materials that makes sense.</p>
<div style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn solid" href="contact.html">Book a design consultation</a><a class="btn ghost" href="projects.html">See projects</a></div>
</div>
<div class="photo-frame portrait"><img src="assets/img/suyash.webp" alt="Suyash Narsaria, founder and lead lighting designer of Optiluxx" width="600" height="750" loading="lazy"></div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><p class="eyebrow">What you get</p><hr class="kelvin"><h2>Complete lighting solutions</h2></div>
<div class="process">{steps}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Our standards</p><hr class="kelvin"><h2>Built to be trusted, then forgotten</h2></div>
<div class="facts">
<div><b>CREE · Bridgelux</b><span>LED chips used across our range</span></div>
<div><b>BIS</b><span>Certified products</span></div>
<div><b>CRI 90+ / 95+</b><span>High colour fidelity options on premium COBs</span></div>
<div><b>1800K – 4000K</b><span>Tunable white available on most COB models</span></div>
<div><b>DALI · Bluetooth</b><span>Dimming, scenes and smart control</span></div>
<div><b>On-site service</b><span>A technician visits you; no fixtures sent back</span></div>
</div>
</div></section>
''' + foot()
write('about.html', about)

# ---------- projects ----------
def proj(p):
    meta = ' · '.join(x for x in [p['type'], p['place'], p['year']] if x)
    if p['images']:
        vis = f'<div class="vis"><img src="assets/img/projects/{p["images"][0]}" alt="{e(p["title"])}" loading="lazy"></div>'
    else:
        vis = f'<div class="vis placeholder"><span class="tag">Photos coming soon</span><span class="big">{e(p["title"])}</span></div>'
    return f'<article class="project">{vis}<p class="meta">{e(meta)}</p><h3>{e(p["title"])}</h3><p>{e(p["text"])}</p></article>'

projects = head('Projects · Optiluxx','Architectural and façade lighting projects by Optiluxx, including heritage façades, schools, galleries, hotels and retail.','projects.html') + f'''
<section class="page-hero"><div class="wrap">
<p class="eyebrow">Projects</p><h1>Work we have lit</h1>
<p class="lede">Heritage façades, campuses, galleries, homes and retail. Each project is designed by Suyash Narsaria and delivered by the Optiluxx team. New projects are added as they are completed.</p>
</div></section>
<section class="section" style="border-top:0;padding-top:8px"><div class="wrap"><div class="projects">{"".join(proj(p) for p in PROJECTS)}</div></div></section>
''' + foot()
write('projects.html', projects)

# ---------- clientele ----------
clientele = head('Clientele · Optiluxx','Clients of Optiluxx include Hyatt, JW Marriott, BMW, Harley-Davidson, Aditya Birla Fashion, Tarun Tahiliani, Emami Realty, L&T, Merlin Group and Bandhan Bank.','clientele.html') + f'''
<section class="page-hero"><div class="wrap">
<p class="eyebrow">Clientele</p><h1>Who we light for</h1>
<p class="lede">Hotels, showrooms, banks, developers and fashion houses trust Optiluxx with spaces where the lighting is part of the brand.</p>
</div></section>
<section class="section" style="border-top:0;padding-top:8px"><div class="wrap">
<div class="clients">{"".join(f'<div class="client">{e(n)}<small>{e(s)}</small></div>' for n,s in CLIENTS)}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Sectors</p><hr class="kelvin"><h2>Industries we work across</h2></div>
<div class="sectors">{"".join(f'<span>{e(s)}</span>' for s in SECTORS)}</div>
</div></section>
''' + foot()
write('clientele.html', clientele)

# ---------- contact ----------
types = ['Residence','Hotel / restaurant','Retail / showroom','Office','Façade / heritage','Landscape / outdoor','Other']
contact = head('Contact Optiluxx · Kolkata','Contact Optiluxx Electricals LLP, Kolkata. Head office at Brabourne Road and the Display Wise experience center in Topsia. Phone +91 76170 17384.','contact.html') + f'''
<section class="page-hero"><div class="wrap">
<p class="eyebrow">Contact</p><h1>Visit, call or send us your plans</h1>
<p class="lede">See the luminaires in person at our experience center, or message us with your floor plan and we will suggest a lighting approach.</p>
</div></section>
<section class="section" style="border-top:0;padding-top:8px"><div class="wrap" style="display:grid;gap:16px">
<div class="contact-grid">
<div class="box"><p class="eyebrow">Head office</p><h3>Optiluxx Electricals LLP</h3><address>Draupadi Mansion, 2nd Floor<br>11 Brabourne Road<br>Kolkata 700001</address><div><a class="btn ghost" href="{HO_MAP}" target="_blank" rel="noopener">Open in Maps</a></div></div>
<div class="box"><p class="eyebrow">Experience center</p><h3>Display Wise</h3><address>PS PACE, Unit 401, 4th Floor<br>Mahendra Roy Lane, Halder Avenue<br>Topsia, Kolkata</address><div><a class="btn ghost" href="{EC_MAP}" target="_blank" rel="noopener">Open in Maps</a></div></div>
</div>
<div class="contact-grid">
<div class="box"><p class="eyebrow">Direct</p>
<div class="line"><span>{PHONE_DISPLAY}</span><button class="copy" type="button" data-copy="+917617017384">Copy</button></div>
<div class="line" style="word-break:break-all"><span>{EMAIL}</span><button class="copy" type="button" data-copy="{EMAIL}">Copy</button></div>
<div class="enq" style="margin-top:6px"><a class="btn solid" href="{WA}" target="_blank" rel="noopener">Chat on WhatsApp</a></div>
<p class="eyebrow" style="margin-top:14px">Follow</p>
<div class="social"><a href="{IG}" target="_blank" rel="noopener">{ICON_IG}@optiluxxlights</a><a href="{FB}" target="_blank" rel="noopener">{ICON_FB}@optiluxxlights</a></div>
</div>
<div class="box"><p class="eyebrow">Project enquiry</p>
<form class="enquiry" id="enquiry">
<div class="row2"><div class="field"><label for="f-name">Name</label><input id="f-name" required autocomplete="name"></div>
<div class="field"><label for="f-phone">Phone</label><input id="f-phone" type="tel" required autocomplete="tel"></div></div>
<div class="row2"><div class="field"><label for="f-city">City</label><input id="f-city" autocomplete="address-level2"></div>
<div class="field"><label for="f-type">Project type</label><select id="f-type">{"".join(f"<option>{t}</option>" for t in types)}</select></div></div>
<div class="field"><label for="f-msg">About the space</label><textarea id="f-msg" placeholder="Size, rooms or areas, timeline, and anything you already have in mind"></textarea></div>
<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center"><button class="btn solid" type="submit">Prepare WhatsApp message</button><a class="btn" id="wa-out" href="{WA}" target="_blank" rel="noopener" hidden>Open WhatsApp to send</a></div>
</form></div>
</div>
</div></section>
''' + foot()
write('contact.html', contact)
print('built', len(PRODS), 'products')
