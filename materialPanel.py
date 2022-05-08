import bpy

class ColorsetPanel(bpy.types.Panel):
    """Panel for material setup and colorset rows"""
    bl_label = "Colorset"
    bl_idname = "MATERIAL_PT_colorset"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        return context.object.active_material

    def draw(self, context):
        layout = self.layout

        if(context.object.active_material):
            if(context.object.active_material.is_colorset):
                normal = context.object.active_material.node_tree.nodes['Normal']
                multi = context.object.active_material.node_tree.nodes['Multi']
                
                row = layout.row()
                row.operator("import.colorsetdds")
                row.operator("export.colorsetdds")
                layout.label(text="Normal Map")
                row = layout.row()
                row.template_ID(normal, 'image', open="image.open")
                layout.label(text="Multi Map")
                row = layout.row()
                row.template_ID(multi, 'image', open="image.open")
            else:
                row = layout.row()
                row.operator("object.add_cs_material", text="Add")

class ColorsetRowPanel(bpy.types.Panel):
    """Panel for one colorset row"""
    bl_label = "Row #"
    bl_idname = "MATERIAL_PT_row"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_parent_id = "MATERIAL_PT_colorset"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return context.object.active_material and context.object.active_material.is_colorset

    def draw(self, context):
        layout = self.layout
        this_row = context.object.active_material.cs_rows[self.row]

        row = layout.row()
        row.prop(this_row, 'diff')
        row.prop(this_row, 'spec')

        row = layout.row()
        row.prop(this_row, 'glow')
        sub = row.row()
        sub.scale_x = 1.4
        sub.prop(this_row, 'gloss')

        row = layout.row()
        row.prop(this_row, 'tile_id')
        row = layout.row()
        row.prop(this_row, 'tile_transform')

        row = layout.row()
        row.prop(this_row, 'dye')

classes = [
    ColorsetPanel,
]

for i in range(16):
    new_label = f"Row {i+1}"
    new_id = f"MATERIAL_PT_row_{i+1}"
    new_child = type(new_id,
        (ColorsetRowPanel, bpy.types.Panel),
        {"bl_label" : new_label,
         "bl_idname" : new_id,
         "row" : i}
        )
    classes.append(new_child)

def register():
    # print("Register materialPanel.py")
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # print("Unregister materialPanel.py")
    for cls in classes:
        bpy.utils.unregister_class(cls)
