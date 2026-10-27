import json, re, sys
sys.path.insert(0,'/home/claude/build')
from catalog import INDOOR, OUTDOOR, NAME_FIX
raw=json.load(open('/home/claude/build/raw.json'))
KEEP={'AXWL','AXOD','AX','SP','SF','CC','ABS','FL','IG','AOSP','AXFTSF','AXFTCC','IP65','IP68','RGB','E-27','E27','12V','24V','A&B','A/B','COB','SMD','MR-16','SQ','LED','SMPS','CCT','IP20','IP67','UGR'}
def tc(s):
    out=[]
    for w in s.split(' '):
        if w.upper() in KEEP or re.search(r'\d',w) or re.fullmatch(r'\(?[A-Z]\)?',w): out.append(w.upper() if w.upper() in KEEP else w)
        else:
            i=1 if w[:1]=='(' else 0
            out.append(w[:i+1].upper()+w[i+1:].lower())
    return ' '.join(out)
def slugify(s): return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s.lower())).strip('-')
def merge_specs(keys):
    s={'watt':[],'beam':[],'ip':[],'cct':[],'features':[]}; d=''
    for k in keys:
        r=raw[k]
        for f in s:
            for v in r['specs'][f]:
                if v not in s[f]: s[f].append(v)
        if r['desc'] and not d: d=r['desc']
    s['watt']=[w for w in s['watt'] if not w.endswith('× 1')]
    s['watt'].sort(key=lambda v:float(v.split('W')[0]))
    s['beam'].sort(key=lambda v:int(v[:-1])); s['cct'].sort()
    return s,d
products=[]; cats=[]; used=set()
def add(cat, side, name, pages):
    pre='in' if side=='indoor' else 'out'
    keys=[f'{side}-{p}' for p in pages]
    s,d=merge_specs(keys)
    slug=slugify(name)
    base=slug; i=2
    while slug in used: slug=f'{base}-{i}'; i+=1
    used.add(slug)
    products.append(dict(slug=slug,name=name,cat=cat['slug'],side=side,img=[f'{pre}-{p:03d}' for p in pages],specs=s,desc=d,page=pages[0]))
for side,CATS in [('indoor',INDOOR),('outdoor',OUTDOOR)]:
    pre='in' if side=='indoor' else 'out'
    for c in CATS:
        cats.append(dict(slug=c['slug'],name=c['name'],side=side,intro=c['intro'],series=c.get('series',''),
                         hero=(f"{pre}-{c['hero'][1]:03d}" if c.get('hero') else None)))
        if 'products' in c:
            for name,pages in c['products']: add(c,side,name,pages)
        else:
            merge=c.get('merge',{}); groups={}
            order=[]
            for p in c['pages']:
                tgt=merge.get(p,p)
                if tgt not in groups: groups[tgt]=[]; order.append(tgt)
                groups[tgt].append(p)
            for p in order:
                pages=groups[p]
                key=(pre,p)
                if key in NAME_FIX: name=NAME_FIX[key]
                elif side=='indoor': name=raw[f'indoor-{p}']['first'][0]
                else:
                    nm=raw[f'outdoor-{p}']['names'] or [raw[f'outdoor-{p}']['first'][0]]
                    name=' / '.join(tc(n) for n in nm)
                name=name.replace('Cyclinder','Cylinder').replace('Dazzale','Dazzle')
                if side=='outdoor' and key not in NAME_FIX: name=tc(name) if name.isupper() else name
                add(c,side,name,pages)
DESC_IN={'the-invisible-02':'Compatible with CCT tunable, DALI and home automation.','dazzle-tracklight':'Available in CCT/DIM, DALI and Zigbee versions.',
 'smart-control-system':'Colour-changing and dimmable lighting controlled by RF remote, mobile app (Smart Life + RF), touch panel or switch panel. Wireless scene control with 4 scenes and 3 light groups, no extra wiring. A gateway is recommended when more than 30 COB devices are connected.',
 'sky-line':'A continuous line of light suspended on a belt, with middle supports for runs longer than 5 metres and matching end caps.',
 'dorado-series':'Suspended track chandeliers in round, straight and rectangle shapes, fitted with laser, wallwasher and pendant modules.',
 'premium-led-strips':'True colour 80/90 CRI, copper PCB, original Bridgelux LEDs. Tested for edging, tape adhesion and twist-roll.'}
for p in products:
    if p['side']=='indoor': p['desc']=''
for p in products:
    if p['slug'] in DESC_IN: p['desc']=DESC_IN[p['slug']]
    if p['slug'].startswith('magnetic-track') or p['slug'].startswith('round-magnetic') or p['slug'].startswith('surface-magnetic'): p['desc']='48V magnetic track system with spotlights, linears and grille modules. Single colour, CCT tunable, Bluetooth and DALI DT6/DT8 options.'
for p in products:
    if p['side']=='indoor': p['name']=p['name'].replace('Staller IP20 / IP54 / IP65','Staller')
json.dump(dict(cats=cats,products=products),open('/home/claude/build/site_data.json','w'),indent=1)
print(len(cats),'cats',len(products),'products')
for p in products: print(p['side'][:2],p['cat'][:14].ljust(14),p['name'][:45].ljust(45),p['img'],p['specs']['watt'][:6],p['specs']['beam'][:5],p['desc'][:30])
