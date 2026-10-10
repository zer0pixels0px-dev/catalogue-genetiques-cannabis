#!/usr/bin/env python3
"""Génère le repo catalogue-genetiques-cannabis :
- fiches/<slug>.md : fiche style Leafly par génétique
- docs/ : site statique (index.html + data + assets) prêt pour GitHub Pages
- README.md, tips-culture/guide.md, produits-c3/fleurs-sechees.md
"""
import json, os, re, shutil, html as ihtml

ROOT = os.path.expanduser("~/workspace/genetiques-site")
DATA = os.path.join(ROOT, "data", "strains.json")
DOCS = os.path.join(ROOT, "docs")

CAT_FR = {"catalogue": "Catalogue", "champion": "Championne", "classique": "Classique",
          "reference": "Référence", "landrace": "Landrace", "perso": "Perso"}
WMC_URLS = json.load(open(os.path.expanduser("~/workspace/wmc_urls.json")))
def _wmc(t): return WMC_URLS[t]["url"]
SPECIFIC_PHOTOS = {
    "wedding-cake": _wmc("File:Wedding Cake Cannabis Strain.jpg"),
    "sour-diesel": _wmc("File:Cannabis (Sour Diesel) Flower.jpg"),
    "do-si-dos": _wmc("File:Dosidos Cannabis Strain, grown by Archive.jpg"),
    "presidential-kush": _wmc("File:Presidential Kush Cannabis Strain.jpg"),
}
DEFAULT_PHOTO = _wmc("File:Cannabis bloom.JPG")
CULTURE_PHOTOS = [
    ("Floraison", _wmc("File:Flowering Cannabis Plants.JPG")),
    ("Plante en floraison", _wmc("File:Flowering cannabis plant.jpg")),
    ("Stade végétatif", _wmc("File:Untrained cannabis plant in the vegetative stage.jpg")),
    ("Jeune plant", _wmc("File:Small cannabis plant growing.jpg")),
    ("Séchage", _wmc("File:Cannabis drying room.jpg")),
    ("Pieds mères", _wmc("File:Mother plants in flower.jpg")),
    ("Serre", _wmc("File:Cannabis flowering in a greenhouse.jpg")),
    ("Début floraison", _wmc("File:Blooming cannabis plant by My 420 Tours.jpg")),
]

def esc(t):
    return ihtml.escape(str(t)) if t is not None else ""

def photo_for(s, for_docs=False):
    """Retourne (src, credit). Toutes les images sont hotlinkées (Wikimedia CC ou Leafly)."""
    pu = s.get("photo_url")
    if pu and pu.startswith("http"):
        return pu, "© Leafly — photo d'illustration" if "leafly" in pu else "Wikimedia Commons — CC"
    if s["slug"] in SPECIFIC_PHOTOS:
        return SPECIFIC_PHOTOS[s["slug"]], "Wikimedia Commons — CC BY-SA"
    return DEFAULT_PHOTO, ""

def md_section(title, body):
    return f"## {title}\n\n{body}\n\n" if body and body != "—" else ""

def fiche_md(s):
    src, credit = photo_for(s, for_docs=False)
    L = [f"# {s['name']}\n"]
    if src:
        L.append(f"![{s['name']}]({src})")
        if credit: L.append(f"\n*{credit}*\n")
    meta = []
    if s.get("type"): meta.append(f"**Type :** {s['type']}" + (f" ({s['dominance']})" if s.get("dominance") else ""))
    if s.get("breeder"): meta.append(f"**Breeder :** {s['breeder']}")
    if s.get("thc"): meta.append(f"**THC :** {s['thc']}")
    if s.get("cbd"): meta.append(f"**CBD :** {s['cbd']}")
    if meta: L.append("\n" + " | ".join(meta) + "\n")
    if s.get("description"): L.append(f"\n{s['description']}\n")
    if s.get("lineage"):
        v = " ✓ vérifiée" if s.get("lineage_verified") else " (à confirmer)"
        L.append(md_section("Lignée", f"{s['lineage']}{v}"))
    if s.get("aromas"): L.append(md_section("Arômes", ", ".join(s["aromas"])))
    if s.get("effects"): L.append(md_section("Effets", ", ".join(s["effects"])))
    if s.get("terpenes"): L.append(md_section("Terpènes dominants", ", ".join("`" + t + "`" for t in s["terpenes"])))
    cult = []
    if s.get("flowering_days"):
        _fd = s["flowering_days"]
        _sfx = "" if re.search(r"(jour|semaine|week|day)", _fd, re.I) else " jours"
        cult.append(f"- **Floraison :** {_fd}{_sfx}")
    if s.get("yield"): cult.append(f"- **Rendement :** {s['yield']}")
    if s.get("stretch"): cult.append(f"- **Stretch :** {s['stretch']}")
    if s.get("pm_resistance"): cult.append(f"- **Résistance moisissures :** {s['pm_resistance']}")
    if s.get("wash_pct"): cult.append(f"- **Lavage hash :** {s['wash_pct']}")
    if s.get("rosin_pct"): cult.append(f"- **Rosin :** {s['rosin_pct']}")
    if cult: L.append(md_section("Culture", "\n".join(cult)))
    if s.get("grow_tips"): L.append(md_section("Tips de culture", "\n".join(f"- {t}" for t in s["grow_tips"])))
    if s.get("awards"): L.append(md_section("Palmarès", "\n".join(f"- {a}" for a in s["awards"])))
    if s.get("bag_appeal"): L.append(md_section("Bag appeal", s["bag_appeal"]))
    if s.get("sources"): L.append(md_section("Sources", "\n".join(f"- {u}" for u in s["sources"])))
    L.append(f"\n*Catégorie : {CAT_FR.get(s.get('category'), s.get('category'))} — fiche générée le 2026-10-09.*\n")
    return "\n".join(L)

def md_to_html(md):
    out, in_list = [], False
    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>"); in_list = False
    for line in md.split("\n"):
        if line.startswith("### "):
            close_list(); out.append(f"<h3>{esc(line[4:])}</h3>")
        elif line.startswith("## "):
            close_list(); out.append(f"<h2>{esc(line[3:])}</h2>")
        elif line.startswith("# "):
            close_list(); out.append(f"<h2>{esc(line[2:])}</h2>")
        elif line.startswith("- "):
            if not in_list: out.append("<ul>"); in_list = True
            item = re.sub(r"\*\*(.+?)\*\*", r"<strong>\\1</strong>", esc(line[2:]))
            out.append(f"<li>{item}</li>")
        elif line.strip() == "":
            close_list()
        else:
            close_list()
            line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\\1</strong>", esc(line))
            out.append(f"<p>{line}</p>")
    close_list()
    return "\n".join(out)

INDEX_HTML = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catalogue Génétiques Cannabis</title>
<style>
:root{--bg:#0f1f16;--card:#16281c;--card2:#1d3325;--txt:#eef4ec;--mut:#a9bfa9;--acc:#7bc96f;--gold:#e8b64c;--line:#2a4232}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{position:sticky;top:0;z-index:20;background:#0c1a12f2;border-bottom:1px solid var(--line);padding:14px 18px}
header h1{margin:0 0 10px;font-size:1.35rem;letter-spacing:.3px}
header h1 span{color:var(--acc)}
.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.controls input[type=search]{flex:1;min-width:200px;padding:10px 14px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--txt);font-size:1rem}
.controls select{padding:10px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--txt)}
nav.tabs{display:flex;gap:6px;padding:10px 18px;flex-wrap:wrap;border-bottom:1px solid var(--line);background:#0c1a12}
nav.tabs button{background:none;border:1px solid var(--line);color:var(--mut);padding:8px 14px;border-radius:20px;cursor:pointer;font-size:.9rem}
nav.tabs button.on{background:var(--acc);color:#0c1a12;border-color:var(--acc);font-weight:700}
main{padding:18px;max-width:1200px;margin:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;cursor:pointer;transition:transform .12s}
.card:hover{transform:translateY(-3px);border-color:var(--acc)}
.card img{width:100%;height:150px;object-fit:cover;display:block;background:#0a140e}
.card .b{padding:12px}
.card h3{margin:0 0 6px;font-size:1.02rem}
.badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px}
.badge{font-size:.72rem;padding:3px 9px;border-radius:12px;background:var(--card2);border:1px solid var(--line);color:var(--mut)}
.badge.indica{background:#3b2a5e;color:#d9c8ff}.badge.sativa{background:#5e2f1a;color:#ffc890}.badge.hybrid{background:#1e4d2b;color:#a9e6b8}
.badge.cat{border-color:var(--gold);color:var(--gold)}
.card .br{font-size:.82rem;color:var(--mut)}
#modal{position:fixed;inset:0;background:#000a;display:none;z-index:50;overflow-y:auto;padding:20px}
#modal.open{display:block}
.sheet{max-width:760px;margin:20px auto;background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.sheet img.hero{width:100%;max-height:340px;object-fit:cover;display:block}
.sheet .pad{padding:22px}
.sheet h2{margin:.2em 0}
.kv{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0}
.kv div{background:var(--card2);border-radius:10px;padding:10px 12px}
.kv small{color:var(--mut);display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.5px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
.chip{background:var(--card2);border:1px solid var(--line);padding:6px 12px;border-radius:16px;font-size:.88rem}
.sec{margin:18px 0}.sec h4{margin:0 0 8px;color:var(--acc);font-size:.85rem;text-transform:uppercase;letter-spacing:1px}
.close{position:sticky;top:10px;float:right;margin:10px;background:var(--card2);border:1px solid var(--line);color:var(--txt);border-radius:50%;width:36px;height:36px;cursor:pointer;font-size:1.1rem;z-index:2}
table.c3{width:100%;border-collapse:collapse;font-size:.9rem}
table.c3 th,table.c3 td{border:1px solid var(--line);padding:8px 10px;text-align:left}
table.c3 th{background:var(--card2)}
.tips h2{color:var(--acc)}.tips h3{margin-top:1.4em}
.count{color:var(--mut);font-size:.85rem;margin:4px 0 12px}
</style></head>
<body>
<header><h1>🌿 Catalogue <span>Génétiques Cannabis</span></h1>
<div class="controls">
<input type="search" id="q" placeholder="Rechercher (nom, breeder, terpène…)">
<select id="fcat"><option value="">Toutes catégories</option></select>
<select id="ftype"><option value="">Tous types</option><option>Indica</option><option>Sativa</option><option>Hybrid</option></select>
<select id="sort"><option value="name">Tri : A–Z</option><option value="cat">Tri : catégorie</option></select>
</div></header>
<nav class="tabs">
<button class="on" data-t="strains">Génétiques</button>
<button data-t="c3">Produits C3</button>
<button data-t="tips">Tips culture</button>
<button data-t="about">À propos</button>
</nav>
<main>
<section id="t-strains"><div class="count" id="count"></div><div class="grid" id="grid"></div></section>
<section id="t-c3" hidden>__C3__</section>
<section id="t-tips" hidden><div class="tips">__TIPS__</div></section>
<section id="t-about" hidden>__ABOUT__</section>
</main>
<div id="modal"><div class="sheet" id="sheet"></div></div>
<script>
const FALLBACK="__FALLBACK__";
let DATA=[];
const $=id=>document.getElementById(id);
const CAT={catalogue:"Catalogue",champion:"Championne",classique:"Classique",reference:"Référence",landrace:"Landrace",perso:"Perso"};
function typeBadge(t){t=(t||"").toLowerCase();if(t.includes("indica"))return"indica";if(t.includes("sativa"))return"sativa";if(t.includes("hybrid"))return"hybrid";return"";}
function photo(s){
  let src=s._img||FALLBACK;
  if(/^https?:/.test(src))return{src:src,ext:1};
  return{src:src,ext:0};
}
function card(s){
  const p=photo(s),tb=typeBadge(s.type);
  return `<div class="card" data-slug="${s.slug}">
    <img loading="lazy" src="${p.src}" onerror="this.onerror=null;this.src='${FALLBACK}'" alt="${s.name}">
    <div class="b"><div class="badges">
      ${s.type?`<span class="badge ${tb}">${s.type}</span>`:""}
      <span class="badge cat">${CAT[s.category]||s.category||""}</span>
    </div><h3>${s.name}</h3><div class="br">${s.breeder||""}</div></div></div>`;
}
function render(){
  const q=$("q").value.toLowerCase(),fc=$("fcat").value,ft=$("ftype").value,so=$("sort").value;
  let r=DATA.filter(s=>{
    const hay=(s.name+" "+(s.breeder||"")+" "+(s.terpenes||[]).join(" ")+" "+(s.aromas||[]).join(" ")).toLowerCase();
    return (!q||hay.includes(q))&&(!fc||s.category===fc)&&(!ft||(s.type||"").toLowerCase().includes(ft.toLowerCase()));
  });
  r.sort((a,b)=>so==="cat"?(a.category+a.name).localeCompare(b.category+b.name):a.name.localeCompare(b.name));
  $("count").textContent=r.length+" génétique(s)";
  $("grid").innerHTML=r.map(card).join("");
  document.querySelectorAll(".card").forEach(c=>c.onclick=()=>openSheet(c.dataset.slug));
}
function sec(t,inner){return inner?`<div class="sec"><h4>${t}</h4>${inner}</div>`:"";}
function chips(a){return a&&a.length?`<div class="chips">${a.map(x=>`<span class="chip">${x}</span>`).join("")}</div>`:"";}
function openSheet(slug){
  const s=DATA.find(x=>x.slug===slug);if(!s)return;
  const p=photo(s),tb=typeBadge(s.type);
  const kv=[["Breeder",s.breeder],["Lignée",s.lineage+((s.lineage_verified&&s.lineage)?" ✓":"")],
    ["Floraison",s.flowering_days?s.flowering_days+((/jour|semaine|week|day/i.test(s.flowering_days))?"":" jours"):null],["Rendement",s.yield],
    ["Stretch",s.stretch],["THC",s.thc],["CBD",s.cbd],["Lavage hash",s.wash_pct]].filter(x=>x[1]);
  $("sheet").innerHTML=`<button class="close" onclick="document.getElementById('modal').classList.remove('open')">✕</button>
  <img class="hero" src="${p.src}" onerror="this.onerror=null;this.src='${FALLBACK}'" alt="${s.name}">
  <div class="pad"><div class="badges">${s.type?`<span class="badge ${tb}">${s.type}</span>`:""}
  <span class="badge cat">${CAT[s.category]||""}</span></div>
  <h2>${s.name}</h2>
  ${s.description?`<p style="color:var(--mut)">${s.description}</p>`:""}
  <div class="kv">${kv.map(x=>`<div><small>${x[0]}</small>${x[1]}</div>`).join("")}</div>
  ${sec("Arômes",chips(s.aromas))}${sec("Effets",chips(s.effects))}${sec("Terpènes dominants",chips(s.terpenes))}
  ${sec("Tips de culture",s.grow_tips&&s.grow_tips.length?`<ul>${s.grow_tips.map(t=>`<li>${t}</li>`).join("")}</ul>`:"")}
  ${sec("Palmarès",s.awards&&s.awards.length?`<ul>${s.awards.map(t=>`<li>${t}</li>`).join("")}</ul>`:"")}
  ${sec("Sources",s.sources&&s.sources.length?`<ul>${s.sources.map(u=>`<li><a style="color:var(--acc)" href="${u}" target="_blank" rel="noopener">${u}</a></li>`).join("")}</ul>`:"")}
  </div>`;
  $("modal").classList.add("open");$("modal").scrollTop=0;
}
$("modal").addEventListener("click",e=>{if(e.target.id==="modal")e.target.classList.remove("open");});
document.querySelectorAll("nav.tabs button").forEach(b=>b.onclick=()=>{
  document.querySelectorAll("nav.tabs button").forEach(x=>x.classList.remove("on"));b.classList.add("on");
  ["strains","c3","tips","about"].forEach(t=>$("t-"+t).hidden=t!==b.dataset.t);
});
Promise.all([fetch("data/strains-1.json"),fetch("data/strains-2.json")]).then(rs=>Promise.all(rs.map(r=>r.json()))).then(ps=>{const d=[...ps[0],...ps[1]];
  DATA=d.map(s=>({...s,_img:photoSrc(s)}));
  const cats=[...new Set(DATA.map(s=>s.category))];
  $("fcat").innerHTML='<option value="">Toutes catégories</option>'+cats.map(c=>`<option value="${c}">${CAT[c]||c}</option>`).join("");
  render();
});
function photoSrc(s){
  if(s.photo_url&&/^https?:/.test(s.photo_url))return s.photo_url;
  const sp=__SPECIFIC_JS__;
  return sp[s.slug]||FALLBACK;
}
["q","fcat","ftype","sort"].forEach(id=>$(id).addEventListener("input",render));
</script></body></html>
"""

C3_HTML = """<h2>Produits C3 — Fleurons / Be Humble</h2>
<p style="color:var(--mut)">Données partagées par Alain (C3 Solutions Innovantes). Contributions photos bienvenues.</p>
<table class="c3"><tr><th>Année</th><th>Marque</th><th>Collection</th><th>Variété</th><th>Type</th><th>THC</th><th>Format</th><th>Notes</th></tr>
<tr><td>2023</td><td>Fleurons</td><td>Menu Dessert</td><td>Grape Galena</td><td>Sativa</td><td>26–29,5 %</td><td>3,5 g</td><td>Très populaire</td></tr>
<tr><td>2023</td><td>Fleurons</td><td>Menu Dessert</td><td>Mike Tai</td><td>Sativa</td><td>28–28,5 %</td><td>3,5 g</td><td></td></tr>
<tr><td>2023</td><td>Fleurons</td><td>Micro QC</td><td>Kali Sunset</td><td>Hybrid</td><td>~29,8 %</td><td>3,5 g</td><td></td></tr>
<tr><td>2023</td><td>Fleurons</td><td>Micro QC</td><td>Mac-1</td><td>Hybrid</td><td>~27 %</td><td>3,5 g</td><td></td></tr>
<tr><td>2023</td><td>Be Humble.</td><td>Champs Verdoyants</td><td>Jet Fuel Cake</td><td>Sativa</td><td>~28,2 %</td><td>3,5 g</td><td></td></tr>
</table>"""

ABOUT_HTML = """<h2>À propos</h2>
<p>Catalogue de génétiques cannabis : fiches style Leafly (arômes, terpènes, effets, lignée, culture), photos et tips de culture.</p>
<p><strong>Données :</strong> compilées de recherches sourcées (breeders officiels, Leafly, SeedFinder, résultats de coupes 2020–2026). Les champs non publiés sont omis — rien n'est inventé.</p>
<p><strong>Images :</strong> Wikimedia Commons (Creative Commons, crédits dans <em>images/CREDITS.md</em>) et liens Leafly avec attribution.</p>
<p><strong>Contribuer :</strong> ajoutez vos photos de culture dans <em>images/</em> et complétez les fiches via pull request.</p>
<h3>En culture — galerie (Wikimedia Commons, CC)</h3>
<div class="grid">__GALLERY__</div>"""

def build():
    strains = json.load(open(os.path.join(ROOT,"data","strains-1.json"))) + json.load(open(os.path.join(ROOT,"data","strains-2.json")))
    # 1. fiches markdown
    fiches = os.path.join(ROOT, "fiches")
    os.makedirs(fiches, exist_ok=True)
    for s in strains:
        open(os.path.join(fiches, s["slug"] + ".md"), "w").write(fiche_md(s))
    # 2. docs/
    os.makedirs(DOCS, exist_ok=True)
    shutil.copy(DATA, os.path.join(DOCS, "data_strains_tmp.json")) if False else None
    dd = os.path.join(DOCS, "data"); os.makedirs(dd, exist_ok=True)
    shutil.copy(os.path.join(ROOT,"data","strains-1.json"), os.path.join(dd, "strains-1.json"))
    shutil.copy(os.path.join(ROOT,"data","strains-2.json"), os.path.join(dd, "strains-2.json"))
    da = os.path.join(DOCS, "assets")
    if os.path.exists(da): shutil.rmtree(da)
    os.makedirs(da, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "images", "CREDITS.md"), os.path.join(da, "CREDITS.md"))
    tips_md = open(os.path.join(ROOT, "tips-culture", "guide.md")).read()
    gallery = "\n".join(
        f'<div class="card"><img loading="lazy" src="{u}" alt="{n}"><div class="b"><div class="br">{n}</div></div></div>'
        for n, u in CULTURE_PHOTOS)
    about = ABOUT_HTML.replace("__GALLERY__", gallery)
    spec_js = json.dumps(SPECIFIC_PHOTOS, ensure_ascii=False)
    page = (INDEX_HTML.replace("__C3__", C3_HTML).replace("__TIPS__", md_to_html(tips_md))
            .replace("__ABOUT__", about).replace("__FALLBACK__", DEFAULT_PHOTO)
            .replace("__SPECIFIC_JS__", spec_js))
    open(os.path.join(DOCS, "index.html"), "w").write(page)
    open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    print(f"fiches: {len(strains)}, index.html OK, assets copiés")

if __name__ == "__main__":
    build()
