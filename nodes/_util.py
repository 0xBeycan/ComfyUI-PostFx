"""Shared helpers for the PostFx ComfyUI nodes.

Bridges ComfyUI's IMAGE/MASK torch tensors and postfx's numpy arrays, and
exposes the theme / condition catalogs used to build node dropdowns.

ComfyUI IMAGE : torch.Tensor (B, H, W, 3), float32, [0,1], RGB.
postfx.process: numpy       (H, W, 3),    float32, [0,1], RGB.
The two formats line up exactly, so per-frame conversion is a plain copy.

torch is imported lazily (inside functions) so this module — and the theme /
condition catalogs — can be imported and unit-tested without torch present.
"""

import copy
import os

import numpy as np

import postfx
from postfx import get_condition, list_conditions, list_themes, load_theme
from postfx.pipeline import resolve_theme
from postfx.theme import DEFAULTS, _deep_merge

# The custom link type carried between look-producing nodes and PostFx Apply.
# The value is a full theme dict (output of load_theme / resolve_theme).
POSTFX_LOOK = "POSTFX_LOOK"

# Directory where users drop their own .cube LUT files (listed by PostFx LUT).
LUTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "luts")


# --- Catalogs (built once, used to populate dropdowns) --------------------

def theme_names():
    """All built-in theme stems, ordered signature -> luts -> experimental."""
    return [stem for stem, _desc, _cat in list_themes()]


def theme_tooltip():
    """`theme -> 'category · description'` map, for dropdown tooltips."""
    return {stem: (f"{cat} · {desc}" if desc else cat)
            for stem, desc, cat in list_themes()}


def condition_names():
    """All condition names, ordered by increasing texture intensity."""
    return [name for name, _desc in list_conditions()]


def lut_files():
    """`.cube` file names sitting in the package `luts/` folder, sorted."""
    if not os.path.isdir(LUTS_DIR):
        return []
    return sorted(f for f in os.listdir(LUTS_DIR)
                  if f.lower().endswith(".cube"))


def neutral_look():
    """A full, valid look with every op at its no-op default."""
    return resolve_theme({})


def merge_look(base, overrides):
    """Deep-merge `overrides` (partial op blocks) onto a base look dict."""
    return _deep_merge(base, overrides)


def clone_look(look):
    return copy.deepcopy(look)


# --- Tensor <-> numpy bridge ----------------------------------------------

def image_to_np_list(image):
    """ComfyUI IMAGE tensor (B,H,W,3) -> list of float32 (H,W,3) numpy arrays."""
    arr = image.detach().cpu().numpy()
    return [np.ascontiguousarray(arr[i], dtype=np.float32)
            for i in range(arr.shape[0])]


def np_list_to_image(frames):
    """List of float32 (H,W,3) arrays -> ComfyUI IMAGE tensor (B,H,W,3)."""
    import torch
    stacked = np.stack([np.clip(f, 0.0, 1.0).astype(np.float32) for f in frames],
                       axis=0)
    return torch.from_numpy(stacked)


def mask_to_np_list(mask, count, hw):
    """ComfyUI MASK (B,H,W) or (H,W) -> list of `count` float32 (H,W) arrays,
    resized to `hw`=(H,W) and value-clamped. A single mask broadcasts to all
    frames; a shorter batch reuses its last mask.
    """
    import cv2
    m = mask.detach().cpu().numpy().astype(np.float32)
    if m.ndim == 2:
        m = m[None]
    h, w = hw
    out = []
    for i in range(count):
        mm = m[i] if i < m.shape[0] else m[-1]
        if mm.shape != (h, w):
            mm = cv2.resize(mm, (w, h), interpolation=cv2.INTER_LINEAR)
        out.append(np.clip(mm, 0.0, 1.0))
    return out


__all__ = [
    "POSTFX_LOOK", "LUTS_DIR",
    "theme_names", "theme_tooltip", "condition_names", "lut_files",
    "neutral_look", "merge_look", "clone_look",
    "image_to_np_list", "np_list_to_image", "mask_to_np_list",
    "postfx", "get_condition", "load_theme", "resolve_theme", "DEFAULTS",
]
