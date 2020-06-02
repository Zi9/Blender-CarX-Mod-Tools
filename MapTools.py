import bpy
import bmesh

types = ['road',
         'grass',
         'kerb',
         'sand',
         'snow',
         'gravel',
         'icyroad',
         'dirt',
         'alpha',
         'nocol',
         'rb',
         'alphanocol',
         'alpharb',
         'nocolrb',
         'alphanocolrb']

def prefix(ctx, phymat):
    for i in ctx.selected_objects:
        if i.name.split('_')[0] in types:
            i.name = i.name.replace(i.name.split('_')[0], phymat, 1)
        else:
            i.name = phymat + '_' + i.name


class CXMap_SetAsphalt(bpy.types.Operator):
    bl_idname = 'object.cxmap_road'
    bl_label = 'Asphalt'
    def execute(self, context):
        prefix(context, 'road')
        return {'FINISHED'}


class CXMap_SetGrass(bpy.types.Operator):
    bl_idname = 'object.cxmap_grass'
    bl_label = 'Grass'
    def execute(self, context):
        prefix(context, 'grass')
        return {'FINISHED'}


class CXMap_SetCurb(bpy.types.Operator):
    bl_idname = 'object.cxmap_curb'
    bl_label = 'Curb'
    def execute(self, context):
        prefix(context, 'kerb')
        return {'FINISHED'}


class CXMap_SetSand(bpy.types.Operator):
    bl_idname = 'object.cxmap_sand'
    bl_label = 'Sand'
    def execute(self, context):
        prefix(context, 'sand')
        return {'FINISHED'}


class CXMap_SetSnow(bpy.types.Operator):
    bl_idname = 'object.cxmap_snow'
    bl_label = 'Snow'
    def execute(self, context):
        prefix(context, 'snow')
        return {'FINISHED'}


class CXMap_SetGravel(bpy.types.Operator):
    bl_idname = 'object.cxmap_gravel'
    bl_label = 'Gravel'
    def execute(self, context):
        prefix(context, 'gravel')
        return {'FINISHED'}


class CXMap_SetDirt(bpy.types.Operator):
    bl_idname = 'object.cxmap_dirt'
    bl_label = 'Dirt'
    def execute(self, context):
        prefix(context, 'dirt')
        return {'FINISHED'}


class CXMap_SetIcyRoad(bpy.types.Operator):
    bl_idname = 'object.cxmap_icyroad'
    bl_label = 'Icy Road'
    def execute(self, context):
        prefix(context, 'icyroad')
        return {'FINISHED'}


class CXMap_SetAlpha(bpy.types.Operator):
    bl_idname = 'object.cxmap_alpha'
    bl_label = 'Alpha'
    def execute(self, context):
        prefix(context, 'alpha')
        return {'FINISHED'}


class CXMap_SetNoCol(bpy.types.Operator):
    bl_idname = 'object.cxmap_nocol'
    bl_label = 'No Collision'
    def execute(self, context):
        prefix(context, 'nocol')
        return {'FINISHED'}


class CXMap_SetRigidbody(bpy.types.Operator):
    bl_idname = 'object.cxmap_rigidbody'
    bl_label = 'Rigidbody'
    def execute(self, context):
        prefix(context, 'rb')
        return {'FINISHED'}


class CXMap_SetAlphaNoCol(bpy.types.Operator):
    bl_idname = 'object.cxmap_alphanocol'
    bl_label = 'Alpha + No Collision'
    def execute(self, context):
        prefix(context, 'alphanocol')
        return {'FINISHED'}


class CXMap_SetAlphaRigidbody(bpy.types.Operator):
    bl_idname = 'object.cxmap_alpharigidbody'
    bl_label = 'Alpha + Rigidbody'
    def execute(self, context):
        prefix(context, 'alpharb')
        return {'FINISHED'}


class CXMap_SetNoColRigidbody(bpy.types.Operator):
    bl_idname = 'object.cxmap_nocolrigidbody'
    bl_label = 'No Collision + Rigidbody'
    def execute(self, context):
        prefix(context, 'nocolrb')
        return {'FINISHED'}


class CXMap_SetAlphaNoColRigidbody(bpy.types.Operator):
    bl_idname = 'object.cxmap_alphanocolrb'
    bl_label = 'Alpha + No Collision + Rigidbody'
    def execute(self, context):
        prefix(context, 'alphanocolrb')
        return {'FINISHED'}

# class CXMap_CreateSpawn(bpy.types.Operator):
    # bl_idname = 'object.cxmap_spawnpoint'
    # bl_label = 'Create Spawn Point'

    # @classmethod
    # def poll(cls, context):
        # return True

    # def execute(self, context):
        # bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
        # context.active_object.name = 'Spawnpoint'
        # return {'FINISHED'}



class CXMap_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_CXMaps'
    bl_label = 'CarX Map Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CarX Mod Tools'
    bl_context = 'objectmode'

    def draw(self, context):
        self.layout.label(text='Set physics material', icon='HAND')
        self.layout.operator(CXMap_SetAsphalt.bl_idname, icon='AUTO')
        self.layout.operator(CXMap_SetGrass.bl_idname, icon='SEQ_HISTOGRAM')
        self.layout.operator(CXMap_SetCurb.bl_idname, icon='PARTICLEMODE')
        self.layout.operator(CXMap_SetSand.bl_idname, icon='FORCE_FORCE')
        self.layout.operator(CXMap_SetSnow.bl_idname, icon='FREEZE')
        self.layout.operator(CXMap_SetGravel.bl_idname, icon='MOD_OCEAN')
        self.layout.operator(CXMap_SetDirt.bl_idname, icon='MOD_SMOOTH')
        self.layout.operator(CXMap_SetIcyRoad.bl_idname, icon='TRACKING')
        self.layout.label(text='Set object type', icon='OUTLINER_OB_MESH')
        self.layout.operator(CXMap_SetAlpha.bl_idname, icon='IMAGE_ALPHA')
        self.layout.operator(CXMap_SetNoCol.bl_idname, icon='MOD_SOLIDIFY')
        self.layout.operator(CXMap_SetRigidbody.bl_idname, icon='RIGID_BODY')
        self.layout.operator(CXMap_SetAlphaNoCol.bl_idname)
        self.layout.operator(CXMap_SetAlphaRigidbody.bl_idname)
        self.layout.operator(CXMap_SetNoColRigidbody.bl_idname)
        self.layout.operator(CXMap_SetAlphaNoColRigidbody.bl_idname)
        # self.layout.label(text='Spawnpoint', icon='EMPTY_AXIS')
        # self.layout.operator(CXMap_CreateSpawn.bl_idname, icon='MOD_ARMATURE')

def register():
    bpy.utils.register_class(CXMap_SetAsphalt)
    bpy.utils.register_class(CXMap_SetGrass)
    bpy.utils.register_class(CXMap_SetCurb)
    bpy.utils.register_class(CXMap_SetSand)
    bpy.utils.register_class(CXMap_SetSnow)
    bpy.utils.register_class(CXMap_SetGravel)
    bpy.utils.register_class(CXMap_SetDirt)
    bpy.utils.register_class(CXMap_SetIcyRoad)
    bpy.utils.register_class(CXMap_SetAlpha)
    bpy.utils.register_class(CXMap_SetNoCol)
    bpy.utils.register_class(CXMap_SetRigidbody)
    bpy.utils.register_class(CXMap_SetAlphaNoCol)
    bpy.utils.register_class(CXMap_SetAlphaRigidbody)
    bpy.utils.register_class(CXMap_SetNoColRigidbody)
    bpy.utils.register_class(CXMap_SetAlphaNoColRigidbody)
    # bpy.utils.register_class(CXMap_CreateSpawn)
    bpy.utils.register_class(CXMap_Panel)


def unregister():
    bpy.utils.unregister_class(CXMap_SetAsphalt)
    bpy.utils.unregister_class(CXMap_SetGrass)
    bpy.utils.unregister_class(CXMap_SetCurb)
    bpy.utils.unregister_class(CXMap_SetSand)
    bpy.utils.unregister_class(CXMap_SetSnow)
    bpy.utils.unregister_class(CXMap_SetGravel)
    bpy.utils.unregister_class(CXMap_SetDirt)
    bpy.utils.unregister_class(CXMap_SetIcyRoad)
    bpy.utils.unregister_class(CXMap_SetAlpha)
    bpy.utils.unregister_class(CXMap_SetNoCol)
    bpy.utils.unregister_class(CXMap_SetRigidbody)
    bpy.utils.unregister_class(CXMap_SetAlphaNoCol)
    bpy.utils.unregister_class(CXMap_SetAlphaRigidbody)
    bpy.utils.unregister_class(CXMap_SetNoColRigidbody)
    bpy.utils.unregister_class(CXMap_SetAlphaNoColRigidbody)
    # bpy.utils.unregister_class(CXMap_CreateSpawn)
    bpy.utils.unregister_class(CXMap_Panel)
