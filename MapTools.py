from math import degrees, radians
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
    """Set the type of objects"""
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
    """Set alpha for object materials"""
    bl_idname = 'object.cxmap_alpha'
    bl_label = 'Set Alpha'
    alpha: bpy.props.BoolProperty()

    def execute(self, context):
        for obj in context.selected_objects:
            for mslot in obj.material_slots:
                if self.alpha:
                    if not mslot.material.name.startswith('alpha_'):
                        mslot.material.name = 'alpha_' + mslot.material.name
                        mslot.material.blend_method = 'BLEND'
                        ndt = mslot.material.node_tree
                        if ('Image Texture' in ndt.nodes and
                                'Principled BSDF' in ndt.nodes):
                            tex = ndt.nodes['Image Texture']
                            bsdf = ndt.nodes['Principled BSDF']
                            ndt.links.new(tex.outputs['Alpha'],
                                          bsdf.inputs['Alpha'])
                else:
                    if mslot.material.name.startswith('alpha_'):
                        mslot.material.name = mslot.material.name.replace('alpha_', '', 1)
                        mslot.material.blend_method = 'OPAQUE'
                        ndt = mslot.material.node_tree
                        if ('Image Texture' in ndt.nodes and
                                'Principled BSDF' in ndt.nodes):
                            tex = ndt.nodes['Image Texture']
                            bsdf = ndt.nodes['Principled BSDF']
                            for lnk in ndt.links:
                                if (lnk.from_socket == tex.outputs['Alpha'] and
                                        lnk.to_socket == bsdf.inputs['Alpha']):
                                    ndt.links.remove(lnk)
                                    break
        return {'FINISHED'}


class CXMap_CreatePlaceholder(bpy.types.Operator):
    """Creates a placeholder that will be replaced on loading the map ingame"""
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


class CXMap_ImportData(bpy.types.Operator):
    """Import objdata file"""
    bl_idname = 'object.cxmap_importdata'
    bl_label = 'Import objdata'
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        file = open(self.filepath, 'r')
        for line in file.readlines():
            otype, obd = line.split(':')
            obd = obd.split(' ')
            if otype == 'Spawn':
                bpy.ops.object.empty_add(type='ARROWS')
                context.active_object.name = 'Spawnpoint'
                context.active_object.location.x = float(obd[0])
                context.active_object.location.y = float(obd[1])
                context.active_object.location.z = float(obd[2])
                context.active_object.rotation_euler.x = radians(float(obd[3]))
                context.active_object.rotation_euler.y = radians(float(obd[4]))
                context.active_object.rotation_euler.z = radians(float(obd[5]))
            elif otype == 'Camera':
                bpy.ops.object.empty_add(type='PLAIN_AXES')
                context.active_object.name = 'CameraPoint'
                context.active_object.location.x = float(obd[0])
                context.active_object.location.y = float(obd[1])
                context.active_object.location.z = float(obd[2])
            elif otype == 'SpotLight':
                bpy.ops.object.light_add(type='SPOT')
                context.active_object.location.x = float(obd[0])
                context.active_object.location.y = float(obd[1])
                context.active_object.location.z = float(obd[2])
                context.active_object.rotation_euler.x = radians(float(obd[3]))
                context.active_object.rotation_euler.y = radians(float(obd[4]))
                context.active_object.rotation_euler.z = radians(float(obd[5]))
                context.active_object.data.energy = float(obd[6])
                context.active_object.data.color.r = float(obd[7])
                context.active_object.data.color.g = float(obd[8])
                context.active_object.data.color.b = float(obd[9])
            elif otype == 'PointLight':
                bpy.ops.object.light_add(type='POINT')
                context.active_object.location.x = float(obd[0])
                context.active_object.location.y = float(obd[1])
                context.active_object.location.z = float(obd[2])
                context.active_object.data.energy = float(obd[3])
                context.active_object.data.color.r = float(obd[4])
                context.active_object.data.color.g = float(obd[5])
                context.active_object.data.color.b = float(obd[6])
            elif otype == 'SunLight':
                bpy.ops.object.light_add(type='SUN')
                context.active_object.location.x = float(obd[0])
                context.active_object.location.y = float(obd[1])
                context.active_object.location.z = float(obd[2])
                context.active_object.rotation_euler.x = radians(float(obd[3]))
                context.active_object.rotation_euler.y = radians(float(obd[4]))
                context.active_object.rotation_euler.z = radians(float(obd[5]))
                context.active_object.data.energy = float(obd[6])
                context.active_object.data.color.r = float(obd[7])
                context.active_object.data.color.g = float(obd[8])
                context.active_object.data.color.b = float(obd[9])
        file.close()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class CXMap_ExportProps(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(default='NewMap',
                                   name='Name',
                                   description='Set the name of the map')
    path: bpy.props.StringProperty(name='Path',
                                   description='Path where to save the map')
    texexp: bpy.props.EnumProperty(
        items=[('AUTO', 'Auto',
                'Use Relative paths with subdirectories only', 0),
               ('ABSOLUTE', 'Absolute',
                'Always write absolute paths', 1),
               ('RELATIVE', 'Relative',
                'Always write relative paths (where possible)', 2),
               ('MATCH', 'Match',
                'Match Absolute/Relative setting with input path', 3),
               ('STRIP', 'Strip',
                'Filename only', 4),
               ('COPY', 'Copy',
                'Copy the file to the destination path (or subdirectory)', 5)],
        name='Texture mode',
        description='Set the texture output mode for OBJ exporter')


class CXMap_Export(bpy.types.Operator):
    """Export the map"""
    bl_idname = 'object.cxmap_exportmap'
    bl_label = 'Export'
    export_type: bpy.props.StringProperty()

    def execute(self, context):
        filepath = context.scene.CX_ExpP.path + context.scene.CX_ExpP.name
        if self.export_type == 'obj':
            bpy.ops.export_scene.obj(filepath=filepath+'.obj',
                                     use_selection=False,
                                     path_mode=context.scene.CX_ExpP.texexp)
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
            fle = open(filepath + '.objdata', 'w')
            for spwn in spawns:
                fle.write('Spawn:{0} {1} {2} {3} {4} {5}\n'
                          .format(round(spwn.location.x, 6),
                                  round(spwn.location.y, 6),
                                  round(spwn.location.z, 6),
                                  round(degrees(spwn.rotation_euler.x), 6),
                                  round(degrees(spwn.rotation_euler.y), 6),
                                  round(degrees(spwn.rotation_euler.z), 6)))
            for cam in cameras:
                fle.write('Camera:{0} {1} {2}\n'
                          .format(round(cam.location.x, 6),
                                  round(cam.location.y, 6),
                                  round(cam.location.z, 6)))
            for spt in spots:
                fle.write('SpotLight:{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'
                          .format(round(spt.location.x, 6),
                                  round(spt.location.y, 6),
                                  round(spt.location.z, 6),
                                  round(degrees(spt.rotation_euler.x), 6),
                                  round(degrees(spt.rotation_euler.y), 6),
                                  round(degrees(spt.rotation_euler.z), 6),
                                  round(spt.data.energy, 6),
                                  round(spt.data.color.r, 6),
                                  round(spt.data.color.g, 6),
                                  round(spt.data.color.b, 6)))
            for pnt in points:
                fle.write('PointLight:{0} {1} {2} {3} {4} {5} {6}\n'
                          .format(round(pnt.location.x, 6),
                                  round(pnt.location.y, 6),
                                  round(pnt.location.z, 6),
                                  round(pnt.data.energy, 6),
                                  round(pnt.data.color.r, 6),
                                  round(pnt.data.color.g, 6),
                                  round(pnt.data.color.b, 6)))
            for sun in suns:
                fle.write('SunLight:{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n'
                          .format(round(sun.location.x, 6),
                                  round(sun.location.y, 6),
                                  round(sun.location.z, 6),
                                  round(degrees(sun.rotation_euler.x), 6),
                                  round(degrees(sun.rotation_euler.y), 6),
                                  round(degrees(sun.rotation_euler.z), 6),
                                  round(sun.data.energy, 6),
                                  round(sun.data.color.r, 6),
                                  round(sun.data.color.g, 6),
                                  round(sun.data.color.b, 6)))
            fle.close()
            self.report({'INFO'}, "Exported Extra Data")
        return {'FINISHED'}


class CXMap_SetExportLoc(bpy.types.Operator):
    """Set the export folder"""
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
        colflow = self.layout.column_flow(columns=2, align=True)
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Asphalt',
                         icon='AUTO').pfx = 'road'
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Grass',
                         icon='SEQ_HISTOGRAM').pfx = 'grass'
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Curb',
                         icon='PARTICLEMODE').pfx = 'kerb'
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Sand',
                         icon='FORCE_FORCE').pfx = 'sand'
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Snow',
                         icon='FREEZE').pfx = 'snow'
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Gravel',
                         icon='MOD_OCEAN').pfx = 'gravel'
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Dirt',
                         icon='MOD_SMOOTH').pfx = 'dirt'
        colflow.operator(CXMap_SetPrefix.bl_idname,
                         text='Icy Road',
                         icon='TRACKING').pfx = 'icyroad'

        self.layout.label(text='Set object type', icon='OUTLINER_OB_MESH')
        row = self.layout.row(align=True)
        row.operator(CXMap_SetPrefix.bl_idname,
                     text='No Collision',
                     icon='MOD_SOLIDIFY').pfx = 'nocol'
        row.operator(CXMap_SetPrefix.bl_idname,
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

        self.layout.label(text='Create placeholders', icon='EMPTY_AXIS')
        row = self.layout.row(align=True)
        row.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Spawn',
                             icon='MOD_ARMATURE').ptype = 'Spawn'
        row.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Camera',
                             icon='VIEW_CAMERA').ptype = 'CameraPoint'

        self.layout.label(text='Create lights', icon='OUTLINER_OB_LIGHT')
        row = self.layout.row(align=True)
        row.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Spot',
                             icon='LIGHT_SPOT').ptype = 'Spot'
        row.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Point',
                             icon='LIGHT_POINT').ptype = 'Point'
        row.operator(CXMap_CreatePlaceholder.bl_idname,
                             text='Sun',
                             icon='LIGHT_SUN').ptype = 'Sun'

        self.layout.label(text='Finalizing', icon='CHECKMARK')
        self.layout.prop(props, 'name')
        row = self.layout.row(align=True)
        row.prop(props, 'path')
        row.operator(CXMap_SetExportLoc.bl_idname,
                     text='', icon='FILE_FOLDER')
        row = self.layout.row(align=True)
        row.label(text='Texture mode:')
        row.prop(props, 'texexp', text='')
        self.layout.operator(CXMap_Export.bl_idname,
                             text='Export Map',
                             icon='EXPORT').export_type = 'obj'
        self.layout.operator(CXMap_Export.bl_idname,
                             text='Export Extra Data',
                             icon='SHADERFX').export_type = 'data'

        self.layout.label(text='Importing', icon='IMPORT')
        self.layout.operator(CXMap_ImportData.bl_idname,
                             text='Import Extra Data',
                             icon='IMPORT')


classes = (CXMap_SetPrefix,
           CXMap_SetAlpha,
           CXMap_CreatePlaceholder,
           CXMap_ImportData,
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
