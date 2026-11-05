"""Génère en/index.html à partir de index.html (source de vérité, FR + attributs data-en).
Usage : python _build/build-en.py   (à relancer après toute modification de index.html)"""
import re, os, json, sys
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(os.path.join(root,'index.html'),encoding='utf-8').read()

# 1. textes : remplace le contenu des éléments portant data-en
open_re=re.compile(r'<([a-z0-9]+)((?:\s[^>]*?)?)\sdata-en="([^"]*)"([^>]*)>')
out=[];pos=0
while True:
    m=open_re.search(s,pos)
    if not m: out.append(s[pos:]);break
    tag=m.group(1)
    out.append(s[pos:m.start()])
    out.append('<%s%s%s>'%(tag,m.group(2),m.group(4)))
    # cherche la balise fermante correspondante (même nom, imbrication gérée)
    depth=1;i=m.end()
    tok=re.compile(r'<(/?)%s(?=[\s>/])[^>]*>'%tag)
    while depth:
        t=tok.search(s,i)
        if not t: sys.exit('balise non fermée : '+tag)
        depth+= -1 if t.group(1) else 1
        i=t.end()
    close_start=t.start()
    out.append(m.group(3))
    pos=close_start
s=''.join(out)

# 2. liens alternatifs (WhatsApp, mailto)
def href(m):
    t=m.group(0)
    en=re.search(r'\sdata-href-en="([^"]*)"',t).group(1)
    t=re.sub(r'\sdata-href-en="[^"]*"','',t)
    return re.sub(r'\shref="[^"]*"',' href="%s"'%en,t,count=1)
s=re.sub(r'<a\s[^>]*data-href-en="[^"]*"[^>]*>',href,s)

# 3. aria-label
def lab(m):
    t=m.group(0)
    en=re.search(r'\sdata-en-label="([^"]*)"',t).group(1)
    t=re.sub(r'\sdata-en-label="[^"]*"','',t)
    return re.sub(r'\saria-label="[^"]*"',' aria-label="%s"'%en,t,count=1)
s=re.sub(r'<[a-z]+\s[^>]*data-en-label="[^"]*"[^>]*>',lab,s)

# 4. tête de page
EN_TITLE='Pierre Kossi DEGBOEVI — Automation &amp; business applications | Togo'
EN_TITLE_SHORT='Pierre Kossi DEGBOEVI — Automation &amp; business applications'
EN_DESC='Pierre Kossi DEGBOEVI (pierredegboevi.com), IT engineer in Togo: Excel/VBA automation, .NET/Blazor business applications and IT support for small businesses.'
def sub(a,b,count=1):
    global s
    assert a in s,a
    s=s.replace(a,b) if count==0 else s.replace(a,b,count)
sub('<html lang="fr">','<html lang="en">')
sub('<title>Pierre Kossi DEGBOEVI — Automatisation & applications métier | Togo</title>','<title>%s</title>'%EN_TITLE.replace('&amp;','&'))
s=re.sub(r'(<meta name="description" content=")[^"]*"',lambda m:m.group(1)+EN_DESC+'"',s,count=1)
sub('<link rel="canonical" href="https://pierredegboevi.com/">','<link rel="canonical" href="https://pierredegboevi.com/en/">')
sub('<meta property="og:url" content="https://pierredegboevi.com/">','<meta property="og:url" content="https://pierredegboevi.com/en/">')
s=re.sub(r'(<meta property="og:title" content=")[^"]*"',lambda m:m.group(1)+EN_TITLE_SHORT+'"',s,count=1)
s=re.sub(r'(<meta property="og:description" content=")[^"]*"',lambda m:m.group(1)+EN_DESC+'"',s,count=1)
s=re.sub(r'(<meta name="twitter:title" content=")[^"]*"',lambda m:m.group(1)+EN_TITLE_SHORT+'"',s,count=1)
s=re.sub(r'(<meta name="twitter:description" content=")[^"]*"',lambda m:m.group(1)+EN_DESC+'"',s,count=1)
ALT='Pierre Kossi DEGBOEVI, IT engineer in Lomé: automation and business applications'
s=re.sub(r'(<meta property="og:image:alt" content=")[^"]*"',lambda m:m.group(1)+ALT+'"',s,count=1)
s=re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*"',lambda m:m.group(1)+ALT+'"',s,count=1)
sub('<meta property="og:locale" content="fr_FR">','<meta property="og:locale" content="en_US">')
sub('<meta property="og:locale:alternate" content="en_US">','<meta property="og:locale:alternate" content="fr_FR">')
# JSON-LD
def ld(m):
    d=json.loads(m.group(1))
    if d['@type']=='Person':
        d['jobTitle']='IT engineer'
        d['description']='IT engineer in Togo: Excel/VBA automation, .NET/Blazor business applications and IT support for small businesses.'
        d['url']='https://pierredegboevi.com/en/'
    else:
        d['url']='https://pierredegboevi.com/en/'
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False,separators=(',',':'))+'</script>'
s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',ld,s)

# 5. sélecteur de langue : EN actif
s=s.replace('<a class="on" href="/" hreflang="fr" lang="fr" aria-label="Français" aria-current="true">FR</a>','<a href="/" hreflang="fr" lang="fr" aria-label="Français">FR</a>')
s=s.replace('<a href="/en/" hreflang="en" lang="en" aria-label="English">EN</a>','<a class="on" href="/en/" hreflang="en" lang="en" aria-label="English" aria-current="true">EN</a>')

# 5b. textes alternatifs des images
ALTS={
'Capture du site Élixir du Terroir : logo, slogan « L’essence pure de la tradition » et photo des préparations de la marque':'Screenshot of the Élixir du Terroir website: logo, tagline “L’essence pure de la tradition” and a photo of the brand’s preparations',
'Capture du site BrendaSTYLE : portrait de Brenda en robe noire dans une arche, titre « La femme qui rayonne » et boutons Voir la collection et Notre histoire':'Screenshot of the BrendaSTYLE website: portrait of Brenda in a black dress under an arch, headline “La femme qui rayonne” and buttons View the collection and Our story',
'Capture du site Dongshoes : logo Dong, mocassins bicolores en cuir sur du bois, devise « Ambition, excellence, audace » et bouton Commander sur WhatsApp':'Screenshot of the Dongshoes website: Dong logo, two-tone leather loafers on wood, motto “Ambition, excellence, audace” and an Order on WhatsApp button',
'Capture du site JonasClean':'Screenshot of the JonasClean website',
'Tableau de bord de CimentStock : ventes du jour, crédits clients, stock et dernières ventes':'CimentStock dashboard: daily sales, customer credit, stock and latest sales',
'Trois écrans d’ASSIMETO : liste de courses, plats réalisables et fiche recette':'Three ASSIMETO screens: shopping list, dishes you can cook and recipe card',
'Logo Pierre Kossi DEGBOEVI':'Pierre Kossi DEGBOEVI logo',
}
for fr,en in ALTS.items():
    a='alt="%s"'%fr
    if a not in s: sys.exit('alt introuvable : '+fr)
    s=s.replace(a,'alt="%s"'%en)

# 6. chemins relatifs des fichiers (la page vit dans /en/)
def rel(m):
    return '%s="../%s"'%(m.group(1),m.group(2))
s=re.sub(r'\b(src|href)="((?:[A-Za-z0-9_-]+)\.(?:jpg|jpeg|png|webp|svg|ico))"',rel,s)
assert 'data-en' not in s.replace('data-en-label','') or True
left=re.findall(r'data-(?:href-)?en[a-z-]*=',s)
if left: sys.exit('attributs restants : %s'%left[:5])
os.makedirs(os.path.join(root,'en'),exist_ok=True)
open(os.path.join(root,'en','index.html'),'w',encoding='utf-8',newline='\n').write(s)
print('en/index.html',len(s),'octets')
