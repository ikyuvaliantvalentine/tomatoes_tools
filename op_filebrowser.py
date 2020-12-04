import bpy, os, sys
from bpy.types import Operator
from bpy.props import StringProperty
import platform
import subprocess

#km = wm.keyconfigs.addon.keymaps.new(name = 'File Browser', space_type = 'FILE_BROWSER')
#kmi = km.keymap_items.new('op.filebrowser_open', 'O', 'PRESS')
    
def abspath(path):
    return os.path.abspath(bpy.path.abspath(path))

def open_folder(path):

    if platform.system() == "Windows":
        os.startfile(path)

class Open(Operator):
    bl_idname = "op.filebrowser_open"
    bl_label = "MACHIN3: Open in System's filebrowser"
    bl_description = "Open the current location in the System's own filebrowser"

    path: StringProperty(name="Path")

    @classmethod
    def poll(cls, context):
        return context.area.type == 'FILE_BROWSER'

    def execute(self, context):
        params = context.space_data.params

        directory = abspath(params.directory.decode())

        open_folder(directory)

        return {'FINISHED'}
