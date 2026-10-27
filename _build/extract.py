import subprocess, re, json, sys
CAT='/home/claude/cat'
def txt(pdf,p,layout=False):
    a=['pdftotext','-f',str(p),'-l',str(p)]+(['-layout'] if layout else [])+[f'{CAT}/{pdf}.pdf','-']
    return subprocess.run(a,capture_output=True,text=True).stdout.replace('ﬁ','fi').replace('ﬂ','fl')

def specs(t):
    s={}
    w=re.findall(r'(?<![\d.])(\d{1,3}(?:\.\d)?)\s?W(?:\s?[xX]\s?(\d))?\b',t)
    ws=[]
    for a,b in w:
        v=f'{a}W'+(f' × {b}' if b else '')
        if float(a)>0 and float(a)<=400 and v not in ws: ws.append(v)
    def key(v): return (float(v.split('W')[0]), v)
    s['watt']=sorted(ws,key=key)
    beams=[]
    for m in re.findall(r'(\d{1,3})\s?°',t):
        v=f'{m}°'
        if 0<int(m)<=360 and v not in beams: beams.append(v)
    s['beam']=sorted(beams,key=lambda v:int(v[:-1]))
    ips=sorted(set('IP'+m for m in re.findall(r'IP\s?(\d{2})\b',t)))
    s['ip']=ips
    ccts=sorted(set(m+'K' for m in re.findall(r'\b([1-6]\d{3})\s?[kK]\b',t)))
    s['cct']=ccts
    f=[]
    T=t.lower()
    for k,lab in [('cri 90+','CRI 90+'),('95+','CRI 95+'),('dali','DALI dimmable'),('tunable','CCT tunable'),('deep recess','Deep recess'),('anti-glare','Anti-glare'),('trimless','Trimless'),('rgb','RGB'),('bluetooth','Bluetooth'),('triac','TRIAC dimmable'),('48v','48V system'),('honeycomb','Honeycomb louver'),('ugr','Low UGR')]:
        if k in T and lab not in f: f.append(lab)
    s['features']=f
    return s

def desc(t):
    out=[]
    for line in t.split('\n'):
        l=line.strip()
        if l.upper().startswith('DIMENSIONS') or l.upper().startswith('APPLICATION'): break
        if len(l)>35 and re.search(r'[a-z]{3}',l) and ' ' in l and '@' not in l:
            out.append(l)
    return ' '.join(out)

out={}
for pdf,n in [('indoor',196),('outdoor',114)]:
    for p in range(1,n+1):
        t=txt(pdf,p); tl=txt(pdf,p,True)
        lines=[l.strip() for l in t.split('\n') if l.strip()]
        names=[]
        for l in tl.split('\n'):
            m=re.match(r'^\s{0,6}([A-Z0-9][A-Z0-9 .&/()\-+\']{2,40}?)\s{3,}(IP\d\d|RGB|Super)\b',l)
            if m: names.append(re.sub(r'\s+',' ',m.group(1)).strip())
        out[f'{pdf}-{p}']={'first':lines[:3],'names':names,'specs':specs(t),'desc':desc(t)}
json.dump(out,open('/home/claude/build/raw.json','w'),indent=1)
