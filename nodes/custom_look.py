"""PostFx Custom Look — build a look from the most-used knobs, or override those
knobs on top of an incoming look. Each control at its neutral value is left
untouched, so connecting a base look + nudging one slider changes only that op.
"""

from . import _util as u


class PostFxCustomLook:
    CATEGORY = "PostFx"
    FUNCTION = "build"
    RETURN_TYPES = (u.POSTFX_LOOK,)
    RETURN_NAMES = ("look",)
    DESCRIPTION = ("Build a custom look from common controls (white balance, "
                   "exposure, contrast, vibrance/saturation, grain, vignette, "
                   "halation, clarity). With a 'look' input, only the controls "
                   "you move off neutral override it; the rest pass through.")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "temp": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0,
                                   "step": 0.01,
                                   "tooltip": "White balance: >0 warm, <0 cool."}),
                "tint": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0,
                                   "step": 0.01,
                                   "tooltip": ">0 magenta, <0 green."}),
                "exposure": ("FLOAT", {"default": 0.0, "min": -3.0, "max": 3.0,
                                       "step": 0.05, "tooltip": "Stops of light."}),
                "contrast": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                       "step": 0.01,
                                       "tooltip": "S-curve contrast strength."}),
                "vibrance": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0,
                                       "step": 0.01,
                                       "tooltip": "Lifts low-sat pixels, "
                                                  "protects skin."}),
                "saturation": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0,
                                         "step": 0.01,
                                         "tooltip": "Uniform saturation "
                                                    "(1 = unchanged)."}),
                "grain": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 0.1,
                                    "step": 0.002,
                                    "tooltip": "Luma grain amount."}),
                "grain_size": ("FLOAT", {"default": 1.5, "min": 0.5, "max": 4.0,
                                         "step": 0.1,
                                         "tooltip": "Grain size (px @ 1024 edge)."}),
                "vignette": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0,
                                       "step": 0.01,
                                       "tooltip": "Edge darkening amount."}),
                "halation": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 2.0,
                                       "step": 0.05,
                                       "tooltip": "Highlight bloom strength."}),
                "clarity": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0,
                                      "step": 0.01,
                                      "tooltip": "Local contrast; <0 softens."}),
            },
            "optional": {
                "look": (u.POSTFX_LOOK, {"tooltip": "Base look to override on "
                                                    "top of (e.g. a theme)."}),
            },
        }

    def build(self, temp, tint, exposure, contrast, vibrance, saturation,
              grain, grain_size, vignette, halation, clarity, look=None):
        base = u.clone_look(look) if look is not None else u.neutral_look()

        ov = {}
        if temp != 0.0 or tint != 0.0:
            ov["white_balance"] = {"temp": float(temp), "tint": float(tint)}
        if exposure != 0.0:
            ov["exposure"] = {"stops": float(exposure)}
        if contrast != 0.0:
            ov["tone_curve"] = {"strength": float(contrast)}
        if vibrance != 0.0 or saturation != 1.0:
            ov["vibrance"] = {"vibrance": float(vibrance),
                              "saturation": float(saturation)}
        if grain > 0.0:
            ov["grain"] = {"luma": float(grain), "size": float(grain_size)}
        if vignette > 0.0:
            ov["vignette"] = {"strength": float(vignette)}
        if halation > 0.0:
            ov["halation"] = {"strength": float(halation)}
        if clarity != 0.0:
            ov["clarity"] = {"amount": float(clarity)}

        merged = u.merge_look(base, ov)
        base_name = base.get("name", "look")
        merged["name"] = base_name if not ov else f"{base_name}+custom"
        return (merged,)


NODE_CLASS_MAPPINGS = {"PostFxCustomLook": PostFxCustomLook}
NODE_DISPLAY_NAME_MAPPINGS = {"PostFxCustomLook": "PostFx Custom Look"}
