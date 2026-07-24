# ComfyUI-PostFx

**Theme-based film-emulation & post-processing nodes for ComfyUI**, powered by
the [`postfx`](https://github.com/0xBeycan/postfx) pipeline — film stocks,
cinematic grades and `.cube` LUTs, defined in YAML, running on the CPU (no GPU,
no ML). Pick a look, dial a shooting condition and a global strength, and every
image gets the same consistent, reusable visual identity.

## Install

**ComfyUI-Manager:** search for *ComfyUI-PostFx* and install.

**Manual:**
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/0xBeycan/ComfyUI-PostFx.git
pip install -r ComfyUI-PostFx/requirements.txt   # installs the `postfx` package
```
Restart ComfyUI. The nodes appear under the **PostFx** category.

## Nodes

| Node | In → Out | What it does |
|------|----------|--------------|
| **PostFx Apply** | IMAGE (+ *look*, *mask*) → IMAGE | The core node. Applies a **theme** + **condition** + **strength** to an image batch. A connected `look` overrides the theme dropdown; an optional `mask` limits the effect to the masked region. |
| **PostFx Theme** | → LOOK | Emits a built-in theme as a `look`, to start a chain from a named theme. |
| **PostFx Custom Look** | (*look*) → LOOK | Build a look from common controls (white balance, exposure, contrast, vibrance/saturation, grain, vignette, halation, clarity). With a `look` input, only the knobs you move off neutral override it. |
| **PostFx LUT** | (*look*) → LOOK | Attach a 3D `.cube` LUT. Standalone by default; connect a `look` to layer the LUT on top of a theme. |
| **PostFx Signature Sheet** | IMAGE → IMAGE | Labeled contact-sheet grid of every theme in a category — quick side-by-side comparison. |

`LOOK` = `POSTFX_LOOK`, the link type carried between the look-producing nodes
and **PostFx Apply**. Every look node has an optional `look` input, so they
chain in any order.

## Usage

**Simple** — one theme:
```
Load Image → PostFx Apply (theme = portra_400) → Save Image
```

**Advanced** — a theme, your own LUT, extra grain, a night condition:
```
PostFx Theme (portra_400)
   → PostFx LUT (my_look.cube)
   → PostFx Custom Look (grain ↑)
   → PostFx Apply (condition = neon_night, strength = 1.0)
   → Save Image
```

## Concepts (from `postfx`)

- **Theme** = the *look* (color/grain/lens), defined in YAML. 15 `signature`
  (real film stocks & industry grades: Portra 400, Cinestill 800T, Kodachrome,
  teal-orange…) + 15 `experimental`.
- **Condition** = a *separate axis*. It scales only the texture (grain, chroma
  noise, halation) for the shooting situation — `neutral`, `day_outdoor`,
  `overcast`, `indoor_evening`, `neon_night`, `night_flash`. It does not change
  color, so one theme stays consistent across conditions.
- **Strength** `0.0–1.5` — linearly blends the whole effect with the original
  (`0` = untouched, `1` = full, `>1` = over).
- **Seed** — grain is deterministic. `batch_seed = increment` gives a different
  grain per frame across a batch; `fixed` uses one seed for all.
- **Deterministic & resolution-safe** — no crop/resize; grain/blur scale with
  image size, so a look reads identically at any resolution.

## LUTs

Drop `.cube` **3D** LUTs into this repo's [`luts/`](luts/) folder to see them in
the **PostFx LUT** dropdown, or point its `lut_path` at any absolute path. A LUT
applies mid-pipeline (display/sRGB space), so a theme's color grade runs before
it and grain/vignette/sharpen finish on top.

## License

[MIT](LICENSE) © 0xBeycan · built on [`postfx`](https://github.com/0xBeycan/postfx).
