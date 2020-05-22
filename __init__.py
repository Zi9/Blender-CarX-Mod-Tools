import bpy
from . import MapTools


bl_info = {
    'name': 'Zi9\'s CarX Mod Tools',
    'description': 'Addon for creating mods for CarX Drift Racing Online',
    'author': 'Zi9',
    'version': (0, 2, 0),
    'blender': (2, 80, 0),
    'location': '3D View',
    'category': 'Development'
}

def register():
    MapTools.register()

def unregister():
    MapTools.unregister()
