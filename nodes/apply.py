"""PostFx Apply — the core node. Applies a look (theme) + condition + global
strength to an IMAGE batch, with optional look override and mask-limited blend.
"""

from . import _util as u


class PostFxApply:
    CATEGORY = "PostFx"
    FUNCTION = "apply"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    DESCRIPTION = ("Apply a postfx film-emulation look to an image batch. Pick a "
                   "built-in theme + shooting condition, or feed a look from a "
                   "PostFx Theme / Custom Look / LUT node (a connected look "
                   "overrides the theme dropdown). An optional mask limits the "
                   "effect to the masked region.")

    @classmethod
    def INPUT_TYPES(cls):
        themes = ["none"] + u.theme_names()
        default_theme = u.default_theme(themes)
        conditions = u.condition_names()
        return {
            "required": {
                "image": ("IMAGE",),
                "theme": (themes, {"default": default_theme,
                                   "tooltip": "Built-in look. 'none' passes the "
                                              "image through untouched. Ignored "
                                              "when a 'look' input is connected."}),
                "condition": (conditions, {"default": "neutral",
                                           "tooltip": "Shooting condition: scales "
                                                      "grain/chroma/halation only."}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.5,
                                       "step": 0.05,
                                       "tooltip": "0 = original, 1 = full look, "
                                                  ">1 = over."}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffff,
                                 "tooltip": "Grain seed (deterministic)."}),
                "batch_seed": (["fixed", "increment"], {"default": "fixed",
                               "tooltip": "increment = a different grain per "
                                          "frame across the batch."}),
            },
            "optional": {
                "look": (u.POSTFX_LOOK, {"tooltip": "A look from a PostFx Theme / "
                                                    "Custom Look / LUT node. "
                                                    "Overrides 'theme'."}),
                "mask": ("MASK", {"tooltip": "Apply the effect only where the "
                                             "mask is white; blend with original. "
                                             "An all-black mask (e.g. LoadImage "
                                             "on an image without alpha) is "
                                             "ignored and the effect applies "
                                             "everywhere."}),
            },
        }

    def apply(self, image, theme, condition, strength, seed, batch_seed,
              look=None, mask=None):
        if look is None and theme == "none":
            return (image,)
        look_cfg = look if look is not None else u.resolve_theme(u.theme_stem(theme))
        cond_cfg = u.get_condition(condition)

        frames = u.image_to_np_list(image)
        h, w = frames[0].shape[:2]
        # LoadImage emits an all-zero placeholder mask for images without an
        # alpha channel; blending against it would be a silent no-op.
        if mask is not None and not bool(mask.any()):
            mask = None
        masks = (u.mask_to_np_list(mask, len(frames), (h, w))
                 if mask is not None else None)

        out_frames = []
        for i, src in enumerate(frames):
            frame_seed = seed + (i if batch_seed == "increment" else 0)
            out = u.postfx.process(src, look_cfg, cond_cfg, float(strength),
                                   int(frame_seed))
            if masks is not None:
                m = masks[i][..., None]
                out = src * (1.0 - m) + out * m
            out_frames.append(out)

        return (u.np_list_to_image(out_frames),)


NODE_CLASS_MAPPINGS = {"PostFxApply": PostFxApply}
NODE_DISPLAY_NAME_MAPPINGS = {"PostFxApply": "PostFx Apply"}
