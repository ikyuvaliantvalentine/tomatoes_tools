bl_info = {
    "name": "Rig Toolset",
    "author": "NPC BV",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Tools > Rig Toolset",
    "description": "Reset All Strecth Constraint",
    "warning": "",
    "wiki_url": "",
    "category": "RIG",
    }

import bpy
from bpy.types import Operator, Panel

class OP_Reset_All_Stretch(Operator):
    """Resets all Stretch To constraints in the selected armature"""
    bl_idname = "rig.reset_all_strecth"
    bl_label = "Resets Stretch To Constraints"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        arm = obj.data

        for bone in arm.bones:
            pbone = obj.pose.bones[bone.name]
            for cons in pbone.constraints:
                if cons.type == 'STRETCH_TO':
                    # length of 0 makes it auto-reset when it next updates
                    cons.rest_length = 0
        return {'FINISHED'}

class RIG_PT_UI(Panel):
    bl_category = "Rig Toolset"
    bl_label = "Rig Toolset"
    bl_idname = "RIG_PT_UI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        layout.scale_x = 1.2
        layout.scale_y = 1.2
        layout.operator("rig.reset_all_strecth", icon="CONSTRAINT_BONE")
            
def register():
    bpy.utils.register_class(OP_Reset_All_Stretch)
    bpy.utils.register_class(RIG_PT_UI)
    
def unregister():
    bpy.utils.unregister_class(OP_Reset_All_Stretch)
    bpy.utils.unregister_class(RIG_PT_UI)

if __name__ == "__main__":
    register()  