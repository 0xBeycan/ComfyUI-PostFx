"""PostFx LUT — attach a 3D .cube LUT to a look. A LUT is a baked color grade,
so by default this produces a standalone LUT look; connect a 'look' to ride the
LUT on top of a theme instead. Drop your own .cube files in the package
`luts/` folder to see them in the dropdown, or point to any absolute path.
"""

import os

from . import _util as u


class PostFxLut:
    CATEGORY = "PostFx"
    FUNCTION = "build"
    RETURN_TYPES = (u.POSTFX_LOOK,)
    RETURN_NAMES = ("look",)
    DESCRIPTION = ("Apply a 3D .cube LUT as a look. Select a file from the "
                   "package luts/ folder or give an absolute lut_path. Standalone "
                   "by default; connect a look to layer the LUT on top of it. The "
                   "LUT applies mid-pipeline, so grain/vignette still finish on top.")

    @classmethod
    def INPUT_TYPES(cls):
        luts = ["none"] + u.lut_files()
        return {
            "required": {
                "lut": (luts, {"default": "none",
                               "tooltip": "A .cube file from the package "
                                          "luts/ folder."}),
                "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0,
                                        "step": 0.01,
                                        "tooltip": "Blend the LUT with its "
                                                   "input (0 = off)."}),
            },
            "optional": {
                "lut_path": ("STRING", {"default": "",
                                        "tooltip": "Absolute path to a .cube "
                                                   "(overrides the dropdown)."}),
                "look": (u.POSTFX_LOOK, {"tooltip": "Base look to layer the LUT "
                                                    "on top of."}),
            },
        }

    def build(self, lut, intensity, lut_path="", look=None):
        base = u.clone_look(look) if look is not None else u.neutral_look()

        path = lut_path.strip()
        if not path and lut != "none":
            path = os.path.join(u.LUTS_DIR, lut)

        if path:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"LUT file not found: {path!r}")
            base = u.merge_look(base, {"lut": {"file": path,
                                               "intensity": float(intensity)}})
            base["name"] = f"{base.get('name', 'look')}+lut"
        return (base,)


NODE_CLASS_MAPPINGS = {"PostFxLut": PostFxLut}
NODE_DISPLAY_NAME_MAPPINGS = {"PostFxLut": "PostFx LUT"}
