from math import degrees
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
        elif self.ptype == 'Spot':
            bpy.ops.object.light_add(type='SPOT')
        elif self.ptype == 'Point':
            bpy.ops.object.light_add(type='POINT')
        elif self.ptype == 'Sun':
            bpy.ops.object.light_add(type='SUN')
        return {'FINISHED'}


class CXMap_ExportProps(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(default='NewMap',
                                   name='Name',
                                   description='Set the name of the map')
    path: bpy.props.StringProperty(name='Path',
                                   description='Path where to save the map')


class CXMap_Export(bpy.types.Operator):
    bl_idname = 'object.cxmap_exportmap'
    bl_label = 'Export'
    export_type: bpy.props.StringProperty()

    def execute(self, context):
        filepath = context.scene.CX_ExpP.path + context.scene.CX_ExpP.name
        if self.export_type == 'obj':
            bpy.ops.export_scene.obj(filepath=filepath+'.obj',
                                     use_selection=False,
                                     path_mode='STRIP')
            self.report({'INFO'}, "Exported Map")
        else:
            spawns = []
            cameras = []
            spots = []
            points = []
            suns = []
            for obj in bpy.data.objects:
                if obj.name.startswith('Spawnpoint'):
                    spawns.append(obj)
                elif obj.name.startswith('CameraPoint'):
                    cameras.append(obj)
                elif obj.name.startswith('Spot'):
                    spots.append(obj)
                elif obj.name.startswith('Point'):
                    points.append(obj)
                elif obj.name.startswith('Sun'):
                    suns.append(obj)
            file = open(filepath + '.objdata', 'w')
            for spwn in spawns:
                file.write('Spawn:{0} {1} {2} {3} {4} {5}\n'
                           .format(round(spwn.location.x, 6),
                                   round(spwn.location.y, 6),
                                   round(spwn.location.z, 6),
                                   round(degrees(spwn.rotation_euler.x), 6),
                                   round(degrees(spwn.rotation_euler.y), 6),
                                   round(degrees(spwn.rotation_euler.z), 6)))
            for cam in cameras:
                file.write('Camera:{0} {1} {2}\n'
                           .format(round(cam.location.x, 6),
                                   round(cam.location.y, 6),
                                   round(cam.location.z, 6)))
            for spt in spots:
                file.write('SpotLight:{0} {1} {2} {3} {4} {5} {6}\n'
                           .format(round(spt.location.x, 6),
                                   round(spt.location.y, 6),
                                   round(spt.location.z, 6),
                                   round(degrees(spt.rotation_euler.x), 6),
                                   round(degrees(spt.rotation_euler.y), 6),
                                   round(degrees(spt.rotation_euler.z), 6),
                                   round(spt.data.energy, 6)))
            for pnt in points:
                file.write('PointLight:{0} {1} {2} {3}\n'
                           .format(round(pnt.location.x, 6),
                                   round(pnt.location.y, 6),
                                   round(pnt.location.z, 6),
                                   round(pnt.data.energy, 6)))
            for sun in suns:
                file.write('SunLight:{0} {1} {2} {3} {4} {5} {6}\n'
                           .format(round(sun.location.x, 6),
                                   round(sun.location.y, 6),
                                   round(sun.location.z, 6),
                                   round(degrees(sun.rotation_euler.x), 6),
                                   round(degrees(sun.rotation_euler.y), 6),
                                   round(degrees(sun.rotation_euler.z), 6),
                                   round(sun.data.energy, 6)))
            file.close()
            self.report({'INFO'}, "Exported Extra Data")
        return {'FINISHED'}


class CXMap_SetExportLoc(bpy.types.Operator):
    bl_idname = 'object.cxmap_exportloc'
    bl_label = 'Select Export Folder'
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        context.scene.CX_ExpP.path = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class CXMap_Panel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_CXMaps'
    bl_label = 'CarX Map Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CarX Mod Tools'
    bl_context = 'objectmode'

    def draw(self, context):
        props = bpy.context.scene.CX_ExpP
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
                             text='Create Spotlight',
                             icon='LIGHT_SPOT').ptype = 'Spot'
        self.layout.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Create Pointlight',
                             icon='LIGHT_POINT').ptype = 'Point'
        self.layout.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Create Sunlight',
                             icon='LIGHT_SUN').ptype = 'Sun'
        self.layout.label(text='Finalizing', icon='CHECKMARK')
        self.layout.prop(props, 'name')
        row = self.layout.row(align=True)
        row.prop(props, 'path')
        row.operator(CXMap_SetExportLoc.bl_idname,
                     text='', icon='FILE_FOLDER')
        self.layout.operator(CXMap_Export.bl_idname,
                             text='Export Map',
                             icon='EXPORT').export_type = 'obj'
        self.layout.operator(CXMap_Export.bl_idname,
                             text='Export Extra Data',
                             icon='SHADERFX').export_type = 'data'


classes = (CXMap_SetPrefix,
           CXMap_SetAlpha,
           CXMap_CreatePlaceholder,
           CXMap_Export,
           CXMap_ExportProps,
           CXMap_SetExportLoc,
           CXMap_Panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.CX_ExpP = bpy.props.PointerProperty(type=CXMap_ExportProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del(bpy.types.Scene.CX_ExpP)
