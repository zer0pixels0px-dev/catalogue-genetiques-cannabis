# COMPILE_REPORT — scraping 2026-10-10

Compilé le 2026-10-10/11. Règles : aucune donnée inventée (absent = null) ;
les 4 MOM (marché gris) sont isolés dans `mom_gray_market.json` et exclus des fichiers propres.
Leafly (8 762) géré séparément — non touché.

## 1. strains_new.json — 190 strains
Sources : FastBuds (112) + GrowDiaries (82), hors Leafly, hors 4 MOM.
Déduplication par nom normalisé (minuscules, sans ponctuation) : 4 fusion(s) inter-sites.
Chaque strain garde `sources[]` (badge) ; les champs sont fusionnés en gardant la première valeur non-nulle.
Couverture : {'thc': 114, 'cbd': 107, 'breeder': 122, 'type': 128, 'image_url': 112, 'price': 112, 'flowering': 112, 'genetics': 94}
Limites :
- FastBuds : prix en USD (`price_currency`), `price_cad` laissé null (pas de taux de conversion vérifié appliqué) ;
  toutes les URLs produit sont `url_derived_from_image_filename: true` (1 cas validé, à re-vérifier avant usage public) ;
  THC complété via le catalogue fabricant sur Leafly quand absent (`thc_source: "leafly"`).
- GrowDiaries : 0 image_url (non exposées en texte), 0 prix (pas de vente), url/breeder/type seulement sur 17/11/17 fiches ;
  82 strains sur 8 108 annoncées (pagination JS inaccessible).
- Dédup stricte : « Ztrawberriez Auto » (FastBuds) et « Ztrawberriez » (GrowDiaries) restent séparées
  (pas de suppression devinée du suffixe « Auto »).

## 2. seeds.json — 112 offres
112 graines FastBuds (catalogue complet du site, cœur de métier).
Types : autoflowering 64, feminized 17, originals (autoflowering) 17, fastflowering 7,
1st edition (autoflowering) 5, cbd (autoflowering) 2.
`url_derived_from_image_filename: true` sur les 112 (même réserve que ci-dessus).
GrowDiaries /seeds et Leafly shop : sections observées mais non scrapées en JSON → rien d'ajouté.

## 3. breeders.json — 11 breeders
Uniques, avec `sources[]` et `strain_count` (nb de strains vues dans les JSON).
Fast Buds : 112 noms uniques (la fiche GrowDiaries « Purple Punch Auto » fusionne avec celle de FastBuds — une des 4 dédups). Royal Queen Seeds : mention du rapport /seeds
uniquement (`strain_count: null`, note explicite).
Marques-maison des MOM (WTF, Island Exclusive…) : exclues du fichier propre (marché gris).

## 4. nutrients.json — 5 entrées (marques)
Aucun produit nutriment scrapé en JSON (ni Leafly ~225 ni GrowDiaries) : le fichier contient les
5 marques citées dans le rapport GrowDiaries /nutrients, avec `url/price/image_url: null` et note explicite.
Ne pas présenter comme des produits.

## 5. equipment.json — 5 entrées (marques)
Idem : 5 marques du rapport GrowDiaries /equipment (toutes des marques d'éclairage/horticole),
aucun produit scrapé. `category` = "marque d'équipement de culture" (descriptif, pas une donnée produit).

## 6. mom_gray_market.json — 433 records
TOUS les records des 4 MOM : WTF Cannabis 275, BuyWeed247 56, CannaBlossom 45, Weed-Deals 57.
Chaque record porte `source` + `warning` : "Marché gris non licencié — ne pas afficher dans le catalogue public sans validation d'Alain".
Champs d'origine conservés tels quels (prix en CAD supposés, sites canadiens ; thc parfois en plage "19-21%").
CannaBlossom : 4 fiches « shroom » (psilocybine) incluses — signalées ici, à filtrer avant tout usage.
Weed-Deals : comestibles jusqu'à 9000 mg THC, chocolat psilocybine (constat du rapport).
À n'utiliser que sur validation explicite d'Alain.

## Fusions inter-sites (dédup)
- Garlic Mint Sherbet (GrowDiaries)
- Z42 (GrowDiaries)
- Gary Sherbet™ (GrowDiaries)
- Purple Punch Auto (GrowDiaries)
