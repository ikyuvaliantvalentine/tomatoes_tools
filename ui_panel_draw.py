import bpy
from bpy.types import Panel, UIList
from bpy.props import *
from .. properties import *

####################################
# Panel Polycount
####################################    
def UIObjectData(context, layout):    
    layout.label(text="Select Tris / Ngon")
    row  = layout.row()
    row.operator("datamesh.facetype_select", text="Select Tris", icon_value=get_icon("triangle")).face_type = "3"
    row.operator("datamesh.facetype_select", text="Select Ngon", icon_value=get_icon("ngon")).face_type = "5"
    
    scriptBox = layout.box()
    row = scriptBox.row(align = True)
    row.label(text = "Object")
    row.label(text = "Verts")
    row.label(text = "Edges")
    row.label(text = "Faces")
    row.label(text = "Tris")
    row.label(text = "Ngons")
    
    # generate table
    sumfaces = []
#    for o in context.selected_objects:
    for o in context.scene.objects:
        if o.type != 'MESH':
            continue
        
        me = o.data
        verts = len(me.vertices)
        edges = len(me.edges)
        faces = len(me.polygons)
    
        tris_count = 0
        for p in o.data.polygons:
            if len(p.vertices) > 3:
                tris_count = tris_count + len(p.vertices) - 2
            else:
                tris_count = tris_count +1 
            pass
        
        ngonCount = 0
        for p in o.data.polygons:
            count = p.loop_total
            if count > 4:
                ngonCount += 1 
            
        row = scriptBox.row(align = True)
        row.label(text = "%s" % (o.name))
        row.label(text = "%d" % (verts))
        row.label(text = "%d" % (edges))
        row.label(text = "%d" % (faces))
        row.label(text = "%d" % (tris_count))
        row.label(text = "%d" % (ngonCount))
        
#    row.label(text = "%i" % (totalEdgesInSelection))
#    row.label(text = "%i" % (totalFacesInSelection))
#    row.label(text = "%i" % (totalTriInSelection))
#    row.label(text = "%i" % (totalNgonsInSelection))
        
#        row.label(text = "%i" % (totalEdgesInSelection))
#        row.label(text = "%i" % (totalFacesInSelection))
#        row.label(text = "%i" % (totalTriInSelection))
#        row.label(text = "%i" % (totalNgonsInSelection))
#        row.label(text = "")
        
#def UIObjectData(context, layout):
#    # test only meshes
#    object_total = []
#    selectedMeshes = [o for o in bpy.context.selected_objects if o.type == 'MESH']
#    
#    totalTriInSelection = 0
#    totalNgonsInSelection = 0
#    totalEdgesInSelection = 0
#    totalFacesInSelection = 0
#    totalVertsInSelection = 0

#    triCount = 0
#    ngonCount = 0
#    hasNGon = False

#    layout.label(text="Select Tris / Ngon")
#    row  = layout.row()
#    row.operator("datamesh.facetype_select", text="Select Tris", icon_value=get_icon("triangle")).face_type = "3"
#    row.operator("datamesh.facetype_select", text="Select Ngon", icon_value=get_icon("ngon")).face_type = "5"
# 
#    scriptBox = layout.box()
#    row = scriptBox.row(align = True)
#    row.label(text = "Object")
#    row.label(text = "Verts")
#    row.label(text = "Edges")
#    row.label(text = "Faces")
#    row.label(text = "Tris")
#    row.label(text = "Ngons")
#    row.label(text = "UV Map")

#    for element in selectedMeshes:
#        for poly in element.data.polygons:
#            # first check if quad
#            if len(poly.vertices) == 4:
#                triCount += 2
#            # or tri
#            elif len(poly.vertices) == 3:
#                triCount += 1
#            # or oops, ngon here, alert !
#            else:
#                triCount += 3
#                hasNGon = True
#                
#            count = poly.loop_total
#            if count > 4:
#                ngonCount += 1 
#        
#        # adding element stats to total count
#        totalTriInSelection += triCount
#        totalNgonsInSelection += ngonCount
#        totalVertsInSelection += len(element.data.vertices)
#        totalEdgesInSelection += len(element.data.edges)
#        totalFacesInSelection += len(element.data.polygons)
#        # generate table
#        row = scriptBox.row(align = True)
#        row.label(text = "%s" % (element.name))
#        row.label(text = "%i " % (len(element.data.vertices)))
#        row.label(text = "%i " % (len(element.data.edges)))
#        row.label(text = "%i " % (len(element.data.polygons)))
#        row.label(text = "%i" % (triCount))
#        row.label(text = "%i" % (ngonCount))
#        
#        if(len(context.view_layer.objects.active.data.uv_layers)) >1:
#            row.label(text= "Error")
#        elif(len(context.view_layer.objects.active.data.uv_layers)) <1:
#            row.label(text= "N/A")
#        else:
#            row.label(text= "OK")
#                    
    # show total stats                
#    scriptBox.row().separator() 
#    row = scriptBox.row(align = True)
#    row.label(text = "TOTAL")
#    row.label(text = "%i" % (totalVertsInSelection))
#    row.label(text = "%i" % (totalEdgesInSelection))
#    row.label(text = "%i" % (totalFacesInSelection))
#    row.label(text = "%i" % (totalTriInSelection))
#    row.label(text = "%i" % (totalNgonsInSelection))
#    row.label(text = "")
    
####################################
# Panel List Light
####################################       
def UIListLight(self, context):
    layout = self.layout  
    objects = bpy.data.objects
    ob_act = context.active_object
    lamps = bpy.data.lights
    maincol = layout.column(align=True)

    if objects:
        box = layout.box()
        rowmain = box.row()
        split = rowmain.split()
        col = split.column()
        row = box.row(align=True)
        
        split = row.split(factor=1.0)
        col = split.column()
        col.label(text="Type")
        
        split = row.split(factor=0.21)
        col = split.column()
        col.label(text="Name")
        
        split = split.split(factor=0.24)
        col = split.column()
        col.label(text="Color")
        
        split = split.split(factor=0.48)
        col = split.column()
        col.label(text="Strength")
        
        split = split.split(factor=0.54)
        col = split.column()
        col.label(text="Use")

        split = split.split(factor=1.0)
        col = split.column()
        col.label(text="Visibility")
        
        for a in objects:
            meshlight = a.type == "MESH"
            
            if a and meshlight:
                mesh = a.data
                
                row = box.row(align=True)
                split = row.split(factor=1.0)
                col = split.column()
                row = col.row(align=True)
                
                for a in bpy.context.object.material_slots:
                    if not a.material:
                        continue
                    if a.material.node_tree and a.material.node_tree.nodes:
                        for node in a.material.node_tree.nodes:
                            if node.type == "EMISSION":
                                row.label(text="", icon='MESH_GRID')
                                
                                split = row.split(factor=0.3)
                                col = split.column()
                                row = col.row(align=True)
                                row.active = True
                                row.operator("scene.object_select", text=mesh.name, emboss=False).object = mesh.name
                
                                
                                ### COLOR ###
                                if not node.inputs[0].is_linked:
                                    row.prop(node.inputs[0], 'default_value', text='')
                                else:
                                    row.label(text='Connected')
                                
                                ### STRENGHT ###
                                split = split.split(factor=0.45)
                                col = split.column()
                                row = col.row(align=True)
                                if not node.inputs[1].is_linked:
                                    row.prop(node.inputs[1], 'default_value', text='')
                                    
                                split = split.split(factor=0.6)
                                col = split.column()
                                row = col.row(align=True)
                                row.prop(context.object.cycles_visibility, "camera", text='Cam', toggle=True)
                                row.prop(context.object.cycles_visibility, "diffuse", text='Diff', toggle=True)
                                row.prop(context.object.cycles_visibility, "glossy", text='Gloss', toggle=True)
                               
                               
#                                split = split.split(factor=1.0)
#                                col = split.column()
#                                row = col.row(align=True)
#                                row.prop(a, "hide_viewport", text="", emboss=False)
#                                row.prop(a, "hide_select", text="", emboss=False)
#                                row.prop(a, "hide_render", text="", emboss=False)
                                 
        for ob in objects:
            is_lamp = ob.type in {"LIGHT", "MESH"}

            if ob and is_lamp:
                lamp = ob.data
        
                row = box.row(align=True)
                split = row.split(factor=1.0)
                col = split.column()
                row = col.row(align=True)
#                col.active = ob == ob_act
            
                row.prop(lamp, "type", text='', icon_only=True, emboss=False, icon="%s" %("LIGHT_%s" %ob.data.type))
                        
                
                split = row.split(factor=0.3)
                col = split.column()
                row = col.row(align=True)
                row.active = True
                row.operator("scene.object_select", text=ob.name, emboss=False).object = ob.name
                
                split = split.split(factor=0.1)
                col = split.column()
                row = col.row()
                if lamp.use_nodes:
                    for node in lamp.node_tree.nodes:
                        if node.type == 'EMISSION':                                       
                            ### COLOR ###
                            if not node.inputs[0].is_linked:
                                row.prop(node.inputs[0], 'default_value', text='')
                            else:
                                row.label(text='Connected')
                            
                            ### STRENGHT ###
                            split = split.split(factor=0.45)
                            col = split.column()
                            row = col.row(align=True)
                            if not node.inputs[1].is_linked:
                                row.prop(node.inputs[1], 'default_value', text='')
                else:
                    split = split.split(factor=0.5)
                    col = split.column()
                    row = col.row(align=True)
                    row.prop(lamp, 'use_nodes', toggle=True)
                             
                split = split.split(factor=0.6)
                col = split.column()
                row = col.row(align=True)
                row.prop(context.object.cycles_visibility, "camera", text='Cam', toggle=True)
                row.prop(context.object.cycles_visibility, "diffuse", text='Diff', toggle=True)
                row.prop(context.object.cycles_visibility, "glossy", text='Gloss', toggle=True)
               
               
                split = split.split(factor=1.0)
                col = split.column()
                row = col.row(align=True)
                row.prop(ob, "hide_viewport", text="", emboss=False)
                row.prop(ob, "hide_select", text="", emboss=False)
                row.prop(ob, "hide_render", text="", emboss=False)
    # else:
    #     box.label(text="No Lamps", icon="LAMP_DATA")

####################################
# Panel UV Toolkit
####################################       
def UIUVToolkit(context, layout):
    tomatoes = context.scene.tomatoes_props
    layout.operator("uv.select_flipped", text="CHECK FLIPPED UV")
    layout.operator("uv.toolkit_unwrap_selected", text="Unwrap Selected", icon='SELECT_SUBTRACT')
    layout.operator("uv.toolkit_quad_unwrap", text="Quad Unwrap", icon='CON_SAMEVOL')
    layout.label(text="Shading")
    col = layout.column(align=True)
    col.operator("uv.toolkit_sharp_edges_from_uv_islands", text="Smooth from UV Islands")
    prop = col.operator("uv.seams_from_islands", text="Sharp Edges Only")
    prop.mark_seams, prop.mark_sharp = False, True
    layout.label(text="Seams")
    col = layout.column(align=True)
    prop = col.operator("uv.seams_from_islands", icon='MOD_EDGESPLIT')
    prop.mark_seams, prop.mark_sharp = True, False
    col.operator("uv.toolkit_boundary_seam")
    col.operator("uv.toolkit_mirror_seam")

    col = layout.column()
    col.label(text="Move UV")
    col.prop(tomatoes, "move_uv_type", text="")

    row = col.row(align=True)
    row.scale_x = 3.0

    if tomatoes.move_uv_type == "1":       
        prop = row.operator("uv.toolkit_move_islands", text="", icon='SORT_DESC')
        prop.move_uv = 0, 1, 0
        row = col.row(align=True)
        split = row.split(align=True)
        prop = split.operator("uv.toolkit_move_islands", text="", icon='BACK')
        prop.move_uv = -1, 0, 0
        prop = split.operator("uv.toolkit_move_islands", text="", icon='SORT_ASC')
        prop.move_uv = 0, -1, 0
        prop = split.operator("uv.toolkit_move_islands", text="", icon='FORWARD')
        prop.move_uv = 1, 0, 0
    elif tomatoes.move_uv_type == "0.5":
        prop = row.operator("uv.toolkit_move_islands", text="", icon='SORT_DESC')
        prop.move_uv = 0, 0.5, 0
        row = col.row(align=True)
        split = row.split(align=True)
        prop = split.operator("uv.toolkit_move_islands", text="", icon='BACK')
        prop.move_uv = -0.5, 0, 0
        prop = split.operator("uv.toolkit_move_islands", text="", icon='SORT_ASC')
        prop.move_uv = 0, -0.5, 0
        prop = split.operator("uv.toolkit_move_islands", text="", icon='FORWARD')
        prop.move_uv = 0.5, 0, 0
    
    col.label(text="Rotate UVs")          
    row = layout.row(align=True)
    row.operator("uv.toolkit_rotate_uv_islands", text="Rotate –90°").angle = -1.5708
    row.operator("uv.toolkit_rotate_uv_islands", text="Rotate +90°").angle = 1.5708
    row = layout.row(align=True)
    row.operator("uv.toolkit_rotate_uv_islands", text="Rotate 180°").angle = 3.14159
    layout.label(text="Mirror")
    row = layout.row(align=True)
    prop = row.operator("uv.toolkit_mirror_uv", text="X")
    prop.x, prop.y, prop.z = True, False, False
    prop = row.operator("uv.toolkit_mirror_uv", text="Y")
    prop.x, prop.y, prop.z = False, True, False
    row = layout.row()
    row.operator("mesh.faces_mirror_uv", text="Copy Mirrored UV Coords")

####################################
# Panel UV Toolkit Checker Map
####################################    
def UIUVToolkitCheckerMap(context, layout):
    tomatoes = context.scene.tomatoes_props            
    row = layout.row()
    row.operator("uv.toolkit_toggle_texture_mode", text="Show Texture in Viewport", icon='UV_DATA')
    row = layout.row(align=True)
    row.operator("uv.toolkit_change_checker_grid", text="Color Grid").checker_grid_type = 'COLOR_GRID'
    row.operator("uv.toolkit_change_checker_grid", text="Checker Grid").checker_grid_type = 'UV_GRID'
    layout.operator("uv.toolkit_disable_selected_checker_materials", text="Disable selected materials", icon='NODE_COMPOSITING')
    
    
    layout.label(text="Auto assign texture in UV Editor")
    layout.prop(tomatoes, "assign_image", expand=True)
    layout.label(text="Default checker style")
    layout.prop(tomatoes, "checker_type", expand=True)
    
    col = layout.column(align=True)
    col.prop(tomatoes, "checker_map_width")
    col.prop(tomatoes, "checker_map_height")
    row = col.row(align=True)
    row .operator("uv.toolkit_custom_sizes_checker_map", icon="UV")
    layout.label(text="Remove")
    row = layout.row()
    row.operator("uv.toolkit_remove_all_checker_maps", text="Remove All Checker Maps", icon='TRASH')
    
####################################
# Panel Modifier List
####################################    
class MODIFIER_UL_modifier_stack(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ob = data
        md = item
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            
            row.prop(md, 'name', text="", emboss=False, icon_value=1, icon = self.get_mod_icon(md))
            row.prop(md, 'show_render', text="", emboss=False, icon_only=True)
            row.prop(md, 'show_viewport', text="", emboss=False, icon_only=True)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=icon)
            
    def get_mod_icon(self, md):
        md_type = md.type
        md_icon = bpy.types.Modifier.bl_rna.properties['type'].enum_items[md_type].icon
        return md_icon

def drawULModifier(context, layout):
    tomatoes = context.scene.tomatoes_props
    ob = context.object
    
    if ob:
        row = layout.row()
        row.label(text='Modifiers')
        row = layout.row()
        col = row.column(align=True)
        col.template_list('MODIFIER_UL_modifier_stack', '', ob, 'modifiers', tomatoes, 'active_modifier_index')
        
        layout.separator()
        
        col = row.column(align=True)
        col.operator("object.modifier_moveup", icon='TRIA_UP', text="")
        col.operator("object.modifier_movedown", icon='TRIA_DOWN', text="")
        col.separator()
        col.operator("object.remove_modifier", text="", icon='X')

####################################
# Panel FBX Importer
####################################       
def UIFbxImporter(context, layout):
    tomatoes = context.scene.tomatoes_props
    layout.scale_x = 1.2
    layout.scale_y = 1.2
            
    row = layout.row()                                                                    
    col = row.column(align=True)
    if context.object is not None:
        if context.mode == 'OBJECT':
            col.label(text="Export Mode:")
            col.prop(tomatoes, 'fbx_export_mode')
            
            col.separator()
            col.label(text="Apply:")
            
            col.prop(tomatoes, "apply_rot", text="Rotation")
            col.prop(tomatoes, "apply_scale", text="Scale")
            col.prop(tomatoes, "delete_all_materials", text="Delete All Materials")
            if tomatoes.fbx_export_mode == '0':
                col.prop(tomatoes, "apply_loc", text="Location")

            row = col.row()
            if tomatoes.fbx_export_mode == '1':
                if tomatoes.set_custom_fbx_name:
                    #Split row
                    row = col.row()
                    c = row.column()
                    row = c.row()
                    split = row.split(factor=0.5, align=True)
                    c = split.column()
                    c.label(text="FBX Name:")
                    split = split.split()
                    c = split.column()
                    c.prop(tomatoes, "custom_fbx_name")

            row = col.row()
            if tomatoes.custom_export_path:
                #Split row
                row = col.row()
                c = row.column()
                row = c.row()
                split = row.split(factor=0.5, align=True)
                c = split.column()
                c.label(text="Export Path:")
                split = split.split()
                c = split.column()
                c.prop(tomatoes, "export_path")
                #----

            row = col.row()
            row.operator("object.multi_fbx_export", text="Export FBX")
            
            if len(tomatoes.export_dir) > 0:
                row = layout.row()
                row.operator("object.open_export_dir", text="Open Export Directory")
                row = layout.row()
        
    
    if context.mode == 'OBJECT':
        row = col.row()
        row.operator("object.import_fbxobj", text="Import FBXs/OBJs")   