# Catalogue Génétiques Cannabis

Catalogue de génétiques cannabis : **190 fiches style Leafly** (arômes, terpènes,
effets, lignée, données de culture), photos et tips de culture.

## Structure
- `fiches/` — une fiche markdown par génétique (présentation style Leafly)
- `data/strains.json` — données structurées de toutes les génétiques
- `images/produits/` — photos de fleurs (Wikimedia Commons, CC — voir `images/CREDITS.md`)
- `images/culture/` — plantes en croissance, floraison, séchage
- `tips-culture/guide.md` — guide de culture indoor (FR)
- `produits-c3/` — produits C3 (Fleurons / Be Humble), contributions d'Alain
- `docs/` — site statique (recherche + fiches), prêt pour GitHub Pages
- `scripts/build.py` — régénère les fiches et le site depuis `data/strains.json`

## Données
Compilées de recherches sourcées (breeders officiels, Leafly, SeedFinder,
résultats de coupes 2020–2026, données SQDC). Les champs non publiés sont omis :
**rien n'est inventé**. Voir `docs/` → onglet « Méthode » du catalogue web pour
le détail des sources.

## Site web
Activez GitHub Pages sur le dossier `docs/` pour une version navigable avec
recherche, filtres et fiches détaillées.

## Contribuer
- Ajoutez vos photos dans `images/produits/` ou `images/culture/` (photos
  personnelles de préférence), avec crédit dans `images/CREDITS.md`.
- Complétez les fiches (lignée, specs) via pull request.
- Régénérez le site : `python3 scripts/build.py`.

© 2026 — Contenu original du repo sous licence CC BY-SA 4.0 sauf mention contraire.
Les photos restent sous leur licence d'origine (voir CREDITS.md).
