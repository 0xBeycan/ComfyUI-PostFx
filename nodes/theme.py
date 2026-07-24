"""PostFx Theme — emits a built-in theme as a POSTFX_LOOK, so a named look can
start a chain (Theme -> LUT / Custom Look -> Apply). For the simple case just
use the theme dropdown on PostFx Apply directly.
"""

from . import _util as u


class PostFxTheme:
    CATEGORY = "PostFx"
    FUNCTION = "load"
    RETURN_TYPES = (u.POSTFX_LOOK,)
    RETURN_NAMES = ("look",)
    DESCRIPTION = ("Load a built-in postfx theme as a look you can pipe into "
                   "PostFx LUT / Custom Look / Apply. Use this only to build a "
                   "chain from a named theme; otherwise pick the theme on Apply.")

    @classmethod
    def INPUT_TYPES(cls):
        themes = u.theme_names()
        default_theme = "portra_400" if "portra_400" in themes else themes[0]
        return {
            "required": {
                "theme": (themes, {"default": default_theme}),
            },
        }

    def load(self, theme):
        return (u.load_theme(theme),)


NODE_CLASS_MAPPINGS = {"PostFxTheme": PostFxTheme}
NODE_DISPLAY_NAME_MAPPINGS = {"PostFxTheme": "PostFx Theme"}
