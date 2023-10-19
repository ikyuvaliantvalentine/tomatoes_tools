bl_info = {
    "name": "123 Render Settings",
    "author": "ikyuvaliantvalentine",
    "version": (1, 0),
    "blender": (2, 80, 0), 
    "location": "Properties > Render > Render Settings Addon",
    "description": "Set custom render settings for 123 Projects.",
    "category": "Render",
}

import bpy
import os

def get_number_episodes(self, context):
    # Define the root folder path
    root_folder = r"P:\\NSS2\\03_Postproduction\\04_OUTPUT\\Renders\\02_COMP\\"

    # Get a list of subdirectories (episodes)
    episodes = [episode for episode in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, episode))]

    # Return a list of tuples for EnumProperty
    return [(episode, episode, f"{episode} Episode Description") for episode in episodes]

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
                
    episode_enum: bpy.props.EnumProperty(
        name="Select Episode",
        items=get_number_episodes, 
        description="Select the episode")
    
    def draw(self, context):
        layout = self.layout 
        layout.prop(self, "episode_enum")
        
class RenderSettingsAddonOperator(bpy.types.Operator):
    bl_idname = "render_settings.addon_operator"
    bl_label = "Apply Render Settings"

    def execute(self, context):
        blend_file_name = bpy.path.basename(bpy.context.blend_data.filepath)
        blend_file_name_without_extension = os.path.splitext(blend_file_name)[0]
        episode = bpy.context.preferences.addons[__name__].preferences.episode_enum
        
        # output_folder = os.path.join("R:\\NSS2\\03_Postproduction\\04_OUTPUT\\Renders\\02_COMP\\NSS210\\mov", blend_file_name_without_extension + ".mov")
        output_folder = os.path.join("R:\\NSS2\\03_Postproduction\\04_OUTPUT\\Renders\\02_COMP\\NSS2" + str(episode) + "\\mov", blend_file_name_without_extension + ".mov")

        bpy.context.scene.render.filepath = output_folder
        bpy.context.scene.render.fps = 25
        bpy.context.scene.render.use_file_extension = False
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
        bpy.context.scene.render.ffmpeg.codec = 'PNG'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        bpy.context.scene.render.ffmpeg.video_bitrate = 50000
        bpy.context.scene.render.ffmpeg.minrate = 50000
        bpy.context.scene.render.ffmpeg.maxrate = 50000
        return {'FINISHED'}

class AutoUpdateImageOperator(bpy.types.Operator):
    bl_idname = "op.update_image"
    bl_label = "Update Image"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for image in bpy.data.images:
            image.reload()
        self.report({'INFO'}, "Reload Image Succesfull")
        return {'FINISHED'}
    

class GetLatestExrOperator(bpy.types.Operator):
    bl_idname = "op.get_latest_exr"
    bl_label = "Get Latest EXR"

    def execute(self, context):
        #########################################################
        # Change Name of Image Node first
        #########################################################
        node_name_mapping = {
            "Image": "MP",
            "Env_Col.001": "Char_Col",
            "Image.004": "Siren_Light",
            "Image.003": "Siren_Cone",
        }

        # Get the Compositor Node Tree
        compositor_tree = bpy.context.scene.node_tree

        # Iterate over the node_name_mapping dictionary and update node names
        for old_name, new_name in node_name_mapping.items():
            for node in compositor_tree.nodes:
                if node.name == old_name:
                    node.name = new_name
                    break
        #########################################################
        # Extract Filename put in scene_shot_number
        current_file_path = bpy.data.filepath
        current_file_name = os.path.splitext(os.path.basename(current_file_path))[0]

        root_folder = r"R:\NSS2\03_Postproduction\04_OUTPUT\Renders\01_FOOTAGES"
        episode = bpy.context.preferences.addons[__name__].preferences.episode_enum
#        episode = "NSS210"
        scene_shot_number = current_file_name

        suffix_env = "_Env_Col"
        suffix_char = "_Char_Col"
        suffix_char_floor_ao = "_Char_Floor_Ao"
        suffix_mp = "_MP"
        suffix_sirenlight = "_Siren_Light"
        suffix_sirencone = "_Siren_Cone"

        # Define folder paths using the provided variables
        folder_env_col = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_env}")
        folder_mp = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_mp}")
        folder_char_col = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_char}")
        folder_char_floor_ao = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_char_floor_ao}")

        folder_siren_light = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_sirenlight}")
        folder_siren_cone = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_sirencone}")

        # Create a list of folder paths
        folder_paths = [folder_env_col, folder_mp, folder_char_col, folder_char_floor_ao, folder_siren_light, folder_siren_cone]

        # Define the names of the image nodes and their corresponding suffixes
        image_nodes_and_suffixes = {
            "Env_Col": "Env_Col",
            "MP": "MP",
            "Char_Col": "Char_Col",
            "Char_Floor_Ao": "Char_Floor_Ao",
            "Siren_Light": "Siren_Light",
            "Siren_Cone": "Siren_Cone",
        }

        # Iterate through the lists using indices
        for folder_path, image_node_name_suffix in zip(folder_paths, image_nodes_and_suffixes.values()):
            image_node_name = [k for k, v in image_nodes_and_suffixes.items() if v == image_node_name_suffix][0]

            # Find the Compositor node tree
            compositor_tree = bpy.context.scene.node_tree

            # Find the Image Node in the Compositor by name
            image_node = compositor_tree.nodes.get(image_node_name)

            # Check if the Image Node was found
            if image_node is not None and image_node.type == 'IMAGE':
                # Store the existing links connected to the Image Node
                existing_links = []
                for link in compositor_tree.links:
                    if link.to_node == image_node:
                        existing_links.append(link)

                # Get a list of image files in the folder with the specified suffix
                image_files = [f for f in os.listdir(folder_path) if f.endswith('.exr') and image_node_name_suffix in f]

                # Remove the old image datablock if it exists
                if image_node.image:
                    bpy.data.images.remove(image_node.image)

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
                    
                    ##########################################################       
                    # Solution to use only Double Char_Col Node
                    ##########################################################
                    char_col_node = None
                    normalize_node = None

                    # Find Char_Col and Normalize.001 nodes
                    for node in compositor_tree.nodes:
                        if node.name == 'Char_Col':
                            char_col_node = node
                        elif node.name == 'Normalize.001':
                            normalize_node = node

                    # Check if both nodes were found
                    if char_col_node is not None and normalize_node is not None:
                        # Create a link between Char_Col and Normalize.001
                        link = compositor_tree.links.new(char_col_node.outputs['Depth'], normalize_node.inputs[0])
                        print("Nodes connected successfully.")
                    else:
                        print("One or both nodes not found.")
                    ##########################################################
                    ##########################################################

                    # Set the new image data for the Image Node
                    image_node.image = image
                    
                    # Check for Image node Env_Col and MP (Single Image / Sequence)
                    if image_node_name in ["Env_Col", "MP"]:
                        if 1 <= len(image_files) <= 5:
                            print (image_node_name + " Single Image")
                            image_node.image.source = 'FILE'
                        else:
                            print (image_node_name + " Image Sequence")
                            image_node.image.source = 'SEQUENCE'
                    else:
                        image_node.image.source = 'SEQUENCE'
                
                
#                    image_node.image.source = 'SEQUENCE'
                    image_node.frame_offset = 1000
                    image_node.use_auto_refresh = True
                    image_node.image.filepath = image_path
                    image_node.image.file_format = 'OPEN_EXR'

                    # Set the frame duration based on the number of images in the folder
                    image_node.frame_duration = len(image_files)
                    
                    # Set default frame first
                    bpy.context.scene.frame_current = 1
                    bpy.context.scene.frame_start = 1

                    # Set the frame end based on the number of images in the folder
                    bpy.context.scene.frame_end = len(image_files)


                    # Reconnect the Image Node to its output nodes
                    for link in existing_links:
                        compositor_tree.links.new(link.from_node.outputs[link.from_socket.name], image_node.inputs['Image'])

                    print(f"{image_node_name} node updated successfully.")
                else:
                    print(f"No image sequences found in the folder for {image_node_name}.")
            else:
                print(f"{image_node_name} node not found in the compositor.")

        return {'FINISHED'}
    
#class GetLatestExrOperator(bpy.types.Operator):
#    bl_idname = "op.get_latest_exr"
#    bl_label = "Get Latest EXR"

#    def execute(self, context):
#        #########################################################
#        # Change Name of Image Node first
#        #########################################################
#        node_name_mapping = {
#            "Image": "MP",
#            "Env_Col.001": "Char_Col",
#            "Image.004": "Siren_Light",
#            "Image.003": "Siren_Cone",
#        }

#        # Get the Compositor Node Tree
#        compositor_tree = bpy.context.scene.node_tree

#        # Iterate over the node_name_mapping dictionary and update node names
#        for old_name, new_name in node_name_mapping.items():
#            for node in compositor_tree.nodes:
#                if node.name == old_name:
#                    node.name = new_name
#                    break
#        #########################################################

#        # Extract Filename put in scene_shot_number
#        current_file_path = bpy.data.filepath
#        current_file_name = os.path.splitext(os.path.basename(current_file_path))[0]

#        # ISSUE
#        # need update by specific suffix ex cryptomatte
#        # 

#        root_folder = r"R:\NSS2\03_Postproduction\04_OUTPUT\Renders\01_FOOTAGES"
#        episode = "NSS210"
#        scene_shot_number = current_file_name

#        suffix_env = "_Env_Col"
#        suffix_char = "_Char_Col"
#        suffix_char_defocus = "_Char_Col"
#        suffix_char_floor_ao = "_Char_Floor_Ao"
#        suffix_mp = "_MP"
#        suffix_sirenlight = "_Siren_Light"
#        suffix_sirencone = "_Siren_Cone"

#        # Define folder paths using the provided variables
#        folder_env_col = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_env}")
#        folder_mp = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_mp}")
#        folder_char_col = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_char}")
#        folder_char_floor_ao = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_char_floor_ao}")

#        folder_siren_light = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_sirenlight}")
#        folder_siren_cone = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_sirencone}")
#        folder_char_col_defocus = os.path.join(root_folder, episode, scene_shot_number, f"{scene_shot_number}{suffix_char_defocus}")

#        # Create a list of folder paths
#        folder_paths = [folder_env_col, folder_mp, folder_char_col, folder_char_floor_ao, folder_siren_light, folder_siren_cone, folder_char_col_defocus]

#        # Define the names of the image nodes and their corresponding suffixes
#        image_nodes_and_suffixes = {
#            "Env_Col": "Env_Col",
#            "MP": "MP",
#            "Char_Col": "Char_Col",
#            "Char_Floor_Ao": "Char_Floor_Ao",
#            "Siren_Light": "Siren_Light",
#            "Siren_Cone": "Siren_Cone",
#            "Char_Col_Defocus": "Char_Col",
#        }

#        # Iterate through the lists using indices
#        for folder_path, image_node_name_suffix in zip(folder_paths, image_nodes_and_suffixes.values()):
#            image_node_name = [k for k, v in image_nodes_and_suffixes.items() if v == image_node_name_suffix][0]

#            # Find the Compositor node tree
#            compositor_tree = bpy.context.scene.node_tree

#            # Find the Image Node in the Compositor by name
#            image_node = compositor_tree.nodes.get(image_node_name)

#            # Check if the Image Node was found
#            if image_node is not None and image_node.type == 'IMAGE':
#                # Store the existing links connected to the Image Node
#                existing_links = []
#                for link in compositor_tree.links:
#                    if link.to_node == image_node:
#                        existing_links.append(link)

#                # Get a list of image files in the folder with the specified suffix
#                image_files = [f for f in os.listdir(folder_path) if f.endswith('.exr') and image_node_name_suffix in f]

#                # Remove the old image datablock if it exists
#                if image_node.image:
#                    bpy.data.images.remove(image_node.image)

#                # Check if there are image sequences in the folder
#                if len(image_files) > 0:
#                    # Sort the image files by name
#                    image_files.sort()

#                    # Set the image_path to the path of the first image in the folder
#                    image_path = os.path.join(folder_path, image_files[0])

#                    # Check if the image datablock already exists in bpy.data.images
#                    existing_image = bpy.data.images.get(image_path)
#                    if existing_image is not None:
#                        # Use the existing image datablock instead of removing it
#                        image = existing_image
#                    else:
#                        # Load the image from the specified path
#                        try:
#                            image = bpy.data.images.load(image_path)
#                        except:
#                            raise Exception("Image not found or cannot be loaded.")

#                    # Set the new image data for the Image Node
#                    image_node.image = image
#                    image_node.image.source = 'SEQUENCE'
#                    image_node.frame_offset = 1000
#                    image_node.use_auto_refresh = True
#                    image_node.image.filepath = image_path
#                    image_node.image.file_format = 'OPEN_EXR'

#                    # Set the frame duration based on the number of images in the folder
#                    image_node.frame_duration = len(image_files)
#                    
#                    # Set default frame first
#                    bpy.context.scene.frame_current = 1
#                    bpy.context.scene.frame_start = 1

#                    # Set the frame end based on the number of images in the folder
#                    bpy.context.scene.frame_end = len(image_files)


#                    # Reconnect the Image Node to its output nodes
#                    for link in existing_links:
#                        compositor_tree.links.new(link.from_node.outputs[link.from_socket.name], image_node.inputs['Image'])

#                    print(f"{image_node_name} node updated successfully.")
#                else:
#                    print(f"No image sequences found in the folder for {image_node_name}.")
#            else:
#                print(f"{image_node_name} node not found in the compositor.")
#        return {'FINISHED'}    
        
class RENDER_PT_RenderSettingsAddonPanel(bpy.types.Panel):
    bl_idname = "RENDER_PT_render_settings_addon"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "123 Render Settings Addon"
    bl_region_type = "UI"
    bl_category = "123"

    def draw(self, context):
        episode = bpy.context.preferences.addons[__name__].preferences.episode_enum
        layout = self.layout
        layout.scale_x =1.2
        layout.scale_y =1.2 
        box = layout.box()
        box.label(text="Status: ", icon="INFO")
        box.label(text="Episode Number: " + episode, icon="KEYTYPE_EXTREME_VEC")
        box.prop(bpy.context.preferences.addons[__name__].preferences, "episode_enum")
        
        layout.operator(RenderSettingsAddonOperator.bl_idname)
        layout.operator(AutoUpdateImageOperator.bl_idname, icon="FILE_REFRESH")
        layout.separator()
        layout.operator(GetLatestExrOperator.bl_idname)
        
def register():
    bpy.utils.register_class(AddonPreferences)
    bpy.utils.register_class(RenderSettingsAddonOperator)
    bpy.utils.register_class(AutoUpdateImageOperator)
    bpy.utils.register_class(GetLatestExrOperator)
    bpy.utils.register_class(RENDER_PT_RenderSettingsAddonPanel)

def unregister():
    bpy.utils.unregister_class(AddonPreferences)
    bpy.utils.unregister_class(RenderSettingsAddonOperator)
    bpy.utils.unregister_class(AutoUpdateImageOperator)
    bpy.utils.unregister_class(GetLatestExrOperator)
    bpy.utils.unregister_class(RENDER_PT_RenderSettingsAddonPanel)

if __name__ == "__main__":
    register()
