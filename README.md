# Card Forge 🜂




> An automated esoteric lockscreen wallpaper forge. Converges Te Ao Māori cosmology, the I Ching, Elder Futhark runes, Hermetic alchemy, and procedural sacred geometry over Studio Ghibli-inspired painterly landscapes.



Calibrated specifically for **Retina iPhone lockscreens** (iPhone 13 mini / 14 / 15 / 16), leaving the clock, widgets, flashlight, and camera controls completely unblocked.

---

## Prerequisites

* **Hardware:** Apple Silicon Mac (M1/M2/M3/M4, 16 GB+ unified memory recommended).

* **Environment:** Python 3.10+ installed.
  

---

## Installation & Setup




### 1. Clone the Repository

```bash
git clone https://github.com/Raphsolt/card-forge.git
cd card-forge
```



### 2. Set Up Virtual Environment & Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install the Manuscript Font (macOS)

The repository includes **Cormorant Garamond**, Christian Thalmann's open-source classical serif revival. Install it to your macOS user font book:

```bash
cp CormorantGaramond-*.ttf ~/Library/Fonts/
```

### 4. Download the Local Synthesis Model (Qwen 2.5 7B)

The symbolic synthesis engine runs 100% locally via Apple Metal using `mlx-lm`. Download the 4-bit quantized model directly into the project folder:

```bash
python3 -c "from huggingface_hub import snapshot_download; snapshot_download('mlx-community/Qwen2.5-7B-Instruct-4bit', local_dir='./Qwen2.5-7B-Instruct-4bit')"
```

---

## Usage

### Forge a Single Card (Dark OLED Codex)

Generates an instant, razor-sharp vector wallpaper on a deep pitch-black OLED background:

```bash
python3 card_forge.py --ai "Silence"
```

### Forge with Studio Ghibli Atmospheric Plate

Synthesizes the card with local Qwen, paints a custom Kazuo Oga-style landscape plate using DreamShaper 8 on Metal (`mps`), and composites embossed gold-foil typography on top:

```bash
python3 card_forge.py --ai "Bonsai" --paint
```

*(Note: On the first `--paint` run, `diffusers` will automatically download the ~2.1 GB pruned DreamShaper 8 model into your cache. Subsequent generations take ~25–35 seconds).*

### Batch Mode (Forge Multiple Cards)

Forge an entire series in sequence without reloading models into memory:

```bash
python3 card_forge.py --batch "Bonsai, Freedom, Threshold, Stillness" --paint
```

### Custom Export Folder (iCloud Shared Album)

To automatically deposit finished wallpapers into a specific folder or iCloud directory:

```bash
python3 card_forge.py --batch "Bonsai, Freedom" --paint --out-dir "/Users/yourname/Pictures/TarotCards"
```

---

## Setting Up on iOS

1. Add the generated images in `output/` to a **Shared iCloud Photo Album**.
2. On your iPhone, create a new Lock Screen wallpaper.
3. Select **Photo Shuffle** → **Album** → choose your shared album.
4. Set the shuffle frequency to **On Tap** or **Hourly**.

---

## Architecture & Stack

```
[ Concept Word ]
       │
       ▼
┌────────────────────────────────────────┐
│  MLX-LM: Qwen 2.5 7B (Instruct 4-bit)  │
│  - Reality Knowledge Bank Lookup       │
│  - Te Ao Māori / Astrology / Runes     │
│  - 4 to 6-word whispered aphorism      │
└──────────────┬─────────────────────────┘
               │
       ┌───────┴────────────────────────┐
       ▼                                ▼
[ Procedural Sacred Geometry ]   [ Diffusers: DreamShaper 8 ]
- Parametric harmonic lattices   - Studio Ghibli pastoral plate
- Astrolabe dials & nodes        - Kazuo Oga watercolor sky
       │                                │
       └────────────────┬───────────────┘
                        ▼
┌────────────────────────────────────────┐
│  Compositor (CairoSVG + Pillow)        │
│  - Dual-layer gold foil shadow armor   │
│  - Atmospheric gradient veil           │
│  - Exact Retina resolution (1080x2340) │
└────────────────────────────────────────┘
```

See [READING_GUIDE.md](READING_GUIDE.md) for the complete symbolic framework.




