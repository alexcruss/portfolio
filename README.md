# Portfolio — Pierre Kossi DEGBOEVI

Site personnel : automatisation Excel/VBA, applications métier .NET/Blazor et accompagnement IT pour les PME au Togo.

**En ligne : [pierredegboevi.com](https://pierredegboevi.com/)**

## Contenu

- Présentation et services
- Réalisations clients : Élixir du Terroir, BrendaSTYLE, JonasClean
- Applications métier : CimentStock, ASSIMETO
- Contact

## Technique

Site statique en HTML, CSS et JavaScript, sans framework, hébergé sur GitHub Pages.

## Version anglaise

`index.html` est la source (français + textes anglais dans les attributs `data-en`). La page `en/index.html` est générée : après toute modification, lancer

```
python _build/build-en.py
```

`python _build/make-og.py` régénère l'image de partage `og-image.jpg` (1200×630).
