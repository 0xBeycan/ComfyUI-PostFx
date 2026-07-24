"""Aggregate the node class + display-name mappings from every node module."""

from . import apply, custom_look, lut, sheet, theme

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for _mod in (apply, theme, custom_look, lut, sheet):
    NODE_CLASS_MAPPINGS.update(_mod.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(_mod.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
