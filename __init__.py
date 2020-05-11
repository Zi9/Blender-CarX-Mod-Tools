import bpy

bl_info = {
    'name': 'CarX Map Mod Helpers',
    'description': 'Addon for creating map mods for CarX Drift Racing Online',
    'author': 'Zi9',
    'version': (0, 0, 2),
    'blender': (2, 80, 0),
    'location': '3D View',
    'category': 'Development'
}

prefixes = ['road_', 'grass_', 'curb_', 'sand_']

def rename(ctx, prefix):
    for i in ctx.selected_objects:
        for j in prefixes:
            if i.name.startswith(j):
                i.name = i.name[len(j):]
        i.name = prefix + i.name


class CXTool_SetAsphalt(bpy.types.Operator):
    bl_idname = 'object.cxtools_road'
    bl_label = 'Asphalt'
    def execute(self, context):
        rename(context, 'road_')
        return {'FINISHED'}


class CXTool_SetGrass(bpy.types.Operator):
    bl_idname = 'object.cxtools_grass'
    bl_label = 'Grass'
    def execute(self, context):
        rename(context, 'grass_')
        return {'FINISHED'}


class CXTool_SetCurb(bpy.types.Operator):
    bl_idname = 'object.cxtools_curb'
    bl_label = 'Curb'
    def execute(self, context):
        rename(context, 'curb_')
        return {'FINISHED'}


class CXTool_SetSand(bpy.types.Operator):
    bl_idname = 'object.cxtools_sand'
    bl_label = 'Sand'
    def execute(self, context):
        rename(context, 'sand_')
        return {'FINISHED'}


class CXTools_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_CXTools'
    bl_label = 'CarX Map Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CarX Map Tools'
    bl_context = 'objectmode'

    def draw(self, context):
        self.layout.label(text='Set physics material', icon='HAND')
        self.layout.operator(CXTool_SetAsphalt.bl_idname, icon='AUTO')
        self.layout.operator(CXTool_SetGrass.bl_idname, icon='SEQ_HISTOGRAM')
        self.layout.operator(CXTool_SetCurb.bl_idname, icon='PARTICLEMODE')
        self.layout.operator(CXTool_SetSand.bl_idname, icon='FORCE_FORCE')

def register():
    bpy.utils.register_class(CXTool_SetAsphalt)
    bpy.utils.register_class(CXTool_SetGrass)
    bpy.utils.register_class(CXTool_SetCurb)
    bpy.utils.register_class(CXTool_SetSand)
    bpy.utils.register_class(CXTools_Panel)


def unregister():
    bpy.utils.unregister_class(CXTool_SetAsphalt)
    bpy.utils.unregister_class(CXTool_SetGrass)
    bpy.utils.unregister_class(CXTool_SetCurb)
    bpy.utils.unregister_class(CXTool_SetSand)
    bpy.utils.unregister_class(CXTools_Panel)
