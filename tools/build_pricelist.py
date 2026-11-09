#!/usr/bin/env python3
"""Build the private price-list brochure (PDF) in PT / EN / ZH.

Prices are PRIVATE and must never be committed (this repo is public).
Usage:  python3 tools/build_pricelist.py /path/to/prices.json /path/to/output_dir
Writes  YK-CROWN-Corujeira-price-list-<lang>.pdf  (upload these to the private Supabase bucket).
"""
import html
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICES = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
DATA = json.load(open(os.path.join(ROOT, "tools", "units.json"), encoding="utf-8"))
UNITS = [u for u in DATA["units"] if u.get("page", True) and u["status"] != "sold"]
LIC = DATA["project"].get("licence", "")
e = html.escape

L10N = {
    "pt": {
        "title": "Tabela de Preços", "h_offer": "Condições especiais até 31 de dezembro de 2026 (à escolha, uma por fração)", "offer": ["Desconto de 2% para os 3 primeiros contratos-promessa assinados", "Custos de escritura e registo predial suportados pela YK CROWN"], "sub": "Apartamentos T0, T1 e T2 · Campanhã, Porto",
        "issued": "Emitida em", "valid": "Válida até",
        "h_table": "Apartamentos disponíveis", "unit": "Fração", "type": "Tipologia", "floor": "Piso", "pos": "Posição",
        "au": "Área útil", "abp": "Área bruta privativa", "bal": "Varanda", "park": "Garagem", "price": "Preço",
        "gf": "R/C", "front": "Frente", "rear": "Tardoz", "on_req": "Sob consulta",
        "incl": "Área útil sem paredes nem varandas; área bruta privativa medida pelo perímetro exterior e eixos das paredes separadoras, sem partes comuns nem estacionamento. Todos os preços incluem um lugar de estacionamento (elevador de automóveis). Classe energética A+. Entrega prevista: fevereiro de 2028.",
        "h_pay": "Condições de pagamento", "pay_res": "Reserva", "pay_cpcv": "Contrato-promessa (CPCV)",
        "pay_found": "Conclusão das fundações", "pay_struct": "Conclusão da estrutura", "pay_deed": "Escritura e entrega das chaves",
        "rest": "Restante", "tbd": "a definir",
        "h_why": "Destaques", "w": ["Classe energética A+", "Lugar de garagem incluído", "Varandas de 8,25 m² nos T2 de frente", "Virado para a Praça da Corujeira, arborizada", "Perto da Estação de Campanhã e da A1/VCI", "Construção própria YK CROWN"],
        "h_plans": "Plantas", "h_contact": "Contacto",
        "legal": "Documento informativo, não constitui proposta contratual. Preços e disponibilidade sujeitos a alteração sem aviso prévio até à assinatura do contrato-promessa. Áreas segundo o projeto de arquitetura; imagens meramente ilustrativas.",
        "lic": "Licença de obras n.º", "months": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
    },
    "en": {
        "title": "Price List", "h_offer": "Special conditions until 31 December 2026 (one per apartment, buyer's choice)", "offer": ["2% discount for the first 3 promissory contracts signed", "Deed and land-registry costs paid by YK CROWN"], "sub": "T0, T1 and T2 apartments · Campanhã, Porto",
        "issued": "Issued", "valid": "Valid until",
        "h_table": "Available apartments", "unit": "Unit", "type": "Type", "floor": "Floor", "pos": "Position",
        "au": "Usable area", "abp": "Gross private area", "bal": "Balcony", "park": "Parking", "price": "Price",
        "gf": "Ground", "front": "Front", "rear": "Rear", "on_req": "On request",
        "incl": "Usable area excludes walls and balconies; gross private area is measured to the outer face of external walls and the centre line of party walls, excluding common areas and parking. All prices include one parking space (car lift). Energy class A+. Delivery planned for February 2028.",
        "h_pay": "Payment terms", "pay_res": "Reservation", "pay_cpcv": "Promissory contract (CPCV)",
        "pay_found": "Foundations completed", "pay_struct": "Structure completed", "pay_deed": "Deed and handover of keys",
        "rest": "Balance", "tbd": "to be confirmed",
        "h_why": "Highlights", "w": ["Energy class A+", "Parking space included", "8.25 m² balconies on front T2s", "Facing the tree-lined Praça da Corujeira", "Close to Campanhã station and the A1/VCI", "Built by YK CROWN's own construction company"],
        "h_plans": "Floor plans", "h_contact": "Contact",
        "legal": "For information only; this is not a contractual offer. Prices and availability may change without notice until a promissory contract is signed. Areas per the architecture project; images are illustrative.",
        "lic": "Building licence n.º", "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    },
    "zh": {
        "title": "价格表", "h_offer": "限时优惠（至 2026 年 12 月 31 日，每套可任选一项）", "offer": ["前 3 位签订买卖预约合同（CPCV）的客户，房价优惠 2%", "过户公证费和产权登记费由 YK CROWN 承担"], "sub": "T0、T1、T2 公寓 · 波尔图 Campanhã",
        "issued": "发布日期", "valid": "有效期至",
        "h_table": "在售公寓", "unit": "单元", "type": "户型", "floor": "楼层", "pos": "位置",
        "au": "套内使用面积", "abp": "套内建筑面积", "bal": "阳台", "park": "车位", "price": "价格",
        "gf": "地面层", "front": "前侧", "rear": "后侧", "on_req": "价格面议",
        "incl": "套内使用面积（Área útil）不含墙体和阳台；套内建筑面积（Área bruta privativa）= 套内使用面积 + 墙体面积，按外墙外沿和分户墙中线计算，不含公摊和车位。所有价格均含一个车位（汽车升降机）。能源等级 A+。预计 2028 年 2 月交房。",
        "h_pay": "付款方式", "pay_res": "预订金", "pay_cpcv": "签订买卖预约合同（CPCV）",
        "pay_found": "地基完成", "pay_struct": "主体结构完成", "pay_deed": "签署过户契约、交付钥匙",
        "rest": "余款", "tbd": "待定",
        "h_why": "项目亮点", "w": ["能源等级 A+", "含车位", "前侧 T2 带 8.25 m² 阳台", "正对绿树成荫的 Praça da Corujeira 广场", "靠近 Campanhã 火车站和 A1/VCI 高速", "由 YK CROWN 自有建筑公司施工"],
        "h_plans": "户型图", "h_contact": "联系方式",
        "legal": "本文件仅供参考，不构成合同要约。在签订买卖预约合同之前，价格及可售情况可能随时调整，恕不另行通知。面积以建筑设计图纸为准，图片仅供参考。",
        "lic": "建筑许可证号", "months": None,
    },
}


def m2(v):
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " m²" if v else "—"


def eur(v):
    return f"{v:,.0f} €".replace(",", ".") if v else None


def ym(s, L):
    y, m = s.split("-")[:2]
    if L == "zh":
        return f"{y} 年 {int(m)} 月"
    return f"{L10N[L]['months'][int(m) - 1]} {y}"


def ymd(s, L):
    y, m, d = s.split("-")
    if L == "zh":
        return f"{y} 年 {int(m)} 月 {int(d)} 日"
    return f"{int(d)} {L10N[L]['months'][int(m) - 1]} {y}"


_IMGDIR = tempfile.mkdtemp()


def img(rel):
    """Downscaled JPEG copy so the PDF stays small enough to email."""
    from PIL import Image
    src = os.path.join(ROOT, rel)
    dst = os.path.join(_IMGDIR, rel.replace("/", "_") + ".jpg")
    if not os.path.exists(dst):
        im = Image.open(src).convert("RGB")
        im.thumbnail((1500, 1500) if "plans" in rel else (1100, 1100))
        im.save(dst, "JPEG", quality=72, optimize=True, progressive=True)
    return "file://" + dst


def build(L):
    t = L10N[L]
    P = PRICES["prices"]
    rows = "".join(
        f"<tr><td><b>{u['letter']}</b></td><td>{u['type']}</td><td>{t['gf'] if u['floor'] == 0 else u['floor']}</td>"
        f"<td>{t['front'] if u['position'].startswith('front') else t['rear']}</td><td>{m2(u['au'])}</td><td>{m2(u['abp'])}</td>"
        f"<td>{m2(u['balcony'])}</td><td>1</td><td class=p>{eur(P.get(u['id'])) or t['on_req']}</td></tr>" for u in UNITS)
    res = eur(PRICES.get("reservation")) or t["tbd"]
    cpcv = f"{PRICES['cpcv_pct']}%" if PRICES.get("cpcv_pct") is not None else t["tbd"]
    rest = f"{100 - 10 - 20 - (PRICES.get('cpcv_pct') or 0)}%" if PRICES.get("cpcv_pct") is not None else t["rest"]
    pay = [(t["pay_res"], res), (t["pay_cpcv"], cpcv), (t["pay_found"], "10%"), (t["pay_struct"], "20%"), (t["pay_deed"], rest)]
    payh = "".join(f"<div class=step><span>{i + 1}</span><div><b>{e(a)}</b><em>{e(b)}</em></div></div>" for i, (a, b) in enumerate(pay))
    why = "".join(f"<li>{e(w)}</li>" for w in t["w"])
    plans = ""
    for i in range(0, len(UNITS), 2):
        pair = UNITS[i:i + 2]
        plans += "<section class='page plans'><h2>" + e(t["h_plans"]) + "</h2>" + "".join(
            f"<img src='{img('assets/img/' + u['plan'])}'/>" for u in pair) + "</section>"
    font = "'Noto Sans CJK SC','Noto Sans SC'," if L == "zh" else ""
    return f"""<!doctype html><html lang="{L}"><head><meta charset="utf-8"><style>
@page{{size:A4;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:{font}Inter,'DejaVu Sans',Arial,sans-serif;color:#17212b;font-size:10.5pt;line-height:1.5}}
.page{{width:210mm;height:297mm;padding:18mm 16mm;position:relative;page-break-after:always;overflow:hidden}}
.cover{{padding:0;color:#fff;background:linear-gradient(180deg,rgba(5,16,27,.15),rgba(5,16,27,.85)),url('{img('assets/photos/hero.webp')}') center/cover}}
.cover .in{{position:absolute;left:16mm;right:16mm;bottom:22mm}}.logo{{font-weight:800;letter-spacing:3px;font-size:14pt}}.logo span{{color:#c7a15a}}
.cover .logo{{position:absolute;top:16mm;left:16mm}}.kick{{color:#e3c37e;font-size:9pt;letter-spacing:.2em;text-transform:uppercase;font-weight:700}}
h1{{font-size:40pt;line-height:1;margin:6mm 0 4mm;letter-spacing:-.03em}}.cover h1 small{{display:block;font-size:20pt;font-weight:400;margin-top:3mm;color:#e3c37e}}
.meta{{display:flex;gap:10mm;margin-top:8mm;font-size:9pt;border-top:1px solid rgba(255,255,255,.35);padding-top:4mm}}.meta b{{display:block;font-size:11pt}}
h2{{font-size:18pt;margin:0 0 5mm;letter-spacing:-.02em}}h2::before{{content:"";display:block;width:14mm;height:2px;background:#c7a15a;margin-bottom:4mm}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt}}th{{text-align:left;font-size:7.5pt;letter-spacing:.08em;text-transform:uppercase;color:#5f6973;border-bottom:1.5px solid #17212b;padding:2.5mm 1.5mm}}
td{{padding:2.4mm 1.5mm;border-bottom:1px solid #e7e3da}}td.p{{font-weight:700;color:#0b1b2b;text-align:right}}th:last-child{{text-align:right}}
.note{{font-size:8.5pt;color:#5f6973;margin-top:4mm}}.steps{{display:grid;gap:2.5mm;margin-top:2mm}}.step{{display:flex;gap:3mm;align-items:center;background:#f5f3ee;padding:2mm 3mm;font-size:9pt}}
.step span{{width:7mm;height:7mm;border-radius:50%;background:#0b1b2b;color:#fff;display:grid;place-items:center;font-size:9pt;font-weight:700;flex:none}}.step div{{display:flex;justify-content:space-between;width:100%}}.step em{{font-style:normal;font-weight:700;color:#0b1b2b}}
.two{{display:grid;grid-template-columns:1.1fr .9fr;gap:8mm;margin-top:5mm}}ul{{margin:0;padding-left:4.5mm}}li{{margin:1.2mm 0}}
.plans img{{width:100%;height:auto;border:1px solid #e7e3da;margin-bottom:6mm}}
.foot{{position:absolute;left:16mm;right:16mm;bottom:10mm;font-size:7.5pt;color:#899097;display:flex;justify-content:space-between;border-top:1px solid #e7e3da;padding-top:2.5mm}}
.photos{{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin:6mm 0}}.photos img{{width:100%;height:34mm;object-fit:cover}}
.offer{{border:1.5px solid #c7a15a;background:#fbf7ee;padding:3mm 5mm;margin-top:4mm;font-size:9.5pt}}.offer b{{color:#0b1b2b}}.offer ul{{margin:1.5mm 0 0}}
.contact{{background:#0b1b2b;color:#fff;padding:7mm;margin-top:6mm}}.contact b{{color:#e3c37e}}
</style></head><body>
<section class="page cover"><div class="logo">YK <span>CROWN</span></div><div class="in"><div class="kick">{e(t['sub'])}</div>
<h1>Praça da Corujeira<small>{e(t['title'])}</small></h1>
<div class="meta"><div>{e(t['issued'])}<b>{ym(PRICES['issued'], L)}</b></div><div>{e(t['valid'])}<b>{ymd(PRICES['valid_until'], L)}</b></div><div>A+<b>{len(UNITS)} × T0–T2</b></div></div></div></section>
<section class="page"><h2>{e(t['h_table'])}</h2>
<table><tr><th>{e(t['unit'])}</th><th>{e(t['type'])}</th><th>{e(t['floor'])}</th><th>{e(t['pos'])}</th><th>{e(t['au'])}</th><th>{e(t['abp'])}</th><th>{e(t['bal'])}</th><th>{e(t['park'])}</th><th>{e(t['price'])}</th></tr>{rows}</table>
<p class="note">{e(t['incl'])}</p>
{('<div class="offer"><b>' + e(t['h_offer']) + '</b><ul>' + ''.join('<li>' + e(o) + '</li>' for o in t['offer']) + '</ul></div>') if PRICES.get('offers') else ''}
<div class="two"><div><h2>{e(t['h_pay'])}</h2><div class="steps">{payh}</div></div><div><h2>{e(t['h_why'])}</h2><ul>{why}</ul>
<div class="photos"><img src="{img('assets/photos/living-room.webp')}"/><img src="{img('assets/photos/bathroom.webp')}"/></div></div></div>
</section>
{plans}
<section class="page"><h2>{e(t['h_contact'])}</h2>
<div class="photos"><img src="{img('assets/photos/park-view.webp')}"/><img src="{img('assets/photos/location.webp')}"/></div>
<div class="contact"><div class="logo">YK <span>CROWN</span></div><p style="margin:4mm 0 0">Praça da Corujeira 201–203, 4300 Porto<br/><b>+351 969 058 818</b> · WhatsApp<br/><b>info@ykcrown.com</b> · <b>ykcrown.com</b></p></div>
<p class="note">{e(t['legal'])}</p><p class="note">YK CROWN, LDA · NIPC 514037555 · Rua Fontes Pereira de Melo 22B, 2720-233 Amadora · {e(t['lic'])} {LIC} (Câmara Municipal do Porto)</p></section>
</body></html>"""


JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[2],{waitUntil:'networkidle'});await p.pdf({path:process.argv[3],format:'A4',printBackground:true});await b.close()})();"""

if __name__ == "__main__":
    tmp = tempfile.mkdtemp()
    js = os.path.join(tmp, "pdf.js")
    open(js, "w").write(JS)
    for L in ["pt", "en", "zh"]:
        h = os.path.join(tmp, f"{L}.html")
        open(h, "w", encoding="utf-8").write(build(L))
        out = os.path.join(OUT, f"YK-CROWN-Corujeira-price-list-{L}.pdf")
        subprocess.run(["node", js, h, out], check=True)
        print(out)
