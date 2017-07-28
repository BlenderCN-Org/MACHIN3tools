import bpy
import os
from bpy.types import Menu
from bpy.props import IntProperty
import bmesh
from .. import M3utils as m3


# SNAPPING

class SnapActive(bpy.types.Operator):
    bl_idname = "snap.active"
    bl_label = "Snap Active"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.use_snap == (True):
            bpy.context.scene.tool_settings.use_snap = False

        elif bpy.context.scene.tool_settings.use_snap == (False):
            bpy.context.scene.tool_settings.use_snap = True

        return {'FINISHED'}


class SnapVolume(bpy.types.Operator):
    bl_idname = "snap.volume"
    bl_label = "Snap Volume"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'VOLUME'

        if bpy.context.scene.tool_settings.snap_element != 'VOLUME':
            bpy.context.scene.tool_settings.snap_element = 'VOLUME'
        return {'FINISHED'}


class SnapFace(bpy.types.Operator):
    bl_idname = "snap.face"
    bl_label = "Snap Face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'FACE'

        if bpy.context.scene.tool_settings.snap_element != 'FACE':
            bpy.context.scene.tool_settings.snap_element = 'FACE'
        return {'FINISHED'}


class SnapEdge(bpy.types.Operator):
    bl_idname = "snap.edge"
    bl_label = "Snap Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'EDGE'

        if bpy.context.scene.tool_settings.snap_element != 'EDGE':
            bpy.context.scene.tool_settings.snap_element = 'EDGE'
        return {'FINISHED'}


class SnapVertex(bpy.types.Operator):
    bl_idname = "snap.vertex"
    bl_label = "Snap Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'VERTEX'

        if bpy.context.scene.tool_settings.snap_element != 'VERTEX':
            bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        return {'FINISHED'}


class SnapIncrement(bpy.types.Operator):
    bl_idname = "snap.increment"
    bl_label = "Snap Increment"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'INCREMENT'

        if bpy.context.scene.tool_settings.snap_element != 'INCREMENT':
            bpy.context.scene.tool_settings.snap_element = 'INCREMENT'
        return {'FINISHED'}


class SnapAlignRotation(bpy.types.Operator):
    bl_idname = "snap.alignrotation"
    bl_label = "Snap Align rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.use_snap_align_rotation == (True):
            bpy.context.scene.tool_settings.use_snap_align_rotation = False

        elif bpy.context.scene.tool_settings.use_snap_align_rotation == (False):
            bpy.context.scene.tool_settings.use_snap_align_rotation = True

        return {'FINISHED'}


class SnapTargetVariable(bpy.types.Operator):
    bl_idname = "object.snaptargetvariable"
    bl_label = "Snap Target Variable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target=self.variable
        return {'FINISHED'}


# ORIENTATION

class OrientationVariable(bpy.types.Operator):
    bl_idname = "object.orientationvariable"
    bl_label = "Orientation Variable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.space_data.transform_orientation=self.variable
        return {'FINISHED'}


# OBJECT SHADING

class WireSelectedAll(bpy.types.Operator):
    bl_idname = "wire.selectedall"
    bl_label = "Wire Selected All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        for obj in bpy.data.objects:
            if bpy.context.selected_objects:
                if obj.select:
                    if obj.show_wire:
                        obj.show_all_edges = False
                        obj.show_wire = False
                    else:
                        obj.show_all_edges = True
                        obj.show_wire = True
            elif not bpy.context.selected_objects:
                if obj.show_wire:
                    obj.show_all_edges = False
                    obj.show_wire = False
                else:
                    obj.show_all_edges = True
                    obj.show_wire = True
        return {'FINISHED'}


class ToggleGridAxis(bpy.types.Operator):
    bl_idname = "scene.togglegridaxis"
    bl_label = "Toggle Grid and Axis in 3D view"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.show_axis_y = not bpy.context.space_data.show_axis_y
        bpy.context.space_data.show_axis_x = not bpy.context.space_data.show_axis_x
        bpy.context.space_data.show_floor = not bpy.context.space_data.show_floor
        return {'FINISHED'}


class MeshDisplayOverlays(bpy.types.Menu):
    bl_idname = "meshdisplay.overlays"
    bl_label = "Mesh Display Overlays"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout

        # with_freestyle = bpy.app.build_options.freestyle

        mesh = context.active_object.data
        # scene = context.scene

        split = layout.split()

        col = split.column()
        col.label(text="Overlays:")
        col.prop(mesh, "show_faces", text="Faces")
        col.prop(mesh, "show_edges", text="Edges")
        col.prop(mesh, "show_edge_crease", text="Creases")
        col.prop(mesh, "show_edge_seams", text="Seams")
        layout.prop(mesh, "show_weight")
        col.prop(mesh, "show_edge_sharp", text="Sharp")
        col.prop(mesh, "show_edge_bevel_weight", text="Bevel")
        col.prop(mesh, "show_freestyle_edge_marks", text="Edge Marks")
        col.prop(mesh, "show_freestyle_face_marks", text="Face Marks")


######################
#    Pivot Point     #
######################

class PivotPointVariable(bpy.types.Operator):
    bl_idname = "pivotpoint.variable"
    bl_label = "PivotPointVariable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.space_data.pivot_point = self.variable
        return {'FINISHED'}


class UsePivotAlign(bpy.types.Operator):
    bl_idname = "use.pivotalign"
    bl_label = "Use Pivot Align"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.space_data.use_pivot_point_align == (False):
            bpy.context.space_data.use_pivot_point_align = True
        elif bpy.context.space_data.use_pivot_point_align == (True):
            bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}

######################
#    Manipulators    #
######################
class ManipTranslate(bpy.types.Operator):
    bl_idname = "manip.translate"
    bl_label = "Manip Translate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE'}
        return {'FINISHED'}

class ManipRotate(bpy.types.Operator):
    bl_idname = "manip.rotate"
    bl_label = "Manip Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'ROTATE'}
        if bpy.context.space_data.transform_manipulators != {'ROTATE'}:
            bpy.context.space_data.transform_manipulators = {'ROTATE'}
        return {'FINISHED'}

class ManipScale(bpy.types.Operator):
    bl_idname = "manip.scale"
    bl_label = "Manip Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'SCALE'}
        return {'FINISHED'}

class TranslateRotate(bpy.types.Operator):
    bl_idname = "translate.rotate"
    bl_label = "Translate Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE', 'ROTATE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE'}
        return {'FINISHED'}

class TranslateScale(bpy.types.Operator):
    bl_idname = "translate.scale"
    bl_label = "Translate Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE', 'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'SCALE'}
        return {'FINISHED'}

class RotateScale(bpy.types.Operator):
    bl_idname = "rotate.scale"
    bl_label = "Rotate Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'ROTATE', 'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'ROTATE', 'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'ROTATE', 'SCALE'}
        return {'FINISHED'}

class TranslateRotateScale(bpy.types.Operator):
    bl_idname = "translate.rotatescale"
    bl_label = "Translate Rotate Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE', 'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE', 'ROTATE', 'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE', 'SCALE'}
        return {'FINISHED'}

class WManupulators(bpy.types.Operator):
    bl_idname = "w.manupulators"
    bl_label = "W Manupulators"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.space_data.show_manipulator == (True):
            bpy.context.space_data.show_manipulator = False

        elif bpy.context.space_data.show_manipulator == (False):
            bpy.context.space_data.show_manipulator = True

        return {'FINISHED'}

######################
#       Modes        #
######################

# Define Class Texture Paint
class ClassTexturePaint(bpy.types.Operator):
    bl_idname = "class.pietexturepaint"
    bl_label = "Class Texture Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.texture_paint_toggle()
        else:
            bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}

# Define Class Weight Paint
class ClassWeightPaint(bpy.types.Operator):
    bl_idname = "class.pieweightpaint"
    bl_label = "Class Weight Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.weight_paint_toggle()
        else:
            bpy.ops.paint.weight_paint_toggle()
        return {'FINISHED'}

# Define Class Vertex Paint
class ClassVertexPaint(bpy.types.Operator):
    bl_idname = "class.pievertexpaint"
    bl_label = "Class Vertex Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.vertex_paint_toggle()
        else:
            bpy.ops.paint.vertex_paint_toggle()
        return {'FINISHED'}

# Define Class Particle Edit
class ClassParticleEdit(bpy.types.Operator):
    bl_idname = "class.pieparticleedit"
    bl_label = "Class Particle Edit"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.particle.particle_edit_toggle()
        else:
            bpy.ops.particle.particle_edit_toggle()

        return {'FINISHED'}


class ClassObject(bpy.types.Operator):
    bl_idname = "class.object"
    bl_label = "Class Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")
            if bpy.context.scene.machin3.pieobjecteditmodeshow:
                m3.unhide_all("MESH")
                if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    m3.unselect_all("MESH")
        else:
            if bpy.context.scene.machin3.pieobjecteditmodehide:
                # TODO: why does this sometimes occur?
                # Traceback (most recent call last):
                  # File "/home/x/.config/blender/2.78/scripts/addons/MACHIN3tools/ui/pie.py", line 453, in execute
                    # m3.hide_all("MESH")
                  # File "/home/x/.config/blender/2.78/scripts/addons/MACHIN3tools/M3utils.py", line 54, in hide_all
                    # select_all(string)
                  # File "/home/x/.config/blender/2.78/scripts/addons/MACHIN3tools/M3utils.py", line 32, in select_all
                    # bpy.ops.mesh.select_all(action='SELECT')
                  # File "/opt/Blender 2.78c/2.78/scripts/modules/bpy/ops.py", line 189, in __call__
                    # ret = op_call(self.idname_py(), None, kw)
                # RuntimeError: Operator bpy.ops.mesh.select_all.poll() failed, context is incorrect
                try:
                    m3.hide_all("MESH")
                except:
                    pass
            bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}


class ClassVertex(bpy.types.Operator):
    bl_idname = "class.vertex"
    bl_label = "Class Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            if bpy.context.scene.machin3.pieobjecteditmodeshow:
                m3.unhide_all("MESH")
                if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    m3.unselect_all("MESH")
        if bpy.ops.mesh.select_mode != "EDGE, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        return {'FINISHED'}


class ClassEdge(bpy.types.Operator):
    bl_idname = "class.edge"
    bl_label = "Class Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            if bpy.context.scene.machin3.pieobjecteditmodeshow:
                m3.unhide_all("MESH")
                if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    m3.unselect_all("MESH")
        if bpy.ops.mesh.select_mode != "VERT, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        return {'FINISHED'}


class ClassFace(bpy.types.Operator):
    bl_idname = "class.face"
    bl_label = "Class Face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            if bpy.context.scene.machin3.pieobjecteditmodeshow:
                m3.unhide_all("MESH")
                if bpy.context.scene.machin3.pieobjecteditmodeshowunselect:
                    m3.unselect_all("MESH")
        if bpy.ops.mesh.select_mode != "VERT, EDGE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        return {'FINISHED'}

######################
#   Selection Mode   #
######################

# Components Selection Mode
class VertsEdges(bpy.types.Operator):
    bl_idname = "verts.edges"
    bl_label = "Verts Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (True, True, False)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (True, True, False)
            return {'FINISHED'}


class EdgesFaces(bpy.types.Operator):
    bl_idname = "edges.faces"
    bl_label = "EdgesFaces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (False, True, True)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (False, True, True)
            return {'FINISHED'}

class VertsFaces(bpy.types.Operator):
    bl_idname = "verts.faces"
    bl_label = "Verts Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (True, False, True)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (True, False, True)
            return {'FINISHED'}

class VertsEdgesFaces(bpy.types.Operator):
    bl_idname = "verts.edgesfaces"
    bl_label = "Verts Edges Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (True, True, True)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (True, True, True)
            return {'FINISHED'}

#Select All By Selection
class SelectAllBySelection(bpy.types.Operator):
    bl_idname = "object.selectallbyselection"
    bl_label = "Verts Edges Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')
        return {'FINISHED'}

######################
#       Views        #
######################

# Split area horizontal
class SplitHorizontal(bpy.types.Operator):
    bl_idname = "split.horizontal"
    bl_label = "split horizontal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        bpy.ops.screen.area_split(direction='HORIZONTAL')
        return {'FINISHED'}

# Split area vertical
class SplitVertical(bpy.types.Operator):
    bl_idname = "split.vertical"
    bl_label = "split vertical"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        bpy.ops.screen.area_split(direction='VERTICAL')
        return {'FINISHED'}


# Join area
class JoinArea(bpy.types.Operator):
    """Join 2 area, clic on the second area to join"""
    bl_idname = "area.joinarea"
    bl_label = "Join Area"
    bl_options = {'REGISTER', 'UNDO'}

    min_x = IntProperty()
    min_y = IntProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            self.max_x = event.mouse_x
            self.max_y = event.mouse_y
            bpy.ops.screen.area_join(min_x=self.min_x, min_y=self.min_y, max_x=self.max_x, max_y=self.max_y)
            bpy.ops.screen.screen_full_area()
            bpy.ops.screen.screen_full_area()
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.min_x = event.mouse_x
        self.min_y = event.mouse_y
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

#View Class menu
class ViewMenu(bpy.types.Operator):
    """Menu to change views"""
    bl_idname = "object.view_menu"
    bl_label = "View_Menu"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.area.type=self.variable
        return {'FINISHED'}

# MACHIN3
class LayoutSwitch(bpy.types.Operator):
    """Menu to switch screen layouts"""
    bl_idname = "machin3.layout_switch"
    bl_label = "Layout_Switch"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.window.screen=bpy.data.screens[self.variable]
        return {'FINISHED'}
# /MACHIN3


##############
#   Sculpt   #
##############

# Sculpt Polish
class SculptPolish(bpy.types.Operator):
    bl_idname = "sculpt.polish"
    bl_label = "Sculpt Polish"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        bpy.context.tool_settings.sculpt.brush=bpy.data.brushes['Polish']
        return {'FINISHED'}

# Sculpt Polish
class SculptSculptDraw(bpy.types.Operator):
    bl_idname = "sculpt.sculptraw"
    bl_label = "Sculpt SculptDraw"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        bpy.context.tool_settings.sculpt.brush=bpy.data.brushes['SculptDraw']
        return {'FINISHED'}

######################
#   Cursor/Origin    #
######################

#Pivot to selection
class PivotToSelection(bpy.types.Operator):
    bl_idname = "object.pivot2selection"
    bl_label = "Pivot To Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        saved_location = bpy.context.scene.cursor_location.copy()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor_location = saved_location
        return {'FINISHED'}

#Pivot to Bottom
class PivotBottom(bpy.types.Operator):
    bl_idname = "object.pivotobottom"
    bl_label = "Pivot To Bottom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        o=bpy.context.active_object
        init=0
        for x in o.data.vertices:
            if init==0:
                a=x.co.z
                init=1
            elif x.co.z<a:
                a=x.co.z

        for x in o.data.vertices:
            x.co.z-=a

        o.location.z+=a
        bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}

#####################
#   Simple Align    #
#####################
#Align X
class AlignX(bpy.types.Operator):
    bl_idname = "align.x"
    bl_label = "Align  X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}

#Align Y
class AlignY(bpy.types.Operator):
    bl_idname = "align.y"
    bl_label = "Align  Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}

#Align Z
class AlignZ(bpy.types.Operator):
    bl_idname = "align.z"
    bl_label = "Align  Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}

#####################
#    Align To 0     #
#####################

#Align to X - 0
class AlignToX0(bpy.types.Operator):
    bl_idname = "align.2x0"
    bl_label = "Align To X-0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[0] = 0
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

#Align to Z - 0
class AlignToY0(bpy.types.Operator):
    bl_idname = "align.2y0"
    bl_label = "Align To Y-0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[1] = 0
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

#Align to Z - 0
class AlignToZ0(bpy.types.Operator):
    bl_idname = "align.2z0"
    bl_label = "Align To Z-0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[2] = 0
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

#Align X Left
class AlignXLeft(bpy.types.Operator):
    bl_idname = "alignx.left"
    bl_label = "Align X Left"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 0
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align X Right
class AlignXRight(bpy.types.Operator):
    bl_idname = "alignx.right"
    bl_label = "Align X Right"

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 0
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Y Back
class AlignYBack(bpy.types.Operator):
    bl_idname = "aligny.back"
    bl_label = "Align Y back"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 1
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Y Front
class AlignYFront(bpy.types.Operator):
    bl_idname = "aligny.front"
    bl_label = "Align Y Front"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 1
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Z Top
class AlignZTop(bpy.types.Operator):
    bl_idname = "alignz.top"
    bl_label = "Align Z Top"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 2
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Z Bottom
class AlignZBottom(bpy.types.Operator):
    bl_idname = "alignz.bottom"
    bl_label = "Align Z Bottom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 2
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#################
#    Delete     #
#################

#Limited Dissolve
class DeleteLimitedDissolve(bpy.types.Operator):
    bl_idname = "delete.limiteddissolve"
    bl_label = "Delete Limited Dissolve"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        bpy.ops.mesh.dissolve_limited(angle_limit=3.14159, use_dissolve_boundaries=False)
        return {'FINISHED'}

####################
#    Animation     #
####################

#Insert Auto Keyframe
class InsertAutoKeyframe(bpy.types.Operator):
    bl_idname = "insert.autokeyframe"
    bl_label = "Insert Auto Keyframe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True :
            bpy.context.scene.tool_settings.use_keyframe_insert_auto = False

        if bpy.context.scene.tool_settings.use_keyframe_insert_auto == False :
            bpy.context.scene.tool_settings.use_keyframe_insert_auto = True

        return {'FINISHED'}

###########################
#    Apply Transforms     #
###########################

#Apply Transforms
class ApplyTransformLocation(bpy.types.Operator):
    bl_idname = "apply.transformlocation"
    bl_label = "Apply Transform Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformRotation(bpy.types.Operator):
    bl_idname = "apply.transformrotation"
    bl_label = "Apply Transform Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformScale(bpy.types.Operator):
    bl_idname = "apply.transformscale"
    bl_label = "Apply Transform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformRotationScale(bpy.types.Operator):
    bl_idname = "apply.transformrotationscale"
    bl_label = "Apply Transform Rotation Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformAll(bpy.types.Operator):
    bl_idname = "apply.transformall"
    bl_label = "Apply Transform All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {'FINISHED'}


# Clear Menu
class ClearMenu(bpy.types.Menu):
    bl_idname = "clear.menu"
    bl_label = "Clear Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.location_clear", text="Clear Location", icon='MAN_TRANS')
        layout.operator("object.rotation_clear", text="Clear Rotation", icon='MAN_ROT')
        layout.operator("object.scale_clear", text="Clear Scale", icon='MAN_SCALE')
        layout.operator("object.origin_clear", text="Clear Origin", icon='MANIPUL')

#Clear all
class ClearAll(bpy.types.Operator):
    bl_idname = "clear.all"
    bl_label = "Clear All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()
        return {'FINISHED'}

########################
#    Open/Save/...     #
########################

#External Data
class ExternalData(bpy.types.Menu):
    bl_idname = "external.data"
    bl_label = "External Data"

    def draw(self, context):
        layout = self.layout

        layout.operator("file.autopack_toggle", text="Automatically Pack Into .blend")
        layout.separator()
        layout.operator("file.pack_all", text="Pack All Into .blend")
        layout.operator("file.unpack_all", text="Unpack All Into Files")
        layout.separator()
        layout.operator("file.make_paths_relative", text="Make All Paths Relative")
        layout.operator("file.make_paths_absolute", text="Make All Paths Absolute")
        layout.operator("file.report_missing_files", text="Report Missing Files")
        layout.operator("file.find_missing_files", text="Find Missing Files")

#Save Incremental
class FileIncrementalSave(bpy.types.Operator):
    bl_idname = "file.save_incremental"
    bl_label = "Save Incremental"
    bl_options = {"REGISTER"}

    def execute(self, context):
        f_path = bpy.data.filepath
        if f_path.find("_") != -1:
            str_nb = f_path.rpartition("_")[-1].rpartition(".blend")[0]
            int_nb = int(str_nb)
            new_nb = str_nb.replace(str(int_nb),str(int_nb+1))
            output = f_path.replace(str_nb,new_nb)

            i = 1
            while os.path.isfile(output):
                str_nb = f_path.rpartition("_")[-1].rpartition(".blend")[0]
                i += 1
                new_nb = str_nb.replace(str(int_nb),str(int_nb+i))
                output = f_path.replace(str_nb,new_nb)
        else:
            output = f_path.rpartition(".blend")[0]+"_001"+".blend"

        bpy.ops.wm.save_as_mainfile(filepath=output)
        self.report({'INFO'}, "File: {0} - Created at: {1}".format(output[len(bpy.path.abspath("//")):], output[:len(bpy.path.abspath("//"))]))
        return {'FINISHED'}


# Load Most Recent
class LoadMostRecent(bpy.types.Operator):
    bl_idname = "machin3.load_most_recent"
    bl_label = "Load Most Recent"
    bl_options = {"REGISTER"}

    def execute(self, context):
        recent_path = bpy.utils.user_resource('CONFIG', "recent-files.txt")

        try:
            with open(recent_path) as file:
                recent_files = file.read().splitlines()
        except (IOError, OSError, FileNotFoundError):
            recent_files = []

        most_recent = recent_files[0]

        bpy.ops.wm.open_mainfile(filepath=most_recent)
        return {'FINISHED'}

######################
#    Views Ortho     #
######################
#Persp/Ortho
class PerspOrthoView(bpy.types.Operator):
    bl_idname = "persp.orthoview"
    bl_label = "Persp/Ortho"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.view3d.view_persportho()
        return {'FINISHED'}


#######################################################
# Camera                                              #
#######################################################

#Lock Camera Transforms
class LockCameraTransforms(bpy.types.Operator):
    bl_idname = "object.lockcameratransforms"
    bl_label = "Lock Camera Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.lock_rotation[0] == False:
            bpy.context.object.lock_rotation[0] = True
            bpy.context.object.lock_rotation[1] = True
            bpy.context.object.lock_rotation[2] = True
            bpy.context.object.lock_location[0] = True
            bpy.context.object.lock_location[1] = True
            bpy.context.object.lock_location[2] = True
            bpy.context.object.lock_scale[0] = True
            bpy.context.object.lock_scale[1] = True
            bpy.context.object.lock_scale[2] = True

        elif bpy.context.object.lock_rotation[0] == True :
            bpy.context.object.lock_rotation[0] = False
            bpy.context.object.lock_rotation[1] = False
            bpy.context.object.lock_rotation[2] = False
            bpy.context.object.lock_location[0] = False
            bpy.context.object.lock_location[1] = False
            bpy.context.object.lock_location[2] = False
            bpy.context.object.lock_scale[0] = False
            bpy.context.object.lock_scale[1] = False
            bpy.context.object.lock_scale[2] = False
        return {'FINISHED'}

#Active Camera
bpy.types.Scene.cameratoto = bpy.props.StringProperty(default="")

class ActiveCameraSelection(bpy.types.Operator):
    bl_idname = "object.activecameraselection"
    bl_label = "Active Camera Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.data.objects[context.scene.cameratoto].select=True
        bpy.ops.view3d.object_as_camera()
        return {'FINISHED'}

#Select Camera
class CameraSelection(bpy.types.Operator):
    bl_idname = "object.cameraselection"
    bl_label = "Camera Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for cam in bpy.data.cameras:
            bpy.ops.object.select_camera()

        return {'FINISHED'}

#Pie Material
class MaterialListMenu(bpy.types.Menu): # menu appelé par le pie
    bl_idname = "object.material_list_menu"
    bl_label = "Material_list"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        if len(bpy.data.materials): # "len" retourne le nombre d'occurence donc, si il y a des materiaux dans les datas:
            for mat in bpy.data.materials:
                name = mat.name
                try:
                    icon_val = layout.icon(mat) # récupère l'icon du materiau
                except:
                    icon_val = 1
                    print ("WARNING [Mat Panel]: Could not get icon value for %s" % name)

                op = col.operator("object.apply_material", text=name, icon_value=icon_val) # opérateur qui apparait dans le menu pour chaque matériau présent dans les datas materials
                op.mat_to_assign = name # on "stock" le nom du matériau dans la variable "mat_to_assign" declarée dans la class opérateur "ApplyMaterial"
        else:
            layout.label("No data materials")



class ApplyMaterial(bpy.types.Operator):
    bl_idname = "object.apply_material"
    bl_label = "Apply material"

    mat_to_assign = bpy.props.StringProperty(default="")

    def execute(self, context):

        if context.object.mode == 'EDIT':
            obj = context.object
            bm = bmesh.from_edit_mesh(obj.data)

            selected_face = [f for f in bm.faces if f.select]  # si des faces sont sélectionnées, elles sont stockées dans la liste "selected_faces"

            mat_name = [mat.name for mat in bpy.context.object.material_slots if len(bpy.context.object.material_slots)] # pour tout les material_slots, on stock les noms des mat de chaque slots dans la liste "mat_name"

            if self.mat_to_assign in mat_name: # on test si le nom du mat sélectionné dans le menu est présent dans la liste "mat_name" (donc, si un des slots possède le materiau du même nom). Si oui:
                context.object.active_material_index = mat_name.index(self.mat_to_assign) # on definit le slot portant le nom du comme comme étant le slot actif
                bpy.ops.object.material_slot_assign() # on assigne le matériau à la sélection
            else: # sinon
                bpy.ops.object.material_slot_add() # on ajout un slot
                bpy.context.object.active_material = bpy.data.materials[self.mat_to_assign] # on lui assigne le materiau choisi
                bpy.ops.object.material_slot_assign() # on assigne le matériau à la sélection

            return {'FINISHED'}

        elif context.object.mode == 'OBJECT':

            obj_list = [obj.name for obj in context.selected_objects]

            for obj in obj_list:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[obj].select = True
                bpy.context.scene.objects.active = bpy.data.objects[obj]
                bpy.context.object.active_material_index = 0

                if self.mat_to_assign == bpy.data.materials:
                    bpy.context.active_object.active_material = bpy.data.materials[mat_name]

                else:
                    if not len(bpy.context.object.material_slots):
                        bpy.ops.object.material_slot_add()

                    bpy.context.active_object.active_material = bpy.data.materials[self.mat_to_assign]

            for obj in obj_list:
                bpy.data.objects[obj].select = True

            return {'FINISHED'}
######################
#     Pie Menus      #
######################

# Pie Edit/Object Others modes - Tab
class PieObjectEditotherModes(Menu):
    bl_idname = "pie.objecteditmodeothermodes"
    bl_label = "Select Other Modes"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("class.pieweightpaint", text="Weight Paint", icon='WPAINT_HLT')
        #6 - RIGHT
        pie.operator("class.pietexturepaint", text="Texture Paint", icon='TPAINT_HLT')
        #2 - BOTTOM
        pie.operator("class.pieparticleedit", text="Particle Edit", icon='PARTICLEMODE')
        #8 - TOP
        pie.operator("class.pievertexpaint", text="Vertex Paint", icon='VPAINT_HLT')
        #7 - TOP - LEFT
        #9 - TOP - RIGHT
        #1 - BOTTOM - LEFT
        #3 - BOTTOM - RIGHT

# Pie Vertex/Edges/Faces Modes - Tab
class PieVertexEdgesFacesModes(Menu):
    bl_idname = "pie.vertexedgesfacesmodes"
    bl_label = "Select Multi Components"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("verts.faces", text="Vertex/Faces", icon='LOOPSEL')
        # 6 - RIGHT
        pie.operator("verts.edges", text="Vertex/Edges", icon='VERTEXSEL')
        # 2 - BOTTOM
        pie.operator("verts.edgesfaces", text="Vertex/Edges/Faces", icon='OBJECT_DATAMODE')
        # 8 - TOP
        pie.operator("edges.faces", text="Edges/Faces", icon='FACESEL')
        # 7 - TOP - LEFT
        # 9 - TOP - RIGHT
        # 1 - BOTTOM - LEFT
        # 3 - BOTTOM - RIGHT


class PieObjectEditMode(Menu):
    bl_idname = "pie.objecteditmode"
    bl_label = "Select Mode"

    def draw(self, context):
        layout = self.layout
        toolsettings = context.tool_settings
        ob = context

        if ob.object.type == 'MESH':
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.operator("class.vertex", text="Vertex", icon='VERTEXSEL')
            # 6 - RIGHT
            pie.operator("class.face", text="Face", icon='FACESEL')
            # 2 - BOTTOM
            pie.operator("class.edge", text="Edge", icon='EDGESEL')
            # 8 - TOP
            pie.operator("class.object", text="Edit/Object", icon='OBJECT_DATAMODE')
            # 7 - TOP - LEFT
            if bpy.context.object.mode == "EDIT":
                pie.prop(bpy.context.space_data, "use_occlude_geometry", text="Occlude")
            elif bpy.context.object.mode == "SCULPT":
                row = pie.row(align=True)
                row.scale_x = 1.5
                row.scale_y = 1.25
                row.prop(bpy.context.scene.tool_settings.sculpt, "use_symmetry_x", text="X")
                row.prop(bpy.context.scene.tool_settings.sculpt, "use_symmetry_y", text="Y")
                row.prop(bpy.context.scene.tool_settings.sculpt, "use_symmetry_z", text="Z")
            elif bpy.context.object.mode == "OBJECT" and bpy.context.gpencil_data:
                pie.operator("gpencil.editmode_toggle", text="Edit Strokes", icon='GREASEPENCIL')
            else:
                pie.separator()

            # 9 - TOP - RIGHT
            pie.operator("sculpt.sculptmode_toggle", text="Sculpt", icon='SCULPTMODE_HLT')
            # 1 - BOTTOM - LEFT
            pie.operator("wm.call_menu_pie", text="Other Modes", icon='TPAINT_HLT').name="pie.objecteditmodeothermodes"
            # 3 - BOTTOM - RIGHT
            box = pie.split()
            column = box.column()
            column.prop(bpy.context.scene.machin3, "pieobjecteditmodehide")
            row = column.row(align=True)
            row.prop(bpy.context.scene.machin3, "pieobjecteditmodeshow")
            row.prop(bpy.context.scene.machin3, "pieobjecteditmodeshowunselect")
            column.prop(toolsettings, "use_mesh_automerge", text="Auto Merge")

        elif ob.object.type == 'CURVE':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

        elif ob.object.type == 'ARMATURE':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit Mode", icon='OBJECT_DATAMODE')
            pie.operator("object.posemode_toggle", text="Pose", icon='POSE_HLT')
            pie.operator("class.object", text="Object Mode", icon='OBJECT_DATAMODE')

        elif ob.object.type == 'FONT':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

        elif ob.object.type == 'SURFACE':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

        elif ob.object.type == 'ARMATURE':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

        elif ob.object.type == 'META':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

        elif ob.object.type == 'LATTICE':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

        elif ob.object.type == 'ARMATURE':
            pie = layout.menu_pie()
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')



#Pie View Animation Etc - Space
class PieAnimationEtc(Menu):
    bl_idname = "pie.animationetc"
    bl_label = "Animation Etc"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.view_menu", text="Timeline", icon= 'TIME').variable="TIMELINE"
        #6 - RIGHT
        pie.operator("object.view_menu", text="Dope Sheet", icon= 'ACTION').variable="DOPESHEET_EDITOR"
        #2 - BOTTOM
        pie.operator("object.view_menu", text="NLA Editor", icon= 'NLA').variable="NLA_EDITOR"
        #8 - TOP
        pie.operator("object.view_menu", text="Graph Editor", icon= 'IPO').variable="GRAPH_EDITOR"
        #7 - TOP - LEFT
        pie.operator("object.view_menu", text="Movie Clip Editor", icon= 'RENDER_ANIMATION').variable="CLIP_EDITOR"
        #9 - TOP - RIGHT
        pie.operator("object.view_menu", text="Sequence Editor", icon= 'SEQUENCE').variable="SEQUENCE_EDITOR"
        #1 - BOTTOM - LEFT
        pie.operator("object.view_menu", text="Logic Editor", icon= 'LOGIC').variable="LOGIC_EDITOR"
        #3 - BOTTOM - RIGHT

#Pie View File Properties Etc - Space
class PieFilePropertiesEtc(Menu):
    bl_idname = "pie.filepropertiesetc"
    bl_label = "Pie File Properties..."

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.view_menu", text="Properties", icon= 'BUTS').variable="PROPERTIES"
        #6 - RIGHT
        pie.operator("object.view_menu", text="Outliner", icon= 'OOPS').variable="OUTLINER"
        #2 - BOTTOM
        pie.operator("object.view_menu", text="User Preferences", icon= 'PREFERENCES').variable="USER_PREFERENCES"
        #8 - TOP
        pie.operator("object.view_menu", text="Text Editor", icon= 'FILE_TEXT').variable="TEXT_EDITOR"
        #7 - TOP - LEFT
        pie.operator("object.view_menu", text="File Browser", icon= 'FILESEL').variable="FILE_BROWSER"
        #1 - BOTTOM - LEFT
        pie.operator("object.view_menu", text="Python Console", icon= 'CONSOLE').variable="CONSOLE"
        #9 - TOP - RIGHT
        pie.operator("object.view_menu", text="Info", icon= 'INFO').variable="INFO"
        #3 - BOTTOM - RIGHT

#Pie View All Sel Glob Etc - Q
class PieViewallSelGlobEtc(Menu):
    bl_idname = "pie.vieallselglobetc"
    bl_label = "Pie View All Sel Glob..."

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("view3d.view_all", text="View All").center = True
        #6 - RIGHT
        pie.operator("view3d.view_selected", text="View Selected")
        #2 - BOTTOM
        pie.operator("persp.orthoview", text="Persp/Ortho", icon='RESTRICT_VIEW_OFF')
        #8 - TOP
        pie.operator("view3d.localview", text="Local/Global")
        #7 - TOP - LEFT
        pie.operator("screen.region_quadview", text="Toggle Quad View", icon='SPLITSCREEN')
        #1 - BOTTOM - LEFT
        pie.operator("screen.screen_full_area", text="Full Screen", icon='FULLSCREEN_ENTER')
        #9 - TOP - RIGHT
        #3 - BOTTOM - RIGHT

# MACHIN3
#Pie Views - Space
class PieAreaViews(Menu):
    bl_idname = "pie.areaviews"
    bl_label = "Screen Layouts"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("machin3.layout_switch", text="MACHIN3", icon='VIEW3D').variable="M3"
        # 6 - RIGHT
        pie.operator("machin3.layout_switch", text="Compositing", icon='NODETREE').variable="M3 compositing"
        # 2 - BOTTOM
        box = pie.split()
        column = box.column(align=True)
        column.operator("machin3.layout_switch", text="Animation", icon='ACTION_TWEAK').variable="M3 animation"
        column.operator("machin3.layout_switch", text="Drivers", icon='UI').variable="M3 drivers"
        # 8 - TOP
        pie.operator("machin3.layout_switch", text="Materials", icon='MATERIAL_DATA').variable="M3 materials"
        # 7 - TOP - LEFT
        pie.operator("machin3.layout_switch", text="UVs", icon='GROUP_UVS').variable="M3 UVs"
        # 9 - TOP - RIGHT
        box = pie.split()
        row = box.row(align=True)
        row.operator("machin3.layout_switch", text="Lighting", icon='IMAGE_COL').variable="M3 lighting"
        row.operator("machin3.layout_switch", text="Baking", icon='MOD_UVPROJECT').variable="M3 baking"
        # 1 - BOTTOM - LEFT
        box = pie.split()
        row = box.row(align=True)
        row.operator("machin3.layout_switch", text="Scripting", icon='SCRIPT').variable="M3 scripting"
        row.operator("machin3.layout_switch", text="Console", icon='CONSOLE').variable="M3 console"
        # 3 - BOTTOM - RIGHT
        pie.operator("machin3.layout_switch", text="Video Editing", icon='RENDER_ANIMATION').variable="M3 video"

# /MACHIN3

#Pie views numpad - Q
class PieViewNumpad(Menu):
    bl_idname = "pie.viewnumpad"
    bl_label = "Pie Views Ortho"

    def draw(self, context):
        layout = self.layout
        ob = bpy.context.object
        obj = context.object
        pie = layout.menu_pie()
        scene = context.scene
        rd = scene.render

        #4 - LEFT
        pie.operator("view3d.viewnumpad", text="Left", icon='TRIA_LEFT').type='LEFT'
        #6 - RIGHT
        pie.operator("view3d.viewnumpad", text="Right", icon='TRIA_RIGHT').type='RIGHT'
        #2 - BOTTOM
        pie.operator("view3d.viewnumpad", text="Bottom", icon='TRIA_DOWN').type='BOTTOM'
        #8 - TOP
        pie.operator("view3d.viewnumpad", text="Top", icon='TRIA_UP').type='TOP'
        #7 - TOP - LEFT
        pie.operator("view3d.viewnumpad", text="Front").type='FRONT'
        #9 - TOP - RIGHT
        pie.operator("view3d.viewnumpad", text="Back").type='BACK'
        #1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        if context.space_data.lock_camera == False:
            row.operator("wm.context_toggle", text="Lock Cam to View", icon='UNLOCKED').data_path = "space_data.lock_camera"
        elif context.space_data.lock_camera == True:
            row.operator("wm.context_toggle", text="Lock Cam to View", icon='LOCKED').data_path = "space_data.lock_camera"

        row = box.row(align=True)
        row.operator("view3d.viewnumpad", text="View Cam", icon='VISIBLE_IPO_ON').type='CAMERA'
        row.operator("view3d.camera_to_view", text="Cam to view", icon = 'MAN_TRANS')

        if ob.lock_rotation[0] == False:
            row = box.row(align=True)
            row.operator("object.lockcameratransforms", text="Lock Transforms", icon = 'LOCKED')

        elif  ob.lock_rotation[0] == True:
            row = box.row(align=True)
            row.operator("object.lockcameratransforms", text="UnLock Transforms", icon = 'UNLOCKED')
        row = box.row(align=True)
        row.prop(rd, "use_border", text="Border")
        #3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="View All/Sel/Glob...", icon='BBOX').name="pie.vieallselglobetc"

#Pie Sculp Pie Menus - W
class PieSculptPie(Menu):
    bl_idname = "pie.sculpt"
    bl_label = "Pie Sculpt"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("paint.brush_select", text="Crease", icon='BRUSH_CREASE').sculpt_tool='CREASE'
        #6 - RIGHT
        pie.operator("paint.brush_select", text="Clay", icon='BRUSH_CLAY').sculpt_tool='CLAY'
        #2 - BOTTOM
        pie.operator("paint.brush_select", text='Flatten', icon='BRUSH_FLATTEN').sculpt_tool='FLATTEN'
        #8 - TOP
        pie.operator("paint.brush_select", text='Brush', icon='BRUSH_SCULPT_DRAW').sculpt_tool='DRAW'
        #7 - TOP - LEFT
        pie.operator("paint.brush_select", text='Inflate/Deflate', icon='BRUSH_INFLATE').sculpt_tool='INFLATE'
        #9 - TOP - RIGHT
        pie.operator("paint.brush_select", text='Grab', icon='BRUSH_GRAB').sculpt_tool='GRAB'
        #1 - BOTTOM - LEFT
        pie.operator("paint.brush_select", text='Simplify', icon='BRUSH_DATA').sculpt_tool='SIMPLIFY'
        #3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="Others Brushes", icon='LINE_DATA').name="pie.sculpttwo"

#Pie Sculp Pie Menus 2 - W
class PieSculpttwo(Menu):
    bl_idname = "pie.sculpttwo"
    bl_label = "Pie Sculpt 2"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("paint.brush_select", text='Claystrips', icon='BRUSH_CREASE').sculpt_tool= 'CLAY_STRIPS'
        #6 - RIGHT
        pie.operator("paint.brush_select", text='Blob', icon='BRUSH_BLOB').sculpt_tool= 'BLOB'
        #2 - BOTTOM
        pie.operator("paint.brush_select", text='Snakehook', icon='BRUSH_SNAKE_HOOK').sculpt_tool= 'SNAKE_HOOK'
        #8 - TOP
        pie.operator("paint.brush_select", text='Smooth', icon='BRUSH_SMOOTH').sculpt_tool= 'SMOOTH'
        #7 - TOP - LEFT
        pie.operator("paint.brush_select", text='Pinch/Magnify', icon='BRUSH_PINCH').sculpt_tool= 'PINCH'
        #9 - TOP - RIGHT
        pie.operator("sculpt.polish", text='Polish', icon='BRUSH_FLATTEN')
        #1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("paint.brush_select", text='Twist', icon='BRUSH_ROTATE').sculpt_tool= 'ROTATE'
        box.operator("paint.brush_select", text='Scrape/Peaks', icon='BRUSH_SCRAPE').sculpt_tool= 'SCRAPE'
        box.operator("sculpt.sculptraw", text='SculptDraw', icon='BRUSH_SCULPT_DRAW')
        box.operator("paint.brush_select", text='Mask', icon='BRUSH_MASK').sculpt_tool='MASK'
        #3 - BOTTOM - RIGHT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("paint.brush_select", text='Layer', icon='BRUSH_LAYER').sculpt_tool= 'LAYER'
        box.operator("paint.brush_select", text='Nudge', icon='BRUSH_NUDGE').sculpt_tool= 'NUDGE'
        box.operator("paint.brush_select", text='Thumb', icon='BRUSH_THUMB').sculpt_tool= 'THUMB'
        box.operator("paint.brush_select", text='Fill/Deepen', icon='BRUSH_FILL').sculpt_tool='FILL'

#Pie Origin/Pivot - Shift + S
class PieOriginPivot(Menu):
    bl_idname = "pie.originpivot"
    bl_label = "Pie Origin/Cursor"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.pivotobottom", text="Origin to Bottom", icon='TRIA_DOWN')
        #6 - RIGHT
        pie.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected", icon='ROTACTIVE')
        #2 - BOTTOM
        pie.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor", icon='CLIPUV_HLT').use_offset = False
        #8 - TOP
        pie.operator("object.origin_set", text="Origin To 3D Cursor", icon='CURSOR').type ='ORIGIN_CURSOR'
        #7 - TOP - LEFT
        pie.operator("object.pivot2selection", text="Origin To Selection", icon='SNAP_INCREMENT')
        #9 - TOP - RIGHT
        pie.operator("object.origin_set", text="Origin To Geometry", icon='ROTATE').type ='ORIGIN_GEOMETRY'
        #1 - BOTTOM - LEFT
        pie.operator("object.origin_set", text="Geometry To Origin", icon='BBOX').type ='GEOMETRY_ORIGIN'
        #3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="Others", icon='CURSOR').name="origin.pivotmenu"

#Pie Pivot Point - Shit + S
class PiePivotPoint(Menu):
    bl_idname = "pie.pivotpoint"
    bl_label = "Pie Pivot Point"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("pivotpoint.variable", text="Active Element", icon='ROTACTIVE').variable = 'ACTIVE_ELEMENT'
        #6 - RIGHT
        pie.operator("pivotpoint.variable", text="Median Point", icon='ROTATECENTER').variable = 'MEDIAN_POINT'
        #2 - BOTTOM
        pie.operator("pivotpoint.variable", text="Individual Origins", icon='ROTATECOLLECTION').variable = 'INDIVIDUAL_ORIGINS'
        #8 - TOP
        pie.operator("pivotpoint.variable", text="Cursor", icon='CURSOR').variable = 'CURSOR'
        #7 - TOP - LEFT
        pie.operator("pivotpoint.variable", text="Bounding Box Center", icon='ROTATE').variable = 'BOUNDING_BOX_CENTER'
        #9 - TOP - RIGHT
        pie.operator("use.pivotalign", text="Use Pivot Align", icon='ALIGN')
        #1 - BOTTOM - LEFT
        #3 - BOTTOM - RIGHT

#Origin/Pivot menu1  - Shift + S
class OriginPivotMenu(Menu):
    bl_idname = "origin.pivotmenu"
    bl_label = "Origin Pivot Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor (Offset)", icon='CURSOR').use_offset = True
        #6 - RIGHT
        pie.operator("view3d.snap_selected_to_grid", text="Selection to Grid", icon='GRID')
        #2 - BOTTOM
        pie.operator("object.origin_set", text="Origin to Center of Mass", icon='BBOX').type = 'ORIGIN_CENTER_OF_MASS'
        #8 - TOP
        pie.operator("view3d.snap_cursor_to_center", text="Cursor to Center", icon='CLIPUV_DEHLT')
        #7 - TOP - LEFT
        pie.operator("view3d.snap_cursor_to_grid", text="Cursor to Grid", icon='GRID')
        #9 - TOP - RIGHT
        pie.operator("view3d.snap_cursor_to_active", text="Cursor to Active", icon='BBOX')
        #1 - BOTTOM - LEFT
        #3 - BOTTOM - RIGHT

#Pie Manipulators - Ctrl + Space
class PieManipulator(Menu):
    bl_idname = "pie.manipulator"
    bl_label = "Pie Manipulator"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("manip.translate", text="Translate", icon='MAN_TRANS')
        #6 - RIGHT
        pie.operator("manip.scale", text="scale", icon='MAN_SCALE')
        #2 - BOTTOM
        pie.operator("manip.rotate", text="Rotate", icon='MAN_ROT')
        #8 - TOP
        pie.operator("w.manupulators", text="Manipulator", icon='MANIPUL')
        #7 - TOP - LEFT
        pie.operator("translate.rotate", text="Translate/Rotate")
        #9 - TOP - RIGHT
        pie.operator("translate.scale", text="Translate/Scale")
        #1 - BOTTOM - LEFT
        pie.operator("rotate.scale", text="Rotate/Scale")
        #3 - BOTTOM - RIGHT
        pie.operator("translate.rotatescale", text="Translate/Rotate/Scale")

#Pie Snapping - Shift + Tab
class PieSnaping(Menu):
    bl_idname = "pie.snapping"
    bl_label = "Pie Snapping"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("snap.vertex", text="Vertex", icon='SNAP_VERTEX')
        #6 - RIGHT
        pie.operator("snap.face", text="Face", icon='SNAP_FACE')
        #2 - BOTTOM
        pie.operator("snap.edge", text="Edge", icon='SNAP_EDGE')
        #8 - TOP
        pie.prop(context.tool_settings, "use_snap", text="Snap On/Off")
        #7 - TOP - LEFT
        pie.operator("snap.volume", text="Volume", icon='SNAP_VOLUME')
        #9 - TOP - RIGHT
        if bpy.context.scene.tool_settings.snap_element != 'INCREMENT':
            pie.operator("snap.increment", text="Increment", icon='SNAP_INCREMENT')
        else:
            pie.prop(context.scene.tool_settings, "use_snap_grid_absolute")
        #1 - BOTTOM - LEFT
        pie.operator("snap.alignrotation", text="Align rotation", icon='SNAP_NORMAL')
        #3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="Snap Target", icon='SNAP_SURFACE').name="snap.targetmenu"

#Menu Snap Target - Shift + Tab
class SnapTargetMenu(Menu):
    bl_idname = "snap.targetmenu"
    bl_label = "Snap Target Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.snaptargetvariable", text="Active").variable='ACTIVE'
        #6 - RIGHT
        pie.operator("object.snaptargetvariable", text="Median").variable='MEDIAN'
        #2 - BOTTOM
        pie.operator("object.snaptargetvariable", text="Center").variable='CENTER'
        #8 - TOP
        pie.operator("object.snaptargetvariable", text="Closest").variable='CLOSEST'
        #7 - TOP - LEFT
        #9 - TOP - RIGHT
        #1 - BOTTOM - LEFT
        #3 - BOTTOM - RIGHT

#Pie Orientation - Alt + Space
class PieOrientation(Menu):
    bl_idname = "pie.orientation"
    bl_label = "Pie Orientation"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.orientationvariable", text="View").variable = 'VIEW'
        #6 - RIGHT
        pie.operator("object.orientationvariable", text="Local").variable = 'LOCAL'
        #2 - BOTTOM
        pie.operator("object.orientationvariable", text="Normal").variable = 'NORMAL'
        #8 - TOP
        pie.operator("object.orientationvariable", text="Global").variable = 'GLOBAL'
        #7 - TOP - LEFT
        pie.operator("object.orientationvariable", text="Gimbal").variable = 'GIMBAL'
        #9 - TOP - RIGHT
        #1 - BOTTOM - LEFT
        #3 - BOTTOM - RIGHT

#Pie Shading - Z
class PieShadingView(Menu):
    bl_idname = "pie.shadingview"
    bl_label = "Pie Shading"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.shadingvariable", text="Material", icon='MATERIAL').variable = 'MATERIAL'
        #6 - RIGHT
        pie.operator("object.shadingvariable", text="Wireframe", icon='WIRE').variable = 'WIREFRAME'
        #2 - BOTTOM
        pie.menu("object.material_list_menu", icon='MATERIAL_DATA')

        #8 - TOP
        pie.operator("object.shadingvariable", text="Solid", icon='SOLID').variable = 'SOLID'
        #7 - TOP - LEFT
        pie.operator("object.shadingvariable", text="Texture", icon='TEXTURE_SHADED').variable = 'TEXTURED'
        #9 - TOP - RIGHT
        pie.operator("object.shadingvariable", text="Render", icon='SMOOTH').variable = 'RENDERED'
        #1 - BOTTOM - LEFT
        pie.operator("shading.smooth", text="Shade Smooth", icon='SOLID')
        #3 - BOTTOM - RIGHT
        pie.operator("shading.flat", text="Shade Flat", icon='MESH_ICOSPHERE')

#Pie Object Shading- Shift + Z
class PieObjectShading(Menu):
    bl_idname = "pie.objectshading"
    bl_label = "Pie Shading Object"

    def draw(self, context):
        layout = self.layout

        toolsettings = context.tool_settings
        view = context.space_data
        obj = context.object
        mesh = context.active_object.data
        fx_settings = view.fx_settings
        scene = context.scene

        pie = layout.menu_pie()
        #4 - LEFT

        # MACHIN3
        box = pie.split()

        column = box.column()
        column.operator("scene.togglegridaxis", text="Grid Toggle", icon="MESH_GRID")
        row = column.row(align=True)
        row.prop(context.space_data, "show_axis_x", text="X")
        row.prop(context.space_data, "show_axis_y", text="Y")
        row.prop(context.space_data, "show_axis_z", text="Z")
        # /MACHIN3

        #6 - RIGHT
        pie.operator("wire.selectedall", text="Wire", icon='WIRE')
        #2 - BOTTOM
        box = pie.split().column()
        row = box.row(align=True)

        if view.viewport_shade not in {'BOUNDBOX', 'WIREFRAME'}:
            row = box.row(align=True)
            row.prop(fx_settings, "use_dof")
            row = box.row(align=True)
            row.prop(fx_settings, "use_ssao", text="AO")
            if fx_settings.use_ssao:
                ssao_settings = fx_settings.ssao
                row = box.row(align=True)
                row.prop(ssao_settings, "factor")
                row = box.row(align=True)
                row.prop(ssao_settings, "distance_max")
                row = box.row(align=True)
                row.prop(ssao_settings, "attenuation")
                row = box.row(align=True)
                row.prop(ssao_settings, "samples")
                row = box.row(align=True)
                row.prop(ssao_settings, "color")
        #8 - TOP
        box = pie.split().column()
        row = box.row(align=True)
        row.prop(obj, "show_x_ray", text="X-Ray")
        row = box.row(align=True)
        row.prop(view, "show_occlude_wire", text="Hidden Wire")
        row = box.row(align=True)
        row.prop(view, "show_backface_culling", text="Backface Culling")

        # MACHIN3
        row = box.row(align=True)
        row.prop(view, "show_grease_pencil", text="Grease Pencil")
        row = box.row(align=True)
        row.prop(view, "show_relationship_lines", text="Relationship Lines")
        # /MACHIN3

        #7 - TOP - LEFT
        if m3.addon_check("measureit"):
            box = pie.split()
            column = box.column()
            column.scale_x = 1.5
            column.operator("measureit.runopenglbutton", text="Show/Hide Annotations", icon="TEXT")
            column.prop(scene, "measureit_gl_txt", text="")
            column.operator("measureit.addnotebutton", text="Annotate", icon="NEW")
        else:
            pie.separator()

        # box = pie.split().column()
        # row = box.row(align=True)
        # row.prop(mesh, "show_normal_face", text="Show Normals Faces", icon='FACESEL')
        # row = box.row()
        # row.menu("meshdisplay.overlays", text="Mesh display", icon='OBJECT_DATAMODE')

        # #9 - TOP - RIGHT

        # MACHIN3
        box = pie.split()
        column = box.column()

        if bpy.context.object.mode == "OBJECT":
            row = column.row(align=True)
            row.operator("object.shade_smooth", text="Smooth", icon="TEXT")
            row.operator("object.shade_flat", text="Flat", icon="TEXT")
        column.prop(mesh, "use_auto_smooth")
        if mesh.use_auto_smooth:
            column.prop(mesh, "auto_smooth_angle", text="Angle")
        if bpy.context.object.mode == "EDIT":
            row = column.row(align=True)
            row.prop(mesh, "show_normal_vertex", text=" ", icon='VERTEXSEL')
            row.prop(mesh, "show_normal_loop", text=" ", icon='LOOPSEL')
            row.prop(mesh, "show_normal_face", text=" ", icon='FACESEL')
            column.menu("meshdisplay.overlays", text="Mesh display", icon='OBJECT_DATAMODE')
        # /MACHIN3

        #1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        box.prop(view, "show_only_render")
        row = box.row(align=True)
        box.prop(view, "show_world")
        row = box.row(align=True)
        box.prop(view, "show_outline_selected")

        #3 - BOTTOM - RIGHT
        box = pie.split().column()
        row = box.row(align=True)
        row.prop(view, "use_matcap", text="Matcaps")
        if view.use_matcap:
            row = box.row(align=True)
            row.menu("meshdisplay.matcaps", text="Choose Matcaps", icon='MATCAP_02')

#Overlays
class MeshDisplayMatcaps(bpy.types.Menu):
    bl_idname = "meshdisplay.matcaps"
    bl_label = "Mesh Display Matcaps"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        view = context.space_data
        layout.template_icon_view(view, "matcap_icon")


#Pie ProportionalEditObj - O
class PieProportionalObj(Menu):
    bl_idname = "pie.proportional_obj"
    bl_label = "Pie Proportional Edit Obj"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("proportional_obj.sphere", text="Sphere", icon='SPHERECURVE')
        #6 - RIGHT
        pie.operator("proportional_obj.root", text="Root", icon='ROOTCURVE')
        #2 - BOTTOM
        pie.operator("proportional_obj.smooth", text="Smooth", icon='SMOOTHCURVE')
        #8 - TOP
        pie.prop(context.tool_settings, "use_proportional_edit_objects", text="Proportional On/Off")
        #7 - TOP - LEFT
        pie.operator("proportional_obj.linear", text="Linear", icon='LINCURVE')
        #9 - TOP - RIGHT
        pie.operator("proportional_obj.sharp", text="Sharp", icon='SHARPCURVE')
        #1 - BOTTOM - LEFT
        pie.operator("proportional_obj.constant", text="Constant", icon='NOCURVE')
        #3 - BOTTOM - RIGHT
        pie.operator("proportional_obj.random", text="Random", icon='RNDCURVE')

#Pie ProportionalEditEdt - O
class PieProportionalEdt(Menu):
    bl_idname = "pie.proportional_edt"
    bl_label = "Pie Proportional Edit"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("proportional_edt.connected", text="Connected", icon='PROP_CON')
        #6 - RIGHT
        pie.operator("proportional_edt.projected", text="Projected", icon='PROP_ON')
        #2 - BOTTOM
        pie.operator("proportional_edt.smooth", text="Smooth", icon='SMOOTHCURVE')
        #8 - TOP
        pie.operator("proportional_edt.active", text="Proportional On/Off", icon='PROP_ON')
        #7 - TOP - LEFT
        pie.operator("proportional_edt.sphere", text="Sphere", icon='SPHERECURVE')
        #9 - TOP - RIGHT
        pie.operator("proportional_edt.root", text="Root", icon='ROOTCURVE')
        #1 - BOTTOM - LEFT
        pie.operator("proportional_edt.constant", text="Constant", icon='NOCURVE')
        #3 - BOTTOM - RIGHT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("proportional_edt.linear", text="Linear", icon='LINCURVE')
        box.operator("proportional_edt.sharp", text="Sharp", icon='SHARPCURVE')
        box.operator("proportional_edt.random", text="Random", icon='RNDCURVE')

# Pie Align - Alt + X
class PieAlign(Menu):
    bl_idname = "pie.align"
    bl_label = "Pie Align"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("align.x", text="Align X", icon='TRIA_LEFT')
        #6 - RIGHT
        pie.operator("align.z", text="Align Z", icon='TRIA_DOWN')
        #2 - BOTTOM
        pie.operator("align.y", text="Align Y", icon='PLUS')
        #8 - TOP
        pie.operator("align.2y0", text="Align To Y-0")
        #7 - TOP - LEFT
        pie.operator("align.2x0", text="Align To X-0")
        #9 - TOP - RIGHT
        pie.operator("align.2z0", text="Align To Z-0")
        #1 - BOTTOM - LEFT
        #pie.menu("align.xyz")
        box = pie.split().box().column()
        box.label("Align :")
        row = box.row(align=True)
        row.label("X")
        row.operator("alignx.left", text="Neg")
        row.operator("alignx.right", text="Pos")
        row = box.row(align=True)
        row.label("Y")
        row.operator("aligny.front", text="Neg")
        row.operator("aligny.back", text="Pos")
        row = box.row(align=True)
        row.label("Z")
        row.operator("alignz.bottom", text="Neg")
        row.operator("alignz.top", text="Pos")
        #3 - BOTTOM - RIGHT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("mesh.vertex_align", icon='ALIGN', text="Align")
        box.operator("retopo.space", icon='ALIGN', text="Distribute")
        box.operator("mesh.vertex_inline", icon='ALIGN', text="Align & Distribute")

# Pie Delete - X
class PieDelete(Menu):
    bl_idname = "pie.delete"
    bl_label = "Pie Delete"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("mesh.delete", text="Delete Vertices", icon='VERTEXSEL').type='VERT'
        #6 - RIGHT
        pie.operator("mesh.delete", text="Delete Faces", icon='FACESEL').type='FACE'
        #2 - BOTTOM
        pie.operator("mesh.delete", text="Delete Edges", icon='EDGESEL').type='EDGE'
        #8 - TOP
        pie.operator("mesh.dissolve_edges", text="Dissolve Edges", icon='SNAP_EDGE')
        #7 - TOP - LEFT
        pie.operator("mesh.dissolve_verts", text="Dissolve Vertices", icon='SNAP_VERTEX')
        #9 - TOP - RIGHT
        pie.operator("mesh.dissolve_faces", text="Dissolve Faces", icon='SNAP_FACE')
        #1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("delete.limiteddissolve", text="Limited Dissolve", icon= 'STICKY_UVS_LOC')
        box.operator("mesh.delete_edgeloop", text="Delete Edge Loops", icon='BORDER_LASSO')
        box.operator("mesh.edge_collapse", text="Edge Collapse", icon='UV_EDGESEL')
        #3 - BOTTOM - RIGHT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("mesh.delete", text="Only Edge & Faces", icon='SPACE2').type='EDGE_FACE'
        box.operator("mesh.delete", text="Only Faces", icon='UV_FACESEL').type='ONLY_FACE'

# Pie Apply Transforms - Ctrl + A
class PieApplyTransforms(Menu):
    bl_idname = "pie.applytranforms"
    bl_label = "Pie Apply Transforms"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("apply.transformlocation", text="Location", icon='MAN_TRANS')
        #6 - RIGHT
        pie.operator("apply.transformscale", text="Scale", icon='MAN_SCALE')
        #2 - BOTTOM
        pie.operator("apply.transformrotation", text="Rotation", icon='MAN_ROT')
        #8 - TOP
        pie.operator("apply.transformall", text="Transforms", icon='FREEZE')
        #7 - TOP - LEFT
        pie.operator("apply.transformrotationscale", text="Rotation/Scale")
        #9 - TOP - RIGHT
        pie.operator("clear.all", text="Clear All", icon='MANIPUL')
        #1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("object.visual_transform_apply", text="Visual Transforms")
        box.operator("object.duplicates_make_real", text="Make Duplicates Real")
        #3 - BOTTOM - RIGHT
        pie.menu("clear.menu", text="Clear Transforms")

# Pie Selection Object Mode - A
class PieSelectionsOM(Menu):
    bl_idname = "pie.selectionsom"
    bl_label = "Pie Selections Object Mode"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("view3d.select_circle", text="Circle Select", icon='BORDER_LASSO')
        #6 - RIGHT
        pie.operator("view3d.select_border", text="Border Select", icon='BORDER_RECT')
        #2 - BOTTOM
        pie.operator("object.select_all", text="Invert Selection", icon='ZOOM_PREVIOUS').action='INVERT'
        #8 - TOP
        pie.operator("object.select_all", text="Select All", icon='RENDER_REGION').action='TOGGLE'
        #7 - TOP - LEFT
        pie.operator("object.select_camera", text="Select Camera", icon='CAMERA_DATA')
        #9 - TOP - RIGHT
        pie.operator("object.select_random", text="Select Random", icon='GROUP_VERTEX')
        #1 - BOTTOM - LEFT
        pie.operator("object.select_by_layer", text="Select By Layer", icon='GROUP_VERTEX')
        #3 - BOTTOM - RIGHT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("object.select_by_type", text="Select By Type", icon='SNAP_VOLUME')
        box.operator("object.select_grouped", text="Select Grouped", icon='ROTATE')
        box.operator("object.select_linked", text="Select Linked", icon='CONSTRAINT_BONE')

# Pie Selection Edit Mode
class PieSelectionsEM(Menu):
    bl_idname = "pie.selectionsem"
    bl_label = "Pie Selections Edit Mode"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("view3d.select_circle", text="Circle Select", icon='BORDER_LASSO')
        #6 - RIGHT
        pie.operator("view3d.select_border", text="Border Select", icon='BORDER_RECT')
        #2 - BOTTOM
        pie.operator("mesh.select_all", text="Invert Selection", icon='ZOOM_PREVIOUS').action='INVERT'
        #8 - TOP
        pie.operator("mesh.select_all", text="De/Select All", icon='RENDER_REGION').action='TOGGLE'
        #7 - TOP - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("mesh.select_nth", text="Checker Select", icon='PARTICLE_POINT')
        box.operator("mesh.loop_to_region", text="Select Loop Inner Region", icon='FACESEL')
        box.operator("mesh.select_similar", text="Select Similar", icon='GHOST')
        #9 - TOP - RIGHT
        pie.operator("object.selectallbyselection", text="Complete Select", icon='RENDER_REGION')
        #1 - BOTTOM - LEFT
        pie.operator("mesh.loop_multi_select", text="Select Ring", icon='ZOOM_PREVIOUS').ring=True
        #3 - BOTTOM - RIGHT
        pie.operator("mesh.loop_multi_select", text="Select Loop", icon='ZOOM_PREVIOUS').ring=False

# Pie Text Editor
class PieTextEditor(Menu):
    bl_idname = "pie.texteditor"
    bl_label = "Pie Text Editor"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        if bpy.context.area.type == 'TEXT_EDITOR':
            #4 - LEFT
            pie.operator("text.comment", text="Comment", icon='FONT_DATA')
            #6 - RIGHT
            pie.operator("text.uncomment", text="Uncomment", icon='NLA')
            #2 - BOTTOM
            pie.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
            #8 - TOP
            pie.operator("text.start_find", text="Search", icon='VIEWZOOM')
            #7 - TOP - LEFT
            pie.operator("text.indent", text="Tab (indent)", icon='FORWARD')
            #9 - TOP - RIGHT
            pie.operator("text.unindent", text="UnTab (unindent)", icon='BACK')
            #1 - BOTTOM - LEFT
            pie.operator("text.save", text="Save Script", icon='SAVE_COPY')
            #3 - BOTTOM - RIGHT

# Pie Animation
class PieAnimation(Menu):
    bl_idname = "pie.animation"
    bl_label = "Pie Animation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("screen.animation_play", text="Reverse", icon='PLAY_REVERSE').reverse = True
        #6 - RIGHT
        if not context.screen.is_animation_playing:# Play / Pause
            pie.operator("screen.animation_play", text="Play", icon='PLAY')
        else:
            pie.operator("screen.animation_play", text="Stop", icon='PAUSE')
        #2 - BOTTOM
        #pie.operator(toolsettings, "use_keyframe_insert_keyingset", toggle=True, text="Auto Keyframe ", icon='REC')
        pie.operator("insert.autokeyframe", text="Auto Keyframe ", icon='REC')
        #8 - TOP
        pie.menu("VIEW3D_MT_object_animation", icon = "CLIP")
        #7 - TOP - LEFT
        pie.operator("screen.frame_jump", text="Jump REW", icon='REW').end = False
        #9 - TOP - RIGHT
        pie.operator("screen.frame_jump", text="Jump FF", icon='FF').end = True
        #1 - BOTTOM - LEFT
        pie.operator("screen.keyframe_jump", text="Previous FR", icon='PREV_KEYFRAME').next = False
        #3 - BOTTOM - RIGHT
        pie.operator("screen.keyframe_jump", text="Next FR", icon='NEXT_KEYFRAME').next = True

#Pie Save/Open
class PieSaveOpen(Menu):
    bl_idname = "pie.saveopen"
    bl_label = "Pie Save/Open"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("wm.read_homefile", text="New", icon='NEW')
        #6 - RIGHT
        pie.operator("file.save_incremental", text="Incremental Save", icon='SAVE_COPY')
        #2 - BOTTOM
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("import_scene.obj", text="Import OBJ", icon='IMPORT')
        box.operator("export_scene.obj", text="Export OBJ", icon='EXPORT')
        box.separator()
        box.operator("import_scene.fbx", text="Import FBX", icon='IMPORT')
        box.operator("export_scene.fbx", text="Export FBX", icon='EXPORT')
        #8 - TOP
        pie.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
        #7 - TOP - LEFT
        pie.operator("wm.open_mainfile", text="Open file", icon='FILE_FOLDER')
        #9 - TOP - RIGHT
        pie.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')
        #1 - BOTTOM - LEFT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("machin3.load_most_recent", text="(R) Load Most Recent", icon='FILE_FOLDER')
        box.separator()
        box.operator("wm.recover_auto_save", text="Recover Auto Save...", icon='RECOVER_AUTO')
        box.operator("wm.recover_last_session", text="Recover Last Session", icon='RECOVER_LAST')
        box.operator("wm.revert_mainfile", text="Revert", icon='FILE_REFRESH')
        #3 - BOTTOM - RIGHT
        box = pie.split().column()
        row = box.row(align=True)
        box.operator("wm.link", text="Link", icon='LINK_BLEND')
        box.operator("wm.append", text="Append", icon='APPEND_BLEND')
        box.menu("external.data", text="External Data", icon='EXTERNAL_DATA')



#Pie UV's Select Mode
class PIE_IMAGE_MT_uvs_select_mode(Menu):
    bl_label = "UV Select Mode"
    bl_idname = "pie.uvsselectmode"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        toolsettings = context.tool_settings
        pie = layout.menu_pie()
        # do smart things depending on whether uv_select_sync is on

        if toolsettings.use_uv_select_sync:

            props = pie.operator("wm.context_set_value", text="Vertex", icon='VERTEXSEL')
            props.value = "(True, False, False)"
            props.data_path = "tool_settings.mesh_select_mode"

            props = pie.operator("wm.context_set_value", text="Face", icon='FACESEL')
            props.value = "(False, False, True)"
            props.data_path = "tool_settings.mesh_select_mode"

            props = pie.operator("wm.context_set_value", text="Edge", icon='EDGESEL')
            props.value = "(False, True, False)"
            props.data_path = "tool_settings.mesh_select_mode"

        else:
            props = pie.operator("wm.context_set_string", text="Vertex", icon='UV_VERTEXSEL')
            props.value = 'VERTEX'
            props.data_path = "tool_settings.uv_select_mode"

            props = pie.operator("wm.context_set_string", text="Face", icon='UV_FACESEL')
            props.value = 'FACE'
            props.data_path = "tool_settings.uv_select_mode"

            props = pie.operator("wm.context_set_string", text="Edge", icon='UV_EDGESEL')
            props.value = 'EDGE'
            props.data_path = "tool_settings.uv_select_mode"

            props = pie.operator("wm.context_set_string", text="Island", icon='UV_ISLANDSEL')
            props.value = 'ISLAND'
            props.data_path = "tool_settings.uv_select_mode"


#Pie UV's Weld/Align
class Pie_UV_W(Menu):
    bl_idname = "pie.uvsweldalign"
    bl_label = "Pie UV's Welde/Align"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("uv.align", text="Align X").axis = 'ALIGN_X'
        #6 - RIGHT
        pie.operator("uv.align", text="Align Y").axis = 'ALIGN_Y'
        #2 - BOTTOM
        pie.operator("uv.align", text="Straighten").axis = 'ALIGN_S'
        #8 - TOP
        pie.operator("uv.align", text="Align Auto").axis = 'ALIGN_AUTO'
        #7 - TOP - LEFT
        pie.operator("uv.weld", text="Weld", icon='AUTOMERGE_ON')
        #9 - TOP - RIGHT
        pie.operator("uv.remove_doubles", text="Remouve doubles")
        #1 - BOTTOM - LEFT
        pie.operator("uv.align", text="Straighten X").axis = 'ALIGN_T'
        #3 - BOTTOM - RIGHT
        pie.operator("uv.align", text="Straighten Y").axis = 'ALIGN_U'

#Pie Texture Paint Pie Menu - W
class PieTexturePainttPie(Menu):
    bl_idname = "pie.texturepaint"
    bl_label = "Pie Texture Paint"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("paint.brush_select", text="Fill", icon='BRUSH_TEXFILL').texture_paint_tool='FILL'
        #6 - RIGHT
        pie.operator("paint.brush_select", text="Draw", icon='BRUSH_TEXDRAW').texture_paint_tool='DRAW'
        #2 - BOTTOM
        pie.operator("paint.brush_select", text='Soften', icon='BRUSH_SOFTEN').texture_paint_tool='SOFTEN'
        #8 - TOP
        pie.operator("paint.brush_select", text='Mask', icon='BRUSH_TEXMASK').texture_paint_tool='MASK'
        #7 - TOP - LEFT
        pie.operator("paint.brush_select", text='Smear', icon='BRUSH_SMEAR').texture_paint_tool='SMEAR'
        #9 - TOP - RIGHT
        pie.operator("paint.brush_select", text='Clone', icon='BRUSH_CLONE').texture_paint_tool='CLONE'

#Search Menu
def SearchMenu(self, context):
    layout = self.layout

    layout.operator("wm.search_menu", text="", icon ='VIEWZOOM')

def view3d_Search_menu(self, context):
    layout = self.layout

    layout.menu("SearchMenu")


"""
addon_keymaps = []

def register():
    bpy.utils.register_module(__name__)


# Keympa Config

    wm = bpy.context.window_manager

#        #Views numpad
#        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS')
#        kmi.properties.name = "pie.viewnumpad"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Sculpt Pie Menu
#        km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS')
#        kmi.properties.name = "pie.sculpt"
#       kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Sculpt Pie Menu 2
#        km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS', alt=True)
#        kmi.properties.name = "pie.sculpttwo"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Origin/Pivot
#        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', shift=True)
#        kmi.properties.name = "pie.originpivot"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Manipulators
#        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', ctrl=True)
#        kmi.properties.name = "pie.manipulator"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Shading
#        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'Z', 'PRESS')
#        kmi.properties.name = "pie.shadingview"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Pivot Point
#        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', alt=True)
#        kmi.properties.name = "pie.pivotpoint"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #ProportionalEditObj
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
#        kmi.properties.name = "pie.proportional_obj"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #ProportionalEditEdt
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Mesh')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
#        kmi.properties.name = "pie.proportional_edt"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Delete
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Mesh')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'X', 'PRESS')
#        kmi.properties.name = "pie.delete"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Apply Transform
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS', ctrl=True)
#        kmi.properties.name = "pie.applytranforms"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Selection Object Mode
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS')
#        kmi.properties.name = "pie.selectionsom"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Selection Edit Mode
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Mesh')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS')
#        kmi.properties.name = "pie.selectionsem"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Tex Editor
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Text', space_type = 'TEXT_EDITOR')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS', ctrl=True, alt=True)
#        kmi.properties.name = "pie.texteditor"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Animation
#        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'PRESS', alt=True)
#        kmi.properties.name = "pie.animation"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        # Set 2d cursor with double click LMB
#        km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name = 'Image', space_type = 'IMAGE_EDITOR')
#        kmi = km.keymap_items.new('uv.cursor_set', 'RIGHTMOUSE', 'DOUBLE_CLICK', ctrl=True)
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        #Texturepaint Pie Menu
#        km = wm.keyconfigs.addon.keymaps.new(name = 'Image Paint')
#        kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS')
#        kmi.properties.name = "pie.texturepaint"
#        kmi.active = True
#        addon_keymaps.append((km, kmi))


#        addon_keymaps.append(km)

"""
