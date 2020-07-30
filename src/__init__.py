import bpy
from . import MapTools


bl_info = {
    "name": "Zi9's CarX Mod Tools",
    "description": "Toolkit to assist creating mods for CarX Drift Racing Online",
    "author": "Zi9",
    "version": (1, 3, 1),
    "blender": (2, 80, 0),
    "location": "3D View",
    "category": "Development",
}


def register():
    MapTools.register()


def unregister():
    MapTools.unregister()
