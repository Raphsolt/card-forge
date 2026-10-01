#!/usr/bin/env python3
"""
Card Forge — Esoteric Lockscreen Wallpaper Generator
Calibrated for iPhone 13 mini (1080 x 2340)
Studio Ghibli Painterly Engine, Gold Foil Armor & Sampling Diversity
"""

import os
import sys
import html
import json
import math
import random
import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

WIDTH = 1080
HEIGHT = 2340
LOCAL_MODEL_PATH = "./Qwen2.5-7B-Instruct-4bit"
DEFAULT_OUT_DIR = "./output"

# Luminous Gold Foil Colors
GOLD_LIGHT = "#fff6de"
GOLD_BRIGHT = "#f5e2be"
GOLD = "#d6b88d"
GOLD_DARK = "#96754b"
BORDER_DARK = "#2a2420"

# ─── REALITY KNOWLEDGE BANKS ───

MAORI_LEXICON = {
    "freedom": ("Rangirua kore", "unbound, total liberation"),
    "threshold": ("Paepae", "the threshold between realms"),
    "boundary": ("Waharoa", "the sacred gateway"),
    "bonsai": ("Rākau whakatipu", "cultivated, nurtured growth"),
    "stillness": ("Tūmārire", "quiet composure, calm rest"),
    "silence": ("Noho puku", "inner quiet, intentional silence"),
    "form": ("Āhua", "the manifest shape and nature"),
    "emergence": ("Whakaputa", "emerging into the light"),
    "dissolution": ("Hukatai", "dissolving into deep water"),
    "solitude": ("Noho mokemoke", "sacred aloneness"),
    "patience": ("Manawanui", "steadfast enduring heart"),
    "void": ("Te Kore", "the realm of primal potential"),
    "truth": ("Pono", "integrity, absolute reality"),
    "breath": ("Ha", "the breath of life"),
    "memory": ("Mahara", "recollection and reflection")
}

MAORI_PLANETS = {
    "Saturn": "Rongo", "Venus": "Kōpū", "Mars": "Matawhero",
    "Jupiter": "Pareārau", "Mercury": "Merikuri", "Sun": "Tama-nui-te-rā",
    "Moon": "Marama", "Neptune": "Tangaroa-whakamautai", "Pluto": "Whiro", "Uranus": "Whanui"
}

MAORI_SIGNS = {
    "Aries": "Eri", "Taurus": "Tauri", "Gemini": "Māhanga",
    "Cancer": "Kāmeta", "Leo": "Reo", "Virgo": "Wahine",
    "Libra": "Rāpiti", "Scorpio": "Kōpūpūtahi", "Sagittarius": "Kaikopere",
    "Capricorn": "Kaparikōna", "Aquarius": "Kārewarewa", "Pisces": "Paea"
}

COSMOLOGY = {
    "earth": {"maori": "WHENUA", "eng": "EARTH", "color": "#b8cf72", "alch": "Coagulatio", "default_planet": "Saturn", "default_sign": "Capricorn"},
    "water": {"maori": "WAI",    "eng": "WATER", "color": "#76c2df", "alch": "Solutio",    "default_planet": "Moon",   "default_sign": "Pisces"},
    "fire":  {"maori": "AHI",    "eng": "FIRE",  "color": "#e28462", "alch": "Calcinatio", "default_planet": "Mars",   "default_sign": "Aries"},
    "air":   {"maori": "HAU",    "eng": "AIR",   "color": "#c0c8d8", "alch": "Separatio",  "default_planet": "Mercury","default_sign": "Aquarius"},
    "void":  {"maori": "TE KORE","eng": "VOID",  "color": "#ad8ad4", "alch": "Nigredo",    "default_planet": "Pluto",  "default_sign": "Scorpio"}
}

HEXAGRAMS = {
    1:  ("The Creative", [1,1,1,1,1,1]),
    2:  ("The Receptive", [0,0,0,0,0,0]),
    11: ("Peace", [1,1,1,0,0,0]),
    12: ("Standstill", [0,0,0,1,1,1]),
    20: ("Contemplation", [0,0,0,0,1,1]),
    23: ("Splitting Apart", [0,0,0,0,0,1]),
    24: ("Return", [1,0,0,0,0,0]),
    29: ("The Abysmal Water", [0,1,0,0,1,0]),
    52: ("Keeping Still", [0,0,1,0,0,1]),
    57: ("The Gentle Wind", [0,1,1,0,1,1]),
    59: ("Dispersion", [0,1,0,0,1,1]),
    60: ("Limitation", [0,1,0,1,1,0])
}

RUNES_SVG = {
    "Jera": "M 0 6 L 12 18 L 0 30 M 24 12 L 12 24 L 24 36",
    "Ansuz": "M 4 0 L 4 36 M 4 6 L 20 12 M 4 14 L 18 20",
    "Fehu": "M 4 0 L 4 36 M 4 6 L 20 2 M 4 14 L 18 10",
    "Uruz": "M 4 0 L 4 36 M 4 0 L 20 10 L 20 36",
    "Thurisaz": "M 4 0 L 4 36 M 4 10 L 18 18 L 4 26",
    "Raidho": "M 4 0 L 4 36 M 4 4 L 18 10 L 4 18 M 12 14 L 20 36",
    "Kenaz": "M 20 4 L 4 18 L 20 32",
    "Gebo": "M 4 4 L 20 32 M 20 4 L 4 32",
    "Wunjo": "M 4 0 L 4 36 M 4 4 L 18 12 L 4 20",
    "Hagalaz": "M 4 0 L 4 36 M 20 0 L 20 36 M 4 12 L 20 24",
    "Nauthiz": "M 12 0 L 12 36 M 4 14 L 20 22",
    "Isa": "M 12 0 L 12 36",
    "Eihwaz": "M 12 0 L 12 36 M 4 4 L 12 0 M 12 36 L 20 32",
    "Perthro": "M 4 0 L 4 36 M 4 4 L 16 4 L 20 12 L 12 18 M 12 18 L 20 24 L 16 32 L 4 32",
    "Algiz": "M 12 0 L 12 36 M 4 4 L 12 14 M 20 4 L 12 14",
    "Sowilo": "M 20 4 L 4 16 L 20 24 L 4 36",
    "Tiwaz": "M 12 0 L 12 36 M 4 10 L 12 0 L 20 10",
    "Berkano": "M 4 0 L 4 36 M 4 2 L 18 10 L 4 18 M 4 18 L 18 26 L 4 34",
    "Ehwaz": "M 4 0 L 4 36 M 20 0 L 20 36 M 4 4 L 12 14 L 20 4",
    "Mannaz": "M 4 0 L 4 36 M 20 0 L 20 36 M 4 4 L 20 20 M 20 4 L 4 20",
    "Laguz": "M 4 0 L 4 36 M 4 4 L 18 12",
    "Ingwaz": "M 12 4 L 20 18 L 12 32 L 4 18 Z",
    "Dagaz": "M 4 4 L 20 32 M 20 4 L 4 32 M 4 4 L 4 32 M 20 4 L 20 32",
    "Othala": "M 12 4 L 20 16 L 4 32 M 12 4 L 4 16 L 20 32"
}

ALCHEMY_SVG = {
    "Coagulatio": "M 18 2 L 34 30 L 2 30 Z M 18 30 L 18 36 M 12 34 L 24 34",
    "Solutio": "M 2 4 L 34 4 L 18 32 Z",
    "Calcinatio": "M 18 4 L 34 32 L 2 32 Z",
    "Separatio": "M 18 4 L 34 32 L 2 32 Z M 6 22 L 30 22",
    "Distillatio": "M 6 8 L 30 8 M 18 8 L 18 28 A 6 6 0 0 1 12 34",
    "Coniunctio": "M 18 6 A 10 10 0 1 0 18 26 A 10 10 0 1 0 18 6 Z M 8 16 L 28 16",
    "Nigredo": "M 18 4 A 14 14 0 1 0 18 32 A 14 14 0 1 0 18 4 Z M 18 11 A 7 7 0 1 0 18 25 A 7 7 0 1 0 18 11 Z"
}

# ─── PROCEDURAL SACRED GEOMETRY (LARGER & BOLDER) ───

def build_procedural_geometry(seed_val, element="void", cx=540, cy=1010):
    rng = random.Random(seed_val)
    svg = f'<g stroke="{GOLD_BRIGHT}" fill="none" opacity="0.85" filter="url(#foil-glow)">'

    archetype = rng.choice(["astrolabe", "vesica", "metatron", "radiant", "tesseract", "concentric"])
    rot = rng.randint(0, 45)
    max_r = rng.randint(290, 325)
    min_r = rng.randint(50, 80)

    # Perimeter ring with ticks
    svg += f'<circle cx="{cx}" cy="{cy}" r="{max_r}" stroke-width="2.4" opacity="0.75"/>'
    num_ticks = rng.choice([24, 36, 48])
    for t in range(num_ticks):
        ang = t * (2 * math.pi / num_ticks)
        tick_len = 8 if t % 4 == 0 else 4.5
        x1 = cx + (max_r - tick_len) * math.cos(ang)
        y1 = cy + (max_r - tick_len) * math.sin(ang)
        x2 = cx + max_r * math.cos(ang)
        y2 = cy + max_r * math.sin(ang)
        svg += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="1.6" opacity="0.6"/>'

    # Orbit rings
    num_inner = rng.randint(2, 4)
    inner_radii = sorted([rng.randint(min_r + 25, max_r - 35) for _ in range(num_inner)])
    for r in inner_radii:
        dash = 'stroke-dasharray="6,8"' if rng.random() > 0.4 else ""
        svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke-width="1.8" {dash} opacity="0.5"/>'

    # Axis Lines
    svg += f'<line x1="{cx}" y1="{cy - max_r - 20}" x2="{cx}" y2="{cy + max_r + 20}" stroke-width="2.0" opacity="0.55"/>'
    svg += f'<line x1="{cx - max_r - 20}" y1="{cy}" x2="{cx + max_r + 20}" y2="{cy}" stroke-width="1.5" opacity="0.45"/>'

    # Archetype Features
    if archetype == "vesica":
        offset = rng.randint(75, 105)
        svg += f'<circle cx="{cx - offset}" cy="{cy}" r="{offset * 1.8}" stroke-width="1.8" opacity="0.5"/>'
        svg += f'<circle cx="{cx + offset}" cy="{cy}" r="{offset * 1.8}" stroke-width="1.8" opacity="0.5"/>'
        svg += f'<path d="M {cx} {cy-150} Q {cx-85} {cy} {cx} {cy+150} Q {cx+85} {cy} {cx} {cy-150} Z" stroke-width="2.8" opacity="0.9"/>'

    elif archetype == "metatron":
        for a in range(6):
            ang = a * (math.pi / 3) + math.radians(rot)
            px = cx + 115 * math.cos(ang)
            py = cy + 115 * math.sin(ang)
            svg += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="115" stroke-width="1.8" opacity="0.55"/>'

    elif archetype == "tesseract":
        s1 = rng.randint(120, 150)
        s2 = s1 * 0.55
        svg += f'<rect x="{cx-s1}" y="{cy-s1}" width="{s1*2}" height="{s1*2}" transform="rotate({rot} {cx} {cy})" stroke-width="2.2" opacity="0.6"/>'
        svg += f'<rect x="{cx-s2}" y="{cy-s2}" width="{s2*2}" height="{s2*2}" transform="rotate({rot} {cx} {cy})" stroke-width="1.6" opacity="0.45"/>'

    elif archetype == "radiant":
        for ray in range(12):
            ang = ray * (math.pi / 6)
            x2 = cx + (max_r - 18) * math.cos(ang)
            y2 = cy + (max_r - 18) * math.sin(ang)
            svg += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="1.8" opacity="0.55"/>'
            if ray % 2 == 0:
                svg += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="5" fill="{GOLD_LIGHT}" opacity="0.9"/>'

    # Center Focal Node
    svg += f'<circle cx="{cx}" cy="{cy}" r="{min_r}" stroke-width="2.4" opacity="0.7"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="9" fill="{GOLD_LIGHT}" opacity="0.95"/>'
    svg += '</g>'
    return svg

def build_hexagram_svg(lines, x=540, y=1465, w=170, h=105):
    gap = h / 5
    line_h = gap * 0.45
    half_w = (w - gap * 0.6) / 2
    svg = '<g id="hexagram" filter="url(#foil-glow)">'
    for i, line in enumerate(lines):
        ly = y - (i * gap)
        op = 0.98
        if int(line) == 1:
            svg += f'<rect x="{x - w/2}" y="{ly}" width="{w}" height="{line_h}" rx="2" fill="{GOLD_BRIGHT}" opacity="{op}"/>'
        else:
            svg += f'<rect x="{x - w/2}" y="{ly}" width="{half_w}" height="{line_h}" rx="2" fill="{GOLD_BRIGHT}" opacity="{op}"/>'
            svg += f'<rect x="{x - w/2 + half_w + gap * 0.6}" y="{ly}" width="{half_w}" height="{line_h}" rx="2" fill="{GOLD_BRIGHT}" opacity="{op}"/>'
    svg += '</g>'
    return svg

def build_trigram_mini_icon(x, y):
    return f"""<g transform="translate({x}, {y})">
      <rect x="0" y="0" width="18" height="2.6" rx="0.5" fill="{GOLD_BRIGHT}" opacity="0.9"/>
      <rect x="0" y="5.2" width="18" height="2.6" rx="0.5" fill="{GOLD_BRIGHT}" opacity="0.9"/>
      <rect x="0" y="10.4" width="18" height="2.6" rx="0.5" fill="{GOLD_BRIGHT}" opacity="0.9"/>
    </g>"""

# ─── MAIN CARD SVG BUILDER (LARGER, BOUNTIFUL TYPOGRAPHY) ───

def generate_card_svg(data):
    elem_key = data.get("element", "void").lower()
    elem = COSMOLOGY.get(elem_key, COSMOLOGY["void"])

    planet = data.get("astrology_planet", elem["default_planet"])
    sign = data.get("astrology_sign", elem["default_sign"])
    maori_planet = MAORI_PLANETS.get(planet, planet)
    maori_sign = MAORI_SIGNS.get(sign, sign)
    astro_maori = f"{maori_planet} ki {maori_sign}"
    astro_english = f"{planet} in {sign}"

    rune_name = data.get("rune_name", "Jera")
    alch_stage = data.get("alchemical_stage", elem["alch"])

    seed_val = hash(data.get("title", "")) + random.randint(1, 999999)
    FONT = "Cormorant Garamond, Georgia, serif"

    # Hexagram name resolution
    hex_name = data.get("hexagram_name", "Limitation")
    hex_lines = data.get("hexagram_lines", [0,1,0,1,1,0])
    for num, (name, lines) in HEXAGRAMS.items():
        if hex_name.lower() in name.lower() or name.lower() in hex_name.lower():
            hex_name = name
            hex_lines = lines
            break

    title = html.escape(str(data.get("title", "UNTITLED")).upper())
    maori_subtitle = html.escape(str(data.get("maori_subtitle", "")))
    aphorism = html.escape(str(data.get("aphorism", "")))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <!-- INTENSE EMBOSSED FOIL SHADOW (Maximum legibility over bright scenery) -->
    <filter id="foil-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000000" flood-opacity="1.0"/>
      <feDropShadow dx="0" dy="5" stdDeviation="12" flood-color="#000000" flood-opacity="0.95"/>
      <feDropShadow dx="0" dy="8" stdDeviation="24" flood-color="#000000" flood-opacity="0.75"/>
    </filter>
  </defs>

  <style>
    .gold-text {{ font-family: {FONT}; fill: {GOLD_BRIGHT}; filter: url(#foil-glow); }}
    .bright-text {{ font-family: {FONT}; fill: {GOLD_LIGHT}; filter: url(#foil-glow); }}
    .italic-text {{ font-family: {FONT}; font-style: italic; fill: {GOLD_BRIGHT}; filter: url(#foil-glow); }}
  </style>

  <!-- BORDER FRAMES -->
  <rect x="40" y="50" width="{WIDTH-80}" height="{HEIGHT-100}" rx="32" fill="none" stroke="{BORDER_DARK}" stroke-width="3.5" filter="url(#foil-glow)"/>
  <rect x="52" y="62" width="{WIDTH-104}" height="{HEIGHT-124}" rx="24" fill="none" stroke="{elem['color']}" stroke-width="2.4" opacity="0.65" filter="url(#foil-glow)"/>

  <!-- TOP FLANKS (Rows C-D: Larger, Bolder) -->
  <text x="90" y="205" class="italic-text" font-size="36" letter-spacing="4" opacity="1.0">{elem['maori']}</text>
  <text x="90" y="250" class="italic-text" font-size="26" opacity="0.85">{astro_maori}</text>

  <text x="{WIDTH-90}" y="205" text-anchor="end" class="gold-text" font-size="36" font-weight="bold" letter-spacing="4" fill="{elem['color']}">{elem['eng']}</text>
  <text x="{WIDTH-90}" y="250" text-anchor="end" class="gold-text" font-size="26" opacity="0.85">{astro_english}</text>

  <!-- PROCEDURAL GENERATIVE SACRED GEOMETRY -->
  {build_procedural_geometry(seed_val, element=elem_key, cx=540, cy=1010)}

  <!-- ESOTERIC FLANKS (Larger & More Radiant) -->
  <g transform="translate(150, 1410) scale(1.8)" filter="url(#foil-glow)">
    <path d="{ALCHEMY_SVG.get(alch_stage, ALCHEMY_SVG['Nigredo'])}" stroke="{GOLD_BRIGHT}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.95"/>
  </g>
  {build_hexagram_svg(hex_lines, x=540, y=1465, w=170, h=105)}
  <g transform="translate({WIDTH-205}, 1400) scale(2.0)" filter="url(#foil-glow)">
    <path d="{RUNES_SVG.get(rune_name, RUNES_SVG['Jera'])}" stroke="{GOLD_BRIGHT}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.98"/>
  </g>

  <!-- TITLE & APHORISM (Bolder, Prominent & Embossed) -->
  <text x="540" y="1670" text-anchor="middle" class="bright-text" font-size="76" font-weight="500" letter-spacing="18">{title}</text>
  <text x="540" y="1740" text-anchor="middle" class="italic-text" font-size="42" letter-spacing="2.5" opacity="0.98">{maori_subtitle}</text>
  <text x="540" y="1825" text-anchor="middle" class="italic-text" font-size="38" opacity="0.92">{aphorism}</text>

  <!-- ATTRIBUTION -->
  <g transform="translate(325, 1885)" filter="url(#foil-glow)">
    {build_trigram_mini_icon(0, 0)}
    <text x="32" y="11" class="gold-text" font-size="24" opacity="0.8" letter-spacing="1.5">{hex_name}   ·   {rune_name}   ·   {alch_stage}</text>
  </g>
</svg>"""
    return svg

# ─── DIFFUSERS: GHIBLI PAINTERLY ENGINE (TOKEN SAFE) ───

_DREAMSHAPER_PIPE = None

def get_dreamshaper_pipe():
    global _DREAMSHAPER_PIPE
    if _DREAMSHAPER_PIPE is None:
        import torch
        from diffusers import StableDiffusionPipeline
        print("Activating DreamShaper 8 on Metal (MPS)...")
        _DREAMSHAPER_PIPE = StableDiffusionPipeline.from_pretrained(
            "Lykon/dreamshaper-8",
            torch_dtype=torch.float16,
            use_safetensors=True
        )
        _DREAMSHAPER_PIPE = _DREAMSHAPER_PIPE.to("mps")
        _DREAMSHAPER_PIPE.enable_attention_slicing()
    return _DREAMSHAPER_PIPE

def generate_ghibli_plate(prompt, output_plate_path="bg_plate.png"):
    pipe = get_dreamshaper_pipe()
    print(f"Painting Studio Ghibli background plate...")
    print(f"Prompt: {prompt}")

    # Compact 18-token signature keeps total tokens safely under CLIP's 77-token ceiling
    full_prompt = f"{prompt}, Studio Ghibli background art, painted by Kazuo Oga, lush anime nature, fluffy clouds, ancient ruins, cinematic lighting"
    negative_prompt = "humans, people, figures, character, silhouettes, walking, portrait, text, watermark, signature, photorealistic, 3d render, blurry"

    # Exact iPhone Aspect Ratio Generation (512x1104 is 1:2.156, nearly identical to 1080x2340 1:2.167)
    image = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=22,
        guidance_scale=7.5,
        width=512,
        height=1104
    ).images[0]

    image.save(output_plate_path)
    return output_plate_path

# ─── SMART SQUISH-FREE COMPOSITING ───

def render_wallpaper(svg_str, background_image_path=None, output_path="output.png"):
    import cairosvg
    import io

    if background_image_path and os.path.exists(background_image_path):
        raw_bg = Image.open(background_image_path).convert("RGBA")
        # ImageOps.fit scales & crops preserving pixel aspect ratio: ZERO squishing!
        base_img = ImageOps.fit(raw_bg, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)

        # Smart Ghibli Atmospheric Veil:
        veil = Image.new("RGBA", (WIDTH, HEIGHT), (10, 8, 7, 0))
        draw = ImageDraw.Draw(veil)
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            if ratio < 0.28:
                alpha = int(160)  # Clock & top flank zone
            elif ratio < 0.68:
                alpha = int(145 + (ratio - 0.28) * 35) # Geometry & text zone
            else:
                # Fade down so lush meadows and flora pop vibrantly
                alpha = int(max(30, 160 - (ratio - 0.68) * 450))
            draw.line([(0, y), (WIDTH, y)], fill=(10, 8, 7, alpha))

        base_img = Image.alpha_composite(base_img, veil)
    else:
        base_img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 9, 8, 255))

    png_bytes = cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), output_width=WIDTH, output_height=HEIGHT)
    overlay_img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")

    final_card = Image.alpha_composite(base_img, overlay_img)
    final_card.save(output_path, "PNG")
    print(f"✓ Card forged: {output_path}")

# ─── LOCAL LLM: DIVERSE SAMPLING (NO REPETITION) ───

def synthesize_with_mlx(concept_word):
    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler

    model_dir = LOCAL_MODEL_PATH if os.path.isdir(LOCAL_MODEL_PATH) else "mlx-community/Qwen2.5-7B-Instruct-4bit"
    print(f"Loading local archive model from: {model_dir}...")
    model, tokenizer = load(model_dir)

    suggested_maori = MAORI_LEXICON.get(concept_word.lower(), ("", ""))[0]
    hint = f"Curated Te Ao Māori hint: '{suggested_maori}'" if suggested_maori else ""

    prompt = f"""<|im_start|>system
You are a master esoteric scholar and poet of Te Ao Māori.
Map the concept to convergent traditions. Write completely unique, creative aphorisms. Never repeat clichés.

RULES:
1. title: Must be '{concept_word.upper()}'.
2. maori_subtitle: Authentic Māori translation (e.g. for Freedom use 'Rangirua kore'; for Threshold use 'Paepae'; for Stillness use 'Tūmārire'). {hint}
3. element: air|earth|void|water|fire.
4. astrology_planet: Saturn, Venus, Mars, Jupiter, Mercury, Sun, Moon, Neptune, Pluto, Uranus.
5. astrology_sign: Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces.
6. hexagram_name: Choose strictly from authentic canonical names: 'The Creative', 'The Receptive', 'Peace', 'Standstill', 'Contemplation', 'Splitting Apart', 'Return', 'The Abysmal Water', 'Keeping Still', 'The Gentle Wind', 'Dispersion', 'Limitation'.
7. rune_name: One of: Jera, Ansuz, Fehu, Uruz, Thurisaz, Raidho, Kenaz, Gebo, Wunjo, Hagalaz, Nauthiz, Isa, Eihwaz, Perthro, Algiz, Sowilo, Tiwaz, Berkano, Ehwaz, Mannaz, Laguz, Ingwaz, Dagaz, Othala.
8. aphorism: Exactly 4 to 6 words. Whispered, enigmatic, evocative wisdom. Never use 'whisper of'. No quotes.
9. scenic_prompt: Studio Ghibli landscape prompt under 35 words. Lush nature, rolling hills, ruins, clouds. STRICTLY NO HUMANS.

Return ONLY raw valid JSON.
<|im_end|>
<|im_start|>user
Concept: {concept_word}<|im_end|>
<|im_start|>assistant
"""
    print(f"Synthesizing convergent symbols for '{concept_word}'...")
    # Sampler with temperature 0.75 unlocks diverse, creative outputs
    sampler = make_sampler(temp=0.75, top_p=0.9)
    response = generate(model, tokenizer, prompt=prompt, max_tokens=350, sampler=sampler, verbose=False)

    text = response.strip()
    if "```" in text:
        text = text.split("```")[1].replace("json", "").strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {}

    data.setdefault("title", concept_word.upper())
    data.setdefault("maori_subtitle", suggested_maori or "Āhua")
    data.setdefault("element", "void")
    data.setdefault("astrology_planet", "Saturn")
    data.setdefault("astrology_sign", "Capricorn")
    data.setdefault("hexagram_name", "Contemplation")
    data.setdefault("rune_name", "Jera")
    data.setdefault("aphorism", "the root knows the stone")
    data.setdefault("scenic_prompt", "ancient overgrown stone archway among lush rolling hills and wildflowers, blue sky with fluffy clouds")

    print(json.dumps(data, indent=2, ensure_ascii=False))
    return data

# ─── BATCH & SINGLE DISPATCHER ───

def forge_single(concept, paint=False, out_dir=DEFAULT_OUT_DIR, custom_bg=None):
    os.makedirs(out_dir, exist_ok=True)
    card_data = synthesize_with_mlx(concept)

    bg_path = custom_bg
    if paint and not bg_path:
        prompt = card_data.get("scenic_prompt", "pastoral landscape, rolling green hills")
        temp_plate = os.path.join(out_dir, f"{concept.lower()}_plate.png")
        bg_path = generate_ghibli_plate(prompt, output_plate_path=temp_plate)

    svg_content = generate_card_svg(card_data)
    out_file = os.path.join(out_dir, f"{concept.lower()}-lockscreen.png")
    render_wallpaper(svg_content, background_image_path=bg_path, output_path=out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Card Forge")
    parser.add_argument("concept", nargs="?", default="Bonsai", help="Single seed word")
    parser.add_argument("--batch", type=str, default=None, help="Comma-separated concepts")
    parser.add_argument("--ai", action="store_true", help="Synthesize with local Qwen")
    parser.add_argument("--paint", action="store_true", help="Paint Studio Ghibli plate with DreamShaper 8")
    parser.add_argument("--out-dir", type=str, default=DEFAULT_OUT_DIR, help="Destination folder for wallpapers")
    parser.add_argument("--bg", type=str, default=None, help="Custom background image")
    args = parser.parse_args()

    if args.batch:
        concepts = [c.strip() for c in args.batch.split(",") if c.strip()]
        print(f"═══ FORGING BATCH OF {len(concepts)} CARDS ═══")
        for idx, word in enumerate(concepts, 1):
            print(f"\n[{idx}/{len(concepts)}] Forging '{word}'...")
            forge_single(word, paint=args.paint, out_dir=args.out_dir, custom_bg=args.bg)
        print(f"\n✓ Batch complete! All cards saved to: {args.out_dir}/")
    else:
        forge_single(args.concept, paint=args.paint, out_dir=args.out_dir, custom_bg=args.bg)
