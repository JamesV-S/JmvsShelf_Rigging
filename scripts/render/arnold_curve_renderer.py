#Created by AnimatorsJourney.com
import maya.cmds as cmds
import functools


def set_render_curve(curve, shader):
    # Get the shape nodes connected to the curve
    curve_shapes = cmds.listRelatives(curve, shapes=True, fullPath=True)
    
    for curve_shape in curve_shapes:
        # Check if the shape node is a NURBS curve
        if cmds.nodeType(curve_shape) != "nurbsCurve":
            continue
        
        # Check if the Arnold node exists for the curve shape
        if not cmds.objExists(curve_shape + ".aiRenderCurve"):
            print("No Arnold node found for", curve_shape)
            continue
        
        # Set render curve attribute to True
        cmds.setAttr(curve_shape + ".aiRenderCurve", True)
        
        # Connect the shader to aiCurveShader attribute
        cmds.connectAttr(shader + ".outColor", curve_shape + ".aiCurveShader", force=True)
        
        print("Render curve enabled and shader connected for", curve_shape)

def set_curve_width(curve, width):
    # Get the shape nodes connected to the curve
    curve_shapes = cmds.listRelatives(curve, shapes=True, fullPath=True)
    
    for curve_shape in curve_shapes:
        # Check if the shape node is a NURBS curve
        if cmds.nodeType(curve_shape) != "nurbsCurve":
            continue
        
        # Set the aiCurveWidth attribute
        cmds.setAttr(curve_shape + ".aiCurveWidth", width)
        print("Curve width set to", width, "for", curve_shape)
       
       
def set_primary_visibility(curve, primary_visibility):
    # Get the shape nodes connected to the curve
    curve_shapes = cmds.listRelatives(curve, shapes=True, fullPath=True)
    
    for curve_shape in curve_shapes:
        # Check if the shape node is a NURBS curve
        if cmds.nodeType(curve_shape) != "nurbsCurve":
            continue
        
        # Set the primaryVisibility attribute
        cmds.setAttr(curve_shape + ".primaryVisibility", primary_visibility)
        print("Primary visibility set to", primary_visibility, "for", curve_shape)

def set_casts_shadows(curve, casts_shadows):
    # Get the shape nodes connected to the curve
    curve_shapes = cmds.listRelatives(curve, shapes=True, fullPath=True)
    
    for curve_shape in curve_shapes:
        # Check if the shape node is a NURBS curve
        if cmds.nodeType(curve_shape) != "nurbsCurve":
            continue
        
        # Set the castsShadows attribute
        cmds.setAttr(curve_shape + ".castsShadows", casts_shadows)
        print("Casts shadows set to", casts_shadows, "for", curve_shape)

def apply_curve_settings(curve, shader, width, primary_visibility, casts_shadows):
    set_render_curve(curve, shader)
    set_curve_width(curve, width)
    set_primary_visibility(curve, primary_visibility)
    set_casts_shadows(curve, casts_shadows)
    

def create_ui():
    if cmds.window("curveSettingsWindow", exists=True):
        cmds.deleteUI("curveSettingsWindow", window=True)
    
    # Create the window
    window = cmds.window("curveSettingsWindow", title="Animator's Journey Arnold Curve Renderer", sizeable=True, widthHeight=(300, 250))
    
    # Create a layout
    layout = cmds.columnLayout(adjustableColumn=True, columnAlign="center", rowSpacing=10, parent=window)
    
    # Add a text field to enter the shader name
    shader_text_field = cmds.textFieldGrp(label="Shader Name", adjustableColumn2=1, columnAlign2=("right", "left"), parent=layout)
    
    # Add a slider for curve width
    width_slider = cmds.floatSliderGrp(label="Curve Width", field=True, minValue=0.0, maxValue=100.0, value=0.5,
                                       adjustableColumn2=1, columnAlign2=("right", "left"), parent=layout)
    
    # Add a checkbox for primary visibility
    primary_visibility_checkbox = cmds.checkBox(label="Primary Visibility", value=True, parent=layout)
    
    # Add a checkbox for casts shadows
    casts_shadows_checkbox = cmds.checkBox(label="Casts Shadows", value=True, parent=layout)
    
    # Add a button to apply settings
    apply_button = cmds.button(label="Apply Settings", command=functools.partial(apply_button_clicked, shader_text_field, width_slider, primary_visibility_checkbox, casts_shadows_checkbox))
    
    cmds.showWindow(window)

def apply_button_clicked(shader_text_field, width_slider, primary_visibility_checkbox, casts_shadows_checkbox, *args):
    shader_name = cmds.textFieldGrp(shader_text_field, query=True, text=True)
    width = cmds.floatSliderGrp(width_slider, query=True, value=True)
    primary_visibility = cmds.checkBox(primary_visibility_checkbox, query=True, value=True)
    casts_shadows = cmds.checkBox(casts_shadows_checkbox, query=True, value=True)
    
    # Get the selected objects
    selection = cmds.ls(selection=True, typ="transform")
    shape = cmds.listRelatives(selection, s=1)
    print(f"Shape = {shape}")

    for shp in shape:
        # cmds.setAttr(f"{shp}.aiRenderCurve", 0)
        cmds.setAttr(f"{shp}.aiMode", 1)
    if not selection:
        print("No objects selected.")
        return
        

    # Create a placeholder shader
    for obj in selection:
        apply_curve_settings(obj, shader_name, width, primary_visibility, casts_shadows)


create_ui()