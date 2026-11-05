"""Génère og-image.jpg (1200x630) pour les aperçus WhatsApp / LinkedIn / X."""
from PIL import Image, ImageDraw, ImageFont
import os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1200,630
bg=Image.new('RGB',(W,H))
px=bg.load()
c1,c2=(0x5B,0x43,0x69),(0x3F,0x2D,0x4A)
for y in range(H):
    for x in range(W):
        t=(x/W+y/H)/2
        px[x,y]=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3))
d=ImageDraw.Draw(bg)
gold=(0xC2,0x9B,0x52); gold2=(0xE8,0xD2,0xA0)
# photo ronde
ph=Image.open(os.path.join(root,'photo.jpg')).convert('RGB')
ph=ph.crop((110,10,690,590)).resize((380,380),Image.LANCZOS)
mask=Image.new('L',(380,380),0); ImageDraw.Draw(mask).ellipse((0,0,379,379),fill=255)
cx,cy=900,315
d.ellipse((cx-198,cy-198,cx+198,cy+198),outline=gold,width=6)
bg.paste(ph,(cx-190,cy-190),mask)
F=lambda n,sz:ImageFont.truetype('C:/Windows/Fonts/'+n,sz)
d.rounded_rectangle((70,90,350,134),radius=22,outline=gold,width=2)
d.text((92,98),'Togo · Lomé',font=F('segoeui.ttf',26),fill=gold2)
d.text((70,170),'Pierre Kossi',font=F('georgiab.ttf',74),fill='white')
d.text((70,252),'DEGBOEVI',font=F('georgiab.ttf',74),fill='white')
d.line((70,360,230,360),fill=gold,width=4)
d.text((70,386),'Automatisation Excel/VBA',font=F('segoeuib.ttf',34),fill=gold2)
d.text((70,436),'Applications métier .NET/Blazor',font=F('segoeuib.ttf',34),fill=gold2)
d.text((70,540),'pierredegboevi.com',font=F('segoeui.ttf',30),fill=(255,255,255))
bg.save(os.path.join(root,'og-image.jpg'),quality=88,optimize=True)
print('ok')
