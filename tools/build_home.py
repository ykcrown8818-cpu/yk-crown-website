#!/usr/bin/env python3
"""Generate index.html (homepage) from tools/units.json. Run: python3 tools/build_home.py"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legal_footer import legal_footer  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "tools", "units.json"), encoding="utf-8"))
UNITS = data["units"]
e = html.escape


def m2(v):
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " m²" if v else "—"


AU = [u["au"] for u in UNITS if u["au"]]
TYPES = sorted({u["type"] for u in UNITS})
N = len(UNITS)
RANGE = f"{min(AU):.0f}–{max(AU):.0f} m²"

COPY = {
    "en": {
        "nav_apts": "Apartments", "nav_why": "Highlights", "nav_gallery": "Gallery", "nav_loc": "Location", "nav_faq": "FAQ", "nav_contact": "Contact", "nav_progress": "Progress", "nav_about": "About",
        "cta_visit": "Book a viewing",
        "hero_kicker": "New development · Campanhã, Porto",
        "hero_text": f"{N} new apartments — T0, T1 and T2 — on a tree-lined square in eastern Porto. Every apartment includes a parking space and energy class A+.",
        "f_types": "Types", "f_area": "Usable area", "f_energy": "Energy class", "f_park": "Parking", "f_park_v": "Included", "f_deliv": "Delivery", "f_deliv_v": "Feb 2028",
        "btn_apts": "See the apartments",
        "apts_kicker": "Apartments", "apts_title": "Choose your apartment",
        "apts_text": "Areas from the approved architecture project. Prices on request — ask us for the price list.",
        "flt_all": "All", "th_unit": "Apartment", "th_type": "Type", "th_floor": "Floor", "th_au": "Usable area", "th_abp": "Gross area", "th_bal": "Balcony", "th_price": "Price", "th_status": "Status", "st_available": "Available", "st_reserved": "Reserved", "st_sold": "Sold",
        "gf": "Ground", "front": "Front", "rear": "Rear", "on_req": "On request", "view": "View →", "price_list": "Ask for the price list", "foot_note": "All apartments: energy class A+ · one parking space included · delivery February 2028",
        "why_kicker": "Why Praça da Corujeira", "why_title": "A new building, made to be lived in",
        "w1_t": "Energy class A+", "w1_d": "New construction with high thermal performance — lower energy bills and better comfort all year.",
        "w2_t": "Parking included", "w2_d": "Every apartment comes with its own space in the building's garage, served by a car lift.",
        "w3_t": "Balconies at the front", "w3_d": "Front-facing T2 apartments have an 8.25 m² balcony over the square.",
        "w4_t": "On a green square", "w4_d": "The building faces Praça da Corujeira, with mature plane trees, a public garden and play areas.",
        "w5_t": "Well connected", "w5_d": "Close to Campanhã station — metro, urban and intercity trains and buses — and the A1/VCI road network.",
        "w6_t": "Delivery February 2028", "w6_d": "Buy now at the project stage and choose from the full range of apartments.",
        "gal_kicker": "Gallery", "gal_title": "The building and its interiors", "tab_ext": "Exterior", "tab_int": "Interiors", "tab_bath": "Bathrooms", "tab_loc": "Surroundings",
        "gal_note": "Illustrative images (renders). Furniture and decoration are not included.",
        "loc_kicker": "Location", "loc_title": "Campanhã, eastern Porto",
        "loc_text": "Praça da Corujeira is a quiet residential square in Campanhã, one of the areas of Porto receiving the most investment in urban renewal. Campanhã station, the city centre and the motorway network are all within easy reach.",
        "loc_btn": "Open in Google Maps",
        "faq_kicker": "Questions", "faq_title": "Buying at Praça da Corujeira",
        "q1": "When will the apartments be ready?", "a1": "Delivery is planned for February 2028. The building is currently at the construction stage.",
        "q2": "Is parking included?", "a2": "Yes. Every apartment includes one parking space in the building's garage, accessed by a car lift.",
        "q3": "Can foreign buyers purchase?", "a3": "Yes, there are no restrictions on foreign buyers in Portugal. You will need a Portuguese tax number (NIF) and we recommend working with an independent lawyer.",
        "q4": "What taxes does the buyer pay?", "a4": "The main purchase taxes are IMT (property transfer tax) and stamp duty (Imposto do Selo, 0.8%). The IMT amount depends on the price and on whether the apartment will be your permanent home. Your lawyer can calculate the exact amount.",
        "q5": "How does the purchase process work?", "a5": "After a viewing or presentation, a reservation is made, followed by a promissory contract (CPCV) with a deposit. The deed (escritura) is signed when the building is complete.",
        "q6": "How do I get the prices?", "a6": "Send us the form below or a WhatsApp message and we will send you the full price list and availability.",
        "ct_kicker": "Contact", "ct_title": "Book a viewing or ask for the price list",
        "ct_text": "Tell us which apartment interests you. We reply within one business day, in English, Portuguese or Chinese.",
        "l_name": "Name", "l_email": "Email", "l_phone": "Phone / WhatsApp", "l_country": "Country", "l_interest": "Apartment", "l_any": "Any / not sure yet",
        "l_lang": "Preferred language", "l_msg": "Message", "l_consent": "I agree that YK CROWN, LDA may use these details to reply to my enquiry, as described in the privacy policy.",
        "l_send": "Send enquiry", "l_alt": "Prefer to talk? WhatsApp or call +351 969 058 818.",
    },
    "pt": {
        "nav_apts": "Apartamentos", "nav_why": "Destaques", "nav_gallery": "Galeria", "nav_loc": "Localização", "nav_faq": "Perguntas", "nav_contact": "Contacto", "nav_progress": "Obra", "nav_about": "Sobre nós",
        "cta_visit": "Marcar visita",
        "hero_kicker": "Novo empreendimento · Campanhã, Porto",
        "hero_text": f"{N} apartamentos novos — T0, T1 e T2 — numa praça arborizada da zona oriental do Porto. Todos com lugar de garagem e classe energética A+.",
        "f_types": "Tipologias", "f_area": "Área útil", "f_energy": "Classe energética", "f_park": "Garagem", "f_park_v": "Incluída", "f_deliv": "Entrega", "f_deliv_v": "Fev. 2028",
        "btn_apts": "Ver apartamentos",
        "apts_kicker": "Apartamentos", "apts_title": "Escolha o seu apartamento",
        "apts_text": "Áreas do projeto de arquitetura aprovado. Preços sob consulta — peça-nos a tabela de preços.",
        "flt_all": "Todos", "th_unit": "Fração", "th_type": "Tipologia", "th_floor": "Piso", "th_au": "Área útil", "th_abp": "Área bruta", "th_bal": "Varanda", "th_price": "Preço", "th_status": "Estado", "st_available": "Disponível", "st_reserved": "Reservado", "st_sold": "Vendido",
        "gf": "R/C", "front": "Frente", "rear": "Tardoz", "on_req": "Sob consulta", "view": "Ver →", "price_list": "Pedir tabela de preços", "foot_note": "Todos os apartamentos: classe energética A+ · um lugar de garagem incluído · entrega em fevereiro de 2028",
        "why_kicker": "Porquê a Praça da Corujeira", "why_title": "Um edifício novo, pensado para viver",
        "w1_t": "Classe energética A+", "w1_d": "Construção nova com elevado desempenho térmico — menos custos de energia e mais conforto todo o ano.",
        "w2_t": "Garagem incluída", "w2_d": "Cada apartamento tem o seu lugar na garagem do edifício, servida por elevador de automóveis.",
        "w3_t": "Varandas na frente", "w3_d": "Os T2 virados para a praça têm varanda de 8,25 m².",
        "w4_t": "Numa praça verde", "w4_d": "O edifício está virado para a Praça da Corujeira, com plátanos centenários, jardim público e zonas de lazer.",
        "w5_t": "Bem servido", "w5_d": "Perto da Estação de Campanhã — metro, comboios urbanos e de longo curso e autocarros — e dos acessos à A1/VCI.",
        "w6_t": "Entrega em fevereiro de 2028", "w6_d": "Compre agora em fase de projeto e escolha entre toda a oferta de apartamentos.",
        "gal_kicker": "Galeria", "gal_title": "O edifício e os interiores", "tab_ext": "Exterior", "tab_int": "Interiores", "tab_bath": "Casas de banho", "tab_loc": "Envolvente",
        "gal_note": "Imagens meramente ilustrativas (renders). Mobiliário e decoração não incluídos.",
        "loc_kicker": "Localização", "loc_title": "Campanhã, zona oriental do Porto",
        "loc_text": "A Praça da Corujeira é uma praça residencial tranquila em Campanhã, uma das zonas do Porto com mais investimento em regeneração urbana. A Estação de Campanhã, o centro da cidade e os acessos às autoestradas ficam próximos.",
        "loc_btn": "Abrir no Google Maps",
        "faq_kicker": "Perguntas", "faq_title": "Comprar na Praça da Corujeira",
        "q1": "Quando ficam prontos os apartamentos?", "a1": "A entrega está prevista para fevereiro de 2028. O edifício encontra-se em fase de construção.",
        "q2": "O lugar de garagem está incluído?", "a2": "Sim. Cada apartamento inclui um lugar na garagem do edifício, com acesso por elevador de automóveis.",
        "q3": "Estrangeiros podem comprar?", "a3": "Sim, não há restrições à compra por estrangeiros em Portugal. É necessário ter NIF português e recomendamos o apoio de um advogado independente.",
        "q4": "Que impostos paga o comprador?", "a4": "Os principais impostos são o IMT e o Imposto do Selo (0,8%). O valor do IMT depende do preço e de o imóvel se destinar ou não a habitação própria e permanente. O seu advogado pode calcular o valor exato.",
        "q5": "Como funciona o processo de compra?", "a5": "Depois da visita ou apresentação, faz-se a reserva e, em seguida, o contrato-promessa de compra e venda (CPCV) com sinal. A escritura é assinada com o edifício concluído.",
        "q6": "Como obtenho os preços?", "a6": "Envie-nos o formulário abaixo ou uma mensagem por WhatsApp e enviamos a tabela de preços e a disponibilidade.",
        "ct_kicker": "Contacto", "ct_title": "Marque uma visita ou peça a tabela de preços",
        "ct_text": "Diga-nos que apartamento lhe interessa. Respondemos num dia útil, em português, inglês ou chinês.",
        "l_name": "Nome", "l_email": "Email", "l_phone": "Telefone / WhatsApp", "l_country": "País", "l_interest": "Apartamento", "l_any": "Qualquer / ainda não sei",
        "l_lang": "Idioma preferido", "l_msg": "Mensagem", "l_consent": "Aceito que a YK CROWN, LDA use estes dados para responder ao meu pedido, nos termos da política de privacidade.",
        "l_send": "Enviar pedido", "l_alt": "Prefere falar? WhatsApp ou telefone +351 969 058 818.",
    },
    "zh": {
        "nav_apts": "在售公寓", "nav_why": "项目亮点", "nav_gallery": "图库", "nav_loc": "位置", "nav_faq": "常见问题", "nav_contact": "联系我们", "nav_progress": "工程进度", "nav_about": "关于我们",
        "cta_visit": "预约看房",
        "hero_kicker": "全新住宅项目 · 波尔图 Campanhã",
        "hero_text": f"位于波尔图东部绿树广场旁的 {N} 套全新公寓，户型 T0、T1、T2，每套均含车位，能源等级 A+。",
        "f_types": "户型", "f_area": "使用面积", "f_energy": "能源等级", "f_park": "车位", "f_park_v": "包含", "f_deliv": "交房", "f_deliv_v": "2028 年 2 月",
        "btn_apts": "查看公寓",
        "apts_kicker": "在售公寓", "apts_title": "选择您的公寓",
        "apts_text": "面积数据来自已批准的建筑设计图纸。价格面议，欢迎索取价格表。",
        "flt_all": "全部", "th_unit": "单元", "th_type": "户型", "th_floor": "楼层", "th_au": "使用面积", "th_abp": "建筑面积", "th_bal": "阳台", "th_price": "价格", "th_status": "状态", "st_available": "可售", "st_reserved": "已预订", "st_sold": "已售",
        "gf": "地面层", "front": "前侧", "rear": "后侧", "on_req": "价格面议", "view": "查看 →", "price_list": "索取价格表", "foot_note": "所有公寓：能源等级 A+ · 含一个车位 · 2028 年 2 月交房",
        "why_kicker": "为什么选择 Praça da Corujeira", "why_title": "一栋为居住而建的新楼",
        "w1_t": "能源等级 A+", "w1_d": "全新建筑，保温性能高，能耗更低，四季更舒适。",
        "w2_t": "含车位", "w2_d": "每套公寓都配有楼内车库车位，通过汽车升降机进出。",
        "w3_t": "前侧带阳台", "w3_d": "朝向广场的 T2 户型带 8.25 m² 阳台。",
        "w4_t": "面朝绿色广场", "w4_d": "大楼正对 Praça da Corujeira，广场有百年梧桐、公园和休闲区。",
        "w5_t": "交通便利", "w5_d": "靠近 Campanhã 火车站（地铁、城郊及城际火车、巴士），并方便上 A1/VCI 高速。",
        "w6_t": "2028 年 2 月交房", "w6_d": "现在购买期房，可在全部户型中挑选。",
        "gal_kicker": "图库", "gal_title": "建筑外观与室内", "tab_ext": "外观", "tab_int": "室内", "tab_bath": "卫浴", "tab_loc": "周边环境",
        "gal_note": "效果图，仅供参考，家具和装饰不包括在内。",
        "loc_kicker": "位置", "loc_title": "波尔图东部 Campanhã",
        "loc_text": "Praça da Corujeira 是 Campanhã 一处安静的住宅广场。Campanhã 是波尔图城市更新投资最多的区域之一，离 Campanhã 火车站、市中心和高速公路都很近。",
        "loc_btn": "在 Google 地图中打开",
        "faq_kicker": "常见问题", "faq_title": "购房须知",
        "q1": "什么时候交房？", "a1": "预计 2028 年 2 月交房，目前处于施工阶段。",
        "q2": "车位包含在内吗？", "a2": "是的。每套公寓都包含一个楼内车库车位，通过汽车升降机进出。",
        "q3": "外国人可以购买吗？", "a3": "可以，葡萄牙对外国买家没有限制。需要办理葡萄牙税号（NIF），建议聘请独立律师协助。",
        "q4": "买方需要缴纳哪些税？", "a4": "主要是房产交易税 IMT 和印花税（0.8%）。IMT 金额取决于房价以及是否作为自住房，律师可以帮您计算准确金额。",
        "q5": "购房流程是怎样的？", "a5": "看房或了解项目后先预订，然后签订买卖预约合同（CPCV）并支付定金，大楼竣工后签署正式过户契约（escritura）。",
        "q6": "如何获取价格？", "a6": "填写下方表单或发 WhatsApp 消息，我们会把完整价格表和可售情况发给您。",
        "ct_kicker": "联系我们", "ct_title": "预约看房或索取价格表",
        "ct_text": "告诉我们您感兴趣的公寓，我们会在一个工作日内用中文、英文或葡萄牙语回复。",
        "l_name": "姓名", "l_email": "邮箱", "l_phone": "电话 / WhatsApp", "l_country": "国家", "l_interest": "感兴趣的公寓", "l_any": "都可以 / 还不确定",
        "l_lang": "沟通语言", "l_msg": "留言", "l_consent": "我同意 YK CROWN, LDA 按隐私政策使用以上信息回复我的咨询。",
        "l_send": "提交咨询", "l_alt": "想直接沟通？WhatsApp 或致电 +351 969 058 818。",
    },
}

GALLERY = {
    "ext": [("hero", "Praça da Corujeira"), ("park-view", "View from the square"), ("front-through-trees", "Front façade"),
            ("square-view", "Building and square"), ("street-view", "Street view"), ("street-level", "Street level"),
            ("entrance", "Entrance"), ("balconies", "Balconies"), ("aerial-roof", "Roof with solar panels")],
    "int": [("living-room", "Living room"), ("living-area", "Living area"), ("open-plan", "Open-plan living"),
            ("kitchen", "Kitchen"), ("dining", "Dining area"), ("living-garden-view", "Living room"),
            ("bedroom", "Bedroom"), ("bedroom-2", "Bedroom"), ("bedroom-3", "Bedroom")],
    "bath": [("bathroom", "Bathroom"), ("bathroom-2", "Bathroom"), ("bathroom-3", "Bathroom"), ("bathroom-4", "Bathroom")],
    "loc": [("location", "Praça da Corujeira"), ("location-station", "Campanhã and Estádio do Dragão"), ("location-porto", "Towards the Douro")],
}

ICONS = {  # simple line icons
    "w1": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "w2": '<rect x="3" y="7" width="18" height="10" rx="2"/><circle cx="7.5" cy="17" r="1.8"/><circle cx="16.5" cy="17" r="1.8"/><path d="M5 7l2-3h10l2 3"/>',
    "w3": '<path d="M3 20h18M5 20v-7h14v7M5 13V4h14v9M9 13v7M15 13v7"/>',
    "w4": '<path d="M12 22v-6M7 16a5 5 0 1 1 10 0z"/><path d="M12 3a5 5 0 0 1 5 5 5 5 0 0 1-10 0 5 5 0 0 1 5-5z"/>',
    "w5": '<rect x="6" y="3" width="12" height="14" rx="3"/><path d="M6 11h12M9 21l-2 0M15 21h2M8 17l-2 4M16 17l2 4"/><circle cx="9" cy="14" r=".8"/><circle cx="15" cy="14" r=".8"/>',
    "w6": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
}


def unit_rows():
    rows = []
    for u in UNITS:
        fl = '<span data-i="gf">R/C</span>' if u["floor"] == 0 else str(u["floor"])
        pos = "front" if u["position"].startswith("front") else "rear"
        rows.append(
            f'<tr data-type="{u["type"]}" class="row-{u["status"]}"><td><a href="apartamentos/fracao-{u["id"]}/"><strong>{u["letter"]}</strong></a></td>'
            f'<td>{u["type"]}</td><td>{fl} · <span data-i="{pos}">{"Front" if pos=="front" else "Rear"}</span></td>'
            f'<td><strong>{m2(u["au"])}</strong></td><td class="hide-s">{m2(u["abp"])}</td><td>{m2(u["balcony"]) if u["balcony"] else "—"}</td>'
            f'<td class="hide-s"><span data-i="on_req">On request</span></td><td><span class="st st-{u["status"]}" data-i="st_{u["status"]}">{COPY["en"]["st_" + u["status"]]}</span></td>'
            f'<td><a class="view" href="apartamentos/fracao-{u["id"]}/" data-i="view">View →</a></td></tr>')
    return "\n".join(rows)


def unit_options():
    return "".join(f'<option value="Fração {u["letter"]} ({u["type"]})">Fração {u["letter"]} · {u["type"]} · {m2(u["au"])}</option>' for u in UNITS)


def gallery():
    out = []
    for k, items in GALLERY.items():
        figs = "".join(
            f'<figure><img alt="{e(c)} — Praça da Corujeira" loading="lazy" decoding="async" src="assets/photos/thumb/{f}.webp" data-full="assets/photos/{f}.webp" width="800" height="533"/></figure>'
            for f, c in items)
        out.append(f'<div class="gal" data-tab="{k}"{" hidden" if k != "ext" else ""}>{figs}</div>')
    return "".join(out)


def t(k):
    return e(COPY["en"][k])


def page():
    why = "".join(
        f'<div class="why"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[w]}</svg><h3 data-i="{w}_t">{t(w + "_t")}</h3><p data-i="{w}_d">{t(w + "_d")}</p></div>'
        for w in ["w1", "w2", "w3", "w4", "w5", "w6"])
    faq = "".join(f'<details><summary data-i="q{i}">{t(f"q{i}")}</summary><p data-i="a{i}">{t(f"a{i}")}</p></details>' for i in range(1, 7))
    types = " · ".join(TYPES)
    flt = "".join(f'<button data-f="{ty}">{ty}</button>' for ty in TYPES)
    ld = {"@context": "https://schema.org", "@type": "ApartmentComplex", "name": "Praça da Corujeira",
          "url": "https://ykcrown.com/", "numberOfAccommodationUnits": N,
          "address": {"@type": "PostalAddress", "streetAddress": data["project"]["street"], "addressLocality": "Porto", "addressCountry": "PT"},
          "image": "https://ykcrown.com/assets/photos/hero.webp"}
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Praça da Corujeira, Porto — New apartments T0, T1, T2 | YK CROWN</title>
<meta content="{N} new apartments T0–T2 at Praça da Corujeira, Campanhã, Porto. {RANGE} usable area, energy class A+, parking included, delivery February 2028." name="description"/>
<meta content="#0b1b2b" name="theme-color"/>
<link href="https://ykcrown.com/" rel="canonical"/>
<meta content="Praça da Corujeira, Porto — new apartments by YK CROWN" property="og:title"/>
<meta content="{N} new apartments T0–T2 · energy class A+ · parking included · delivery February 2028." property="og:description"/>
<meta content="https://ykcrown.com/assets/photos/hero.webp" property="og:image"/>
<meta content="website" property="og:type"/>
<link as="image" href="assets/photos/hero.webp" rel="preload"/>
<link href="assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="assets/site.css" rel="stylesheet"/>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
:root{{--navy:#0b1b2b;--gold:#c7a15a;--cream:#f5f3ee;--ink:#17212b;--muted:#5f6973;--line:#e7e3da}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:72px}}body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.6}}
a{{color:inherit;text-decoration:none}}img{{display:block;max-width:100%}}button{{font:inherit}}
.wrap{{width:min(1180px,90vw);margin:auto}}
.nav{{position:sticky;top:0;z-index:50;height:68px;padding:0 5vw;display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}
.logo{{font-weight:800;letter-spacing:2.6px;font-size:18px;white-space:nowrap}}.logo span{{color:var(--gold)}}
.navlinks{{display:flex;gap:22px;font-size:13px;color:#3e4852;margin-left:auto}}.navlinks a:hover{{color:var(--gold)}}
.lang{{display:flex;gap:4px}}.lang button{{border:1px solid var(--line);background:#fff;padding:5px 7px;font-size:11px;cursor:pointer}}.lang button.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.btn{{display:inline-flex;align-items:center;justify-content:center;padding:13px 20px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--navy);cursor:pointer;white-space:nowrap}}
.btn.gold{{background:var(--gold);border-color:var(--gold);color:var(--navy)}}.btn.navy{{background:var(--navy);color:#fff}}.btn.ghost{{border-color:rgba(255,255,255,.7);color:#fff}}.btn.sm{{padding:9px 14px;font-size:12px}}
.hero{{min-height:min(88vh,760px);color:#fff;display:flex;align-items:flex-end;background:linear-gradient(90deg,rgba(5,16,27,.78),rgba(5,16,27,.3) 55%,rgba(5,16,27,0)),url("assets/photos/hero.webp") center/cover}}
.hero .wrap{{padding:90px 0 44px}}.kicker{{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-weight:700}}.hero .kicker{{color:#e3c37e}}
h1{{font-size:clamp(44px,7vw,88px);line-height:.98;margin:14px 0 18px;letter-spacing:-.045em}}.hero p{{font-size:clamp(17px,2vw,21px);max-width:620px;color:rgba(255,255,255,.9);margin:0 0 28px}}
.hero .acts{{display:flex;gap:12px;flex-wrap:wrap}}
.facts{{display:grid;grid-template-columns:repeat(5,1fr);margin-top:44px;border-top:1px solid rgba(255,255,255,.25)}}.facts div{{padding:16px 16px 0 0}}.facts span{{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.65)}}.facts strong{{font-size:20px}}
section{{padding:88px 0}}.alt{{background:var(--cream)}}h2{{font-size:clamp(30px,4vw,48px);line-height:1.08;letter-spacing:-.03em;margin:10px 0 14px}}.lead{{font-size:17px;color:var(--muted);max-width:720px;margin:0}}
.head{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:28px}}
.filters{{display:flex;gap:6px}}.filters button{{border:1px solid var(--line);background:#fff;padding:8px 14px;cursor:pointer;font-size:13px}}.filters button.on{{background:var(--navy);color:#fff;border-color:var(--navy)}}
table.units{{width:100%;border-collapse:collapse;background:#fff;font-size:15px}}.units th{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);text-align:left;font-weight:600;padding:12px 14px;border-bottom:2px solid var(--ink)}}
.units td{{padding:15px 14px;border-bottom:1px solid var(--line)}}.units tr:hover td{{background:#fbfaf7}}.units td:first-child strong{{font-size:18px}}.units .view{{font-weight:700;font-size:13px;color:var(--navy);border-bottom:1px solid var(--gold)}}
.st{{display:inline-block;font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px;white-space:nowrap}}.st-available{{background:#e6f4ea;color:#1e7b3a}}.st-reserved{{background:#fdf1dc;color:#9a6200}}.st-sold{{background:#f0eded;color:#8a5050}}.row-sold td{{color:#9aa1a7}}.row-sold td .st{{color:#8a5050}}
.units-foot{{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-top:18px;color:var(--muted);font-size:14px}}
.whys{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:36px}}.why{{background:#fff;border:1px solid var(--line);padding:28px}}.why svg{{width:30px;height:30px;fill:none;stroke:var(--gold);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}.why h3{{margin:14px 0 6px;font-size:18px}}.why p{{margin:0;color:var(--muted);font-size:15px}}
.tabs{{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 18px}}.tabs button{{border:0;border-bottom:2px solid transparent;background:none;padding:8px 2px;margin-right:18px;cursor:pointer;font-size:15px;color:var(--muted)}}.tabs button.on{{color:var(--ink);border-color:var(--gold);font-weight:600}}
.gal{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}.gal figure{{margin:0;overflow:hidden;background:#eee;cursor:zoom-in}}.gal[hidden]{{display:none}}.gal img{{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;transition:transform .4s}}.gal figure:hover img{{transform:scale(1.03)}}
.note{{font-size:12px;color:#899097;margin-top:12px}}
.loc{{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}}.loc img{{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}}.loc address{{font-style:normal;margin:20px 0;font-weight:600}}
.faq{{max-width:820px}}details{{border-bottom:1px solid var(--line);padding:18px 0}}summary{{cursor:pointer;font-weight:600;font-size:17px;list-style:none;display:flex;justify-content:space-between;gap:16px}}summary::after{{content:"+";color:var(--gold);font-size:22px;line-height:1}}details[open] summary::after{{content:"–"}}details p{{color:var(--muted);margin:10px 0 0}}
.contact{{background:var(--navy);color:#fff}}.contact .lead{{color:rgba(255,255,255,.75)}}.cgrid{{display:grid;grid-template-columns:.8fr 1.2fr;gap:56px}}
form{{display:grid;gap:14px;background:#fff;color:var(--ink);padding:30px}}.row{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}label{{display:block;font-size:12px;font-weight:700;letter-spacing:.06em;margin-bottom:6px;color:#39454e}}
input,select,textarea{{width:100%;border:1px solid #d7d8d5;background:#fbfbfa;padding:12px;font:inherit;font-size:15px;border-radius:0}}textarea{{min-height:110px;resize:vertical}}input:focus,select:focus,textarea:focus{{outline:2px solid var(--gold);outline-offset:-1px}}
.consent{{display:flex;gap:10px;align-items:flex-start;font-weight:400;letter-spacing:0;font-size:13px;color:#5c6871}}.consent input{{width:auto;margin-top:3px}}.consent a{{text-decoration:underline}}.hp{{position:absolute;left:-9999px}}
#form-status{{font-size:14px;color:#5c6871}}button[type=submit]:disabled{{opacity:.6}}.alt-c{{margin-top:22px;display:flex;gap:10px;flex-wrap:wrap}}
footer{{padding:26px 5vw;font-size:12px;color:#747d84;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;border-top:1px solid var(--line)}}
.lightbox{{position:fixed;inset:0;background:rgba(5,12,20,.94);z-index:999;display:none;align-items:center;justify-content:center}}.lightbox.open{{display:flex}}.lightbox img{{max-width:94vw;max-height:88vh}}.lb{{position:fixed;border:0;background:rgba(255,255,255,.14);color:#fff;width:46px;height:46px;border-radius:50%;font-size:26px;cursor:pointer}}.lb.x{{top:16px;right:16px}}.lb.p{{left:14px;top:50%}}.lb.n{{right:14px;top:50%}}
@media(max-width:980px){{.navlinks{{display:none}}.facts{{grid-template-columns:repeat(3,1fr)}}.whys{{grid-template-columns:1fr 1fr}}.loc,.cgrid{{grid-template-columns:1fr;gap:32px}}.hide-s{{display:none}}}}
@media(max-width:640px){{.nav{{gap:10px}}.nav .btn{{display:none}}.lang{{margin-left:auto}}section{{padding:60px 0}}.facts{{grid-template-columns:1fr 1fr}}.whys{{grid-template-columns:1fr}}.gal{{grid-template-columns:1fr 1fr}}.why{{padding:20px}}.row{{grid-template-columns:1fr}}form{{padding:20px}}
.units th,.units td{{padding:12px 6px;font-size:14px}}.units th:nth-child(3),.units td:nth-child(3),.units th:nth-child(6),.units td:nth-child(6),.units th:nth-child(9),.units td:nth-child(9){{display:none}}.units .st{{font-size:11px;padding:2px 7px}}.units td:first-child strong{{color:var(--navy);border-bottom:2px solid var(--gold)}}.hero .btn{{flex:1}}}}
</style>
</head>
<body>
<header class="nav">
<a class="logo" href="#top">YK <span>CROWN</span></a>
<nav class="navlinks"><a data-i="nav_apts" href="#apartments">{t('nav_apts')}</a><a data-i="nav_why" href="#highlights">{t('nav_why')}</a><a data-i="nav_gallery" href="#gallery">{t('nav_gallery')}</a><a data-i="nav_loc" href="#location">{t('nav_loc')}</a><a data-i="nav_faq" href="#faq">{t('nav_faq')}</a><a data-i="nav_progress" href="progress.html">{t('nav_progress')}</a><a data-i="nav_about" href="about.html">{t('nav_about')}</a></nav>
<div class="lang"><button class="active" data-lang="en">EN</button><button data-lang="pt">PT</button><button data-lang="zh">中文</button></div>
<a class="btn navy sm" data-i="cta_visit" href="#contact">{t('cta_visit')}</a>
</header>
<main id="top">
<div class="hero"><div class="wrap">
<div class="kicker" data-i="hero_kicker">{t('hero_kicker')}</div>
<h1>Praça da Corujeira</h1>
<p data-i="hero_text">{t('hero_text')}</p>
<div class="acts"><a class="btn gold" data-i="btn_apts" href="#apartments">{t('btn_apts')}</a><a class="btn ghost" data-i="cta_visit" href="#contact">{t('cta_visit')}</a></div>
<div class="facts">
<div><span data-i="f_types">{t('f_types')}</span><strong>{types}</strong></div>
<div><span data-i="f_area">{t('f_area')}</span><strong>{RANGE}</strong></div>
<div><span data-i="f_energy">{t('f_energy')}</span><strong>A+</strong></div>
<div><span data-i="f_park">{t('f_park')}</span><strong data-i="f_park_v">{t('f_park_v')}</strong></div>
<div><span data-i="f_deliv">{t('f_deliv')}</span><strong data-i="f_deliv_v">{t('f_deliv_v')}</strong></div>
</div></div></div>

<section id="apartments"><div class="wrap">
<div class="head"><div><div class="kicker" data-i="apts_kicker">{t('apts_kicker')}</div><h2 data-i="apts_title">{t('apts_title')}</h2><p class="lead" data-i="apts_text">{t('apts_text')}</p></div>
<div class="filters"><button class="on" data-f="all" data-i="flt_all">{t('flt_all')}</button>{flt}</div></div>
<table class="units"><thead><tr><th data-i="th_unit">{t('th_unit')}</th><th data-i="th_type">{t('th_type')}</th><th data-i="th_floor">{t('th_floor')}</th><th data-i="th_au">{t('th_au')}</th><th class="hide-s" data-i="th_abp">{t('th_abp')}</th><th data-i="th_bal">{t('th_bal')}</th><th class="hide-s" data-i="th_price">{t('th_price')}</th><th data-i="th_status">{t('th_status')}</th><th></th></tr></thead>
<tbody>
{unit_rows()}
</tbody></table>
<div class="units-foot"><span data-i="foot_note">{t('foot_note')}</span><a class="btn navy sm" data-i="price_list" href="#contact">{t('price_list')}</a></div>
</div></section>

<section class="alt" id="highlights"><div class="wrap">
<div class="kicker" data-i="why_kicker">{t('why_kicker')}</div><h2 data-i="why_title">{t('why_title')}</h2>
<div class="whys">{why}</div>
</div></section>

<section id="gallery"><div class="wrap">
<div class="kicker" data-i="gal_kicker">{t('gal_kicker')}</div><h2 data-i="gal_title">{t('gal_title')}</h2>
<div class="tabs"><button class="on" data-t="ext" data-i="tab_ext">{t('tab_ext')}</button><button data-t="int" data-i="tab_int">{t('tab_int')}</button><button data-t="bath" data-i="tab_bath">{t('tab_bath')}</button><button data-t="loc" data-i="tab_loc">{t('tab_loc')}</button></div>
{gallery()}
<p class="note" data-i="gal_note">{t('gal_note')}</p>
</div></section>

<section class="alt" id="location"><div class="wrap loc">
<div><div class="kicker" data-i="loc_kicker">{t('loc_kicker')}</div><h2 data-i="loc_title">{t('loc_title')}</h2><p class="lead" data-i="loc_text">{t('loc_text')}</p>
<address>Praça da Corujeira 201–203<br/>4300 Campanhã, Porto</address>
<a class="btn navy" data-i="loc_btn" href="https://www.google.com/maps/search/?api=1&amp;query=Pra%C3%A7a+da+Corujeira+203%2C+Porto" rel="noopener" target="_blank">{t('loc_btn')}</a></div>
<img alt="Aerial view of Praça da Corujeira, Porto" loading="lazy" decoding="async" src="assets/photos/location.webp" width="1920" height="1280"/>
</div></section>

<section id="faq"><div class="wrap faq">
<div class="kicker" data-i="faq_kicker">{t('faq_kicker')}</div><h2 data-i="faq_title">{t('faq_title')}</h2>
{faq}
</div></section>

<section class="contact" id="contact"><div class="wrap cgrid">
<div><div class="kicker" data-i="ct_kicker">{t('ct_kicker')}</div><h2 data-i="ct_title">{t('ct_title')}</h2><p class="lead" data-i="ct_text">{t('ct_text')}</p>
<div class="alt-c"><a class="btn gold" data-wa="Praça da Corujeira" href="https://wa.me/351969058818" rel="noopener" target="_blank">WhatsApp</a><a class="btn ghost" href="tel:+351969058818">+351 969 058 818</a></div></div>
<form id="enquiry-form">
<div class="row"><div><label for="name" data-i="l_name">{t('l_name')}</label><input id="name" name="name" autocomplete="name" required/></div><div><label for="email" data-i="l_email">{t('l_email')}</label><input id="email" name="email" type="email" autocomplete="email" required/></div></div>
<div class="row"><div><label for="phone" data-i="l_phone">{t('l_phone')}</label><input id="phone" name="phone" type="tel" autocomplete="tel"/></div><div><label for="country" data-i="l_country">{t('l_country')}</label><input id="country" name="country" autocomplete="country-name"/></div></div>
<div class="row"><div><label for="interest" data-i="l_interest">{t('l_interest')}</label><select id="interest" name="interest"><option value="Praça da Corujeira apartments" data-i="l_any">{t('l_any')}</option>{unit_options()}</select></div>
<div><label for="language" data-i="l_lang">{t('l_lang')}</label><select id="language" name="language"><option>English</option><option>Português</option><option>中文</option></select></div></div>
<div><label for="message" data-i="l_msg">{t('l_msg')}</label><textarea id="message" name="message"></textarea></div>
<div class="hp" aria-hidden="true"><label for="website">Website</label><input id="website" name="website" tabindex="-1" autocomplete="off"/></div>
<label class="consent"><input type="checkbox" name="consent" value="yes" required/> <span><span data-i="l_consent">{t('l_consent')}</span> <a href="privacidade.html" target="_blank">↗</a></span></label>
<button class="btn navy" type="submit" data-i="l_send">{t('l_send')}</button>
<div id="form-status" role="status" aria-live="polite" data-i="l_alt">{t('l_alt')}</div>
</form>
</div></section>
</main>
<footer><span>© 2026 YK CROWN, LDA · Real estate development · Porto</span><span><a href="progress.html">Progress</a> · <a href="about.html">About</a> · <a href="insights.html">Insights</a> · <a href="contact.html">Contact</a></span></footer>
{legal_footer('')}
<div class="lightbox" id="lightbox" aria-hidden="true"><button class="lb x" aria-label="Close">×</button><button class="lb p" aria-label="Previous">‹</button><img alt="" id="lb-img"/><button class="lb n" aria-label="Next">›</button></div>
<script>
const copy={json.dumps(COPY, ensure_ascii=False)};
function setLang(l){{if(!copy[l])return;document.documentElement.lang=l==="zh"?"zh-CN":l;document.querySelectorAll("[data-lang]").forEach(b=>b.classList.toggle("active",b.dataset.lang===l));document.querySelectorAll("[data-i]").forEach(el=>{{const v=copy[l][el.dataset.i];if(v)el.textContent=v}});try{{localStorage.setItem("yk_lang",l)}}catch(e){{}}
const ls={{en:"English",pt:"Português",zh:"中文"}};const s=document.getElementById("language");if(s)s.value=ls[l]}}
document.querySelectorAll("[data-lang]").forEach(b=>b.addEventListener("click",()=>setLang(b.dataset.lang)));
try{{const q=new URLSearchParams(location.search).get("lang")||localStorage.getItem("yk_lang")||((navigator.language||"").slice(0,2));if(q&&q!=="en")setLang(q)}}catch(e){{}}
document.querySelectorAll(".filters button").forEach(b=>b.addEventListener("click",()=>{{document.querySelectorAll(".filters button").forEach(x=>x.classList.toggle("on",x===b));document.querySelectorAll(".units tbody tr").forEach(r=>r.hidden=b.dataset.f!=="all"&&r.dataset.type!==b.dataset.f)}}));
document.querySelectorAll(".units tbody tr").forEach(r=>r.addEventListener("click",ev=>{{if(!ev.target.closest("a"))location.href=r.querySelector("a").href}}));
document.querySelectorAll(".tabs button").forEach(b=>b.addEventListener("click",()=>{{document.querySelectorAll(".tabs button").forEach(x=>x.classList.toggle("on",x===b));document.querySelectorAll(".gal").forEach(g=>g.hidden=g.dataset.tab!==b.dataset.t)}}));
document.querySelectorAll('a[href="#contact"][data-unit]').forEach(a=>a.addEventListener("click",()=>{{document.getElementById("interest").value=a.dataset.unit}}));
const lb=document.getElementById("lightbox"),lbi=document.getElementById("lb-img");let list=[],idx=0;
function show(i){{idx=(i+list.length)%list.length;lbi.src=list[idx].dataset.full;lbi.alt=list[idx].alt}}
document.querySelectorAll(".gal img").forEach(img=>img.addEventListener("click",()=>{{list=[...img.closest(".gal").querySelectorAll("img")];show(list.indexOf(img));lb.classList.add("open");document.body.style.overflow="hidden"}}));
function close(){{lb.classList.remove("open");document.body.style.overflow=""}}
lb.querySelector(".x").onclick=close;lb.querySelector(".p").onclick=()=>show(idx-1);lb.querySelector(".n").onclick=()=>show(idx+1);lb.addEventListener("click",ev=>{{if(ev.target===lb)close()}});
document.addEventListener("keydown",ev=>{{if(!lb.classList.contains("open"))return;if(ev.key==="Escape")close();if(ev.key==="ArrowLeft")show(idx-1);if(ev.key==="ArrowRight")show(idx+1)}});
let tx=0;lb.addEventListener("touchstart",ev=>tx=ev.changedTouches[0].screenX,{{passive:true}});lb.addEventListener("touchend",ev=>{{const dx=ev.changedTouches[0].screenX-tx;if(Math.abs(dx)>50)show(idx+(dx<0?1:-1))}},{{passive:true}});
</script>
<script defer src="assets/site.js"></script>
</body></html>
"""


if __name__ == "__main__":
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page())
    print("built index.html")
