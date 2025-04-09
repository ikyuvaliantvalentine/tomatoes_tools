bl_info = {
    "name": "Material Transfer Tool",
    "author": "Valiant Valentine + ChatGPT",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Material Transfer",
    "description": "Transfer materials from master blend file using object-material mapping.",
    "category": "Object",
}

import bpy
import json
import os
import re

from bpy.props import PointerProperty, StringProperty
from bpy.types import Operator, Panel, PropertyGroup

# ---------- Operator: Export Object-Material Mapping ----------

class EXPORT_OT_material_mapping2(Operator):
    bl_idname = "export.material_mapping02"
    bl_label = "Export Material Mapping"
    bl_description = "Export object-material mapping to JSON"

    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        obj_mat_map = {}
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.data.materials:
                obj_mat_map[obj.name] = [mat.name for mat in obj.data.materials]

        try:
            with open(self.filepath, "w") as f:
                json.dump(obj_mat_map, f, indent=4)
            self.report({'INFO'}, f"Mapping exported to {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export: {e}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class EXPORT_OT_material_mapping(Operator):
    bl_idname = "export.material_mapping"
    bl_label = "Export Material Mapping"
    bl_description = "Export object-material mapping to JSON"

    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        obj_mat_map = {}
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.data.materials:
                mat_names = [mat.name for mat in obj.data.materials]
                face_indices = [poly.material_index for poly in obj.data.polygons]
                obj_mat_map[obj.name] = {
                    "materials": mat_names,
                    "face_material_indices": face_indices
                }

        # for obj in bpy.data.objects:
        #     if obj.type == 'MESH' and obj.data.materials:
        #         obj_mat_map[obj.name] = [mat.name for mat in obj.data.materials]

        try:
            with open(self.filepath, "w") as f:
                json.dump(obj_mat_map, f, indent=4)
            self.report({'INFO'}, f"Mapping exported to {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export: {e}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# ---------- Operator: Assign Materials ----------
class ASSIGN_OT_materials(Operator):
    bl_idname = "assign.materials_from_mapping"
    bl_label = "Assign Materials"
    bl_description = "Assign materials to objects from JSON mapping"

    def execute(self, context):
        props = context.scene.mat_transfer_prop
        filepath = bpy.path.abspath(props.importJson)

        if not os.path.exists(filepath):
            self.report({'ERROR'}, f"JSON file not found at {filepath}")
            return {'CANCELLED'}

        try:
            with open(filepath, "r") as f:
                obj_mat_map = json.load(f)

            assigned_count = 0
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    # --- Extract Core Name ---
                    name_parts = obj.name.split(":")  # Handle names like "RIG5:MSH_BodyRM.001"
                    core_with_suffix = name_parts[-1]  # Take the last part (e.g., MSH_BodyRM.001)

                    # Remove Blender's duplicate numbering (e.g., ".001", ".002")
                    core_without_number = re.sub(r"\.\d+$", "", core_with_suffix)

                    # Remove suffix (last 2 characters, e.g., RM) to get "MSH_Body"
                    if len(core_without_number) > 2:
                        core_name = core_without_number[:-2]  
                    else:
                        core_name = core_without_number  

                    # --- Look up material mapping ---
                    if core_name in obj_mat_map:
                        data = obj_mat_map[core_name]
                        mat_names = data["materials"]
                        face_indices = data["face_material_indices"]

                        # Assign materials to the original object
                        obj.data.materials.clear()
                        for mat_name in mat_names:
                            if mat_name in bpy.data.materials:
                                obj.data.materials.append(bpy.data.materials[mat_name])

                        for i, poly in enumerate(obj.data.polygons):
                            if i < len(face_indices):
                                poly.material_index = face_indices[i]

                        assigned_count += 1

            self.report({'INFO'}, f"Assigned materials to {assigned_count} objects.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to assign: {e}")
            return {'CANCELLED'}


class ASSIGN_OT_materials02(Operator):
    bl_idname = "assign.materials_from_mapping_02"
    bl_label = "Assign Materials 02"
    bl_description = "Assign materials to objects from JSON mapping"

    def execute(self, context):
        props = context.scene.mat_transfer_prop
        filepath = bpy.path.abspath(props.importJson)

        if not os.path.exists(filepath):
            self.report({'ERROR'}, f"JSON file not found at {filepath}")
            return {'CANCELLED'}

        try:
            with open(filepath, "r") as f:
                obj_mat_map = json.load(f)

            assigned_count = 0
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    # --- Extract Core Name ---
                    name_parts = obj.name.split(":")  # Handle names like "RIG5:MSH_BodyRM.001"
                    core_with_suffix = name_parts[-1]  # Get last part (e.g., MSH_BodyRM.001)

                    # Remove Blender's duplicate numbering (".001", ".002", etc.)
                    core_without_number = re.sub(r"\.\d+$", "", core_with_suffix)

                    # Remove suffix (last 2 characters, e.g., "RM") if needed
                    if len(core_without_number) > 2:
                        core_name = core_without_number[:-2]  
                    else:
                        core_name = core_without_number  

                    # --- Assign Materials ---
                    if core_name in obj_mat_map:
                        mat_names = obj_mat_map[core_name]
                        obj.data.materials.clear()
                        for mat_name in mat_names:
                            if mat_name in bpy.data.materials:
                                obj.data.materials.append(bpy.data.materials[mat_name])
                        assigned_count += 1

            self.report({'INFO'}, f"Assigned materials to {assigned_count} objects.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to assign: {e}")
            return {'CANCELLED'}

# ---------- Panel ----------

class MATERIALTRANSFER_PT_panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Material Transfer"

class Exporter_PT_MaterialTransfer(MATERIALTRANSFER_PT_panel):
    bl_label = "1. Material Export"
    bl_idname = "Exporter_PT_MaterialTransfer"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.scale_x = 1.5
        layout.scale_y = 1.5
        layout.operator("export.material_mapping", text="Export Material Mapping")
        layout.operator("export.material_mapping02", text="Export Material Mapping 02")

class Inporter_PT_MaterialTransfer(MATERIALTRANSFER_PT_panel):
    bl_label = "2. Material Import"
    bl_idname = "Inporter_PT_MaterialTransfer"
    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        mat_transfer_prop = context.scene.mat_transfer_prop
        layout = self.layout
        layout.scale_x = 1.5
        layout.scale_y = 1.5
        layout.operator("wm.append")
        layout.prop(mat_transfer_prop, "importJson")
        layout.separator()
        layout.operator("assign.materials_from_mapping", text="Assign Materials")
        layout.operator("assign.materials_from_mapping_02", text="Assign Material 02 ")


class MaterialTransfer_Properties(PropertyGroup):
    importJson: StringProperty(
        name="Json",
        description="camera.json path",
        default="",
        maxlen=1024,
        subtype="FILE_PATH"
        )



# ---------- Register ----------

classes = (
    EXPORT_OT_material_mapping,
    EXPORT_OT_material_mapping2,
    Exporter_PT_MaterialTransfer,
    Inporter_PT_MaterialTransfer,
    ASSIGN_OT_materials,
    ASSIGN_OT_materials02,
    MaterialTransfer_Properties
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mat_transfer_prop = PointerProperty(type=MaterialTransfer_Properties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mat_transfer_prop

if __name__ == "__main__":
    register()
