#!/usr/bin/env python3
"""Generate one page per apartment from tools/units.json.

Usage (from repo root):  python3 tools/build_units.py
Writes apartamentos/fracao-<id>/index.html and sitemap.xml.
"""
import html
import sys
import json
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legal_footer import legal_footer  # noqa: E402
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://ykcrown.com"
data = json.load(open(os.path.join(ROOT, "tools", "units.json"), encoding="utf-8"))
P = data["project"]
ALL_UNITS = data["units"]
UNITS = [x for x in ALL_UNITS if x.get("page", True) and (data["project"].get("show_status", True) or x["status"] != "sold")]

T = {
    "en": {
        "floor": lambda f: "Ground floor" if f == 0 else f"Floor {f}",
        "pos": {"front_left": "Front left", "rear_left": "Rear left", "rear_right": "Rear right", "front_right": "Front right"},
        "rooms": {"living": "Living room", "living_dining": "Living / dining", "kitchen": "Kitchen", "kitchenette": "Kitchenette",
                  "bed1": "Bedroom 1", "bed2": "Bedroom 2", "wc": "Bathroom", "wc1": "Bathroom 1", "wc2": "Bathroom 2",
                  "corridor": "Corridor", "hall": "Entrance hall", "balcony": "Balcony"},
        "k_type": "Type", "k_floor": "Floor", "k_pos": "Position", "k_au": "Usable area (Au)", "k_abp": "Gross private area (Abp)",
        "k_bal": "Balcony", "k_bed": "Bedrooms", "k_bath": "Bathrooms", "k_park": "Parking", "k_energy": "Energy class",
        "k_status": "Status", "st": {"available": "Available", "reserved": "Reserved", "sold": "Sold"}, "k_price": "Price", "on_request": "On request", "parking_inc": "1 space included (car lift)", "tbc": "To be confirmed", "energy_tbc": "Certificate in progress",
        "rooms_title": "Room areas", "plan_title": "Floor plan", "plan_soon": "Detailed floor plan available on request.",
        "pl": "Price list", "facts": "Key facts", "book": "Book a viewing", "wa": "WhatsApp", "others": "Other apartments",
        "back": "← All apartments", "indicative": "Areas are indicative and may change during the development of the project. Final values follow the approved technical documentation.",
        "photos": "Interiors", "photos_note": "Illustrative images (renders) of the development's finishes.",
        "about_t": "About Praça da Corujeira", "about_d": "A contemporary residential building on a tree-lined square in Campanhã, eastern Porto — ten apartments with generous glazing, timber accents and calm, functional interiors.",
        "lead": lambda u: f"{u['type']} apartment on {('the ground floor' if u['floor']==0 else 'floor ' + str(u['floor']))} of Praça da Corujeira, a new residential development by YK CROWN in Campanhã, Porto.",
    },
    "pt": {
        "floor": lambda f: "R/C" if f == 0 else f"{f}.º piso",
        "pos": {"front_left": "Frente esquerdo", "rear_left": "Traseiro esquerdo", "rear_right": "Traseiro direito", "front_right": "Frente direito"},
        "rooms": {"living": "Sala", "living_dining": "Sala / refeições", "kitchen": "Cozinha", "kitchenette": "Kitchenette",
                  "bed1": "Quarto 1", "bed2": "Quarto 2", "wc": "Casa de banho", "wc1": "Casa de banho 1", "wc2": "Casa de banho 2",
                  "corridor": "Corredor", "hall": "Hall de entrada", "balcony": "Varanda"},
        "k_type": "Tipologia", "k_floor": "Piso", "k_pos": "Posição", "k_au": "Área útil (Au)", "k_abp": "Área bruta privativa (Abp)",
        "k_bal": "Varanda", "k_bed": "Quartos", "k_bath": "Casas de banho", "k_park": "Estacionamento", "k_energy": "Classe energética",
        "k_status": "Estado", "st": {"available": "Disponível", "reserved": "Reservado", "sold": "Vendido"}, "k_price": "Preço", "on_request": "Sob consulta", "parking_inc": "1 lugar incluído (elevador de automóveis)", "tbc": "A confirmar", "energy_tbc": "Certificado em emissão",
        "rooms_title": "Áreas das divisões", "plan_title": "Planta", "plan_soon": "Planta detalhada disponível mediante pedido.",
        "pl": "Tabela de preços", "facts": "Características", "book": "Marcar visita", "wa": "WhatsApp", "others": "Outros apartamentos",
        "back": "← Todos os apartamentos", "indicative": "As áreas são indicativas e poderão sofrer alterações durante o desenvolvimento do projeto. Os valores finais seguem a documentação técnica aprovada.",
        "photos": "Interiores", "photos_note": "Imagens meramente ilustrativas (renders) dos acabamentos do empreendimento.",
        "about_t": "Sobre a Praça da Corujeira", "about_d": "Um edifício residencial contemporâneo numa praça arborizada em Campanhã, zona oriental do Porto — dez apartamentos com amplos envidraçados, apontamentos em madeira e interiores calmos e funcionais.",
        "lead": lambda u: f"Apartamento {u['type']} {('no R/C' if u['floor']==0 else 'no ' + str(u['floor']) + '.º piso')} da Praça da Corujeira, novo empreendimento residencial da YK CROWN em Campanhã, Porto.",
    },
    "zh": {
        "floor": lambda f: "地面层" if f == 0 else f"{f} 楼",
        "pos": {"front_left": "前侧左", "rear_left": "后侧左", "rear_right": "后侧右", "front_right": "前侧右"},
        "rooms": {"living": "客厅", "living_dining": "客厅 / 餐厅", "kitchen": "厨房", "kitchenette": "开放式厨房",
                  "bed1": "卧室 1", "bed2": "卧室 2", "wc": "卫生间", "wc1": "卫生间 1", "wc2": "卫生间 2",
                  "corridor": "走廊", "hall": "玄关", "balcony": "阳台"},
        "k_type": "户型", "k_floor": "楼层", "k_pos": "位置", "k_au": "套内使用面积（Au）", "k_abp": "套内建筑面积（Abp，含墙体）",
        "k_bal": "阳台", "k_bed": "卧室", "k_bath": "卫生间", "k_park": "车位", "k_energy": "能源等级",
        "k_status": "状态", "st": {"available": "可售", "reserved": "已预订", "sold": "已售"}, "k_price": "价格", "on_request": "价格面议", "parking_inc": "含 1 个车位（汽车升降机）", "tbc": "待确认", "energy_tbc": "证书办理中",
        "rooms_title": "各房间面积", "plan_title": "户型图", "plan_soon": "详细户型图可按需索取。",
        "pl": "获取价格表", "facts": "基本信息", "book": "预约看房", "wa": "WhatsApp", "others": "其他户型",
        "back": "← 全部户型", "indicative": "面积为参考数据，可能在项目开发过程中调整，最终以批准的技术文件为准。",
        "photos": "室内实景", "photos_note": "效果图，仅供参考。",
        "about_t": "关于 Praça da Corujeira", "about_d": "位于波尔图东部 Campanhã 一处绿树成荫广场上的现代住宅楼，共十套公寓，大面积玻璃、木质元素，室内安静实用。",
        "lead": lambda u: f"Praça da Corujeira {('地面层' if u['floor']==0 else str(u['floor']) + ' 楼')}的 {u['type']} 公寓，YK CROWN 在波尔图 Campanhã 开发的全新住宅项目。",
    },
}
LANGS = ["en", "pt", "zh"]
PHOTOS = [("living-room", "Living room"), ("kitchen", "Kitchen"), ("dining", "Dining area"),
          ("bedroom", "Bedroom"), ("bathroom", "Bathroom"), ("park-view", "Building")]

e = html.escape


def m2(v):
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " m²" if v is not None else None


def facts(u, L):
    t = T[L]
    rows = [
        ("k_type", u["type"]), ("k_floor", t["floor"](u["floor"])), ("k_pos", t["pos"][u["position"]]),
        ("k_au", m2(u["au"]) or t["tbc"]), ("k_abp", m2(u["abp"]) or t["tbc"]),
    ]
    if u["balcony"]:
        rows.append(("k_bal", m2(u["balcony"])))
    rows += [("k_bed", str(u["bedrooms"])), ("k_bath", str(u["bathrooms"])),
             ("k_park", t["parking_inc"] if u["parking"] == "included" else (u["parking"] or t["tbc"])), ("k_energy", u["energy"] or t["energy_tbc"]),
             ("k_price", u["price"] or t["on_request"])] + ([("k_status", t["st"][u["status"] or "available"])] if data["project"].get("show_status", True) else [])
    return rows


def i18n_blob(u):
    out = {}
    for L in LANGS:
        t = T[L]
        d = {k: t[k] for k in ["pl", "rooms_title", "plan_title", "plan_soon", "facts", "book", "wa", "others", "back",
                               "indicative", "photos", "photos_note", "about_t", "about_d"]}
        d["lead"] = t["lead"](u)
        d["sub"] = f"{t['floor'](u['floor'])} · {t['pos'][u['position']]}"
        for i, (k, v) in enumerate(facts(u, L)):
            d[f"fk{i}"] = t[k]
            d[f"fv{i}"] = v
        for i, (r, _) in enumerate(u["rooms"]):
            d[f"r{i}"] = t["rooms"][r]
        for o in UNITS:
            d[f"o_{o['id']}"] = f"{o['type']} · {t['floor'](o['floor'])}"
        out[L] = d
    return out


CSS = """:root{--navy:#0b1b2b;--gold:#c7a15a;--cream:#f5f3ee;--ink:#17212b;--muted:#6d7680;--line:#e7e3da}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.6}a{color:inherit;text-decoration:none}img{display:block;max-width:100%}
.nav{position:sticky;top:0;z-index:50;min-height:68px;padding:0 5vw;display:flex;align-items:center;justify-content:space-between;gap:16px;background:rgba(255,255,255,.95);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.logo{font-weight:800;letter-spacing:2.6px;font-size:18px}.logo span{color:var(--gold)}.navlinks{display:flex;gap:22px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#3e4852}.navlinks a:hover{color:var(--gold)}
.lang{display:flex;gap:6px}.lang button{border:1px solid var(--line);background:#fff;padding:6px 8px;font-size:11px;cursor:pointer}.lang button.active{background:var(--navy);color:#fff;border-color:var(--navy)}
.wrap{width:min(1180px,90vw);margin:auto}.crumb{font-size:12px;letter-spacing:.08em;color:var(--muted);padding:26px 0 0}.crumb a:hover{color:var(--gold)}
.head{padding:18px 0 34px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;border-bottom:1px solid var(--line)}
.kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);font-weight:700}h1{font-size:clamp(36px,6vw,64px);line-height:1;margin:10px 0 12px;letter-spacing:-.035em}.sub{font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.lead{font-size:18px;color:var(--muted);max-width:640px;margin:14px 0 0}.actions{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 22px;border:1px solid var(--navy);font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}.btn.primary{background:var(--navy);color:#fff}.btn.wa{border-color:#25d366;color:#128c4a}
.grid{display:grid;grid-template-columns:1.35fr .65fr;gap:48px;padding:44px 0 64px;align-items:start}
.plan{background:var(--cream);padding:14px;border:1px solid var(--line)}.plan img{width:100%;height:auto;cursor:zoom-in}.plan .soon{padding:80px 20px;text-align:center;color:var(--muted)}
h2{font-size:22px;letter-spacing:-.01em;margin:0 0 14px}.facts{width:100%;border-collapse:collapse;font-size:15px}.facts th,.facts td{padding:11px 0;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.facts th{font-weight:500;color:var(--muted);width:55%}.facts td{font-weight:600}
.rooms{margin-top:34px}.note{font-size:12px;color:#899097;margin-top:14px}
.photos{background:var(--cream);padding:64px 0}.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:20px}.pgrid img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}
.about{padding:64px 0;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}.about img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}
.others{padding:0 0 80px}.ogrid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:16px}.ogrid a{border:1px solid var(--line);padding:14px;display:block}.ogrid a:hover{border-color:var(--gold)}.ogrid strong{display:block;font-size:20px}.ogrid span{font-size:12px;color:var(--muted)}.ogrid a.cur{background:var(--navy);color:#fff;border-color:var(--navy)}.ogrid a.cur span{color:rgba(255,255,255,.7)}
footer{padding:36px 5vw;border-top:1px solid var(--line);font-size:12px;color:#747d84;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
@media(max-width:900px){.nav{flex-wrap:wrap;padding:12px 5vw}.navlinks{order:3;width:100%;overflow:auto;gap:16px;font-size:11px}.grid,.about{grid-template-columns:1fr;gap:32px}.ogrid{grid-template-columns:repeat(3,1fr)}.pgrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.ogrid{grid-template-columns:repeat(2,1fr)}.actions{width:100%}.actions .btn{flex:1}}"""


def page(u):
    L = "en"
    t = T[L]
    name = f"Fração {u['letter']}"
    title = f"{name} · {u['type']} · {t['floor'](u['floor'])} | Praça da Corujeira, Porto | YK CROWN"
    url = f"{SITE}/apartamentos/fracao-{u['id']}/"
    desc = (f"{name}, {u['type']} apartment at Praça da Corujeira, Campanhã, Porto"
            + (f" — {m2(u['au'])} usable area" if u["au"] else "") + ". Floor plan, room areas and viewings with YK CROWN.")
    img = f"../../assets/img/{u['plan']}" if u["plan"] else None
    rows = "".join(f'<tr><th data-i="fk{i}">{e(k_l)}</th><td data-i="fv{i}">{e(v)}</td></tr>'
                   for i, (k_l, v) in enumerate((t[k], v) for k, v in facts(u, L)))
    rrows = "".join(f'<tr><th data-i="r{i}">{e(t["rooms"][r])}</th><td>{e(m2(a))}</td></tr>' for i, (r, a) in enumerate(u["rooms"]))
    others = "".join(
        f'<a href="../fracao-{o["id"]}/"{" class=\"cur\" aria-current=\"page\"" if o["id"]==u["id"] else ""}><strong>{o["letter"]}</strong>'
        f'<span data-i="o_{o["id"]}">{e(o["type"])} · {e(t["floor"](o["floor"]))}</span></a>' for o in UNITS)
    photos = "".join(f'<img alt="{e(c)} — Praça da Corujeira" loading="lazy" decoding="async" src="../../assets/photos/thumb/{p}.webp" width="800" height="533"/>' for p, c in PHOTOS)
    plan_html = (f'<a href="{img}" target="_blank" rel="noopener"><img alt="{e(name)} {u["type"]} floor plan" src="{img}" width="2000" height="1250"/></a>'
                 if img else f'<div class="soon" data-i="plan_soon">{e(t["plan_soon"])}</div>')
    ld = {"@context": "https://schema.org", "@type": "Apartment", "name": f"{name} · {u['type']} — Praça da Corujeira",
          "url": url, "numberOfRooms": u["bedrooms"] + 1, "numberOfBedrooms": u["bedrooms"],
          "numberOfBathroomsTotal": u["bathrooms"],
          "address": {"@type": "PostalAddress", "streetAddress": P["street"], "addressLocality": P["locality"],
                      "addressRegion": P["region"], "addressCountry": P["country"]}}
    if u["au"]:
        ld["floorSize"] = {"@type": "QuantitativeValue", "value": u["au"], "unitCode": "MTK"}
    if img:
        ld["image"] = f"{SITE}/assets/img/{u['plan']}"
    unit_q = f"interest=Praca%20da%20Corujeira&unit=Fra%C3%A7%C3%A3o%20{u['letter']}%20({u['type']})"
    blob = json.dumps(i18n_blob(u), ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{e(title)}</title>
<meta content="{e(desc)}" name="description"/>
<meta content="#0b1b2b" name="theme-color"/>
<link href="{url}" rel="canonical"/>
<meta content="{e(name)} · {u['type']} — Praça da Corujeira, Porto" property="og:title"/>
<meta content="{e(desc)}" property="og:description"/>
<meta content="{SITE}/assets/img/{u['plan'] or '../photos/hero.webp'}" property="og:image"/><meta content="summary_large_image" name="twitter:card"/>
<meta content="website" property="og:type"/>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link href="../../assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="../../assets/site.css" rel="stylesheet"/>
<style>
{CSS}
</style>
</head>
<body>
<header class="nav">
<a class="logo" href="../../index.html">YK <span>CROWN</span></a>
<nav class="navlinks"><a href="../../index.html#overview">Praça da Corujeira</a><a href="../../index.html#floorplans">Plans</a><a href="../../progress.html">Progress</a><a href="../../about.html">About</a><a href="../../index.html#contact">Contact</a></nav>
<div class="lang"><button class="active" data-lang="en">EN</button><button data-lang="pt">PT</button><button data-lang="zh">中文</button></div>
</header>
<main class="wrap">
<div class="crumb"><a href="../../index.html#floorplans" data-i="back">{e(t['back'])}</a></div>
<section class="head"><div><div class="kicker">Praça da Corujeira · Porto</div><h1>{e(name)} · {u['type']}</h1><div class="sub" data-i="sub">{e(t['floor'](u['floor']))} · {e(t['pos'][u['position']])}</div><p class="lead" data-i="lead">{e(t['lead'](u))}</p></div>
<div class="actions"><a class="btn" data-i="pl" href="../../index.html#pricelist">{e(t['pl'])}</a><a class="btn primary" data-i="book" href="../../contact.html?{unit_q}">{e(t['book'])}</a><a class="btn wa" data-wa="{e(name)} ({u['type']}) — Praça da Corujeira" href="https://wa.me/351969058818" rel="noopener" target="_blank">WhatsApp</a></div></section>
<section class="grid"><div><h2 data-i="plan_title">{e(t['plan_title'])}</h2><div class="plan">{plan_html}</div></div>
<div><h2 data-i="facts">{e(t['facts'])}</h2><table class="facts">{rows}</table>
<div class="rooms"><h2 data-i="rooms_title">{e(t['rooms_title'])}</h2><table class="facts">{rrows}</table></div>
<p class="note" data-i="indicative">{e(t['indicative'])}</p></div></section>
</main>
<section class="photos"><div class="wrap"><h2 data-i="photos">{e(t['photos'])}</h2><p class="note" data-i="photos_note">{e(t['photos_note'])}</p><div class="pgrid">{photos}</div></div></section>
<section class="wrap about"><div><div class="kicker">YK CROWN</div><h2 data-i="about_t">{e(t['about_t'])}</h2><p class="lead" data-i="about_d">{e(t['about_d'])}</p><p class="note">{e(P['address'])}</p></div><img alt="Praça da Corujeira, Porto" loading="lazy" decoding="async" src="../../assets/photos/thumb/location.webp" width="800" height="533"/></section>
<section class="wrap others"><h2 data-i="others">{e(t['others'])}</h2><div class="ogrid">{others}</div></section>
<footer><span>© {date.today().year} YK CROWN, LDA · Portugal</span><span>{e(P['address'])}</span></footer>
{legal_footer('../../')}
<script>
const copy={blob};
function setLang(l){{if(!copy[l])return;document.documentElement.lang=l==="zh"?"zh-CN":l;document.querySelectorAll("[data-lang]").forEach(b=>b.classList.toggle("active",b.dataset.lang===l));document.querySelectorAll("[data-i]").forEach(el=>{{const v=copy[l][el.dataset.i];if(v)el.textContent=v}});try{{localStorage.setItem("yk_lang",l)}}catch(e){{}}}}
document.querySelectorAll("[data-lang]").forEach(b=>b.addEventListener("click",()=>setLang(b.dataset.lang)));
try{{const q=new URLSearchParams(location.search).get("lang")||localStorage.getItem("yk_lang")||((navigator.language||"").slice(0,2));if(q&&q!=="en")setLang(q)}}catch(e){{}}
</script>
<script defer src="../../assets/site.js"></script>
</body></html>
"""


def main():
    for u in UNITS:
        d = os.path.join(ROOT, "apartamentos", f"fracao-{u['id']}")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(u))
    import build_insights
    arts = build_insights.main()
    urls = ["", "about.html", "contact.html", "insights.html", "privacidade.html", "progress.html"] + [f"apartamentos/fracao-{u['id']}/" for u in UNITS]
    urls += [f"insights/{L}/{a['slug']}/" for a in arts for L in build_insights.LANGS]
    today = date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{today}</lastmod></url>\n" for p in urls)
    sm += "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
    print(f"built {len(UNITS)} unit pages + sitemap.xml")
    import build_home
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(build_home.page())
    print("built index.html")
    import build_pages
    open(os.path.join(ROOT, "about.html"), "w", encoding="utf-8").write(build_pages.about())
    open(os.path.join(ROOT, "progress.html"), "w", encoding="utf-8").write(build_pages.progress())
    for name, fn in [("contact.html", build_pages.contact), ("404.html", build_pages.not_found)]:
        open(os.path.join(ROOT, name), "w", encoding="utf-8").write(fn())
    print("built about, progress, contact, 404")


if __name__ == "__main__":
    main()
