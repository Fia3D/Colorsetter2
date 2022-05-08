import bpy
from struct import unpack, pack
from os.path import isfile

class AddCSMaterial(bpy.types.Operator):
    """Adds a default colorset material to the current object"""
    bl_idname = "object.add_cs_material"
    bl_label = "Add Colorset Material"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        print("Ping: AddCSMaterial")

        context.blend_data.materials.remove(context.object.active_material)
        
        library_path = bpy.utils.script_path_user() + '\\addons\\Colorsetter\\material_library.blend'
        with bpy.data.libraries.load(library_path) as (data_from, data_to):
            data_to.materials = data_from.materials

        context.object.active_material = data_to.materials[0]

        context.object.active_material.is_colorset = True

        return {'FINISHED'}

class ImportDDS(bpy.types.Operator):
    """Load a colorset dds to the current material"""
    bl_idname = "import.colorsetdds"
    bl_label = "Import DDS"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default='*.dds',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def read_i(self, file, i):
        return [unpack('e', file.read(2))[0] for x in range(i)]

    def execute(self, context):
        colorsetdat = False
        if isfile(self.filepath[:-3]+'dat'):
            colorsetdat = open(self.filepath[:-3]+'dat', 'rb')
        with open(self.filepath, 'rb') as colorset:
            colorset.seek(128)
            for i in range(16):
                context.object.active_material.cs_rows[i].diff = self.read_i(colorset, 4)
                # these properties have to be 4 long to update properly, 4th is dummy,
                # won't append directly to the read_i call for some reason...
                spec = self.read_i(colorset, 3)
                spec.append(1.0)
                context.object.active_material.cs_rows[i].spec = spec
                context.object.active_material.cs_rows[i].gloss = self.read_i(colorset, 1)[0]
                glow = self.read_i(colorset, 3)
                glow.append(1.0)
                context.object.active_material.cs_rows[i].glow = glow
                context.object.active_material.cs_rows[i].tile_id = self.read_i(colorset, 1)[0] * 64
                context.object.active_material.cs_rows[i].tile_transform = [x for x in self.read_i(colorset, 4)]
                if colorsetdat:
                    context.object.active_material.cs_rows[i].dye = hex(unpack('>H', colorsetdat.read(2))[0])[2:]

            colorset.close()
        if colorsetdat:
            colorsetdat.close()
        return {'FINISHED'}

    def invoke(self, context, event):
        bpy.context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ExportDDS(bpy.types.Operator):
    """Export current material's colorset to a dds file"""
    bl_idname = "export.colorsetdds"
    bl_label = "Export DDS"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default='*.dds',
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def write_header(self, colorset):
        # Quick header for the DDS file, based on TexTools' DDS.CreateColorDDSHeader() function
        # for details: https://msdn.microsoft.com/en-us/library/windows/desktop/bb943982(v=vs.85).aspx
        
        header = bytes()

        # DDS header magic number
        dwMagic = b'DDS '
        header += dwMagic

        # Size of structure, must be set to 124
        dwSize = pack('I', 124)
        header += dwSize

        # Flags to indicate which members contain valid data
        dwFlags = pack('I', 528399)
        header += dwFlags

        # Surface height (in pixels)
        dwHeight = pack('I', 16)
        header += dwHeight

        # Surface width (in pixels)
        dwWidth = pack('I', 4)
        header += dwWidth

        # The pitch or number of bytes per scan line in an uncompressed texture; the total number of bytes in the top level texture for a compressed texture.
        dwPitchOrLinearSize = pack('I', 512)
        header += dwPitchOrLinearSize

        # Depth of a colume texture (in pixels), otherwise unused
        dwDepth = pack('I', 0)
        header += dwDepth

        # Number of mipmap levels, othwerwise unused
        dwMipMapCount = pack('I', 0)
        header += dwMipMapCount

        # Unused
        dwReserved1 = bytes(44)
        header += dwReserved1

        # DDS_PIXELFORMAT start

        # Structure size; set to 32 (bytes)
        pfSize = pack('I', 32)
        header += pfSize

        # Values which indicate what type of data is in the surface
        pfFlags = pack('I', 4)
        header += pfFlags

        # Four-character codes for specifying compressed or custom formats.
        dwFourCC = b'\x71'
        header += dwFourCC

        # dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask, dwCaps, dwCaps2, dwCaps3, dwCaps4, dwReserved2
        # Unused
        blank1 = bytes(43)
        header += blank1

        return header

    def execute(self, context):
        colorsetdat = False
        for row in context.object.active_material.cs_rows:
            if row.dye is not '0':
                colorsetdat = open(self.filepath[:-3]+'dat', 'wb')
                dat_bytes = bytes()
                break
        with open(self.filepath, 'wb') as colorset:
            cs_bytes = self.write_header(colorset)

            for i in range(16):
                diff = bytes().join([pack('e', x) for x in context.object.active_material.cs_rows[i].diff])
                cs_bytes += diff

                spec = bytes().join([pack('e', x) for x in context.object.active_material.cs_rows[i].spec[0:3]])
                cs_bytes += spec

                gloss = pack('e', context.object.active_material.cs_rows[i].gloss/255)
                cs_bytes += gloss

                glow = bytes().join([pack('e', x) for x in context.object.active_material.cs_rows[i].glow[0:3]])
                cs_bytes += glow

                tile_id = pack('e', context.object.active_material.cs_rows[i].tile_id/255)
                cs_bytes += tile_id

                tile_transform = bytes().join([pack('e', x/255) for x in context.object.active_material.cs_rows[i].tile_transform])
                cs_bytes += tile_transform

                if colorsetdat:
                    dye_mod = pack('>H', int(context.object.active_material.cs_rows[i].dye, 16))
                    dat_bytes += dye_mod

            colorset.write(cs_bytes)
            colorset.close()
        if colorsetdat:
            colorsetdat.write(dat_bytes)
            colorsetdat.close()
        return {'FINISHED'}

    def invoke(self, context, event):
        bpy.context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

classes = [
    AddCSMaterial,
    ImportDDS,
    ExportDDS,
]

def register():
    # print("Register materialOperators.py")
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # print("Unregister materialOperators.py")
    for cls in classes:
        bpy.utils.unregister_class(cls)
