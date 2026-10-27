import json, subprocess
from PIL import Image, ImageOps
d=json.load(open('site_data.json'))
need=set()
for p in d['products']: need.update(p['img'])
for c in d['cats']:
    if c['hero']: need.add(c['hero'])
src='/home/claude/cat/r110'; out='/home/claude/site/assets/img/p'
tot=0
for k in sorted(need):
    im=Image.open(f'{src}/{k}.jpg').convert('RGB')
    im.save(f'{out}/{k}.webp','WEBP',quality=72,method=5)
    tot+=__import__('os').path.getsize(f'{out}/{k}.webp')
print(len(need),'images',tot//1024,'KB')
# heroes from higher-res
C='/home/claude/cat'
for pdf,pg,name in [('indoor',1,'aura'),('outdoor',1,'nocturne'),('outdoor',61,'facade'),('indoor',2,'pyramid'),('outdoor',6,'sera'),('indoor',12,'home')]:
    subprocess.run(['pdftoppm','-f',str(pg),'-l',str(pg),'-r','170','-jpeg','-jpegopt','quality=95','-singlefile',f'{C}/{pdf}.pdf',f'/tmp/h_{name}'],check=True)
    im=Image.open(f'/tmp/h_{name}.jpg').convert('RGB')
    w,h=im.size
    if name in('aura','nocturne'): im=im.crop((0,int(h*0.14),w,int(h*0.72)))
    if name=='pyramid': im=im.crop((0,int(h*0.27),w,h))
    if name=='home': im=im.crop((0,int(h*0.30),w,int(h*0.85)))
    im.save(f'/home/claude/site/assets/img/h/{name}.webp','WEBP',quality=78,method=5)
    print(name,im.size)
# logo
subprocess.run(['pdftoppm','-f','196','-l','196','-r','400','-png','-singlefile',f'{C}/indoor.pdf','/tmp/back'],check=True)
im=Image.open('/tmp/back.png').convert('L').crop((1000,2030,2310,2385))
a=im.point(lambda v: 0 if v<60 else min(255,int((v-60)*255/150)))
logo=Image.new('RGBA',im.size,(255,255,255,0)); logo.putalpha(a)
bb=logo.getbbox(); logo=logo.crop(bb)
logo=logo.resize((600,int(600*logo.size[1]/logo.size[0])),Image.LANCZOS)
logo.save('/home/claude/site/assets/img/logo.png',optimize=True); print('logo',logo.size)
