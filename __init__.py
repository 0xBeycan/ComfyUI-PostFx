"""ComfyUI-PostFx — theme-based film-emulation & post-processing nodes.

Wraps the `postfx` pipeline (https://github.com/0xBeycan/postfx) as ComfyUI
nodes. ComfyUI imports this package and reads the two mappings below.
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
