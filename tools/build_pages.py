#!/usr/bin/env python3
"""Generate about.html and progress.html (construction progress). Run: python3 tools/build_pages.py"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legal_footer import legal_footer  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

NAV = {
    "en": {"nav_apts": "Apartments", "nav_gallery": "Gallery", "nav_progress": "Progress", "nav_about": "About", "nav_contact": "Contact", "cta_visit": "Book a viewing"},
    "pt": {"nav_apts": "Apartamentos", "nav_gallery": "Galeria", "nav_progress": "Obra", "nav_about": "Sobre nós", "nav_contact": "Contacto", "cta_visit": "Marcar visita"},
    "zh": {"nav_apts": "在售公寓", "nav_gallery": "图库", "nav_progress": "工程进度", "nav_about": "关于我们", "nav_contact": "联系我们", "cta_visit": "预约看房"},
}

CSS = """:root{--navy:#0b1b2b;--gold:#c7a15a;--cream:#f5f3ee;--ink:#17212b;--muted:#5f6973;--line:#e7e3da}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:72px}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.6}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%;height:auto}.wrap{width:min(1180px,90vw);margin:auto}
.nav{position:sticky;top:0;z-index:50;height:68px;padding:0 5vw;display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.logo{font-weight:800;letter-spacing:2.6px;font-size:18px;white-space:nowrap}.logo span{color:var(--gold)}
.navlinks{display:flex;gap:22px;font-size:13px;color:#3e4852;margin-left:auto}.navlinks a:hover,.navlinks a.cur{color:var(--gold)}
.lang{display:flex;gap:4px}.lang button{border:1px solid var(--line);background:#fff;padding:5px 7px;font-size:11px;cursor:pointer;font:inherit;font-size:11px}.lang button.active{background:var(--navy);color:#fff;border-color:var(--navy)}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:13px 20px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--navy);white-space:nowrap}.btn.navy{background:var(--navy);color:#fff}.btn.gold{background:var(--gold);border-color:var(--gold);color:var(--navy)}.btn.sm{padding:9px 14px;font-size:12px}
.phero{color:#fff;background:linear-gradient(90deg,rgba(5,16,27,.85),rgba(5,16,27,.35)),var(--img) center/cover;padding:120px 0 70px}
.kicker{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-weight:700}.phero .kicker{color:#e3c37e}
h1{font-size:clamp(38px,6vw,72px);line-height:1;margin:14px 0 16px;letter-spacing:-.04em}.phero p{font-size:clamp(17px,2vw,20px);max-width:640px;color:rgba(255,255,255,.88);margin:0}
section{padding:80px 0}.alt{background:var(--cream)}h2{font-size:clamp(28px,3.6vw,44px);line-height:1.1;letter-spacing:-.03em;margin:10px 0 14px}.lead{font-size:17px;color:var(--muted);max-width:720px;margin:0}
.two{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}.two img{width:100%;aspect-ratio:4/3;object-fit:cover}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:32px}.card{background:#fff;border:1px solid var(--line);padding:28px}.card .n{font-size:13px;color:var(--gold);font-weight:700;letter-spacing:.1em}.card h3{margin:10px 0 6px;font-size:19px}.card p{margin:0;color:var(--muted);font-size:15px}
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:30px;border-top:1px solid var(--line)}.facts div{padding:18px 18px 0 0}.facts span{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}.facts strong{font-size:22px}
.proj{display:grid;grid-template-columns:1.2fr .8fr;background:var(--navy);color:#fff;margin-top:32px}.proj img{width:100%;height:100%;object-fit:cover;aspect-ratio:3/2}.proj .c{padding:44px}.proj .c p{color:rgba(255,255,255,.75)}.proj .tag{display:inline-block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;border:1px solid var(--gold);color:#e3c37e;padding:4px 10px}
.timeline{list-style:none;padding:0;margin:36px 0 0;display:grid;grid-template-columns:repeat(7,1fr);gap:0;counter-reset:s}
.timeline li{position:relative;padding:34px 12px 0 0;font-size:14px;color:var(--muted)}.timeline li::before{content:"";position:absolute;top:10px;left:0;right:0;height:3px;background:var(--line)}
.timeline li::after{content:"";position:absolute;top:2px;left:0;width:19px;height:19px;border-radius:50%;background:#fff;border:3px solid var(--line)}
.timeline li.done::before,.timeline li.current::before{background:var(--gold)}.timeline li.done::after{background:var(--gold);border-color:var(--gold)}.timeline li.current::after{background:#fff;border-color:var(--gold);box-shadow:0 0 0 5px rgba(199,161,90,.25)}
.timeline strong{display:block;color:var(--ink);font-size:15px;margin-bottom:2px}.timeline li.current strong{color:var(--navy)}.timeline .st{font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700}.timeline li.done .st,.timeline li.current .st{color:var(--gold)}
.log{margin-top:30px;display:grid;gap:22px}.entry{background:#fff;border:1px solid var(--line);padding:26px}.entry time{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700}.entry p{margin:8px 0 0;font-size:16px}
.entry .ph{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}.entry .ph img{aspect-ratio:4/3;object-fit:cover;width:100%}
.note{font-size:12px;color:#899097;margin-top:14px}.ctab{background:var(--navy);color:#fff}.ctab .lead{color:rgba(255,255,255,.75)}.ctab .in{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
footer{padding:26px 5vw;font-size:12px;color:#747d84;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;border-top:1px solid var(--line)}
@media(max-width:980px){.navlinks{display:none}.two,.proj{grid-template-columns:1fr;gap:32px}.cards{grid-template-columns:1fr 1fr}.facts{grid-template-columns:1fr 1fr}.timeline{grid-template-columns:repeat(4,1fr);row-gap:24px}}
@media(max-width:640px){.nav{gap:10px}.nav .btn{display:none}.lang{margin-left:auto}section{padding:56px 0}.cards{grid-template-columns:1fr}.proj .c{padding:28px}
.timeline{grid-template-columns:1fr;row-gap:0}.timeline li{padding:0 0 22px 34px}.timeline li::before{top:0;bottom:0;left:8px;right:auto;width:3px;height:auto}.timeline li::after{top:0}.entry .ph{grid-template-columns:1fr 1fr}}"""


def shell(page, title, desc, canonical, body, copy, cur):
    t = lambda k: e(copy["en"][k])  # noqa: E731
    links = [("index.html#apartments", "nav_apts"), ("index.html#gallery", "nav_gallery"),
             ("progress.html", "nav_progress"), ("about.html", "nav_about"), ("index.html#contact", "nav_contact")]
    nav = "".join(f'<a{" class=cur" if h == cur else ""} data-i="{k}" href="{h}">{t(k)}</a>' for h, k in links)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{e(title)}</title>
<meta content="{e(desc)}" name="description"/>
<meta content="#0b1b2b" name="theme-color"/>
<link href="https://ykcrown.com/{canonical}" rel="canonical"/>
<meta content="{e(title)}" property="og:title"/><meta content="{e(desc)}" property="og:description"/>
<meta content="https://ykcrown.com/assets/photos/hero.webp" property="og:image"/>
<link href="assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="assets/site.css" rel="stylesheet"/>
<style>
{CSS}
</style>
</head>
<body>
<header class="nav">
<a class="logo" href="index.html">YK <span>CROWN</span></a>
<nav class="navlinks">{nav}</nav>
<div class="lang"><button class="active" data-lang="en">EN</button><button data-lang="pt">PT</button><button data-lang="zh">中文</button></div>
<a class="btn navy sm" data-i="cta_visit" href="index.html#contact">{t('cta_visit')}</a>
</header>
<main>
{body}
</main>
<footer><span>© 2026 YK CROWN, LDA · Porto</span><span><a href="index.html">Praça da Corujeira</a> · <a href="progress.html">Progress</a> · <a href="about.html">About</a> · <a href="insights.html">Insights</a></span></footer>
{legal_footer('')}
<script>
const copy={json.dumps(copy, ensure_ascii=False)};
function setLang(l){{if(!copy[l])return;document.documentElement.lang=l==="zh"?"zh-CN":l;document.querySelectorAll("[data-lang]").forEach(b=>b.classList.toggle("active",b.dataset.lang===l));document.querySelectorAll("[data-i]").forEach(el=>{{const v=copy[l][el.dataset.i];if(v)el.textContent=v}});try{{localStorage.setItem("yk_lang",l)}}catch(e){{}}}}
document.querySelectorAll("[data-lang]").forEach(b=>b.addEventListener("click",()=>setLang(b.dataset.lang)));
try{{const q=new URLSearchParams(location.search).get("lang")||localStorage.getItem("yk_lang")||((navigator.language||"").slice(0,2));if(q&&q!=="en")setLang(q)}}catch(e){{}}
</script>
<script defer src="assets/site.js"></script>
</body></html>
"""


# ---------------- About ----------------
ABOUT = {
    "en": {
        "a_kicker": "About YK CROWN", "a_title": "Real estate development in Porto",
        "a_text": "YK CROWN, LDA is a Portuguese real estate development company. We buy, design and build residential projects. Construction is carried out by our own construction company, so one group is responsible from the first sketch to the handover of keys.",
        "w_kicker": "What we do", "w_title": "From site to keys, under one company",
        "w_text": "Development and construction are in the same hands, so buyers deal with one responsible group from reservation to deed — with no outside contractor in between.",
        "c1_t": "Site & planning", "c1_d": "Selecting well-located plots and taking projects through municipal licensing.",
        "c2_t": "Design", "c2_d": "Working with architects and engineers on efficient layouts, natural light and high energy performance.",
        "c3_t": "Our own construction", "c3_d": "Built by our own construction company — direct control of the works, materials and quality, with regular updates for buyers.",
        "c4_t": "Sales & aftercare", "c4_d": "Direct sales with no intermediaries, clear documentation and support after handover.",
        "c5_t": "Energy efficiency", "c5_d": "New buildings designed for energy class A+: lower running costs and better comfort.",
        "c6_t": "Three languages", "c6_d": "We work with Portuguese and international buyers in Portuguese, English and Chinese.",
        "p_kicker": "Current project", "p_tag": "Under construction", "p_title": "Praça da Corujeira, Porto",
        "p_text": "18 new apartments — T0, T1 and T2 — on a tree-lined square in Campanhã, each with a parking space and energy class A+. Delivery planned for February 2028.",
        "p_btn": "See the apartments", "p_btn2": "Construction progress",
        "f_units": "Apartments", "f_floors": "Floors above ground", "f_energy": "Energy class", "f_deliv": "Delivery", "f_deliv_v": "Feb 2028",
        "k_kicker": "Our commitments", "k_title": "What buyers can expect",
        "k1_t": "Clear information", "k1_d": "Areas from the approved architecture project, published for every apartment.",
        "k2_t": "Regular updates", "k2_d": "Construction progress is published on this website so buyers can follow the works.",
        "k3_t": "One point of contact", "k3_d": "Questions are answered directly by YK CROWN, by email, phone or WhatsApp.",
        "co_kicker": "Company", "co_title": "Company details",
        "ct_title": "Talk to us", "ct_text": "Ask for the price list or book a viewing of Praça da Corujeira.", "ct_btn": "Contact us",
    },
    "pt": {
        "a_kicker": "Sobre a YK CROWN", "a_title": "Promoção imobiliária no Porto",
        "a_text": "A YK CROWN, LDA é uma empresa portuguesa de promoção imobiliária. Adquirimos, projetamos e construímos empreendimentos residenciais. A obra é executada pela nossa própria empresa de construção, pelo que um só grupo é responsável do primeiro esboço até à entrega das chaves.",
        "w_kicker": "O que fazemos", "w_title": "Do terreno às chaves, numa só empresa",
        "w_text": "Promoção e construção estão nas mesmas mãos: o comprador tem um único grupo responsável, da reserva à escritura, sem empreiteiros externos pelo meio.",
        "c1_t": "Terreno e licenciamento", "c1_d": "Seleção de lotes bem localizados e acompanhamento do licenciamento municipal.",
        "c2_t": "Projeto", "c2_d": "Trabalho com arquitetos e engenheiros em plantas eficientes, luz natural e elevado desempenho energético.",
        "c3_t": "Construção própria", "c3_d": "Obra executada pela nossa própria empresa de construção — controlo direto dos trabalhos, materiais e qualidade, com atualizações regulares.",
        "c4_t": "Venda e pós-venda", "c4_d": "Venda direta sem intermediários, documentação clara e apoio depois da entrega.",
        "c5_t": "Eficiência energética", "c5_d": "Edifícios novos pensados para a classe energética A+: menos custos e mais conforto.",
        "c6_t": "Três idiomas", "c6_d": "Trabalhamos com compradores portugueses e internacionais em português, inglês e chinês.",
        "p_kicker": "Projeto atual", "p_tag": "Em construção", "p_title": "Praça da Corujeira, Porto",
        "p_text": "18 apartamentos novos — T0, T1 e T2 — numa praça arborizada em Campanhã, todos com lugar de garagem e classe energética A+. Entrega prevista para fevereiro de 2028.",
        "p_btn": "Ver apartamentos", "p_btn2": "Acompanhar a obra",
        "f_units": "Apartamentos", "f_floors": "Pisos acima do solo", "f_energy": "Classe energética", "f_deliv": "Entrega", "f_deliv_v": "Fev. 2028",
        "k_kicker": "Os nossos compromissos", "k_title": "O que o comprador pode esperar",
        "k1_t": "Informação clara", "k1_d": "Áreas do projeto de arquitetura aprovado, publicadas para cada fração.",
        "k2_t": "Atualizações regulares", "k2_d": "O avanço da obra é publicado neste site, para que os compradores possam acompanhar.",
        "k3_t": "Um único interlocutor", "k3_d": "As questões são respondidas diretamente pela YK CROWN, por email, telefone ou WhatsApp.",
        "co_kicker": "Empresa", "co_title": "Dados da empresa",
        "ct_title": "Fale connosco", "ct_text": "Peça a tabela de preços ou marque uma visita à Praça da Corujeira.", "ct_btn": "Contactar",
    },
    "zh": {
        "a_kicker": "关于 YK CROWN", "a_title": "波尔图房地产开发",
        "a_text": "YK CROWN, LDA 是一家葡萄牙房地产开发公司。我们负责购地、设计和建造住宅项目，施工由我们自己的建筑公司完成，从第一张草图到交付钥匙，都由同一个集团负责。",
        "w_kicker": "我们做什么", "w_title": "从土地到钥匙，一家公司负责到底",
        "w_text": "开发和施工由同一个集团负责，买家从预订到过户只需面对一方，中间没有外包施工方。",
        "c1_t": "选地与审批", "c1_d": "挑选位置优越的地块，负责完成市政建筑审批。",
        "c2_t": "设计", "c2_d": "与建筑师和工程师合作，追求合理户型、充足采光和高能效。",
        "c3_t": "自有施工团队", "c3_d": "由我们自己的建筑公司施工，直接把控工程、材料和质量，并定期向买家更新进度。",
        "c4_t": "销售与售后", "c4_d": "开发商直销，没有中间商，文件清楚，交房后继续提供服务。",
        "c5_t": "节能", "c5_d": "新建楼按能源等级 A+ 设计，使用成本更低，居住更舒适。",
        "c6_t": "三种语言", "c6_d": "用葡萄牙语、英语和中文为本地及国际买家服务。",
        "p_kicker": "在建项目", "p_tag": "施工中", "p_title": "Praça da Corujeira，波尔图",
        "p_text": "位于 Campanhã 绿树广场旁的 18 套全新公寓，户型 T0、T1、T2，每套含车位，能源等级 A+，预计 2028 年 2 月交房。",
        "p_btn": "查看公寓", "p_btn2": "工程进度",
        "f_units": "公寓", "f_floors": "地上楼层", "f_energy": "能源等级", "f_deliv": "交房", "f_deliv_v": "2028 年 2 月",
        "k_kicker": "我们的承诺", "k_title": "买家可以期待什么",
        "k1_t": "信息透明", "k1_d": "每套公寓的面积均来自已批准的建筑设计图纸，并在网上公开。",
        "k2_t": "定期更新", "k2_d": "工程进度会在本网站发布，买家可以随时查看施工情况。",
        "k3_t": "专人对接", "k3_d": "所有问题都由 YK CROWN 直接通过邮件、电话或 WhatsApp 回复。",
        "co_kicker": "公司", "co_title": "公司信息",
        "ct_title": "联系我们", "ct_text": "索取 Praça da Corujeira 价格表或预约看房。", "ct_btn": "联系我们",
    },
}


def about():
    c = {L: {**NAV[L], **ABOUT[L]} for L in NAV}
    t = lambda k: e(c["en"][k])  # noqa: E731
    cards = "".join(f'<div class="card"><div class="n">0{i}</div><h3 data-i="c{i}_t">{t(f"c{i}_t")}</h3><p data-i="c{i}_d">{t(f"c{i}_d")}</p></div>' for i in range(1, 7))
    commits = "".join(f'<div class="card"><h3 data-i="k{i}_t">{t(f"k{i}_t")}</h3><p data-i="k{i}_d">{t(f"k{i}_d")}</p></div>' for i in range(1, 4))
    body = f"""<div class="phero" style="--img:url('assets/photos/front-through-trees.webp')"><div class="wrap">
<div class="kicker" data-i="a_kicker">{t('a_kicker')}</div><h1 data-i="a_title">{t('a_title')}</h1><p data-i="a_text">{t('a_text')}</p></div></div>
<section><div class="wrap">
<div class="kicker" data-i="w_kicker">{t('w_kicker')}</div><h2 data-i="w_title">{t('w_title')}</h2><p class="lead" data-i="w_text">{t('w_text')}</p>
<div class="cards">{cards}</div></div></section>
<section class="alt"><div class="wrap">
<div class="kicker" data-i="p_kicker">{t('p_kicker')}</div>
<div class="proj"><img alt="Praça da Corujeira, Porto" loading="lazy" src="assets/photos/hero.webp" width="1920" height="1280"/>
<div class="c"><span class="tag" data-i="p_tag">{t('p_tag')}</span><h2 data-i="p_title">{t('p_title')}</h2><p data-i="p_text">{t('p_text')}</p>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px"><a class="btn gold" data-i="p_btn" href="index.html#apartments">{t('p_btn')}</a><a class="btn" style="border-color:rgba(255,255,255,.6);color:#fff" data-i="p_btn2" href="progress.html">{t('p_btn2')}</a></div></div></div>
<div class="facts"><div><span data-i="f_units">{t('f_units')}</span><strong>18</strong></div><div><span data-i="f_floors">{t('f_floors')}</span><strong>5</strong></div><div><span data-i="f_energy">{t('f_energy')}</span><strong>A+</strong></div><div><span data-i="f_deliv">{t('f_deliv')}</span><strong data-i="f_deliv_v">{t('f_deliv_v')}</strong></div></div>
</div></section>
<section><div class="wrap">
<div class="kicker" data-i="k_kicker">{t('k_kicker')}</div><h2 data-i="k_title">{t('k_title')}</h2>
<div class="cards">{commits}</div></div></section>
<section class="alt"><div class="wrap two">
<div><div class="kicker" data-i="co_kicker">{t('co_kicker')}</div><h2 data-i="co_title">{t('co_title')}</h2>
<p class="lead"><strong>YK CROWN, LDA</strong><br/>NIPC 514037555<br/>Licença de obras n.º NUD/679095/2025/CMP (Câmara Municipal do Porto)<br/>Rua Fontes Pereira de Melo 22B<br/>2720-233 Amadora, Portugal<br/><a href="mailto:info@ykcrown.com">info@ykcrown.com</a> · <a href="tel:+351969058818">+351 969 058 818</a></p></div>
<img alt="Praça da Corujeira, Porto" loading="lazy" src="assets/photos/thumb/location.webp" width="800" height="533"/></div></section>
<section class="ctab"><div class="wrap in"><div><h2 data-i="ct_title">{t('ct_title')}</h2><p class="lead" data-i="ct_text">{t('ct_text')}</p></div>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn gold" data-i="ct_btn" href="index.html#contact">{t('ct_btn')}</a><a class="btn" style="border-color:rgba(255,255,255,.6);color:#fff" data-wa="YK CROWN" href="https://wa.me/351969058818" rel="noopener" target="_blank">WhatsApp</a></div></div></section>"""
    return shell("about", "About YK CROWN | Real estate development in Porto",
                 "YK CROWN, LDA is a Portuguese real estate development company building new energy-efficient homes in Porto.",
                 "about.html", body, c, "about.html")


# ---------------- Progress ----------------
STAGES = {
    "en": {"licence": "Licensing", "demolition": "Demolition & levelling", "site": "Site enclosure & foundations", "structure": "Structure", "envelope": "Façade & roof",
           "interiors": "Interiors & finishes", "handover": "Handover · Feb 2028",
           "done": "Completed", "current": "In progress", "next": "Upcoming",
           "g_kicker": "Construction progress", "g_title": "Follow the works at Praça da Corujeira",
           "g_text": "Demolition is complete and the site is enclosed. We publish regular updates with photos from the site so buyers can follow every stage until handover in February 2028.",
           "s_kicker": "Stages", "s_title": "Where we are now", "l_kicker": "Site diary", "l_title": "Latest updates",
           "l_note": "Photos taken on site. Stage dates are estimates and may change.",
           "ct_title": "Want to see the site?", "ct_text": "Ask us for the latest photos or book a visit to Praça da Corujeira.", "ct_btn": "Contact us"},
    "pt": {"licence": "Licenciamento", "demolition": "Demolição e regularização", "site": "Estaleiro e fundações", "structure": "Estrutura", "envelope": "Fachada e cobertura",
           "interiors": "Interiores e acabamentos", "handover": "Entrega · fev. 2028",
           "done": "Concluído", "current": "Em curso", "next": "A seguir",
           "g_kicker": "Acompanhamento da obra", "g_title": "Acompanhe a obra da Praça da Corujeira",
           "g_text": "A demolição está concluída e o estaleiro vedado. Publicamos atualizações regulares com fotografias do estaleiro, para que os compradores possam acompanhar cada fase até à entrega em fevereiro de 2028.",
           "s_kicker": "Fases", "s_title": "Em que ponto estamos", "l_kicker": "Diário de obra", "l_title": "Últimas atualizações",
           "l_note": "Fotografias tiradas em obra. As datas das fases são estimativas e podem sofrer alterações.",
           "ct_title": "Quer visitar a obra?", "ct_text": "Peça-nos as fotografias mais recentes ou marque uma visita à Praça da Corujeira.", "ct_btn": "Contactar"},
    "zh": {"licence": "建筑审批", "demolition": "拆除与平整", "site": "围挡与地基", "structure": "主体结构", "envelope": "外立面与屋顶",
           "interiors": "室内与装修", "handover": "交房 · 2028 年 2 月",
           "done": "已完成", "current": "进行中", "next": "未开始",
           "g_kicker": "工程进度", "g_title": "关注 Praça da Corujeira 的施工进展",
           "g_text": "旧建筑已拆除，工地已封闭。我们会定期发布工地实拍照片，买家可以一直关注到 2028 年 2 月交房。",
           "s_kicker": "施工阶段", "s_title": "目前进展", "l_kicker": "工地日志", "l_title": "最新动态",
           "l_note": "照片为工地实拍。各阶段时间为预估，可能会调整。",
           "ct_title": "想去工地看看？", "ct_text": "可以向我们索取最新照片，或预约参观 Praça da Corujeira。", "ct_btn": "联系我们"},
}
MONTHS = {"en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
          "pt": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]}


def month(d, L):
    if "/" in d:
        a, b = d.split("/")
        if L == "zh":
            return f"{a[:4]} 年 {int(a[5:7])}–{int(b[5:7])} 月"
        return f"{MONTHS[L][int(a[5:7]) - 1]} – {MONTHS[L][int(b[5:7]) - 1]} {b[:4]}"
    y, m = d.split("-")[:2]
    m = int(m)
    return f"{y} 年 {m} 月" if L == "zh" else f"{MONTHS[L][m - 1]} {y}"


def progress():
    data = json.load(open(os.path.join(ROOT, "tools", "progress.json"), encoding="utf-8"))
    c = {L: {**NAV[L], **STAGES[L]} for L in NAV}
    for L in c:
        for i, u in enumerate(data["updates"]):
            c[L][f"u{i}_d"] = month(u["date"], L)
            c[L][f"u{i}_t"] = u["text"][L]
    t = lambda k: e(c["en"][k])  # noqa: E731
    tl = "".join(f'<li class="{s["status"]}"><strong data-i="{s["id"]}">{t(s["id"])}</strong><span class="st" data-i="{s["status"]}">{t(s["status"])}</span></li>' for s in data["stages"])
    entries = []
    for i, u in enumerate(data["updates"]):
        ph = "".join(f'<a href="{p}" target="_blank"><img alt="Construction site — Praça da Corujeira, {u["date"]}" loading="lazy" src="{p}"/></a>' for p in u["photos"])
        entries.append(f'<article class="entry"><time datetime="{u["date"].split("/")[0]}" data-i="u{i}_d">{e(c["en"][f"u{i}_d"])}</time><p data-i="u{i}_t">{e(u["text"]["en"])}</p>{f"<div class=ph>{ph}</div>" if ph else ""}</article>')
    body = f"""<div class="phero" style="--img:url('assets/photos/park-view.webp')"><div class="wrap">
<div class="kicker" data-i="g_kicker">{t('g_kicker')}</div><h1>Praça da Corujeira</h1><p data-i="g_text">{t('g_text')}</p></div></div>
<section><div class="wrap">
<div class="kicker" data-i="s_kicker">{t('s_kicker')}</div><h2 data-i="s_title">{t('s_title')}</h2>
<ol class="timeline">{tl}</ol><p class="note">Licença de obras de demolição e construção n.º NUD/679095/2025/CMP · Câmara Municipal do Porto</p></div></section>
<section class="alt"><div class="wrap">
<div class="kicker" data-i="l_kicker">{t('l_kicker')}</div><h2 data-i="l_title">{t('l_title')}</h2>
<div class="log">{''.join(entries)}</div><p class="note" data-i="l_note">{t('l_note')}</p></div></section>
<section class="ctab"><div class="wrap in"><div><h2 data-i="ct_title">{t('ct_title')}</h2><p class="lead" data-i="ct_text">{t('ct_text')}</p></div>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn gold" data-i="ct_btn" href="index.html#contact">{t('ct_btn')}</a><a class="btn" style="border-color:rgba(255,255,255,.6);color:#fff" data-wa="Praça da Corujeira — construction progress" href="https://wa.me/351969058818" rel="noopener" target="_blank">WhatsApp</a></div></div></section>"""
    return shell("progress", "Construction progress | Praça da Corujeira, Porto | YK CROWN",
                 "Follow the construction of Praça da Corujeira in Porto: stages, site photos and delivery planned for February 2028.",
                 "progress.html", body, c, "progress.html")


if __name__ == "__main__":
    open(os.path.join(ROOT, "about.html"), "w", encoding="utf-8").write(about())
    open(os.path.join(ROOT, "progress.html"), "w", encoding="utf-8").write(progress())
    print("built about.html, progress.html")


# ---------------- Contact / Insights / 404 ----------------
def _home_form():
    import build_home
    page = build_home.page()
    a = page.index('<form id="enquiry-form"')
    b = page.index("</form>", a) + len("</form>")
    keys = {L: {k: v for k, v in build_home.COPY[L].items() if k.startswith("l_")} for L in build_home.COPY}
    return page[a:b], keys


FORM_CSS = """form{display:grid;gap:14px;background:#fff;color:var(--ink);padding:30px;border:1px solid var(--line)}.row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
label{display:block;font-size:12px;font-weight:700;letter-spacing:.06em;margin-bottom:6px;color:#39454e}input,select,textarea{width:100%;border:1px solid #d7d8d5;background:#fbfbfa;padding:12px;font:inherit;font-size:15px;border-radius:0}
textarea{min-height:110px;resize:vertical}input:focus,select:focus,textarea:focus{outline:2px solid var(--gold);outline-offset:-1px}.consent{display:flex;gap:10px;align-items:flex-start;font-weight:400;letter-spacing:0;font-size:13px;color:#5c6871}
.consent input{width:auto;margin-top:3px}.consent a{text-decoration:underline}.hp{position:absolute;left:-9999px}#form-status{font-size:14px;color:#5c6871}button.btn{cursor:pointer;font:inherit;font-size:13px;font-weight:700}
.clist{display:grid;gap:0;margin-top:26px}.clist a,.clist div{display:flex;gap:16px;padding:14px 0;border-bottom:1px solid var(--line)}.clist span{width:110px;flex:none;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:700;padding-top:3px}
@media(max-width:640px){.row{grid-template-columns:1fr}form{padding:20px}}"""

CONTACT = {
    "en": {"c_kicker": "Contact", "c_title": "Get in touch", "c_text": "Ask for the price list of Praça da Corujeira, book a viewing or tell us what you are looking for. We reply within one business day.",
           "c_phone": "Phone", "c_wa": "WhatsApp", "c_email": "Email", "c_site": "Project", "c_lang": "Languages", "c_lang_v": "Português · English · 中文",
           "v_title": "Viewings", "v_text": "Viewings and project presentations are by appointment. While the building is under construction we meet you near the site at Praça da Corujeira and walk you through the plans, renders and specifications.",
           "wa_chat": "Chat on WhatsApp"},
    "pt": {"c_kicker": "Contacto", "c_title": "Fale connosco", "c_text": "Peça a tabela de preços da Praça da Corujeira, marque uma visita ou diga-nos o que procura. Respondemos num dia útil.",
           "c_phone": "Telefone", "c_wa": "WhatsApp", "c_email": "Email", "c_site": "Projeto", "c_lang": "Idiomas", "c_lang_v": "Português · English · 中文",
           "v_title": "Visitas", "v_text": "As visitas e apresentações do projeto são feitas por marcação. Durante a obra, encontramo-nos junto ao local, na Praça da Corujeira, e apresentamos plantas, imagens e especificações.",
           "wa_chat": "Falar no WhatsApp"},
    "zh": {"c_kicker": "联系我们", "c_title": "与我们联系", "c_text": "索取 Praça da Corujeira 价格表、预约看房，或者告诉我们您的需求。我们会在一个工作日内回复。",
           "c_phone": "电话", "c_wa": "WhatsApp", "c_email": "邮箱", "c_site": "项目地址", "c_lang": "语言", "c_lang_v": "Português · English · 中文",
           "v_title": "看房", "v_text": "看房和项目介绍需提前预约。施工期间，我们会在 Praça da Corujeira 工地附近与您见面，介绍户型图、效果图和交付标准。",
           "wa_chat": "WhatsApp 咨询"},
}


def contact():
    form, fkeys = _home_form()
    c = {L: {**NAV[L], **CONTACT[L], **fkeys[L]} for L in NAV}
    t = lambda k: e(c["en"][k])  # noqa: E731
    body = f"""<style>{FORM_CSS}</style>
<section><div class="wrap two" style="align-items:start">
<div><div class="kicker" data-i="c_kicker">{t('c_kicker')}</div><h1 style="color:var(--ink);font-size:clamp(34px,5vw,56px)" data-i="c_title">{t('c_title')}</h1><p class="lead" data-i="c_text">{t('c_text')}</p>
<div class="clist">
<a href="tel:+351969058818"><span data-i="c_phone">{t('c_phone')}</span>+351 969 058 818</a>
<a data-wa="YK CROWN" href="https://wa.me/351969058818" rel="noopener" target="_blank"><span data-i="c_wa">{t('c_wa')}</span><b data-i="wa_chat">{t('wa_chat')}</b></a>
<a href="mailto:info@ykcrown.com"><span data-i="c_email">{t('c_email')}</span>info@ykcrown.com</a>
<a href="https://www.google.com/maps/search/?api=1&amp;query=Pra%C3%A7a+da+Corujeira+203%2C+Porto" rel="noopener" target="_blank"><span data-i="c_site">{t('c_site')}</span>Praça da Corujeira 201–203, Porto ↗</a>
<div><span data-i="c_lang">{t('c_lang')}</span>{t('c_lang_v')}</div></div>
<h2 style="font-size:24px;margin-top:36px" data-i="v_title">{t('v_title')}</h2><p class="lead" style="font-size:15px" data-i="v_text">{t('v_text')}</p></div>
{form}
</div></section>"""
    return shell("contact", "Contact | YK CROWN · Praça da Corujeira, Porto",
                 "Contact YK CROWN for the price list and viewings of Praça da Corujeira, Porto.", "contact.html", body, c, "index.html#contact")


INSIGHTS = {
    "en": {"i_kicker": "Insights", "i_title": "Porto property market", "i_text": "Market data and news on Porto and Portuguese real estate — housing prices, tourism, interest rates — in English, Portuguese and Chinese.",
           "i_soon": "Coming soon", "i_soon_t": "Our first market updates will be published here shortly. Meanwhile, see the apartments at Praça da Corujeira or follow the construction progress.",
           "b1": "See the apartments", "b2": "Construction progress"},
    "pt": {"i_kicker": "Insights", "i_title": "Mercado imobiliário do Porto", "i_text": "Dados e notícias sobre o imobiliário no Porto e em Portugal — preços da habitação, turismo, taxas de juro — em português, inglês e chinês.",
           "i_soon": "Em breve", "i_soon_t": "As primeiras análises de mercado serão publicadas aqui em breve. Entretanto, veja os apartamentos da Praça da Corujeira ou acompanhe a obra.",
           "b1": "Ver apartamentos", "b2": "Acompanhar a obra"},
    "zh": {"i_kicker": "市场资讯", "i_title": "波尔图房地产市场", "i_text": "用中文、英文和葡萄牙语发布波尔图及葡萄牙房地产的市场数据和新闻，包括房价、旅游和利率。",
           "i_soon": "即将发布", "i_soon_t": "第一批市场资讯将很快在这里发布。您可以先看看 Praça da Corujeira 的在售公寓，或关注工程进度。",
           "b1": "查看公寓", "b2": "工程进度"},
}


def insights():
    c = {L: {**NAV[L], **INSIGHTS[L]} for L in NAV}
    t = lambda k: e(c["en"][k])  # noqa: E731
    body = f"""<div class="phero" style="--img:url('assets/photos/location-porto.webp')"><div class="wrap">
<div class="kicker" data-i="i_kicker">{t('i_kicker')}</div><h1 data-i="i_title">{t('i_title')}</h1><p data-i="i_text">{t('i_text')}</p></div></div>
<section><div class="wrap"><div class="card" style="max-width:760px"><div class="n" data-i="i_soon">{t('i_soon')}</div><p style="font-size:17px;margin:10px 0 22px" data-i="i_soon_t">{t('i_soon_t')}</p>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn navy" data-i="b1" href="index.html#apartments">{t('b1')}</a><a class="btn" data-i="b2" href="progress.html">{t('b2')}</a></div></div></div></section>"""
    return shell("insights", "Insights | Porto property market | YK CROWN",
                 "Market data and news on Porto and Portuguese real estate.", "insights.html", body, c, "")


NF = {
    "en": {"n_title": "Page not found", "n_text": "The page you are looking for does not exist or has moved.", "n_b1": "Go to the homepage", "n_b2": "See the apartments"},
    "pt": {"n_title": "Página não encontrada", "n_text": "A página que procura não existe ou foi movida.", "n_b1": "Ir para a página inicial", "n_b2": "Ver apartamentos"},
    "zh": {"n_title": "页面不存在", "n_text": "您要找的页面不存在或已经移动。", "n_b1": "返回首页", "n_b2": "查看公寓"},
}


def not_found():
    c = {L: {**NAV[L], **NF[L]} for L in NAV}
    t = lambda k: e(c["en"][k])  # noqa: E731
    body = f"""<div class="phero" style="--img:url('/assets/photos/park-view.webp');min-height:70vh;display:flex;align-items:center"><div class="wrap">
<div class="kicker">404</div><h1 data-i="n_title">{t('n_title')}</h1><p data-i="n_text">{t('n_text')}</p>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:24px"><a class="btn gold" data-i="n_b1" href="/">{t('n_b1')}</a><a class="btn" style="border-color:rgba(255,255,255,.6);color:#fff" data-i="n_b2" href="/#apartments">{t('n_b2')}</a></div></div></div>"""
    html_ = shell("404", "Page not found | YK CROWN", "Page not found.", "", body, c, "")
    # 404 is served at any path: make links absolute
    for a in ['href="assets/', 'src="assets/', 'href="index.html', 'href="progress.html', 'href="about.html', 'href="insights.html', 'href="privacidade.html', 'href="contact.html']:
        html_ = html_.replace(a, a.replace('"', '"/', 1))
    return html_.replace('<meta content="width=device-width', '<meta name="robots" content="noindex"/>\n<meta content="width=device-width', 1)
