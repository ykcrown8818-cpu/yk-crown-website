#!/usr/bin/env python3
"""Build unit floor-plan cards from the architecture project PDFs (ARQ.PE R1).

The PDFs are NOT stored in this repo. Run with the folder that holds them:
    python3 tools/make_plans.py /path/to/pdfs
Writes assets/img/plans/fracao-<id>.webp (+ thumb) using data from tools/units.json.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageOps

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = sys.argv[1]
OUT = os.path.join(ROOT, "assets", "img", "plans")
os.makedirs(os.path.join(OUT, "thumb"), exist_ok=True)

# drawing sheet per unit and crop box at 300 dpi (left, top, right, bottom)
REAR_T2 = (1190, 780, 2350, 1730)
FRONT_T2 = (1190, 1715, 2350, 2760)
REAR_T1 = (2600, 780, 3580, 1730)
CROPS = {
    "c": ("04_Piso1", (1190, 1700, 2150, 2617)),
    "d": ("04_Piso1", REAR_T2), "e": ("05_Piso2", FRONT_T2), "f": ("05_Piso2", REAR_T2), "g": ("05_Piso2", REAR_T1),
    "i": ("06_Piso3", FRONT_T2), "j": ("06_Piso3", REAR_T2), "m": ("07_Piso4", FRONT_T2), "n": ("07_Piso4", REAR_T2),
    "q": ("08_Piso5", FRONT_T2), "r": ("08_Piso5", REAR_T2),
}
FLOOR_PT = {0: "R/C · Piso 0", 1: "1.º Piso", 2: "2.º Piso", 3: "3.º Piso", 4: "4.º Piso"}
FLOOR_EN = {0: "Ground floor", 1: "1st floor", 2: "2nd floor", 3: "3rd floor", 4: "4th floor"}
POS_PT = {"front_left": "Frente esquerdo", "rear_left": "Traseiro esquerdo", "rear_right": "Traseiro direito"}
POS_EN = {"front_left": "Front left", "rear_left": "Rear left", "rear_right": "Rear right"}

NAVY = (11, 27, 43)
GOLD = (199, 161, 90)
MUTED = (109, 118, 128)
LINE = (231, 227, 218)
BG = (250, 249, 246)
F = "/usr/share/fonts/truetype"
serif = lambda s: ImageFont.truetype(f"{F}/google-fonts/Lora-Variable.ttf", s)
sans = lambda s: ImageFont.truetype(f"{F}/dejavu/DejaVuSans.ttf", s)
sansb = lambda s: ImageFont.truetype(f"{F}/dejavu/DejaVuSans-Bold.ttf", s)


def render(sheet, cache={}):
    if sheet not in cache:
        pdf = glob.glob(os.path.join(PDF_DIR, f"*_R1_{sheet}.pdf"))[0]
        tmp = tempfile.mkdtemp()
        subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", pdf, os.path.join(tmp, "p")], check=True)
        cache[sheet] = Image.open(os.path.join(tmp, "p.png")).convert("RGB")
    return cache[sheet]


def m2(v):
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " m²"


def card(u):
    sheet, box = CROPS[u["id"]]
    plan = render(sheet).crop(box)
    if u["id"] == "c":  # car-lift shaft (common area) beside the T0: mask it so it is not read as part of the unit
        dm = ImageDraw.Draw(plan)
        x0, y0 = 1262 - box[0], 1995 - box[1]
        dm.rectangle((x0, y0, 1565 - box[0], box[3] - box[1] - 40), fill=(236, 236, 236))
        dm.text((x0 + 30, y0 + 250), "Elevador de\nautomóveis\n(área comum)", font=sans(30), fill=(120, 120, 120))
    plan = ImageOps.autocontrast(ImageOps.grayscale(plan), cutoff=0.5).convert("RGB")
    W, H, PW = 2000, 1250, 1300
    img = Image.new("RGB", (W, H), BG)
    pl = plan.copy()
    pl.thumbnail((PW - 120, H - 170), Image.LANCZOS)
    px, py = 60 + (PW - 120 - pl.width) // 2, 60 + (H - 170 - pl.height) // 2
    img.paste(pl, (px, py))
    d = ImageDraw.Draw(img)
    d.rectangle((px - 1, py - 1, px + pl.width, py + pl.height), outline=LINE, width=2)
    # orientation hint
    hint = "▲ Tardoz / Rear" if u["position"].startswith("rear") else "▼ Praça da Corujeira / Front"
    hy = py - 34 if u["position"].startswith("rear") else py + pl.height + 10
    d.text((px, hy), hint, font=sans(20), fill=MUTED)
    d.text((60, H - 70), "Planta do projeto de arquitetura (ARQ.PE R1). Áreas indicativas, sujeitas à documentação técnica aprovada.",
           font=sans(18), fill=MUTED)
    d.text((60, H - 44), "Floor plan from the architecture project. Areas are indicative and subject to the approved technical documentation.",
           font=sans(18), fill=MUTED)
    # side panel
    x = PW + 40
    d.line((PW, 60, PW, H - 100), fill=LINE, width=2)
    d.text((x, 70), "YK CROWN", font=serif(58), fill=NAVY)
    d.text((x + 2, 140), "REAL ESTATE DEVELOPMENT", font=sans(18), fill=MUTED)
    d.line((x, 185, W - 60, 185), fill=GOLD, width=3)
    d.text((x, 215), f"FRAÇÃO {u['letter']}  |  {u['type']}", font=serif(64), fill=NAVY)
    d.text((x, 300), f"{FLOOR_PT[u['floor']]} · {POS_PT[u['position']]}", font=sans(24), fill=NAVY)
    d.text((x, 334), f"{FLOOR_EN[u['floor']]} · {POS_EN[u['position']]}", font=sans(20), fill=MUTED)
    rows = [("Área útil (Au)", m2(u["au"])), ("Área bruta privativa (Abp)", m2(u["abp"]))]
    if u.get("balcony"):
        rows.append(("Varanda / Balcony", m2(u["balcony"])))
    rows += [("Quartos / Bedrooms", str(u["bedrooms"])), ("Casas de banho / Bathrooms", str(u["bathrooms"])),
             ("Estacionamento / Parking", "Incluído · included"), ("Classe energética", u["energy"])]
    y = 395
    for k, v in rows:
        d.line((x, y, W - 60, y), fill=LINE, width=2)
        d.text((x, y + 16), k, font=sans(22), fill=MUTED)
        d.text((W - 60, y + 14), v, font=sansb(26), fill=NAVY, anchor="ra")
        y += 66
    d.line((x, y, W - 60, y), fill=LINE, width=2)
    d.text((x, H - 205), "Praça da Corujeira", font=serif(34), fill=NAVY)
    d.text((x, H - 158), "Campanhã · Porto", font=sans(22), fill=MUTED)
    d.text((x, H - 120), "ykcrown.com", font=sans(22), fill=GOLD)
    path = os.path.join(OUT, f"fracao-{u['id']}.webp")
    img.save(path, "WEBP", quality=86, method=6)
    t = img.copy()
    t.thumbnail((900, 900), Image.LANCZOS)
    t.save(os.path.join(OUT, "thumb", f"fracao-{u['id']}.webp"), "WEBP", quality=82, method=6)
    return path


if __name__ == "__main__":
    units = json.load(open(os.path.join(ROOT, "tools", "units.json"), encoding="utf-8"))["units"]
    for u in units:
        print(card(u))
