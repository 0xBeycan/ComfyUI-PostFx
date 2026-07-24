"""PostFx Signature Sheet — render a labeled grid of every theme in a category
applied to one image, for quick side-by-side comparison (postfx `sheet`).
"""

import os
import tempfile
import uuid

from . import _util as u


class PostFxSignatureSheet:
    CATEGORY = "PostFx"
    FUNCTION = "build"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("sheet",)
    DESCRIPTION = ("Render a labeled contact sheet of every theme in a category "
                   "applied to the first image, as a single preview image. "
                   "'signature' is the market-standard set.")

    @classmethod
    def INPUT_TYPES(cls):
        conditions = u.condition_names()
        return {
            "required": {
                "image": ("IMAGE",),
                "category": (["signature", "experimental", "all"],
                             {"default": "signature"}),
                "condition": (conditions, {"default": "neutral"}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.5,
                                       "step": 0.05}),
                "columns": ("INT", {"default": 5, "min": 1, "max": 10}),
            },
        }

    def build(self, image, category, condition, strength, columns):
        from postfx.sheet import build_contact_sheet

        src = u.image_to_np_list(image)[0]  # first frame is the sample
        tmp = os.path.join(tempfile.gettempdir(),
                           f"postfx_sheet_{uuid.uuid4().hex}.jpg")
        try:
            build_contact_sheet(src, tmp, category=category, condition=condition,
                                strength=float(strength), cols=int(columns))
            rgb, _alpha = u.postfx.imgio.load_image(tmp)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

        return (u.np_list_to_image([rgb]),)


NODE_CLASS_MAPPINGS = {"PostFxSignatureSheet": PostFxSignatureSheet}
NODE_DISPLAY_NAME_MAPPINGS = {"PostFxSignatureSheet": "PostFx Signature Sheet"}
