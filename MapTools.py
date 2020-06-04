import bpy
import bmesh

objtypes = ['road',
            'grass',
            'kerb',
            'sand',
            'snow',
            'gravel',
            'icyroad',
            'dirt',
            'nocol',
            'rb']

class CXMap_SetPrefix(bpy.types.Operator):
    bl_idname = 'object.cxmap_setpfx'
    bl_label = 'Set Prefix'
    pfx: bpy.props.StringProperty()
    def execute(self, context):
        for i in context.selected_objects:
            if i.name.split('_')[0] in objtypes:
                i.name = i.name.replace(i.name.split('_')[0], self.pfx, 1)
            else:
                i.name = self.pfx + '_' + i.name
        return {'FINISHED'}


class CXMap_SetAlpha(bpy.types.Operator):
    bl_idname = 'object.cxmap_alpha'
    bl_label = 'Set Alpha'
    alpha: bpy.props.BoolProperty()
    def execute(self, context):
        for o in context.selected_objects:
            for mslot in o.material_slots:
                if self.alpha:
                    if not mslot.material.name.startswith('alpha_'):
                        mslot.material.name = 'alpha_' + mslot.material.name
                else:
                    if mslot.material.name.startswith('alpha_'):
                        mslot.material.name = mslot.material.name.replace('alpha_', '', 1)
        return {'FINISHED'}

class CXMap_CreatePlaceholder(bpy.types.Operator):
    bl_idname = 'object.cxmap_placeholder'
    bl_label = 'Create Placeholder'
    ptype: bpy.props.StringProperty()

    def execute(self, context):
        if self.ptype == 'Spawn':
            bpy.ops.object.empty_add(type='ARROWS')
            context.active_object.name = 'Spawnpoint'
        elif self.ptype == 'CameraPoint':
            bpy.ops.object.empty_add(type='PLAIN_AXES')
            context.active_object.name = 'CameraPoint'
        elif self.ptype == 'Light':
            bpy.ops.object.empty_add(type='SINGLE_ARROW')
            context.active_object.name = 'Light'
        return {'FINISHED'}

class CXMap_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_CXMaps'
    bl_label = 'CarX Map Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CarX Mod Tools'
    bl_context = 'objectmode'

    def draw(self, context):
        self.layout.label(text='Set physics material', icon='HAND')
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Asphalt',
                             icon='AUTO').pfx = 'road'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Grass',
                             icon='SEQ_HISTOGRAM').pfx = 'grass'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Curb',
                             icon='PARTICLEMODE').pfx = 'kerb'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Sand',
                             icon='FORCE_FORCE').pfx = 'sand'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Snow',
                             icon='FREEZE').pfx = 'snow'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Gravel',
                             icon='MOD_OCEAN').pfx = 'gravel'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Dirt',
                             icon='MOD_SMOOTH').pfx = 'dirt'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Icy Road',
                             icon='TRACKING').pfx = 'icyroad'

        self.layout.label(text='Set object type', icon='OUTLINER_OB_MESH')
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='No Collision',
                             icon='MOD_SOLIDIFY').pfx = 'nocol'
        self.layout.operator(CXMap_SetPrefix.bl_idname,
                             text='Rigidbody',
                             icon='RIGID_BODY').pfx = 'rb'

        self.layout.label(text='Set alpha mode', icon='IMAGE_ALPHA')
        row = self.layout.row(align=True)
        row.operator(CXMap_SetAlpha.bl_idname,
                     text='Enable',
                     icon='DECORATE_ANIMATE').alpha = True
        row.operator(CXMap_SetAlpha.bl_idname,
                     text='Disable',
                     icon='DECORATE_KEYFRAME').alpha = False
        self.layout.label(text='Map placeholders', icon='EMPTY_AXIS')
        self.layout.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Create Spawnpoint',
                             icon='MOD_ARMATURE').ptype = 'Spawn'
        self.layout.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Create Camera Point',
                             icon='VIEW_CAMERA').ptype = 'CameraPoint'
        self.layout.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Create Light',
                             icon='OUTLINER_OB_LIGHT').ptype = 'Light'

def register():
    bpy.utils.register_class(CXMap_SetPrefix)
    bpy.utils.register_class(CXMap_SetAlpha)
    bpy.utils.register_class(CXMap_CreatePlaceholder)
    bpy.utils.register_class(CXMap_Panel)


def unregister():
    bpy.utils.unregister_class(CXMap_SetPrefix)
    bpy.utils.unregister_class(CXMap_SetAlpha)
    bpy.utils.unregister_class(CXMap_CreatePlaceholder)
    bpy.utils.unregister_class(CXMap_Panel)
