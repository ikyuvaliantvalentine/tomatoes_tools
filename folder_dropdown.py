import bpy
import os

bl_info = {
    "name": "Folder Dropdown",
    "blender": (2, 80, 0),
    "category": "Object",
}

# Define the names of the image nodes
image_node_names = ["Env_Col", "MP", "Char_Col"]

class FOLDER_PT_dropdown(bpy.types.Panel):
    bl_label = "Folder Dropdown"
    bl_idname = "FOLDER_PT_dropdown"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        layout.operator("folder.list_exr_files")

        row = layout.row()
        row.label(text="Select a folder:")

        # Create a row with the folder dropdown and a refresh button
        row = layout.row()
        row.prop(context.scene, "selected_folder")
        row.operator("folder.refresh_folder_list", text="", icon="FILE_REFRESH")

        row = layout.row()
        row.operator("folder.update_image_path", text="Update Image Path")

class FOLDER_OT_update_image_path(bpy.types.Operator):
    bl_idname = "folder.update_image_path"
    bl_label = "Update Image Path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the active scene's compositor tree
        scene = bpy.context.scene
        compositor = scene.node_tree

        # Iterate through the lists using indices
        for i, image_node_name in enumerate(image_node_names):
            folder_name = context.scene.selected_folder

            # Find the compositor image node by name
            target_node = None
            for node in compositor.nodes:
                if node.name == image_node_name:
                    target_node = node
                    break

            if target_node is not None:
                folder_path = os.path.join("D:\\Source_Testing_EXR", folder_name, image_node_name)

                # Store the existing links connected to the Image Node
                existing_links = []
                for link in compositor.links:
                    if link.to_node == target_node:
                        existing_links.append(link)

                # Get a list of image files in the folder
                image_files = [f for f in os.listdir(folder_path) if f.endswith('.exr')]

                # Remove the old image datablock if it exists
                if target_node.image:
                    bpy.data.images.remove(target_node.image)

                # Check if there are image sequences in the folder
                if len(image_files) > 0:
                    # Sort the image files by name
                    image_files.sort()

                    # Set the image_path to the path of the first image in the folder
                    image_path = os.path.join(folder_path, image_files[0])

                    # Check if the image datablock already exists in bpy.data.images
                    existing_image = bpy.data.images.get(image_path)
                    if existing_image is not None:
                        # Use the existing image datablock instead of removing it
                        image = existing_image
                    else:
                        # Load the image from the specified path
                        try:
                            image = bpy.data.images.load(image_path)
                        except:
                            raise Exception("Image not found or cannot be loaded.")

                    # Set the new image data for the Image Node
                    target_node.image = image
                    target_node.image.source = 'SEQUENCE'
                    target_node.use_auto_refresh = True
                    target_node.image.filepath = image_path
                    target_node.image.file_format = 'OPEN_EXR'

                    # Set the frame duration based on the number of images in the folder
                    target_node.frame_duration = len(image_files)

                    # Reconnect the Image Node to its output nodes
                    for link in existing_links:
                        compositor.links.new(link.from_socket, target_node.inputs['Image'])

                    print(f"{image_node_name} node updated successfully.")
                else:
                    print(f"No image sequences found in the folder for {image_node_name}.")
            else:
                print(f"{image_node_name} node not found in the compositor.")

        return {'FINISHED'}

class FOLDER_OT_list_exr_files(bpy.types.Operator):
    bl_idname = "folder.list_exr_files"
    bl_label = "List EXR Files"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the selected folder from the scene
        selected_folder = context.scene.selected_folder

        # Find and use the existing "EXR_File_List" text datablock if it exists
        text_block_name = "EXR_File_List"
        text_block = bpy.data.texts.get(text_block_name)

        if text_block is None:
            # If the text datablock does not exist, create a new one
            text_block = bpy.data.texts.new(text_block_name)

        # Clear the existing content of the text datablock
        text_block.clear()

        # Iterate through the lists using indices
        for i in range(len(folder_paths)):
            folder_path = folder_paths[i]
            image_node_name = image_node_names[i]

            # Find the Compositor node tree
            compositor_tree = bpy.context.scene.node_tree

            # Find the Image Node in the Compositor by name
            image_node = compositor_tree.nodes.get(image_node_name)

            # Check if the Image Node was found
            if image_node is not None and image_node.type == 'IMAGE':
                # Get a list of image files in the folder
                image_files = [f for f in os.listdir(folder_path) if f.endswith('.exr')]

                # Append the image node name and count to the text datablock
                text_block.write(f"{image_node_name} node:\n")
                text_block.write(f"Total EXR files: {len(image_files)}\n")
                text_block.write("EXR files:\n")
                for image_file in image_files:
                    text_block.write(f"{image_file}\n")

                text_block.write("\n")  # Separate sections with a newline
            else:
                print(f"{image_node_name} node not found in the compositor.")

        # # Construct the full folder path based on the selected folder
        # folder_path = os.path.join("D:\\Source_Testing_EXR", selected_folder)

        # # Find the Compositor node tree
        # compositor_tree = bpy.context.scene.node_tree

        # # Iterate through all nodes in the compositor
        # for node in compositor_tree.nodes:
        #     # Check if the node is of type 'IMAGE'
        #     if node.type == 'IMAGE':
        #         # Get a list of image files in the folder
        #         image_files = [f for f in os.listdir(folder_path) if f.endswith('.exr')]

        #         # Append the image node name and count to the text datablock
        #         text_block.write(f"{node.name} node:\n")
        #         text_block.write(f"Total EXR files: {len(image_files)}\n")
        #         text_block.write("EXR files:\n")
        #         for image_file in image_files:
        #             text_block.write(f"{image_file}\n")

        #         text_block.write("\n")  # Separate sections with a newline

        self.report({'INFO'}, f"EXR file list stored in the text datablock: {text_block_name}")
        return {'FINISHED'}
    
#class FOLDER_OT_update_image_path(bpy.types.Operator):
#    bl_idname = "folder.update_image_path"
#    bl_label = "Update Image Path"
#    bl_options = {'REGISTER', 'UNDO'}

#    def execute(self, context):
#        selected_folder = context.scene.selected_folder

#        if selected_folder:
#            # Get the active scene's compositor tree
#            scene = bpy.context.scene
#            compositor = scene.node_tree

#            target_node_name = "Env_Col"

#            # Find the compositor image node by name
#            target_node = None
#            for node in compositor.nodes:
#                if node.name == target_node_name:
#                    target_node = node
#                    break

#            if target_node is not None:
#                # Construct the image path based on the selected folder
#                subfolder_path = f"{selected_folder}_Env_Col"
#                image_filename = f"{subfolder_path}.1001.exr"
#                image_path = os.path.join("D:\\Source_Testing_EXR", selected_folder, subfolder_path, image_filename)
#                print(f"Image path: {image_path}")  # Print the image path for debugging
#                target_node.image.filepath = image_path

#                # Reload the image data
#                target_node.image.reload()

#        return {'FINISHED'}

class FOLDER_OT_refresh_folder_list(bpy.types.Operator):
    bl_idname = "folder.refresh_folder_list"
    bl_label = "Refresh Folder List"
    bl_options = {'REGISTER'}

    def execute(self, context):
        # Update the folder list
        bpy.types.Scene.selected_folder_items = [(folder_name, folder_name, '') for folder_name in os.listdir("D:\\Source_Testing_EXR") if os.path.isdir(os.path.join("D:\\Source_Testing_EXR", folder_name))]
        bpy.types.Scene.selected_folder = bpy.props.EnumProperty(
            items=bpy.types.Scene.selected_folder_items,
            description="Select a folder"
        )
        return {'FINISHED'}

classes = (
    FOLDER_PT_dropdown,
    FOLDER_OT_update_image_path,
    FOLDER_OT_list_exr_files,
    FOLDER_OT_refresh_folder_list,
)

def register():
    bpy.types.Scene.selected_folder_items = [(folder_name, folder_name, '') for folder_name in os.listdir("D:\\Source_Testing_EXR") if os.path.isdir(os.path.join("D:\\Source_Testing_EXR", folder_name))]
    bpy.types.Scene.selected_folder = bpy.props.EnumProperty(
        items=bpy.types.Scene.selected_folder_items,
        description="Select a folder"
    )

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.selected_folder
    del bpy.types.Scene.selected_folder_items

if __name__ == "__main__":
    register()
