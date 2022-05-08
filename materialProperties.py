import bpy
from . import materialProperties

dye_modifiers = [
    ("0", "Undyed", ""),

    ("b19", "0b19", "0"),
    ("4b1a", "4b1a", ""),
    ("b32", "0b32", ""),
    ("4b33", "4b33", ""),
    ("8b3e", "8b3e", ""),
    ("cb3f", "cb3f", ""),
    ("b41", "0b41", ""),
    ("b4b", "0b4b", ""),

    ("2b19", "2b19", ""),
    ("6b1a", "6b1a", ""),
    ("ab25", "ab25", ""),
    ("2b32", "2b32", ""),
    ("6b33", "6b33", ""),
    ("ab3e", "ab3e", ""),
    ("2b41", "2b41", ""),
    ("2b4b", "2b4b", ""),

    ("4b19", "4b19", ""),
    ("8b1a", "8b1a", ""),
    ("cb25", "cb25", ""),
    ("4b32", "4b32", ""),
    ("8b1b", "8b1b", ""),
    ("8b33", "8b33", ""),
    ("cb3e", "cb3e", ""),
    ("4b41", "4b41", ""),
    ("4b4b", "4b4b", ""),
    ("cb34", "cb34", ""),

    ("f40", "0f40", ""),
    ("f41", "0f41", ""),
    ("eb34", "eb34", ""),
    ("cf3f", "cf3f", ""),
    ("4f41", "4f41", ""),
    ("cb44", "cb44", ""),
    ("3b41", "3b41", ""),
    ("3b41", "3b41", ""),
    ("891a", "891a", ""),    
    ("8b43", "8b43", ""),
    ("141", "0141", ""),
    ("eb44", "eb44", "")
]

def diff_update(self, context):
    context.object.active_material.node_tree.nodes["DiffRamp"].color_ramp.elements[self.row].color = self.diff

def spec_update(self, context):
    context.object.active_material.node_tree.nodes["SpecRamp"].color_ramp.elements[self.row].color = self.spec

def glow_update(self, context):
    context.object.active_material.node_tree.nodes["GlowRamp"].color_ramp.elements[self.row].color = self.glow

def gloss_update(self, context):
    normalized = self.gloss / 65025
    context.object.active_material.node_tree.nodes["GlossRamp"].color_ramp.elements[self.row].color = (normalized, normalized, normalized, 1)

class ColorsetRow(bpy.types.PropertyGroup):
    # parentMat: bpy.props.StringProperty(name="Parent Material", default="Unknown")
    row: bpy.props.IntProperty(name='Row', min = 0, max = 15)
    diff: bpy.props.FloatVectorProperty(name="Diffuse", update=diff_update, subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
    spec: bpy.props.FloatVectorProperty(name="Specular", update=spec_update, subtype='COLOR', size=4, default=(1.0,1.0,1.0,1.0))
    glow: bpy.props.FloatVectorProperty(name="Glow", update=glow_update, subtype='COLOR', size=4, default=(0.0,0.0,0.0,1.0))
    gloss: bpy.props.FloatProperty(name="Gloss", update=gloss_update, default=5100)
    tile_id: bpy.props.IntProperty(name="Tile ID", max=63, min=0, default=2)
    tile_transform: bpy.props.FloatVectorProperty(name="Transform", size=4, default=[4080,0,0,4080])
    dye: bpy.props.EnumProperty(items=dye_modifiers, name="Dye Modifier")

def register():
    # print("Register materialProperties.py")
    bpy.utils.register_class(ColorsetRow)
    bpy.types.Material.is_colorset = bpy.props.BoolProperty(default=False)
    bpy.types.Material.cs_rows = bpy.props.CollectionProperty(type=materialProperties.ColorsetRow)

def unregister():
    # print("Unregister materialProperties.py")
    bpy.utils.unregister_class(ColorsetRow)
    del bpy.types.Material.is_colorset
    del bpy.types.Material.cs_rows
