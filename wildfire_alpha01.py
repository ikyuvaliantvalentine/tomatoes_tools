# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    'name' : 'RIG UI PICKER',
    'author' : 'Septyan Roche',
    'version' : (0, 1),
    'blender' : (2, 7, 2),
    'location' : 'View3D > Toolbar',
    'description' : 'rig selector dan char selector ',
    'category' : 'MD Animation'}


import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator, Panel
#from . import charselector 
#from . import boneselector 


tab_all = [
    ("selector", "Selector", "", 1),
    ("layer", "Layer", "", 2),
    ("anim_lib", "Anim Lib", "", 3),
    ("vocal", "Vocal", "",4),]

tab_anim = [
    ("body", "Body", "",1),
    ("facial", "Facial", "",2),]

tab_picker = [('body','Body','',1),
    ('fingers','Fingers','',2)]
    
    
bpy.types.Scene.tab = EnumProperty(items=tab_all, default="selector")  
bpy.types.Scene.tab_anim = EnumProperty(items=tab_anim, default="body")    
bpy.types.Scene.tab_picker = EnumProperty(items=tab_picker, default="body")  
bpy.types.Scene.focus_char = BoolProperty(name='focus', default=True, description='aktifkan fokus karakter secara langsung saat karakter dipilih')


#------------------------------------------------------- panel ---------------------------------------------------------       
class wildpanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'RIG UI'
    
   
        
    
    

#================ real simplify =================

class selbon_op(bpy.types.Operator):
    bl_idname = 'scn.simplify'
    bl_label = 'Simplify'
    bl_description =  'simplify to zero subdiv'
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        
        try:
            
           scn = bpy.context.scene.render
           
           if not scn.use_simplify:
               scn.use_simplify = True
               scn.simplify_subdivision = 0
               scn.simplify_child_particles = 0
               scn.simplify_shadow_samples = 0
               scn.simplify_ao_sss = 0
               scn.use_unsimplify_render = True
           else:
               scn.use_simplify = False

        except:
           pass
                
        return {'FINISHED'}
    

#================= bone selector ================

class selbon_op(bpy.types.Operator):
    bl_idname = 'ob.selectbone'
    bl_label = 'select'
    bl_description =  'select single bone (shift+click = tambah select) (shift+ctrl+click = kurang select)'
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'X'
    
    bone = StringProperty()
    ext = BoolProperty()
           
    @classmethod
    def poll(cls, context):
        return context.active_object is not None 
    
    def invoke(self, context, event):
        try:
            rig = bpy.context.active_object
            bones = bpy.context.scene.objects[rig.name].data.bones
            
        except keyError:
            self.report({'INFO'}, 'ngga ada')
        if context.object:
            
            try:
                def deselect():
                        
                    for bone in bones:
                        bone.select = False
                
                if event.shift != True:
                    deselect()        
                
                if event.ctrl:
                    if bones[self.bone]:
                        bones[self.bone].select = False
                else:
                    if bones[self.bone]:
                        bones.active = bones[self.bone]
                        bones[self.bone].select = True
                        
                        
            except:
                self.report({'WARNING'}, 'ngga ada')

            return {'FINISHED'}


 
#============= bone group selector ===============

class selbon_group_op(bpy.types.Operator):
    group = StringProperty()
    ext = BoolProperty()
    
    bl_idname = 'ob.selectbonegroup'
    bl_label = 'select group'
    bl_description =  'select bone group (shift+click = tambah select)'
    bl_options = {'REGISTER', 'UNDO'}
    
    def invoke(self, context, event):
        
        tangan_R = ['upper_arm.fk.R','forearm.fk.R','hand.fk.R']
        tangan_L = ['upper_arm.fk.L','forearm.fk.L','hand.fk.L']
        kaki_R  = ['thigh.fk.R','shin.fk.R','foot.fk.R', 'foot.ik.R','knee_target.ik.R','toe.R','foot_roll.ik.R','TOE ROT R']
        kaki_L  = ['thigh.fk.L','shin.fk.L','foot.fk.L', 'foot.ik.L','knee_target.ik.L','toe.L','foot_roll.ik.L','TOE ROT L']
        
        p = 'f_pinky'
        r = 'f_ring'
        m = 'f_middle'
        i = 'f_index'
        t = 'thumb'

        f_pinky_R = [p +'.01.R',p +'.02.R',p+'.03.R']
        f_pinky_L = [p +'.01.L',p +'.02.L',p+'.03.L']
        f_ring_R = [r +'.01.R',r +'.02.R',r+'.03.R']
        f_ring_L = [r +'.01.L',r +'.02.L',r+'.03.L']
        f_middle_R = [m +'.01.R',m +'.02.R',m+'.03.R']
        f_middle_L = [m +'.01.L',m +'.02.L',m+'.03.L']
        f_index_R = [i +'.01.R',i +'.02.R',i+'.03.R']
        f_index_L = [i +'.01.L',i +'.02.L',i+'.03.L']
        f_thumb_R = [t +'.01.R',t +'.02.R',t+'.03.R']
        f_thumb_L = [t +'.01.L',t +'.02.L',t+'.03.L']
                
        f_1_R = [p+'.01.R',r+'.01.R',m+'.01.R',i+'.01.R']
        f_2_R = [p+'.02.R',r+'.02.R',m+'.02.R',i+'.02.R']
        f_3_R = [p+'.03.R',r+'.03.R',m+'.03.R',i+'.03.R']
        f_s_R  = [p+'.R',r+'.R',m+'.R',i+'.R', 'thumb.R']

        f_1_L = [p+'.01.L',r+'.01.L',m+'.01.L',i+'.01.L']
        f_2_L = [p+'.02.L',r+'.02.L',m+'.02.L',i+'.02.L']
        f_3_L = [p+'.03.L',r+'.03.L',m+'.03.L',i+'.03.L']
        f_s_L  = [p+'.L',r+'.L',m+'.L',i+'.L', 'thumb.L']

        f_R = f_pinky_R+f_ring_R+f_middle_R+f_index_R+f_thumb_R
        f_L = f_pinky_L+f_ring_L+f_middle_L+f_index_L+f_thumb_L

        f_all_R = f_R + f_s_R + f_thumb_R + ['thumb.R']
        f_all_L = f_L + f_s_L + f_thumb_L + ['thumb.L']
        
        
        shoulder_R = ['CTRL_Shoulder R','ctrl-bahu.R', 'CTRL-bahu.R','DEF-shoulder.R.001','CTRL_Shoulder.R','CTRL_bahu.R','ctrl Shoulder R']
        shoulder_L = ['CTRL_Shoulder L','ctrl-bahu.L', 'CTRL-bahu.L','DEF-shoulder.L.001','CTRL_Shoulder.L','CTRL_bahu.L','ctrl Shoulder L']
        master_root = ['master_root','MASTER ROOT','master root']
        rig = bpy.context.active_object
        bones = bpy.context.scene.objects[rig.name].data.bones
        try:
            if context.object:
                
                if event.shift != True:
                    bpy.ops.pose.select_all(action='DESELECT')
               
                for gr in eval(self.group):
                    bpy.ops.object.select_pattern(pattern=gr, extend=True)
                    
                context.window_manager.modal_handler_add(self)
                self.report({'INFO'}, str(self.ext))
        except:
            self.report({'ERROR'}, self.group + ' ngga ada di viewport') 
        return {'RUNNING_MODAL'}
 

#=================== char selector ===================

class selchar(bpy.types.Operator):
    bl_idname = 'ob.selectchar'
    bl_label = 'char'
    bl_description = 'select char'
    bl_options = {'REGISTER', 'UNDO'}
    
    char = StringProperty()
    
    def execute(self, context):
        try:
            
            bpy.data.objects[self.char].hide = False
            bpy.data.objects[self.char.replace('_proxy','')].hide = False    
            if context.object and context.active_object != None:
                
                if context.active_object.mode =='POSE':
                    bpy.ops.object.mode_set(mode='OBJECT')
                    
                bpy.ops.object.select_pattern(pattern=str(bpy.data.objects[self.char].name), extend=False)
                bpy.context.scene.objects.active = bpy.data.objects[self.char]
                
                if context.scene.focus_char:
                    bpy.ops.view3d.view_selected(use_all_regions=1)
                    
                bpy.ops.object.mode_set(mode='POSE')
                
                
                #self.report({'INFO'}, self.char + ' udah keseleksi'  )
        except:
            self.report({'ERROR'}, 'ngga ada di viewport')
                
        return {'FINISHED'}

#=================== hide char selector ===================

class hide_char(bpy.types.Operator):
    bl_idname = 'ob.hidechar'
    bl_label = 'hide'
    bl_description =  'hide character'
    bl_options = {'REGISTER', 'UNDO'}
    
    char_name = StringProperty()
    
    
    def execute(self, context):
        try:
            
            obj = bpy.data.objects
            objchar = obj[self.char_name]
            objproxy = obj[self.char_name.replace('_proxy','')]
        
            
        
            if objchar.name != context.active_object.name:
                    
                if objchar.hide or objproxy.hide:
                    objchar.hide = False
                    objproxy.hide = False
                else:
                    objchar.hide = True
                    objproxy.hide = True
            else:
                self.report({'INFO'}, 'active character ngga bisa di hide')
        except:
            self.report({'INFO'}, 'ngga ada')
            
 
                    
        return {'FINISHED'}   
    

           
#===================== fungsi features ====================

class posemirror(bpy.types.Operator):
    bl_label  = 'mirror'
    bl_idname = 'pose.mirror'
    bl_description =  'mirror selected pose bone (shift+click = mirror all pose bone)'
    bl_options = {'REGISTER', 'UNDO'}
    
    def invoke(self, context, event):
        if context.object:
            if event.shift:
                bpy.ops.pose.select_all(action='DESELECT')
                for bon in ['root','MASTER ROOT']:
                    bpy.ops.object.select_pattern(pattern= bon, extend=True)
                bpy.ops.pose.select_all(action='INVERT')
            
            bpy.ops.pose.copy()
            bpy.ops.pose.paste(flipped=True)
            
        context.window_manager.modal_handler_add(self)
        return {'FINISHED'}


#_________________________ tabulasi ______________________

class selectchar(wildpanel, Panel):
    bl_idname='nomore'
    bl_label = 'WILD FIRE v.01'
    #bl_options = {'HIDE_HEADER'}
    def draw(self, context):
        try:
            activechar = bpy.context.active_object.name.upper().lower().replace('char', '').replace('01','').replace('02','').replace('03','').replace('grp','').replace('rig','').replace('_proxy','').replace('_', ' ').replace('-','').upper()
            scn = bpy.context.scene
            layout = self.layout
            
            row = layout.row(align=1)
            row.prop(scn, 'tab', expand=True)
            row = layout.row(align=1)
            row.alignment = 'CENTER'
            row.label("-------------%s -----------" % activechar)
            row = layout.row(align=1)
            
            row.prop(context.space_data, 'show_only_render', 'Only Render')
            row.prop(context.space_data, 'show_textured_solid', 'Show Texture')
            
            if scn.render.use_simplify:
                sim_icon = 'CHECKBOX_HLT'
            else:
                sim_icon = 'CHECKBOX_DEHLT'
                
            row.operator('scn.simplify', icon=sim_icon)
        except:
            pass
#____________________ panel select character ______________        
     
class selectchar(wildpanel, Panel):
    bl_idname='RIG CHAR SELECT'
    bl_label = ' '
        
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and bpy.context.scene.tab == "selector"
    def draw_header(self, context):
        try:
            if context.active_object != None:
               
                layout = self.layout
                row = layout.row()
                row.label(text='SELECT CHARACTER', icon='OUTLINER_OB_ARMATURE')
                row.prop(context.scene, 'focus_char',)
                
                
        except:
            self.report({'INFO'}, 'ngga ada')    
                
    def draw(self, context):
        layout = self.layout       
        col = layout.column(align=True)
        
        for obj in context.scene.objects:
            #ICON char----------------------------------------------
            if obj.select:
                icons = 'OUTLINER_OB_ARMATURE'
            else:
                icons = 'OUTLINER_DATA_ARMATURE'
            #ICON hide----------------------------------------------
            if obj.hide:
                iconh = 'VISIBLE_IPO_OFF'
            else:
                iconh = 'VISIBLE_IPO_ON'    
            
            #simple obj----------------------------------------
            obname= obj.name.upper().lower().replace('char', '').replace('01','').replace('02','').replace('03','').replace('grp_','').replace('rig_','').replace('_proxy','').replace('_', ' ').replace('-','').upper()
            
                    
            if obj.type == 'ARMATURE':
                if obj.name.lower().startswith('char'):
                    row = col.row(align=1)
                    row.operator('ob.selectchar', obname, icon=icons).char = obj.name      
                    
                    row.operator('ob.hidechar', '',icon=iconh).char_name=str(obj.name)
                    
                elif obj.name.lower().startswith('grp') or obj.name.lower().startswith('rig'):
                    row = col.row(align=1)
                    row.operator('ob.selectchar', obname, icon=icons).char = obj.name 
                    
                    row.operator('ob.hidechar', '',icon=iconh).char_name=str(obj.name)
                    


#_______________________ panel picker ____________________
    
class picker_panel(wildpanel, Panel):
    bl_idname = 'picker_panel'
    bl_label = ' '
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and bpy.context.scene.tab == "selector"
    
    def draw_header(self, context):
        try:
            if context.active_object != None:
                activechar = bpy.context.active_object.name.upper().lower().replace('char', '').replace('01','').replace('02','').replace('03','').replace('grp','').replace('rig','').replace('_proxy','').replace('_', ' ').replace('-','').upper()
                layout = self.layout
                row = layout.column()
                row.label(text=activechar +' UI BODY', icon='OUTLINER_OB_ARMATURE')
        except:
            self.report({'INFO'}, 'ngga ada di viewport')
    
    def draw(self,context):
        
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, 'tab_picker', expand=1)
        row = layout.row()
        
        layout.separator()
        if context.scene.tab_picker == 'body':
            
            row.alignment = 'EXPAND'
            row.scale_y = 1.0
            row.scale_x = 1.0
            subrow = row.row()
            subrow.scale_x=0.8
            subrow.alignment = 'LEFT'
            subrow.operator("pose.user_transforms_clear", text='reset all' ).only_selected=False
                  
            subrow = row.row()
            subrow.scale_x=0.8
            subrow.alignment = 'RIGHT'
            subrow.operator("pose.mirror", text='mirror' )
                    
            layout = self.layout
            row = layout.row()
            row.alignment = 'CENTER'
            row.scale_y = 1.0
            row.scale_x = 0.6
            
            sub = row.row()
            sub.alignment= 'CENTER'
            sub.scale_y = 1.0
            sub.scale_x = 2.0
            sub.operator("ob.selectbone", text='', icon='VISIBLE_IPO_ON').bone = 'CTRL-EYES.R'
            row.operator("ob.selectbone", text='', icon='ARROW_LEFTRIGHT').bone = 'CTRL-EYES'
            sub = row.row()
            sub.alignment= 'CENTER'
            sub.scale_y = 1.0
            sub.scale_x = 2.0
            sub.operator("ob.selectbone", text='', icon='VISIBLE_IPO_ON').bone = 'CTRL-EYES.L'
            
    #kepala--------------------------------
            scene = context.scene
            layout = self.layout
            row = layout.row()
            row.alignment = 'CENTER'
            row.scale_y = 2.0
            row.scale_x = 1.5
            row.operator("ob.selectbone", text='head').bone = 'head'
            
            
    #leher---------------------------------        
            layout = self.layout
            row = layout.row()
            row.alignment = 'CENTER'
            row.scale_y = 1.5
            row.scale_x = 1.0
            row.operator("ob.selectbone", text='neck').bone = 'neck'

    #pundak--------------------------------      
            layout = self.layout
            row = layout.row()
            row.alignment = 'CENTER'
            row = row.row()
            row.alignment = 'CENTER'
            row.scale_y = 1
            row.scale_x = 0.8
            row.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group = 'tangan_R'
            row.operator("ob.selectbonegroup", text='IK').group = 'shoulder_R'
            sub = row.row()
            sub.alignment = 'CENTER'
            sub.scale_y = 1
            sub.scale_x = 1
            
            sub.operator("ob.selectbone", text='shlder.R').bone = 'shoulder.R'
            sub.operator("ob.selectbone", text='shlder.L').bone = 'shoulder.L'
            
            row.operator("ob.selectbonegroup", text='IK').group = 'shoulder_L'
            row.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group = 'tangan_L'
            
    #tangan.R-------------------------------      
            layout = self.layout
            row = layout.row()
            row.alignment = 'CENTER'
            col =row.column()
            col.alignment = 'CENTER'
            col.scale_y = 1.0
            col.scale_x = 0.5
            sub = col.column()
            sub.alignment = 'CENTER'
            sub.scale_y = 3.5
            sub.scale_x = 0.6
            sub.operator("ob.selectbone", text='upper arm').bone = 'upper_arm.fk.R'
            sub = col.column()
            sub.alignment = 'CENTER'
            sub.scale_y = 1.0
            sub.scale_x = 0.5
            sub.operator("ob.selectbone", text= '', icon='CURSOR').bone = 'elbow_target.ik.R'
            sub = col.column()
            sub.alignment = 'CENTER'
            sub.scale_y = 3.5
            sub.scale_x = 0.6
            sub.operator("ob.selectbone", text='forearm').bone = 'forearm.fk.R'
            
            col.operator("ob.selectbone", text='FK').bone = 'hand.fk.R'
            col.operator("ob.selectbone", text='IK').bone = 'hand.ik.R'

    #badan----------------------------------        
            col = row.column()
            col.alignment = 'CENTER'
            col.scale_y = 1.0
            col.scale_x = 2.0
            
            kcol = col.column()
            kcol.alignment = 'CENTER'
            kcol.scale_y = 1.5   
            
            kcol.operator('ob.selectbone',text='chest.001').bone = 'chest.001'
            kcol.operator('ob.selectbone',text='chest').bone = 'chest'
            kcol.operator('ob.selectbone',text='spine').bone = 'spine'
            kcol.operator('ob.selectbone',text='hips').bone = 'hips'
            kcol.operator('ob.selectbone',text='torso').bone = 'torso'
       
    #kaki.R----------------------------------
            krow = col.row()
            krow.alignment = 'CENTER'
            subcol = krow.column()
            subcol.alignment = 'CENTER'
            subcol.scale_x=0.15
            subrow = subcol.row()
            subrow.operator("ob.selectbonegroup", 'all', icon='TRIA_DOWN').group = 'kaki_R'
            
            subcl = subcol.column()
            subcl.alignment = 'CENTER'
            subcl.scale_y = 3.5
            subcl.scale_x = 0.7
            subcl.operator("ob.selectbone", text= 'thigh.R').bone = 'thigh.fk.R'
            subcl = subcol.column()
            subcl.alignment = 'CENTER'
            subcl.scale_y = 1.0
            subcl.scale_x = 0.5
            subcl.operator("ob.selectbone", text= '', icon='CURSOR').bone = 'knee_target.ik.R'
            subcl = subcol.column()
            subcl.alignment = 'CENTER'
            subcl.scale_y = 3.5
            subcl.scale_x = 0.7
            subcl.operator("ob.selectbone", text= 'shin.R').bone = 'shin.fk.R'
            
            subcl.operator("ob.selectbone", text= 'FK').bone = 'foot.fk.R'             

    #kaki.l----------------------------------
            subcol = krow.column()
            subcol.alignment = 'CENTER'
            subcol.scale_x=0.15
            subrow = subcol.row()
            subrow.operator("ob.selectbonegroup", 'all', icon='TRIA_DOWN').group = 'kaki_L'
            
            subcl = subcol.column()
            subcl.alignment = 'CENTER'
            subcl.scale_y = 3.5
            subcl.scale_x = 0.7
            subcl.operator("ob.selectbone", text= 'thigh.L').bone = 'thigh.fk.L'
            subcl = subcol.column()
            subcl.alignment = 'CENTER'
            subcl.scale_y = 1.0
            subcl.scale_x = 0.5
            subcl.operator("ob.selectbone", text= '', icon='CURSOR').bone = 'knee_target.ik.L'
            subcl = subcol.column()
            subcl.alignment = 'CENTER'
            subcl.scale_y = 3.5
            subcl.scale_x = 0.7
            subcl.operator("ob.selectbone", text= 'shin.L').bone = 'shin.fk.L'
            
            subcl.operator("ob.selectbone", text= 'FK').bone = 'foot.fk.L'           

    #tangan.L---------------------------------        
            col =row.column()
            col.alignment = 'CENTER'
            col.scale_y = 1.0
            col.scale_x = 0.5
            sub = col.column()
            sub.alignment = 'CENTER'
            sub.scale_y = 3.5
            sub.scale_x = 0.6
            sub.operator("ob.selectbone", text='upper arm').bone = 'upper_arm.fk.L'
            sub = col.column()
            sub.alignment = 'CENTER'
            sub.scale_y = 1.0
            sub.scale_x = 0.5
            sub.operator("ob.selectbone", text= '', icon='CURSOR').bone = 'elbow_target.ik.L'
            sub = col.column()
            sub.alignment = 'CENTER'
            sub.scale_y = 3.5
            sub.scale_x = 0.6
            sub.operator("ob.selectbone", text='forearm').bone = 'forearm.fk.L'
            
            col.operator("ob.selectbone", text='FK').bone = 'hand.fk.L'
            col.operator("ob.selectbone", text='IK').bone = 'hand.ik.L'    
            
            layout = self.layout
            row = layout.row()
            row.alignment = 'CENTER'
            row = row.row()
            row.alignment = 'CENTER'
            row.scale_y = 1
            row.scale_x = 0.4
            row.operator("ob.selectbone", text= 'toe.L').bone = 'toe.R'
            sub = row.row()
            sub.alignment = 'CENTER'
            sub.scale_y = 1
            sub.scale_x = 2.7
            row.operator("ob.selectbone", text= 'roll.L').bone = 'foot_roll.ik.R'
            row.operator("ob.selectbone", text= 'roll.L').bone = 'foot_roll.ik.L'
            sub.operator("ob.selectbone", text= 'IK').bone = 'foot.ik.R'
            sub = row.row()
            sub.alignment = 'CENTER'
            sub.scale_y = 1
            sub.scale_x = 2.7
            sub.operator("ob.selectbone", text= 'IK').bone = 'foot.ik.L'
            
            row.operator("ob.selectbone", text= 'toe.L').bone = 'toe.L'


    #master root---------------------------------        
            layout = self.layout
            row = layout.row()
            row.alignment = 'CENTER'
            row = row.row(align=True)
            row.alignment = 'CENTER'
            row.scale_y = 1
            row.scale_x = 2
            row.operator("ob.selectbone", text='ROOT').bone = 'root'
            row.operator("ob.selectbonegroup", text='MASTER ROOT').group = 'master_root'
   
        
#----------------------------------------------------panel jari----------------------------------------------------        
class ui_fingers(wildpanel, Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = " "
    bl_idname = "RIG_UI_fingers"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and bpy.context.scene.tab == "selector" and bpy.context.scene.tab_picker == 'fingers'
    def draw_header(self, context):
        try:
            if context.active_object != None:
                activechar = bpy.context.active_object.name.upper().lower().replace('char', '').replace('01','').replace('02','').replace('03','').replace('grp','').replace('rig','').replace('_proxy','').replace('_', ' ').replace('-','').upper()
                layout = self.layout
                row = layout.column()
                row.label(text=activechar +' UI FINGERS', icon='HAND')
        except:
            self.report({'INFO'}, 'ngga ada di viewport')
                    
    def draw(self, context):        

#jari------------------------------------------
        layout = self.layout
        row = layout.row()
        row.alignment = 'CENTER'
        col =row.column()
        col.alignment = 'CENTER'
        col.scale_y = 1.0
        col.scale_x = 0.7
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 1.0
        sub.scale_x = 8.0
        sub.operator("ob.selectbonegroup", text='All Fingers.R',icon='TRIA_DOWN').group = 'f_all_R'
        
        row.split()
        col =row.column()
        col.alignment = 'CENTER'
        col.scale_y = 1.0
        col.scale_x = 0.7
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 1.0
        sub.scale_x = 8.0
        sub.operator("ob.selectbonegroup", text='All Fingers.L',icon='TRIA_DOWN').group = 'f_all_L'
        
#jari.R----------------------------------------
        layout = self.layout
        row = layout.row()
        row.alignment = 'CENTER'
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 1.85
        col.scale_x = 0.1
        sub = col.column()
        sub.scale_y = 1.0
        sub.scale_x = 1.0
        sub.operator("ob.selectbonegroup", 's', icon='MESH_GRID',emboss=False).group= 'f_R'
        col.operator("ob.selectbonegroup", '', icon='TRIA_RIGHT', emboss=False).group = 'f_1_R'
        col.operator("ob.selectbonegroup", '', icon='TRIA_RIGHT', emboss=False).group = 'f_2_R'
        col.operator("ob.selectbonegroup", '', icon='TRIA_RIGHT', emboss=False).group = 'f_3_R'
        col.operator("ob.selectbonegroup", '', icon='TRIA_RIGHT', emboss=False).group = 'f_s_R'
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_pinky_R'
        col.operator("ob.selectbone", '').bone = 'f_pinky.01.R'       
        col.operator("ob.selectbone", '').bone = 'f_pinky.02.R' 
        col.operator("ob.selectbone", '').bone = 'f_pinky.03.R'
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_pinky.R'
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_ring_R'
        col.operator("ob.selectbone", '').bone = 'f_ring.01.R'       
        col.operator("ob.selectbone", '').bone = 'f_ring.02.R' 
        col.operator("ob.selectbone", '').bone = 'f_ring.03.R'
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_ring.R'
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_middle_R'
        col.operator("ob.selectbone", '').bone = 'f_middle.01.R'       
        col.operator("ob.selectbone", '').bone = 'f_middle.02.R' 
        col.operator("ob.selectbone", '').bone = 'f_middle.03.R' 
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_middle.R'      
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_index_R'
        col.operator("ob.selectbone", '').bone = 'f_index.01.R'       
        col.operator("ob.selectbone", '').bone = 'f_index.02.R' 
        col.operator("ob.selectbone", '').bone = 'f_index.03.R'
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_index.R'
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 1.8
        col.scale_x = 1
        sub = col.column()
        sub.scale_y=0.3
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_thumb_R'
        col.operator("ob.selectbone", '').bone = 'thumb.01.R'       
        col.operator("ob.selectbone", '').bone = 'thumb.02.R' 
        col.operator("ob.selectbone", '').bone = 'thumb.03.R' 
        
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'thumb.R' 

        row.split()
        
#jari.L-----------------------------------
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 1.8
        col.scale_x = 1
        sub = col.column()
        sub.scale_y=0.3
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_thumb_L'
        col.operator("ob.selectbone", '').bone = 'thumb.01.L'       
        col.operator("ob.selectbone", '').bone = 'thumb.02.L' 
        col.operator("ob.selectbone", '').bone = 'thumb.03.L' 
        
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'thumb.L'         
        
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_index_L'
        col.operator("ob.selectbone", '').bone = 'f_index.01.L'       
        col.operator("ob.selectbone", '').bone = 'f_index.02.L' 
        col.operator("ob.selectbone", '').bone = 'f_index.03.L'
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_index.L'
        
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_middle_L'
        col.operator("ob.selectbone", '').bone = 'f_middle.01.L'       
        col.operator("ob.selectbone", '').bone = 'f_middle.02.L' 
        col.operator("ob.selectbone", '').bone = 'f_middle.03.L' 
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_middle.L'      
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_ring_L'
        col.operator("ob.selectbone", '').bone = 'f_ring.01.L'       
        col.operator("ob.selectbone", '').bone = 'f_ring.02.L' 
        col.operator("ob.selectbone", '').bone = 'f_ring.03.L'
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_ring.L'
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 2.5
        col.scale_x = 0.8
        sub = col.column()
        sub.scale_y=0.2
        sub.operator("ob.selectbonegroup", '', icon='TRIA_DOWN', emboss=False).group= 'f_pinky_L'
        col.operator("ob.selectbone", '').bone = 'f_pinky.01.L'       
        col.operator("ob.selectbone", '').bone = 'f_pinky.02.L' 
        col.operator("ob.selectbone", '').bone = 'f_pinky.03.L'
        sub = col.column()
        sub.alignment = 'CENTER'
        sub.scale_y = 0.8
        sub.scale_x = 0.6
        
        sub.operator("ob.selectbone", 'S').bone = 'f_pinky.L'
        
        col = row.column()
        col.alignment = 'CENTER'
        col.scale_y = 1.85
        col.scale_x = 0.1
        sub = col.column()
        sub.scale_y = 1.0
        sub.scale_x = 1.0
        
        sub.operator("ob.selectbonegroup", 's', icon='MESH_GRID',emboss=False).group= 'f_L'
        col.operator("ob.selectbonegroup", '', icon='TRIA_LEFT', emboss=False).group = 'f_1_L'
        col.operator("ob.selectbonegroup", '', icon='TRIA_LEFT', emboss=False).group = 'f_2_L'
        col.operator("ob.selectbonegroup", '', icon='TRIA_LEFT', emboss=False).group = 'f_3_L'
        col.operator("ob.selectbonegroup", '', icon='TRIA_LEFT', emboss=False).group = 'f_s_L'


 
#----------------------rigify generate-------------------------------------------------------------

##############################################################################################
##############################################################################################
##############################################################################################

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####




from mathutils import Matrix, Vector
from math import acos, pi

rig_id = 'septyan'

############################
## Math utility functions ##
############################

def perpendicular_vector(v):
    """ Returns a vector that is perpendicular to the one given.
        The returned vector is _not_ guaranteed to be normalized.
    """
    # Create a vector that is not aligned with v.
    # It doesn't matter what vector.  Just any vector
    # that's guaranteed to not be pointing in the same
    # direction.
    if abs(v[0]) < abs(v[1]):
        tv = Vector((1,0,0))
    else:
        tv = Vector((0,1,0))

    # Use cross prouct to generate a vector perpendicular to
    # both tv and (more importantly) v.
    return v.cross(tv)


def rotation_difference(mat1, mat2):
    """ Returns the shortest-path rotational difference between two
        matrices.
    """
    q1 = mat1.to_quaternion()
    q2 = mat2.to_quaternion()
    angle = acos(min(1,max(-1,q1.dot(q2)))) * 2
    if angle > pi:
        angle = -angle + (2*pi)
    return angle


#########################################
## "Visual Transform" helper functions ##
#########################################

def get_pose_matrix_in_other_space(mat, pose_bone):
    """ Returns the transform matrix relative to pose_bone's current
        transform space.  In other words, presuming that mat is in
        armature space, slapping the returned matrix onto pose_bone
        should give it the armature-space transforms of mat.
        TODO: try to handle cases with axis-scaled parents better.
    """
    rest = pose_bone.bone.matrix_local.copy()
    rest_inv = rest.inverted()
    if pose_bone.parent:
        par_mat = pose_bone.parent.matrix.copy()
        par_inv = par_mat.inverted()
        par_rest = pose_bone.parent.bone.matrix_local.copy()
    else:
        par_mat = Matrix()
        par_inv = Matrix()
        par_rest = Matrix()

    # Get matrix in bone's current transform space
    smat = rest_inv * (par_rest * (par_inv * mat))

    # Compensate for non-local location
    #if not pose_bone.bone.use_local_location:
    #    loc = smat.to_translation() * (par_rest.inverted() * rest).to_quaternion()
    #    smat.translation = loc

    return smat


def get_local_pose_matrix(pose_bone):
    """ Returns the local transform matrix of the given pose bone.
    """
    return get_pose_matrix_in_other_space(pose_bone.matrix, pose_bone)


def set_pose_translation(pose_bone, mat):
    """ Sets the pose bone's translation to the same translation as the given matrix.
        Matrix should be given in bone's local space.
    """
    if pose_bone.bone.use_local_location == True:
        pose_bone.location = mat.to_translation()
    else:
        loc = mat.to_translation()

        rest = pose_bone.bone.matrix_local.copy()
        if pose_bone.bone.parent:
            par_rest = pose_bone.bone.parent.matrix_local.copy()
        else:
            par_rest = Matrix()

        q = (par_rest.inverted() * rest).to_quaternion()
        pose_bone.location = q * loc


def set_pose_rotation(pose_bone, mat):
    """ Sets the pose bone's rotation to the same rotation as the given matrix.
        Matrix should be given in bone's local space.
    """
    q = mat.to_quaternion()

    if pose_bone.rotation_mode == 'QUATERNION':
        pose_bone.rotation_quaternion = q
    elif pose_bone.rotation_mode == 'AXIS_ANGLE':
        pose_bone.rotation_axis_angle[0] = q.angle
        pose_bone.rotation_axis_angle[1] = q.axis[0]
        pose_bone.rotation_axis_angle[2] = q.axis[1]
        pose_bone.rotation_axis_angle[3] = q.axis[2]
    else:
        pose_bone.rotation_euler = q.to_euler(pose_bone.rotation_mode)


def set_pose_scale(pose_bone, mat):
    """ Sets the pose bone's scale to the same scale as the given matrix.
        Matrix should be given in bone's local space.
    """
    pose_bone.scale = mat.to_scale()


def match_pose_translation(pose_bone, target_bone):
    """ Matches pose_bone's visual translation to target_bone's visual
        translation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_translation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_rotation(pose_bone, target_bone):
    """ Matches pose_bone's visual rotation to target_bone's visual
        rotation.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_rotation(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def match_pose_scale(pose_bone, target_bone):
    """ Matches pose_bone's visual scale to target_bone's visual
        scale.
        This function assumes you are in pose mode on the relevant armature.
    """
    mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
    set_pose_scale(pose_bone, mat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


##############################
## IK/FK snapping functions ##
##############################

def match_pole_target(ik_first, ik_last, pole, match_bone, length):
    """ Places an IK chain's pole target to match ik_first's
        transforms to match_bone.  All bones should be given as pose bones.
        You need to be in pose mode on the relevant armature object.
        ik_first: first bone in the IK chain
        ik_last:  last bone in the IK chain
        pole:  pole target bone for the IK chain
        match_bone:  bone to match ik_first to (probably first bone in a matching FK chain)
        length:  distance pole target should be placed from the chain center
    """
    a = ik_first.matrix.to_translation()
    b = ik_last.matrix.to_translation() + ik_last.vector

    # Vector from the head of ik_first to the
    # tip of ik_last
    ikv = b - a

    # Get a vector perpendicular to ikv
    pv = perpendicular_vector(ikv).normalized() * length

    def set_pole(pvi):
        """ Set pole target's position based on a vector
            from the arm center line.
        """
        # Translate pvi into armature space
        ploc = a + (ikv/2) + pvi

        # Set pole target to location
        mat = get_pose_matrix_in_other_space(Matrix.Translation(ploc), pole)
        set_pose_translation(pole, mat)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='POSE')

    set_pole(pv)

    # Get the rotation difference between ik_first and match_bone
    angle = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Try compensating for the rotation difference in both directions
    pv1 = Matrix.Rotation(angle, 4, ikv) * pv
    set_pole(pv1)
    ang1 = rotation_difference(ik_first.matrix, match_bone.matrix)

    pv2 = Matrix.Rotation(-angle, 4, ikv) * pv
    set_pole(pv2)
    ang2 = rotation_difference(ik_first.matrix, match_bone.matrix)

    # Do the one with the smaller angle
    if ang1 < ang2:
        set_pole(pv1)


def fk2ik_arm(obj, fk, ik):
    """ Matches the fk bones in an arm rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]

    # Stretch
    if handi['auto_stretch'] == 0.0:
        uarm['stretch_length'] = handi['stretch_length']
    else:
        diff = (uarmi.vector.length + farmi.vector.length) / (uarm.vector.length + farm.vector.length)
        uarm['stretch_length'] *= diff

    # Upper arm position
    match_pose_rotation(uarm, uarmi)
    match_pose_scale(uarm, uarmi)

    # Forearm position
    match_pose_rotation(farm, farmi)
    match_pose_scale(farm, farmi)

    # Hand position
    match_pose_rotation(hand, handi)
    match_pose_scale(hand, handi)


def ik2fk_arm(obj, fk, ik):
    """ Matches the ik bones in an arm rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    uarm  = obj.pose.bones[fk[0]]
    farm  = obj.pose.bones[fk[1]]
    hand  = obj.pose.bones[fk[2]]
    uarmi = obj.pose.bones[ik[0]]
    farmi = obj.pose.bones[ik[1]]
    handi = obj.pose.bones[ik[2]]
    pole  = obj.pose.bones[ik[3]]

    # Stretch
    handi['stretch_length'] = uarm['stretch_length']

    # Hand position
    match_pose_translation(handi, hand)
    match_pose_rotation(handi, hand)
    match_pose_scale(handi, hand)

    # Pole target position
    match_pole_target(uarmi, farmi, pole, uarm, (uarmi.length + farmi.length))


def fk2ik_leg(obj, fk, ik):
    """ Matches the fk bones in a leg rig to the ik bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh  = obj.pose.bones[fk[0]]
    shin   = obj.pose.bones[fk[1]]
    foot   = obj.pose.bones[fk[2]]
    mfoot  = obj.pose.bones[fk[3]]
    thighi = obj.pose.bones[ik[0]]
    shini  = obj.pose.bones[ik[1]]
    footi  = obj.pose.bones[ik[2]]
    mfooti = obj.pose.bones[ik[3]]

    # Stretch
    if footi['auto_stretch'] == 0.0:
        thigh['stretch_length'] = footi['stretch_length']
    else:
        diff = (thighi.vector.length + shini.vector.length) / (thigh.vector.length + shin.vector.length)
        thigh['stretch_length'] *= diff

    # Thigh position
    match_pose_rotation(thigh, thighi)
    match_pose_scale(thigh, thighi)

    # Shin position
    match_pose_rotation(shin, shini)
    match_pose_scale(shin, shini)

    # Foot position
    mat = mfoot.bone.matrix_local.inverted() * foot.bone.matrix_local
    footmat = get_pose_matrix_in_other_space(mfooti.matrix, foot) * mat
    set_pose_rotation(foot, footmat)
    set_pose_scale(foot, footmat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')


def ik2fk_leg(obj, fk, ik):
    """ Matches the ik bones in a leg rig to the fk bones.
        obj: armature object
        fk:  list of fk bone names
        ik:  list of ik bone names
    """
    thigh    = obj.pose.bones[fk[0]]
    shin     = obj.pose.bones[fk[1]]
    mfoot    = obj.pose.bones[fk[2]]
    thighi   = obj.pose.bones[ik[0]]
    shini    = obj.pose.bones[ik[1]]
    footi    = obj.pose.bones[ik[2]]
    footroll = obj.pose.bones[ik[3]]
    pole     = obj.pose.bones[ik[4]]
    mfooti   = obj.pose.bones[ik[5]]

    # Stretch
    footi['stretch_length'] = thigh['stretch_length']

    # Clear footroll
    set_pose_rotation(footroll, Matrix())

    # Foot position
    mat = mfooti.bone.matrix_local.inverted() * footi.bone.matrix_local
    footmat = get_pose_matrix_in_other_space(mfoot.matrix, footi) * mat
    set_pose_translation(footi, footmat)
    set_pose_rotation(footi, footmat)
    set_pose_scale(footi, footmat)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='POSE')

    # Pole target position
    match_pole_target(thighi, shini, pole, thigh, (thighi.length + shini.length))


##############################
## IK/FK snapping operators ##
##############################

class Rigify_Arm_FK2IK(bpy.types.Operator):
    """ Snaps an FK arm to an IK arm.
    """
    bl_idname = "pose.rigify_arm_fk2ik_" + rig_id
    bl_label = "Rigify Snap FK arm to IK"
    bl_options = {'UNDO'}

    uarm_fk = bpy.props.StringProperty(name="Upper Arm FK Name")
    farm_fk = bpy.props.StringProperty(name="Forerm FK Name")
    hand_fk = bpy.props.StringProperty(name="Hand FK Name")

    uarm_ik = bpy.props.StringProperty(name="Upper Arm IK Name")
    farm_ik = bpy.props.StringProperty(name="Forearm IK Name")
    hand_ik = bpy.props.StringProperty(name="Hand IK Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            fk2ik_arm(context.active_object, fk=[self.uarm_fk, self.farm_fk, self.hand_fk], ik=[self.uarm_ik, self.farm_ik, self.hand_ik])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Arm_IK2FK(bpy.types.Operator):
    """ Snaps an IK arm to an FK arm.
    """
    bl_idname = "pose.rigify_arm_ik2fk_" + rig_id
    bl_label = "Rigify Snap IK arm to FK"
    bl_options = {'UNDO'}

    uarm_fk = bpy.props.StringProperty(name="Upper Arm FK Name")
    farm_fk = bpy.props.StringProperty(name="Forerm FK Name")
    hand_fk = bpy.props.StringProperty(name="Hand FK Name")

    uarm_ik = bpy.props.StringProperty(name="Upper Arm IK Name")
    farm_ik = bpy.props.StringProperty(name="Forearm IK Name")
    hand_ik = bpy.props.StringProperty(name="Hand IK Name")
    pole    = bpy.props.StringProperty(name="Pole IK Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            ik2fk_arm(context.active_object, fk=[self.uarm_fk, self.farm_fk, self.hand_fk], ik=[self.uarm_ik, self.farm_ik, self.hand_ik, self.pole])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Leg_FK2IK(bpy.types.Operator):
    """ Snaps an FK leg to an IK leg.
    """
    bl_idname = "pose.rigify_leg_fk2ik_" + rig_id
    bl_label = "Rigify Snap FK leg to IK"
    bl_options = {'UNDO'}

    thigh_fk = bpy.props.StringProperty(name="Thigh FK Name")
    shin_fk  = bpy.props.StringProperty(name="Shin FK Name")
    foot_fk  = bpy.props.StringProperty(name="Foot FK Name")
    mfoot_fk = bpy.props.StringProperty(name="MFoot FK Name")

    thigh_ik = bpy.props.StringProperty(name="Thigh IK Name")
    shin_ik  = bpy.props.StringProperty(name="Shin IK Name")
    foot_ik  = bpy.props.StringProperty(name="Foot IK Name")
    mfoot_ik = bpy.props.StringProperty(name="MFoot IK Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            fk2ik_leg(context.active_object, fk=[self.thigh_fk, self.shin_fk, self.foot_fk, self.mfoot_fk], ik=[self.thigh_ik, self.shin_ik, self.foot_ik, self.mfoot_ik])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}


class Rigify_Leg_IK2FK(bpy.types.Operator):
    """ Snaps an IK leg to an FK leg.
    """
    bl_idname = "pose.rigify_leg_ik2fk_" + rig_id
    bl_label = "Rigify Snap IK leg to FK"
    bl_options = {'UNDO'}

    thigh_fk = bpy.props.StringProperty(name="Thigh FK Name")
    shin_fk  = bpy.props.StringProperty(name="Shin FK Name")
    mfoot_fk = bpy.props.StringProperty(name="MFoot FK Name")

    thigh_ik = bpy.props.StringProperty(name="Thigh IK Name")
    shin_ik  = bpy.props.StringProperty(name="Shin IK Name")
    foot_ik  = bpy.props.StringProperty(name="Foot IK Name")
    footroll = bpy.props.StringProperty(name="Foot Roll Name")
    pole     = bpy.props.StringProperty(name="Pole IK Name")
    mfoot_ik = bpy.props.StringProperty(name="MFoot IK Name")

    @classmethod
    def poll(cls, context):
        return (context.active_object != None and context.mode == 'POSE')

    def execute(self, context):
        use_global_undo = context.user_preferences.edit.use_global_undo
        context.user_preferences.edit.use_global_undo = False
        try:
            ik2fk_leg(context.active_object, fk=[self.thigh_fk, self.shin_fk, self.mfoot_fk], ik=[self.thigh_ik, self.shin_ik, self.foot_ik, self.footroll, self.pole, self.mfoot_ik])
        finally:
            context.user_preferences.edit.use_global_undo = use_global_undo
        return {'FINISHED'}




class RigLayers(wildpanel, Panel):
    bl_label = "Rig Layers"
    bl_idname = rig_id + "_PT_rig_layers"
    
    @classmethod
    def poll(self, context):
        try:
            return (context.active_object != None)  and bpy.context.scene.tab =="layer"
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row = col.row(align=1)
        
        row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='head')
        
        row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Facial')
        row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Torso')
        row.separator()
        
        row.prop(context.active_object.data, 'layers', index=4, toggle=True, text='Fingers')
        row.prop(context.active_object.data, 'layers', index=5, toggle=True, text='(Tweak)')
                
        row = col.row(align=1)
        row.label('Arm FK')
               
        row.prop(context.active_object.data, 'layers', index=6, toggle=True, text='L')
        
        row.prop(context.active_object.data, 'layers', index=9, toggle=True, text='R')
        row.label('Arm IK')
        row.prop(context.active_object.data, 'layers', index=7, toggle=True, text='L')
        row.prop(context.active_object.data, 'layers', index=10, toggle=True, text='R')
        
        row = col.row(align=1)
        row.label('Leg FK')
        row.prop(context.active_object.data, 'layers', index=12, toggle=True, text='L')
        row.prop(context.active_object.data, 'layers', index=15, toggle=True, text='R')
        row.label('Leg IK')
        row.prop(context.active_object.data, 'layers', index=13, toggle=True, text='L')
        row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='R')
        

        row = col.row(align=1)
        row.label('Tweak Arm')
        row.prop(context.active_object.data, 'layers', index=8, toggle=True, text='L')
        row.prop(context.active_object.data, 'layers', index=11, toggle=True, text='R')
        row.label('Tweak Leg')
        row.prop(context.active_object.data, 'layers', index=14, toggle=True, text='L')
        row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='R')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=28, toggle=True, text='Root')


###################
## Rig UI Panels ##
###################

class RigUI(wildpanel, Panel):
    bl_label = "Rig Main Properties"
    bl_idname = rig_id + "_PT_rig_ui"
    
    
    @classmethod
    def poll(self, context):
        if context.mode != 'POSE':
            return False
        try:
            return (context.active_object != None)  and bpy.context.scene.tab == "layer"
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout
        pose_bones = context.active_object.pose.bones
        try:
            selected_bones = [bone.name for bone in context.selected_pose_bones]
            selected_bones += [context.active_pose_bone.name]
        except (AttributeError, TypeError):
            pass

        def is_selected(names):
            # Returns whether any of the named bones are selected.
            if type(names) == list:
                for name in names:
                    if name in selected_bones:
                        return True
            elif names in selected_bones:
                return True
            return False


        
        try:
            
            fk_leg_L = ["thigh.fk.L", "shin.fk.L", "foot.fk.L", "MCH-foot.L"]
            ik_leg_L = ["MCH-thigh.ik.L", "MCH-shin.ik.L", "foot.ik.L", "knee_target.ik.L", "foot_roll.ik.L", "MCH-foot.L.001"]
            fk_leg_R = ["thigh.fk.R", "shin.fk.R", "foot.fk.R", "MCH-foot.R"]
            ik_leg_R = ["MCH-thigh.ik.R", "MCH-shin.ik.R", "foot.ik.R", "knee_target.ik.R", "foot_roll.ik.R", "MCH-foot.R.001"]
            
            fk_arm_L = ["upper_arm.fk.L", "forearm.fk.L", "hand.fk.L"]
            ik_arm_L = ["MCH-upper_arm.ik.L", "MCH-forearm.ik.L", "hand.ik.L", "elbow_target.ik.L", "CTRL_Shoulder L"]
            
            fk_arm_R = ["upper_arm.fk.R", "forearm.fk.R", "hand.fk.R"]
            ik_arm_R = ["MCH-upper_arm.ik.R", "MCH-forearm.ik.R", "hand.ik.R", "elbow_target.ik.R", "CTRL_Shoulder R"]
            
            switch = ['foot.ik.L','foot.ik.R','hand.ik.L','hand.ik.R']
            row = layout.row(align=0)
            row.label('ARM LEFT----')
            row.split()
            
            row.label('----ARM RIGHT')
            row = layout.row(align=0)
            row.prop(pose_bones[switch[2]], '["ikfk_switch"]', text="FK / IK Arm.L", slider=True)
            row.prop(pose_bones[switch[3]], '["ikfk_switch"]', text="FK / IK Arm.R", slider=True)
    #arm--------------------    
            try:    
                row =layout.row()
                row.prop(pose_bones[ik_arm_L[4]], '["ik_fk"]', text="FK / IK (bahu.L)", slider=True)
                row.prop(pose_bones[ik_arm_R[4]], '["ik_fk"]', text="FK / IK (bahu.R)", slider=True)
            except:
                pass
            
            #if is_selected(fk_arm_L+ik_arm_L):
            row =layout.row()
            props = row.operator("pose.rigify_arm_fk2ik_" + rig_id, text="FK->IK", icon='SNAP_ON')
            props.uarm_fk = fk_arm_L[0]
            props.farm_fk = fk_arm_L[1]
            props.hand_fk = fk_arm_L[2]
            props.uarm_ik = ik_arm_L[0]
            props.farm_ik = ik_arm_L[1]
            props.hand_ik = ik_arm_L[2]
            props = row.operator("pose.rigify_arm_ik2fk_" + rig_id, text="IK->FK", icon='SNAP_ON')
            props.uarm_fk = fk_arm_L[0]
            props.farm_fk = fk_arm_L[1]
            props.hand_fk = fk_arm_L[2]
            props.uarm_ik = ik_arm_L[0]
            props.farm_ik = ik_arm_L[1]
            props.hand_ik = ik_arm_L[2]
            props.pole = ik_arm_L[3]
           
            #if is_selected(fk_arm_R+ik_arm_R):
            
           
            props = row.operator("pose.rigify_arm_fk2ik_" + rig_id, text="FK->IK", icon='SNAP_ON')
            props.uarm_fk = fk_arm_R[0]
            props.farm_fk = fk_arm_R[1]
            props.hand_fk = fk_arm_R[2]
            props.uarm_ik = ik_arm_R[0]
            props.farm_ik = ik_arm_R[1]
            props.hand_ik = ik_arm_R[2]
            props = row.operator("pose.rigify_arm_ik2fk_" + rig_id, text="IK->FK", icon='SNAP_ON')
            props.uarm_fk = fk_arm_R[0]
            props.farm_fk = fk_arm_R[1]
            props.hand_fk = fk_arm_R[2]
            props.uarm_ik = ik_arm_R[0]
            props.farm_ik = ik_arm_R[1]
            props.hand_ik = ik_arm_R[2]
            props.pole = ik_arm_R[3]
                    
    #foot------------------------------------------------------------------------        
            row = layout.row(align=0)
            row.label('FOOT LEFT---')
            row.split()
            
            row.label('---FOOT RIGHT')
            
            row = layout.row(align=0)
            row.prop(pose_bones[switch[0]], '["ikfk_switch"]', text="FK / IK foot.L", slider=True)
            row.prop(pose_bones[switch[1]], '["ikfk_switch"]', text="FK / IK foot.R", slider=True)

            
            #if is_selected(fk_leg_L+ik_leg):
            row = layout.row()
            p = row.operator("pose.rigify_leg_fk2ik_" + rig_id, text="FK->IK", icon='SNAP_ON')
            p.thigh_fk = fk_leg_L[0]
            p.shin_fk  = fk_leg_L[1]
            p.foot_fk  = fk_leg_L[2]
            p.mfoot_fk = fk_leg_L[3]
            p.thigh_ik = ik_leg_L[0]
            p.shin_ik  = ik_leg_L[1]
            p.foot_ik = ik_leg_L[2]
            p.mfoot_ik = ik_leg_L[5]
            p = row.operator("pose.rigify_leg_ik2fk_" + rig_id, text="IK->FK", icon='SNAP_ON')
            p.thigh_fk  = fk_leg_L[0]
            p.shin_fk   = fk_leg_L[1]
            p.mfoot_fk  = fk_leg_L[3]
            p.thigh_ik  = ik_leg_L[0]
            p.shin_ik   = ik_leg_L[1]
            p.foot_ik   = ik_leg_L[2]
            p.pole      = ik_leg_L[3]
            p.footroll  = ik_leg_L[4]
            p.mfoot_ik  = ik_leg_L[5]
            
            
            #if is_selected(fk_leg_R+ik_leg_R):
                
            p = row.operator("pose.rigify_leg_fk2ik_" + rig_id, text="FK->IK", icon='SNAP_ON')
            p.thigh_fk = fk_leg_R[0]
            p.shin_fk  = fk_leg_R[1]
            p.foot_fk  = fk_leg_R[2]
            p.mfoot_fk = fk_leg_R[3]
            p.thigh_ik = ik_leg_R[0]
            p.shin_ik  = ik_leg_R[1]
            p.foot_ik = ik_leg_R[2]
            p.mfoot_ik = ik_leg_R[5]
            p = row.operator("pose.rigify_leg_ik2fk_" + rig_id, text="IK->FK", icon='SNAP_ON')
            p.thigh_fk  = fk_leg_R[0]
            p.shin_fk   = fk_leg_R[1]
            p.mfoot_fk  = fk_leg_R[3]
            p.thigh_ik  = ik_leg_R[0]
            p.shin_ik   = ik_leg_R[1]
            p.foot_ik   = ik_leg_R[2]
            p.pole      = ik_leg_R[3]
            p.footroll  = ik_leg_R[4]
            p.mfoot_ik  = ik_leg_R[5]
            
            layout.separator()
            layout.label('')
    #-----------------------------------------------------------------------------------------------       
            if is_selected(fk_leg_L):
                try:
                    pose_bones[fk_leg_L[0]]["isolate"]
                    layout.prop(pose_bones[fk_leg_L[0]], '["isolate"]', text="Isolate Rotation (" + fk_leg_L[0] + ")", slider=True)
                except KeyError:
                    pass
                layout.prop(pose_bones[fk_leg_L[0]], '["stretch_length"]', text="Length FK (" + fk_leg_L[0] + ")", slider=True)
            if is_selected(ik_leg_L):
                layout.prop(pose_bones[ik_leg_L[2]], '["stretch_length"]', text="Length IK (" + ik_leg_L[2] + ")", slider=True)
                layout.prop(pose_bones[ik_leg_L[2]], '["auto_stretch"]', text="Auto-Stretch IK (" + ik_leg_L[2] + ")", slider=True)
            if is_selected([ik_leg_L[3]]):
                layout.prop(pose_bones[ik_leg_L[3]], '["follow"]', text="Follow Foot (" + ik_leg_L[3] + ")", slider=True)
            
            hose_leg = ["thigh_hose_end.L", "thigh_hose.L", "knee_hose.L", "shin_hose.L", "shin_hose_end.L"]
            if is_selected(hose_leg):
                layout.prop(pose_bones[hose_leg[2]], '["smooth_bend"]', text="Smooth Knee (" + hose_leg[2] + ")", slider=True)
          
            
            if is_selected(fk_leg_R):
                try:
                    pose_bones[fk_leg_R[0]]["isolate"]
                    layout.prop(pose_bones[fk_leg_R[0]], '["isolate"]', text="Isolate Rotation (" + fk_leg_R[0] + ")", slider=True)
                except KeyError:
                    pass
                layout.prop(pose_bones[fk_leg_R[0]], '["stretch_length"]', text="Length FK (" + fk_leg_R[0] + ")", slider=True)
            if is_selected(ik_leg_R):
                layout.prop(pose_bones[ik_leg_R[2]], '["stretch_length"]', text="Length IK (" + ik_leg_R[2] + ")", slider=True)
                layout.prop(pose_bones[ik_leg_R[2]], '["auto_stretch"]', text="Auto-Stretch IK (" + ik_leg_R[2] + ")", slider=True)
            if is_selected([ik_leg_R[3]]):
                layout.prop(pose_bones[ik_leg_R[3]], '["follow"]', text="Follow Foot (" + ik_leg_R[3] + ")", slider=True)
            
            hose_leg = ["thigh_hose_end.R", "thigh_hose.R", "knee_hose.R", "shin_hose.R", "shin_hose_end.R"]
            if is_selected(hose_leg):
                layout.prop(pose_bones[hose_leg[2]], '["smooth_bend"]', text="Smooth Knee (" + hose_leg[2] + ")", slider=True)
            

            head_neck = ["head", "neck"]
            
            if is_selected(head_neck[0]):
                layout.prop(pose_bones[head_neck[0]], '["isolate"]', text="Isolate (" + head_neck[0] + ")", slider=True)
            
            if is_selected(head_neck):
                layout.prop(pose_bones[head_neck[0]], '["neck_follow"]', text="Neck Follow Head (" + head_neck[0] + ")", slider=True)
           
            
            if is_selected(fk_arm_L):
                try:
                    pose_bones[fk_arm_L[0]]["isolate"]
                    layout.prop(pose_bones[fk_arm_L[0]], '["isolate"]', text="Isolate Rotation (" + fk_arm_L[0] + ")", slider=True)
                except KeyError:
                    pass
                layout.prop(pose_bones[fk_arm_L[0]], '["stretch_length"]', text="Length FK (" + fk_arm_L[0] + ")", slider=True)
            if is_selected(ik_arm_L):
                layout.prop(pose_bones[ik_arm_L[2]], '["stretch_length"]', text="Length IK (" + ik_arm_L[2] + ")", slider=True)
                layout.prop(pose_bones[ik_arm_L[2]], '["auto_stretch"]', text="Auto-Stretch IK (" + ik_arm_L[2] + ")", slider=True)
            if is_selected([ik_arm_L[3]]):
                layout.prop(pose_bones[ik_arm_L[3]], '["follow"]', text="Follow Parent (" + ik_arm_L[3] + ")", slider=True)
            
            hose_arm = ["upper_arm_hose_end.L", "upper_arm_hose.L", "elbow_hose.L", "forearm_hose.L", "forearm_hose_end.L"]
            if is_selected(hose_arm):
                layout.prop(pose_bones[hose_arm[2]], '["smooth_bend"]', text="Smooth Elbow (" + hose_arm[2] + ")", slider=True)
            
            if is_selected(fk_arm_L+ik_arm_L):
                layout.separator()
            

            if is_selected(fk_arm_R):
                try:
                    pose_bones[fk_arm_R[0]]["isolate"]
                    layout.prop(pose_bones[fk_arm_R[0]], '["isolate"]', text="Isolate Rotation (" + fk_arm_R[0] + ")", slider=True)
                except KeyError:
                    pass
                layout.prop(pose_bones[fk_arm_R[0]], '["stretch_length"]', text="Length FK (" + fk_arm_R[0] + ")", slider=True)
            if is_selected(ik_arm_R):
                layout.prop(pose_bones[ik_arm_R[2]], '["stretch_length"]', text="Length IK (" + ik_arm_R[2] + ")", slider=True)
                layout.prop(pose_bones[ik_arm_R[2]], '["auto_stretch"]', text="Auto-Stretch IK (" + ik_arm_R[2] + ")", slider=True)
            if is_selected([ik_arm_R[3]]):
                layout.prop(pose_bones[ik_arm_R[3]], '["follow"]', text="Follow Parent (" + ik_arm_R[3] + ")", slider=True)
            
            hose_arm = ["upper_arm_hose_end.R", "upper_arm_hose.R", "elbow_hose.R", "forearm_hose.R", "forearm_hose_end.R"]
            if is_selected(hose_arm):
                layout.prop(pose_bones[hose_arm[2]], '["smooth_bend"]', text="Smooth Elbow (" + hose_arm[2] + ")", slider=True)
            
            if is_selected(fk_arm_R+ik_arm_R):
                layout.separator()

        except:
            pass       
        

##############################################################################################
##############################################################################################
##############################################################################################


# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####



class tanganL(bpy.types.Operator):
    bl_idname = 'ob.grouplib'
    bl_label = 'group lib'
    bl_description = 'apply pose group'
    bl_options = {'REGISTER', 'UNDO'}
    
    pose_index = IntProperty()
    group = StringProperty()
    
        

    def execute(self, context):
       # all = [(bone.name) for bone in bpy.data.armatures[bpy.context.active_object.name.replace('_proxy','')].bones  ]
        
        arm_R = ['upper_arm.fk.R','forearm.fk.R','hand.fk.R','hand.ik.R','elbow_target.ik.R','elbow_hose.R','CTRL_Shoulder R','shoulder.R']
        arm_L = ['upper_arm.fk.L','forearm.fk.L','hand.fk.L','hand.ik.L','elbow_target.ik.L','elbow_hose.L','CTRL_Shoulder L','shoulder.L']
        leg_R  = ['thigh.fk.R','shin.fk.R','foot.fk.R', 'foot.ik.R','knee_target.ik.R','toe.R','foot_roll.ik.R','TOE ROT R','knee_hose.R']
        leg_L  = ['thigh.fk.L','shin.fk.L','foot.fk.L', 'foot.ik.L','knee_target.ik.L','toe.L','foot_roll.ik.L','TOE ROT L','knee_hose.L']
       
        
        body = ['torso','chest.001','hips','spine','chest']
        head = ['head','neck','CTRL-TOPI']
        
        p = 'f_pinky'
        r = 'f_ring'
        m = 'f_middle'
        i = 'f_index'
        t = 'thumb'
        
        f_pinky_R = [p +'.01.R',p +'.02.R',p+'.03.R']
        f_pinky_L = [p +'.01.L',p +'.02.L',p+'.03.L']
        f_ring_R = [r +'.01.R',r +'.02.R',r+'.03.R']
        f_ring_L = [r +'.01.L',r +'.02.L',r+'.03.L']
        f_middle_R = [m +'.01.R',m +'.02.R',m+'.03.R']
        f_middle_L = [m +'.01.L',m +'.02.L',m+'.03.L']
        f_index_R = [i +'.01.R',i +'.02.R',i+'.03.R']
        f_index_L = [i +'.01.L',i +'.02.L',i+'.03.L']
        f_thumb_R = [t +'.01.R',t +'.02.R',t+'.03.R']
        f_thumb_L = [t +'.01.L',t +'.02.L',t+'.03.L']
        
        palm_L = ['palm.01.L','palm.02.L','palm.03.L','palm.04.L','palm.L']
        palm_R = ['palm.01.R','palm.02.R','palm.03.R','palm.04.R','palm.R']      
          
        f_1_R = [p+'.01.R',r+'.01.R',m+'.01.R',i+'.01.R']
        f_2_R = [p+'.02.R',r+'.02.R',m+'.02.R',i+'.02.R']
        f_3_R = [p+'.03.R',r+'.03.R',m+'.03.R',i+'.03.R']
        f_s_R  = [p+'.R',r+'.R',m+'.R',i+'.R']

        f_1_L = [p+'.01.L',r+'.01.L',m+'.01.L',i+'.01.L']
        f_2_L = [p+'.02.L',r+'.02.L',m+'.02.L',i+'.02.L']
        f_3_L = [p+'.03.L',r+'.03.L',m+'.03.L',i+'.03.L']
        f_s_L  = [p+'.L',r+'.L',m+'.L',i+'.L']

        f_R = f_pinky_R+f_ring_R+f_middle_R+f_index_R+f_thumb_R
        f_L = f_pinky_L+f_ring_L+f_middle_L+f_index_L+f_thumb_L

        hand_R = f_R + f_s_R + f_thumb_R + ['thumb.R'] + palm_R + ['hand.R']
        hand_L = f_L + f_s_L + f_thumb_L + ['thumb.L'] + palm_L + ['hand.L']
        
        full_body = arm_R + arm_L + leg_R + leg_L +body + head + hand_R + hand_L
        #FACIAL----------------------------------------------------------------------------------------------
        
        eyes = ['CTRL-EYES','CTRL-EYES.L','CTRL-EYES.R']
        lid_R = ['CTRL_Lid Bot B R','CTRL_Lid Bot C R','CTRL_Lid Bot A R','CTRL_Lid Top B R','CTRL_Lid Top C R','CTRL_Lid Top A R','FCL_Kelopak Bawah R','FCL_Kelopak Atas R']
        lid_L = ['CTRL_Lid Top B L','CTRL_Lid Top A L','CTRL_Lid Top C L','CTRL_Lid Bot B L','CTRL_Lid Bot C L','CTRL_Lid Bot A L','FCL_Kelopak Atas L','FCL_Kelopak Bawah L']
        
        pupil = ['FCL_PUPIL.R','FCL_PUPIL.L']
        iris = ['FCL_IRIS.R','FCL_IRIS.L']
        
        ceyes = eyes + lid_R + lid_L + pupil + iris
        
        eyebrow_L = ['CTRL Alis 1 L','CTRL Alis 3 L','CTRL Alis 2 L','CTRL Alis 5 L','CTRL Alis 4 L','FCL_ALIS DALAM.L','FCL_ALIS_UJUNG.L']
        eyebrow_R = ['CTRL Alis 1 R','CTRL Alis 3 R','CTRL Alis 2 R','CTRL Alis 5 R','CTRL Alis 4 R','FCL_ALIS DALAM.R','FCL_ALIS_UJUNG.R']
        
        nose = ['CTRL Nose Center','CTRL-NOSE.L','CTRL-NOSE.R']
        
        cheek_L = ['CTRL_PIPI BOT L','CTRL-PIPI TOP L','FCL_PIPI.L']
        cheek_R = ['CTRL_PIPI BOT R','CTRL-PIPI TOP R','FCL_PIPI.R']
                
        tongue = ['CTRL-LIDAH_STRECH_3','CTRL-LIDAH_STRECH_2','CTRL-LIDAH_STRECH_1','CTRL-LIDAH_3.001','CTRL-LIDAH_2.001','CTRL-LIDAH_1.001']
        teeth = ['CTRL_JAW','CTRL-lower teeth','CTRL-upper teeth']
        lip = ['CTRL_LIP TOP M','CTRL_LIP.L','CTRL_LIP TOP.L','CTRL_LIP.R','CTRL_LIP TOP.R','CTRL_LIP BOT M','CTRL_LIP BOT.L','CTRL_LIP BOT.R','FCL_LIPS','CTRL_MARAH','FCL_SENYUM-SEDIH',]
        mouth = lip + teeth + tongue
        
        face = mouth + nose + ceyes + cheek_L + cheek_R + eyebrow_L + eyebrow_R 
        
        #LIP SYNC-------------------------------------------------------------------------------------------
        
        try:
            if self.group == 'all':
                bpy.ops.pose.select_all(action='SELECT')
                bpy.ops.poselib.apply_pose(pose_index=context.object.pose_library.pose_markers.active_index)
            else:
                bpy.ops.pose.select_all(action='DESELECT')
                for bone in eval(self.group):
                    bpy.ops.object.select_pattern(pattern=bone, extend=1)

                bpy.ops.poselib.apply_pose(pose_index=context.object.pose_library.pose_markers.active_index)
           
        except:
            self.report({'INFO'}, 'ngga ada')
        
        return {'FINISHED'}

class resetvokal(bpy.types.Operator):
    bl_label = 'reset vocal'
    bl_idname = 'pose.vokal_reset'
    bl_options = {'REGISTER','UNDO'}
    bl_description = 'reset semua vocal/facial'
    
    set = StringProperty()
    def execute(self, context):
        try:
            bone = bpy.data.objects[context.active_object.name].pose.bones
            vocal = ['AHK','CDEST','UW','OO','II','FV','LNR','MBP']
            facebone = ['CTRL-EYES','CTRL-EYES.L','CTRL-EYES.R','CTRL_JAW','CTRL-lower teeth','CTRL Nose Center','CTRL-LIDAH_STRECH_3',
                        'CTRL-LIDAH_STRECH_2','CTRL-LIDAH_STRECH_1','CTRL Alis 1 L','CTRL Alis 1 R','CTRL Alis 3 L','CTRL Alis 2 L',
                        'CTRL Alis 5 L','CTRL Alis 4 L','CTRL Alis 3 R','CTRL Alis 2 R','CTRL Alis 5 R','CTRL Alis 4 R','CTRL_PIPI BOT R',
                        'CTRL_PIPI BOT L','CTRL-upper teeth','CTRL_Lid Top B L','CTRL_Lid Top A L','CTRL_Lid Top C L','CTRL_Lid Bot B R',
                        'CTRL_Lid Bot C R','CTRL_Lid Bot A R','CTRL_Lid Bot B L','CTRL_Lid Bot C L','CTRL_Lid Bot A L','CTRL_Lid Top B R',
                        'CTRL_Lid Top C R','CTRL_Lid Top A R','CTRL_LIP TOP M','CTRL_LIP.L','CTRL-NOSE.L','CTRL-PIPI TOP L','CTRL_LIP TOP.L',
                        'CTRL_LIP.R','CTRL-NOSE.R','CTRL-PIPI TOP R','CTRL_LIP TOP.R','CTRL_LIP BOT M','CTRL_LIP BOT.L','CTRL_LIP BOT.R',]
                        
            facial = facebone + vocal + ['FCL_PUPIL.R','CTRL_MARAH','CTRL-LIDAH_3.001','CTRL-LIDAH_2.001','CTRL-LIDAH_1.001','FCL_PUPIL.L',
                        'FCL_ALIS DALAM.L','FCL_ALIS DALAM.R','FCL_ALIS_UJUNG.L','FCL_ALIS_UJUNG.R','FCL_PIPI.R','FCL_PIPI.L','FCL_LIPS',
                        'FCL_Kelopak Atas L','FCL_Kelopak Bawah R','FCL_Kelopak Bawah L','FCL_Kelopak Atas R','FCL_IRIS.R','FCL_IRIS.L','FCL_SENYUM-SEDIH',]
            
            if self.set == "vocal":
                for voc in vocal:
                    bone[voc].location[0] = 0
            else:
                bpy.ops.pose.select_all(action='DESELECT')
                for voc in facial:
                    bone[voc].bone.select = 1
                    
                bpy.ops.pose.loc_clear()
                bpy.ops.pose.rot_clear()
                bpy.ops.pose.scale_clear()
                    
        except:
            pass
           
        return {'FINISHED'}
    
class maxvokal(bpy.types.Operator):
    '''apply vocal max/min'''
    bl_label = '1'
    bl_idname = 'pose.vokal_max'
    bl_options = {'REGISTER','UNDO'}
    
    nama = StringProperty()
    set = StringProperty()
    
    def execute(self, context):
        bone = bpy.data.objects[bpy.context.active_object.name].pose.bones
        max_x = bone[self.nama].constraints[0].max_x
        max_vokal = max_x
        if self.set == 'max':
            bone[self.nama].location.x = max_vokal
        else:
            bone[self.nama].location.x = 0
        
        return {'FINISHED'}
        
class animPanel(wildpanel, Panel):
    
    bl_label = "anim_lib"
    bl_idname = "panel_animlib"
    
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and bpy.context.scene.tab == 'anim_lib'
    
    def draw(self, context):
        layout = self.layout
        row = layout.column()
        bone = bpy.data.objects[context.active_object.name].pose.bones
        scn = bpy.context.scene
        
        try:
            layout = self.layout
            
            scene = context.scene
                    
            ob = context.object
            poselib = ob.pose_library
            
            row = layout.row()
            row.prop(scn, 'tab_anim', expand=True)
            
            
            
            if scn.tab_anim == 'body':
                box = layout.box()
                row= box.column()
                lab = row.row()
                lab.alignment='CENTER'
                lab.label('------- APPLY POSE TO BODY PART -------')
                
                col = row.row(align=1)
                colh = col.row(align=1)
                
                colh.operator('ob.grouplib', 'head',icon='MOD_MASK').group = 'head'
                #row utama
                col = row.row(align=1)
                col.alignment = 'CENTER'
                cols = col.column(align=1)
                cols.operator('ob.grouplib', 'arm R').group = 'arm_R'
                cols.operator('ob.grouplib', 'fingers R').group = 'hand_R'
                
                
                cols = col.column()
                cols.scale_y=2
                cols.scale_x=1
                cols.operator('ob.grouplib', 'body', icon='MOD_CLOTH').group = 'body'
                
                cols = col.column(align=1)
                cols.operator('ob.grouplib', 'arm L').group = 'arm_L'
                cols.operator('ob.grouplib', 'fingers L').group = 'hand_L'
                
                
                col = row.row(align=1)
                
                col = row.row(align=1)
                
                col.operator('ob.grouplib', 'leg R').group = 'leg_R'
                
                col.operator('ob.grouplib', 'leg L').group = 'leg_L'
                
                col = row.row(align=1)
                col.operator('ob.grouplib', 'all body', icon='MESH_GRID').group = 'full_body'
            
            if scn.tab_anim == 'facial':
                #-------------------------------------facial brooooooooooooo------------------------------
                box = layout.box()
                row= box.column()
                lab = row.row()
                lab.alignment='CENTER'
                lab.label('------- APPLY POSE TO FACE PART -------')
                y =1.0
                col = row.column(align=1)
                col.scale_y = y
                row = col.row(align=1)
                row.scale_y = y
                row.operator('ob.grouplib', 'eyebrow R', icon='NOCURVE').group = 'eyebrow_R'
                row.operator('ob.grouplib', 'eyebrow L', icon='NOCURVE').group = 'eyebrow_L'
                
                row = col.row(align=1)
                row.scale_y = y
                row.operator('ob.grouplib', 'eye R', icon='RESTRICT_VIEW_OFF').group = 'lid_R'
                row.operator('ob.grouplib', '<--eyes-->').group = 'ceyes'
                row.operator('ob.grouplib', 'eye L',icon='RESTRICT_VIEW_OFF').group = 'lid_L'
                
                row = col.row(align=1)
                row.operator('ob.grouplib', 'cheek R',).group = 'cheek_R'
                row.operator('ob.grouplib', 'nose',icon='MESH_CONE').group = 'nose'
                row.operator('ob.grouplib', 'cheek L',).group = 'cheek_L'
                
                row = col.row(align=1)
                row.operator('ob.grouplib', 'mouth', icon='SPHERECURVE').group = 'mouth'
                
                row = col.row(align=1)
                row.scale_y = y
                row.operator('ob.grouplib', 'all face', icon='MESH_GRID').group = 'face'
                
            
            layout.template_ID(ob, "pose_library", new="poselib.new", unlink="poselib.unlink")  
            row=layout.column()
            
                                   
            if poselib:
                # list of poses in pose library
                row = layout.row()
                row.template_list("UI_UL_list", "pose_markers", poselib, "pose_markers",
                                  poselib.pose_markers, "active_index", rows=3)

                # column of operators for active pose
                # - goes beside list
                col = row.column(align=True)
                col.active = (poselib.library is None)

                # invoke should still be used for 'add', as it is needed to allow
                # add/replace options to be used properly
                col.operator("poselib.pose_add", icon='ZOOMIN', text="")

                col.operator_context = 'EXEC_DEFAULT'  # exec not invoke, so that menu doesn't need showing

                pose_marker_active = poselib.pose_markers.active

                if pose_marker_active is not None:
                    col.operator("poselib.pose_remove", icon='ZOOMOUT', text="")
                    col.operator("poselib.apply_pose", icon='ZOOM_SELECTED', text="").pose_index = poselib.pose_markers.active_index
                
                col.operator("poselib.action_sanitize", icon='HELP', text="")  # XXX: put in menu? 
            
        except:
            pass             
        

# kedip    
class mataKedip(bpy.types.Operator):
    ''' blink otomatis, untuk jarak frame tekan f6 setelah tombol di klik'''
    bl_idname = 'pose.autoblink'
    bl_label = 'Auto Blink'
    bl_options = {'UNDO', 'REGISTER'}
    
    
    melek_kedip = IntProperty(min=0, default= 2)
    kedip_tahan = IntProperty(min=0, default= 1)
    kedip_melek = IntProperty(min=0, default= 2)
    
    def execute(self, context):
        try:
            # select bone kelopak dan insert key awal
            bpy.ops.pose.select_all(action='DESELECT')
            bone = ["FCL_Kelopak Atas L","FCL_Kelopak Bawah R","FCL_Kelopak Bawah L","FCL_Kelopak Atas R",]
            for b in bone:
                bpy.ops.object.select_pattern(pattern=b, extend=1)
            
            bpy.ops.anim.keyframe_insert_menu(type='Location')
            
            # melek ----------> kedip
            bpy.context.scene.frame_current += self.melek_kedip
            
            #select bone kelopak dan kedip
            pose_bone = bpy.data.objects[bpy.context.active_object.name].pose.bones
            
            for b in bone:
                pose_bone[b].location[1] = pose_bone[b].constraints[0].min_y
            
            bpy.ops.anim.keyframe_insert_menu(type='Location') 
            
            # kedip ----------> kedip
            bpy.context.scene.frame_current += self.kedip_tahan
            
            bpy.ops.anim.keyframe_insert_menu(type='Location') 
            
            # kedip ----------> melek
            bpy.context.scene.frame_current += self.kedip_melek
            
            for b in bone:
                pose_bone[b].location[1] = 0
                
            bpy.ops.anim.keyframe_insert_menu(type='Location') 
        
        except:
            self.report({'ERROR'}, ' bone ( FCL_Kelopak Atas L , FCL_Kelopak Bawah R , FCL_Kelopak Bawah L , FCL_Kelopak Atas R ) ngga ada')    
        
            
        
        return {'FINISHED'}
    
            
class vocalPanel(wildpanel, Panel):
    
    bl_label = "Vocal"
    bl_idname = "panel_vocal"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and bpy.context.scene.tab == 'vocal'
    
    def draw(self, context):
        layout = self.layout
        col= layout.column()
        bone = bpy.data.objects[context.active_object.name].pose.bones
        scn = bpy.context.scene
        
        vokal = ['AHK','CDEST','UW','OO','II','FV','LNR','MBP']
        try:
                
            if scn.tab == 'vocal':
                row = col.row(align=1)
                row.operator('pose.vokal_reset','reset facial', icon='X').set = 'facial'
                row.operator('pose.vokal_reset', icon='X').set = 'vocal'
                
                col.separator()
                
                col= layout.column()
                for v in vokal:
                    text = v
                    if v =='OO' or v=='II' :
                        text = v[1:]
                    else:
                        text = v
                    
                    subrow=col.row(align=1)
                    subrow.prop(bone[v], 'location', index=0, text=text)
                    subrow.scale_x =2
                    m = subrow.operator('pose.vokal_max','', icon='FRAME_NEXT')
                    m.nama = v
                    m.set = 'max'
                    res = subrow.operator('pose.vokal_max','', icon='X')
                    res.nama = v
                    res.set = 'min'
        except:
             pass      
                                    
class addinsPanel(wildpanel, Panel):
    
    bl_label = "Additional Features"
    bl_idname = "panel_additional_features"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and bpy.context.scene.tab == 'vocal'
    
    def draw(self, context):
        layout = self.layout
        col= layout.column()
        
        row = col.row()
        row.operator("pose.autoblink",icon='ACTION')
        
                        
    
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    

if __name__ == "__main__":
    register()
