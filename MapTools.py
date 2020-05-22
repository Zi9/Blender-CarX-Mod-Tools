from struct import pack
from math import degrees
import time
import bpy
import bmesh

EXPORTER_VERSION = 1

TEXTYPES = {'dds': 0,
            'png': 1,
            'jpg': 2,
            'jpeg': 2,
            'tga': 3}

def set_mat(ctx, phymat):
    for i in ctx.selected_objects:
        i['phys_material'] = phymat


class CXMap_SetAsphalt(bpy.types.Operator):
    bl_idname = 'object.cxmap_road'
    bl_label = 'Asphalt'
    def execute(self, context):
        set_mat(context, 0)
        return {'FINISHED'}


class CXMap_SetGrass(bpy.types.Operator):
    bl_idname = 'object.cxmap_grass'
    bl_label = 'Grass'
    def execute(self, context):
        set_mat(context, 1)
        return {'FINISHED'}


class CXMap_SetCurb(bpy.types.Operator):
    bl_idname = 'object.cxmap_curb'
    bl_label = 'Curb'
    def execute(self, context):
        set_mat(context, 2)
        return {'FINISHED'}


class CXMap_SetSand(bpy.types.Operator):
    bl_idname = 'object.cxmap_sand'
    bl_label = 'Sand'
    def execute(self, context):
        set_mat(context, 3)
        return {'FINISHED'}


class CXMap_SetSnow(bpy.types.Operator):
    bl_idname = 'object.cxmap_snow'
    bl_label = 'Snow'
    def execute(self, context):
        set_mat(context, 4)
        return {'FINISHED'}


class CXMap_SetGravel(bpy.types.Operator):
    bl_idname = 'object.cxmap_gravel'
    bl_label = 'Gravel'
    def execute(self, context):
        set_mat(context, 5)
        return {'FINISHED'}


class CXMap_SetDirt(bpy.types.Operator):
    bl_idname = 'object.cxmap_dirt'
    bl_label = 'Dirt'
    def execute(self, context):
        set_mat(context, 6)
        return {'FINISHED'}


class CXMap_SetIcyRoad(bpy.types.Operator):
    bl_idname = 'object.cxmap_icyroad'
    bl_label = 'Icy Road'
    def execute(self, context):
        set_mat(context, 7)
        return {'FINISHED'}


class CXMap_CreateSpawn(bpy.types.Operator):
    bl_idname = 'object.cxmap_spawnpoint'
    bl_label = 'Create Spawn Point'

    @classmethod
    def poll(cls, context):
        if 'MapModData' not in bpy.data.collections:
            return False
        return 'Spawnpoint' not in bpy.data.collections['MapModData'].objects

    def execute(self, context):
        coll = bpy.data.collections['MapModData']
        bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
        context.active_object.name = 'Spawnpoint'
        coll.objects.link(context.active_object)
        for c in bpy.data.collections:
            if c.name != 'MapModData':
                for o in c.objects:
                    if o.name == 'Spawnpoint':
                        c.objects.unlink(o)
        return {'FINISHED'}


class CXMap_Setup(bpy.types.Operator):
    bl_idname = 'object.cxmap_setup'
    bl_label = 'Setup'

    @classmethod
    def poll(cls, context):
        return 'MapMod' not in bpy.data.collections

    def execute(self, context):
        bpy.data.collections[0].name = 'MapMod'
        coll = bpy.data.collections.new('MapModData')
        context.scene.collection.children.link(coll)
        return {'FINISHED'}


class CXMap_Export(bpy.types.Operator):
    bl_idname = 'object.cxmap_export'
    bl_label = 'Export'

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        mm = 'MapMod' in bpy.data.collections
        mmd = 'MapModData' in bpy.data.collections
        return mm and mmd

    def execute(self, context):
        if not self.filepath.endswith('.cxmap'):
            self.filepath = self.filepath + '.cxmap'
        starttime = time.time()
        file = open(self.filepath, 'wb')
        fw = file.write
        fw(pack('7sB36x', b'CXMAPzi', EXPORTER_VERSION))
        if 'Spawnpoint' in bpy.data.collections['MapModData'].objects:
            spawn = bpy.data.collections['MapModData'].objects['Spawnpoint']
            fw(pack('ffffff',
                    spawn.location[0],
                    spawn.location[1],
                    spawn.location[2],
                    degrees(spawn.rotation_euler[0]),
                    degrees(spawn.rotation_euler[1]),
                    degrees(spawn.rotation_euler[2])))
        else:
            fw(pack('24x'))
        fw(pack('60x'))  # pad

        # TEXTURES
        texstart = file.tell()
        texcount = 0
        texcache = []
        for mat in bpy.data.materials:
            img = mat.node_tree.nodes['Image Texture'].image
            if img not in texcache:
                texcache.append(img)
        print(f'Texcache has {len(texcache)} items')
        for texture in texcache:
            fw(pack('3s', b'TEX'))
            print(f'{texcount}: Writing texture {texture.name}')
            fw(pack('B', len(texture.name)))
            fw(pack(str(len(texture.name))+'s', texture.name.encode('UTF-8')))
            fw(pack('B', TEXTYPES[texture.name.split('.')[-1]]))
            texpath = bpy.path.abspath(texture.filepath)
            with open(texpath, 'rb') as texf:
                texf.seek(0, 2)
                fw(pack('I', texf.tell()))
                texf.seek(0)
                fw(texf.read())
            texcount = texcount + 1
        texsz = file.tell() - texstart

        # MATERIALS
        matstart = file.tell()
        matcount = 0
        for mat in bpy.data.materials:
            print(f'{matcount}: Writing material {mat.name}')
            fw(pack('3s', b'MAT'))
            fw(pack('B', len(mat.name)))
            fw(pack(str(len(mat.name))+'s', mat.name.encode('UTF-8')))
            if 'alphaflag' in mat:
                fw(pack('B', mat['alphaflag']))
            else:
                fw(pack('B', 0))
            fw(pack('I', texcache.index(img)))

            matcount = matcount + 1
        matsz = file.tell() - matstart

        # OBJECTS
        objstart = file.tell()
        objcount = 0
        for o in bpy.data.collections['MapMod'].objects:
            print(f'{objcount}: Writing object {o.name}')
            fw(pack('3s', b'OBJ'))
            fw(pack('B', len(o.name)))
            fw(pack(str(len(o.name))+'s', o.name.encode('UTF-8')))
            fw(pack('9f',
                    o.location[0],
                    o.location[1],
                    o.location[2],
                    degrees(o.rotation_euler[0]),
                    degrees(o.rotation_euler[1]),
                    degrees(o.rotation_euler[2]),
                    o.scale[0],
                    o.scale[1],
                    o.scale[2]))
            if len(o.material_slots) > 1:
                print('WARNING: Object ' + o.name +
                      ' contains more than 1 material, this is not supported')
            fw(pack('B', len(o.material_slots[0].name)))
            fw(pack(str(len(o.material_slots[0].name))+'s',
                    o.material_slots[0].name.encode('UTF-8')))
            if 'phys_material' in o:
                fw(pack('B', o['phys_material']))
            else:
                fw(pack('B', 0))
            mesh = bmesh.new()
            mesh.from_mesh(o.data)
            bmesh.ops.triangulate(mesh, faces=mesh.faces[:])
            mesh.to_mesh(o.data)
            mesh.free()
            fw(pack('I', len(o.data.vertices)))
            for vert in o.data.vertices:
                fw(pack('3f', vert.co[0], vert.co[1], vert.co[2]))
            # for vert in o.data.vertices:
                # fw(pack('3f', vert.normal[0], vert.normal[1], vert.normal[2]))
            fw(pack('I', len(o.data.uv_layers.active.data)))
            for uvd in o.data.uv_layers.active.data:
                fw(pack('2f', uvd.uv[0], uvd.uv[1]))
            fw(pack('I', len(o.data.polygons)*3))
            for poly in o.data.polygons:
                fw(pack('3I',
                        poly.vertices[0],
                        poly.vertices[1],
                        poly.vertices[2]))
            objcount = objcount + 1
        objsz = file.tell() - objstart

        # FINALIZING
        file.seek(8)
        fw(pack('9I',
                texstart, texsz, texcount,
                matstart, matsz, matcount,
                objstart, objsz, objcount))
        file.close()
        print('Exported version ' +
              str(EXPORTER_VERSION) +
              ' CarX Mod Map')
        endtime = time.time()
        print('Exporting took ' + str(endtime-starttime) + ' seconds')
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
        self.layout.label(text='Setup for map', icon='OUTLINER_DATA_MESH')
        self.layout.operator(CXMap_Setup.bl_idname, icon='PLUS')
        self.layout.label(text='Set physics material', icon='HAND')
        self.layout.operator(CXMap_SetAsphalt.bl_idname, icon='AUTO')
        self.layout.operator(CXMap_SetGrass.bl_idname, icon='SEQ_HISTOGRAM')
        self.layout.operator(CXMap_SetCurb.bl_idname, icon='PARTICLEMODE')
        self.layout.operator(CXMap_SetSand.bl_idname, icon='FORCE_FORCE')
        self.layout.operator(CXMap_SetSnow.bl_idname, icon='FREEZE')
        self.layout.operator(CXMap_SetGravel.bl_idname, icon='MOD_OCEAN')
        self.layout.operator(CXMap_SetDirt.bl_idname, icon='MOD_SMOOTH')
        self.layout.operator(CXMap_SetIcyRoad.bl_idname, icon='TRACKING')
        self.layout.label(text='Spawnpoint', icon='EMPTY_AXIS')
        self.layout.operator(CXMap_CreateSpawn.bl_idname, icon='MOD_ARMATURE')
        self.layout.label(text='Finalizing', icon='CHECKMARK')
        self.layout.operator(CXMap_Export.bl_idname, icon='EXPORT')

def register():
    bpy.utils.register_class(CXMap_SetAsphalt)
    bpy.utils.register_class(CXMap_SetGrass)
    bpy.utils.register_class(CXMap_SetCurb)
    bpy.utils.register_class(CXMap_SetSand)
    bpy.utils.register_class(CXMap_SetSnow)
    bpy.utils.register_class(CXMap_SetGravel)
    bpy.utils.register_class(CXMap_SetDirt)
    bpy.utils.register_class(CXMap_SetIcyRoad)
    bpy.utils.register_class(CXMap_CreateSpawn)
    bpy.utils.register_class(CXMap_Setup)
    bpy.utils.register_class(CXMap_Export)
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
    bpy.utils.unregister_class(CXMap_CreateSpawn)
    bpy.utils.unregister_class(CXMap_Setup)
    bpy.utils.unregister_class(CXMap_Export)
    bpy.utils.unregister_class(CXMap_Panel)
