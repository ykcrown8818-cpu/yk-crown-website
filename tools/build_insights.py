#!/usr/bin/env python3
"""Build the Insights (news) section from content/insights/*.json.

Each JSON file is one approved article, written by the n8n publish workflow:
{
  "id": "<news_item uuid>", "slug": "2026-10-30-portugal-tourist-stays", "date": "2026-10-30",
  "topic": "tourism",
  "source": {"name": "INE", "url": "https://...", "published_at": "2026-10-30T11:00:00+00:00"},
  "pt": {"headline", "lead", "body", "yk_observation", "seo_title", "seo_description"},
  "en": {...}, "zh": {...}
}
Output: insights/<lang>/<slug>/index.html for pt/en/zh, the insights.html hub, and
insights/feed.json (used by the sitemap). Run: python3 tools/build_insights.py
"""
import glob
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import CSS, NAV, shell  # noqa: E402
from legal_footer import legal_footer  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://ykcrown.com"
LANGS = ["pt", "en", "zh"]
e = html.escape

TOPICS = {
    "real_estate": {"pt": "Imobiliário", "en": "Real estate", "zh": "房地产"},
    "housing_policy": {"pt": "Política de habitação", "en": "Housing policy", "zh": "住房政策"},
    "construction": {"pt": "Construção", "en": "Construction", "zh": "建筑业"},
    "tourism": {"pt": "Turismo", "en": "Tourism", "zh": "旅游"},
    "finance": {"pt": "Finanças", "en": "Finance", "zh": "金融"},
    "economy": {"pt": "Economia", "en": "Economy", "zh": "经济"},
    "investment_policy": {"pt": "Investimento", "en": "Investment", "zh": "投资政策"},
}
UI = {
    "pt": {"obs": "Observação YK CROWN", "src": "Fonte", "orig": "Ver original", "pub": "Publicado",
           "note": "Artigo redigido com apoio de inteligência artificial a partir da fonte indicada e revisto pela equipa YK CROWN antes da publicação. Informação geral; não constitui aconselhamento de investimento, jurídico ou fiscal.",
           "more": "Mais artigos", "all": "Todos os artigos", "cta_k": "Praça da Corujeira · Porto",
           "cta_t": "Apartamentos novos T0–T2 em Campanhã", "cta_d": "Classe energética A+, garagem incluída, entrega prevista em fevereiro de 2028.",
           "cta_b": "Pedir tabela de preços", "months": "jan fev mar abr mai jun jul ago set out nov dez"},
    "en": {"obs": "YK CROWN view", "src": "Source", "orig": "View original", "pub": "Published",
           "note": "This article was drafted with the help of artificial intelligence from the source cited and reviewed by the YK CROWN team before publication. General information only; not investment, legal or tax advice.",
           "more": "More articles", "all": "All articles", "cta_k": "Praça da Corujeira · Porto",
           "cta_t": "New T0–T2 apartments in Campanhã", "cta_d": "Energy class A+, parking included, delivery planned for February 2028.",
           "cta_b": "Get the price list", "months": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec"},
    "zh": {"obs": "YK CROWN 观察", "src": "来源", "orig": "查看原文", "pub": "发布",
           "note": "本文由人工智能根据所注明的来源辅助撰写，并经 YK CROWN 编辑团队审核后发布。仅供一般参考，不构成投资、法律或税务建议。",
           "more": "更多文章", "all": "全部文章", "cta_k": "Praça da Corujeira · 波尔图",
           "cta_t": "Campanhã 全新公寓 T0–T2", "cta_d": "能源等级 A+，每套含车位，预计 2028 年 2 月交房。",
           "cta_b": "索取价格表", "months": ""},
}
HTML_LANG = {"pt": "pt-PT", "en": "en", "zh": "zh-CN"}
ART_CSS = """.art{max-width:760px;margin:auto;padding:56px 0 30px}.art .meta{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700}
.art h1{font-size:clamp(30px,4.6vw,48px);line-height:1.12;letter-spacing:-.03em;margin:14px 0 18px;text-wrap:balance}
.art .lede{font-size:20px;line-height:1.55;color:#33404c;margin:0 0 26px}.art .body p{font-size:17.5px;line-height:1.75;margin:0 0 20px}
.obs{border-left:3px solid var(--gold);background:var(--cream);padding:20px 24px;margin:30px 0}.obs strong{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--navy);margin-bottom:6px}.obs p{margin:0;font-size:16.5px}
.srcbox{font-size:14px;color:var(--muted);border-top:1px solid var(--line);padding-top:18px;margin-top:30px}.srcbox a{color:var(--navy);text-decoration:underline}
.aibox{font-size:12.5px;color:#7c848b;margin-top:12px}
.ctabox{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;background:var(--navy);color:#fff;padding:28px;margin:36px 0 0}.ctabox .k{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#e3c37e;font-weight:700}.ctabox h3{margin:6px 0 4px;font-size:21px}.ctabox p{margin:0;color:rgba(255,255,255,.75);font-size:14.5px}
.alist{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}.acard{background:#fff;border:1px solid var(--line);padding:24px;display:flex;flex-direction:column;gap:10px}.acard:hover{border-color:var(--gold)}
.acard .meta{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700}.acard h3{margin:0;font-size:18px;line-height:1.3}.acard p{margin:0;color:var(--muted);font-size:14.5px}
@media(max-width:980px){.alist{grid-template-columns:1fr 1fr}}@media(max-width:640px){.alist{grid-template-columns:1fr}.art{padding-top:36px}.art .lede{font-size:18px}}"""


def load():
    arts = []
    for f in glob.glob(os.path.join(ROOT, "content", "insights", "*.json")):
        a = json.load(open(f, encoding="utf-8"))
        if not re.fullmatch(r"[a-z0-9-]{8,120}", a.get("slug", "")):
            raise SystemExit(f"bad slug in {f}")
        for L in LANGS:
            if not a.get(L, {}).get("headline") or not a[L].get("body"):
                raise SystemExit(f"{f}: missing {L} headline/body")
        arts.append(a)
    arts.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    return arts


def fdate(d, L):
    y, m, dd = d[:10].split("-")
    if L == "zh":
        return f"{y} 年 {int(m)} 月 {int(dd)} 日"
    mon = UI[L]["months"].split()[int(m) - 1]
    return f"{int(dd)} {mon} {y}"


def url(a, L):
    return f"/insights/{L}/{a['slug']}/"


def paras(text):
    return "".join(f"<p>{e(p.strip())}</p>" for p in re.split(r"\n\s*\n|\n", text or "") if p.strip())


def nav(L, alt):
    n = NAV[L]
    links = [("/#apartments", "nav_apts"), ("/progress.html", "nav_progress"), ("/about.html", "nav_about"), ("/#contact", "nav_contact")]
    a = "".join(f'<a href="{h}?lang={L}">{e(n[k])}</a>' for h, k in links)
    lang = "".join(f'<a class="{"active" if x == L else ""}" hreflang="{HTML_LANG[x]}" href="{alt[x]}">{ {"pt": "PT", "en": "EN", "zh": "中文"}[x]}</a>' for x in LANGS)
    return (f'<header class="nav"><a class="logo" href="/?lang={L}">YK <span>CROWN</span></a><nav class="navlinks">{a}'
            f'<a class="cur" href="/insights.html?lang={L}">{e(n["nav_news"])}</a></nav><div class="lang">{lang}</div>'
            f'<a class="btn navy sm" href="/?lang={L}#contact">{e(n["cta_visit"])}</a></header>')


def card(a, L):
    x = a[L]
    t = TOPICS.get(a.get("topic"), {}).get(L, "")
    return (f'<a class="acard" href="{url(a, L)}"><div class="meta">{e(t)}{" · " if t else ""}{e(fdate(a["date"], L))}</div>'
            f'<h3>{e(x["headline"])}</h3><p>{e(x["lead"])}</p></a>')


def article(a, L, arts):
    x, u = a[L], UI[L]
    alt = {k: url(a, k) for k in LANGS}
    canon = SITE + url(a, L)
    hreflang = "".join(f'<link rel="alternate" hreflang="{HTML_LANG[k]}" href="{SITE + alt[k]}"/>' for k in LANGS)
    hreflang += f'<link rel="alternate" hreflang="x-default" href="{SITE + alt["en"]}"/>'
    title = x.get("seo_title") or x["headline"]
    desc = x.get("seo_description") or x["lead"]
    topic = TOPICS.get(a.get("topic"), {}).get(L, "")
    src = a.get("source", {})
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": x["headline"][:110], "description": desc,
          "datePublished": a["date"], "inLanguage": HTML_LANG[L], "mainEntityOfPage": canon,
          "image": [SITE + "/assets/photos/location-porto.webp"],
          "author": {"@type": "Organization", "name": "YK CROWN"},
          "publisher": {"@type": "Organization", "name": "YK CROWN, LDA", "url": SITE}}
    if src.get("url"):
        ld["isBasedOn"] = src["url"]
    more = [b for b in arts if b["slug"] != a["slug"]][:3]
    more_html = f'<section class="alt"><div class="wrap"><h2>{e(u["more"])}</h2><div class="alist">{"".join(card(b, L) for b in more)}</div><p style="margin-top:22px"><a class="btn" href="/insights.html?lang={L}">{e(u["all"])}</a></p></div></section>' if more else ""
    obs = f'<div class="obs"><strong>{e(u["obs"])}</strong><p>{e(x["yk_observation"])}</p></div>' if x.get("yk_observation") else ""
    srcline = e(src.get("name", ""))
    if src.get("url"):
        srcline += f' · <a href="{e(src["url"])}" rel="nofollow noopener" target="_blank">{e(u["orig"])}</a>'
    if src.get("published_at"):
        srcline += f' · {e(fdate(src["published_at"], L))}'
    utm = f"utm_source=insights&utm_medium=article&utm_campaign=corujeira&utm_content={a['slug'][:60]}"
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[L]}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{e(title)} | YK CROWN Insights</title>
<meta content="{e(desc)}" name="description"/>
<meta content="#0b1b2b" name="theme-color"/>
<link href="{canon}" rel="canonical"/>{hreflang}
<meta content="article" property="og:type"/><meta content="{e(title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/>
<meta content="{canon}" property="og:url"/><meta content="{SITE}/assets/photos/location-porto.webp" property="og:image"/><meta content="summary_large_image" name="twitter:card"/>
<link href="/assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="/assets/site.css" rel="stylesheet"/>
<style>
{CSS}
{ART_CSS}
.lang a{{border:1px solid var(--line);background:#fff;padding:5px 7px;font-size:11px}}.lang a.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{nav(L, alt)}
<main>
<article class="wrap art">
<div class="meta">{e(topic)}{" · " if topic else ""}{e(u["pub"])} {e(fdate(a["date"], L))}</div>
<h1>{e(x["headline"])}</h1>
<p class="lede">{e(x["lead"])}</p>
<div class="body">{paras(x["body"])}</div>
{obs}
<div class="srcbox"><strong>{e(u["src"])}:</strong> {srcline}<div class="aibox">{e(u["note"])}</div></div>
<div class="ctabox"><div><div class="k">{e(u["cta_k"])}</div><h3>{e(u["cta_t"])}</h3><p>{e(u["cta_d"])}</p></div><a class="btn gold" href="/?lang={L}&amp;{utm}#pricelist">{e(u["cta_b"])}</a></div>
</article>
{more_html}
</main>
<footer><span>© 2026 YK CROWN, LDA · Porto</span><span><a href="/">Praça da Corujeira</a> · <a href="/progress.html">Progress</a> · <a href="/about.html">About</a> · <a href="/insights.html">Insights</a></span></footer>
{legal_footer('/')}
<script>try{{localStorage.setItem("yk_lang","{L}")}}catch(e){{}}</script>
<script defer src="/assets/site.js"></script>
</body></html>
"""


HUB = {
    "en": {"i_kicker": "Insights", "i_title": "Porto & Portugal property news", "i_text": "Housing prices, construction, tourism and interest rates: the official data that matters for buyers and investors, explained in English, Portuguese and Chinese.",
           "i_empty": "The first articles will be published here shortly."},
    "pt": {"i_kicker": "Insights", "i_title": "Notícias do imobiliário no Porto e em Portugal", "i_text": "Preços da habitação, construção, turismo e taxas de juro: os dados oficiais que interessam a compradores e investidores, em português, inglês e chinês.",
           "i_empty": "Os primeiros artigos serão publicados aqui em breve."},
    "zh": {"i_kicker": "市场资讯", "i_title": "波尔图与葡萄牙房产资讯", "i_text": "房价、建筑、旅游和利率——用中文、英文和葡萄牙语解读对买家和投资者有用的官方数据。",
           "i_empty": "第一批文章即将在这里发布。"},
}


def hub(arts):
    """insights.html: cards in all three languages, switched by the site's language buttons."""
    c = {L: {**NAV[L], **HUB[L]} for L in NAV}
    for i, a in enumerate(arts[:60]):
        for L in LANGS:
            c[L][f"a{i}m"] = (TOPICS.get(a.get("topic"), {}).get(L, "") + " · " if a.get("topic") in TOPICS else "") + fdate(a["date"], L)
            c[L][f"a{i}h"] = a[L]["headline"]
            c[L][f"a{i}l"] = a[L]["lead"]
            c[L][f"a{i}u"] = url(a, L)
    t = lambda k: e(c["en"][k])  # noqa: E731
    cards = "".join(
        f'<a class="acard" data-u="a{i}u" href="{url(a, "en")}"><div class="meta" data-i="a{i}m">{t(f"a{i}m")}</div>'
        f'<h3 data-i="a{i}h">{t(f"a{i}h")}</h3><p data-i="a{i}l">{t(f"a{i}l")}</p></a>' for i, a in enumerate(arts[:60]))
    if not cards:
        cards = f'<div class="card"><p data-i="i_empty">{t("i_empty")}</p></div>'
    body = f"""<div class="phero" style="--img:url('assets/photos/location-porto.webp')"><div class="wrap">
<div class="kicker" data-i="i_kicker">{t('i_kicker')}</div><h1 data-i="i_title">{t('i_title')}</h1><p data-i="i_text">{t('i_text')}</p></div></div>
<section><div class="wrap"><div class="alist">{cards}</div></div></section>
<script>document.addEventListener("click",function(ev){{var a=ev.target.closest("a[data-u]");if(!a)return;var l=document.documentElement.lang.slice(0,2);var v=(copy[l]||{{}})[a.dataset.u];if(v)a.href=v}},true)</script>"""
    out = shell("insights", "Insights | Porto & Portugal property news | YK CROWN",
                "News and official data on Porto and Portuguese real estate, construction and tourism, in English, Portuguese and Chinese.",
                "insights.html", body, c, "insights.html")
    return out.replace("</style>", ART_CSS + "\n</style>", 1)


def main():
    import shutil
    arts = load()
    slugs = {a["slug"] for a in arts}
    for L in LANGS:  # drop pages of articles that were un-published
        d = os.path.join(ROOT, "insights", L)
        if os.path.isdir(d):
            for s in os.listdir(d):
                if s not in slugs:
                    shutil.rmtree(os.path.join(d, s))
    for L in LANGS:
        for a in arts:
            d = os.path.join(ROOT, "insights", L, a["slug"])
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(article(a, L, arts))
    open(os.path.join(ROOT, "insights.html"), "w", encoding="utf-8").write(hub(arts))
    os.makedirs(os.path.join(ROOT, "insights"), exist_ok=True)
    feed = [{"slug": a["slug"], "date": a["date"], "urls": {L: url(a, L) for L in LANGS}} for a in arts]
    json.dump(feed, open(os.path.join(ROOT, "insights", "feed.json"), "w"), ensure_ascii=False, indent=0)
    print(f"built {len(arts)} articles x {len(LANGS)} languages + insights.html")
    return arts


if __name__ == "__main__":
    main()
