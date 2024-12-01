
import maya.cmds as cmds

selection = cmds.ls(sl=1, type="transform")

def expand_curve_shape(ctrl):
    # shove a transform node in between the shape node and the control(transform).
    shapes = cmds.listRelatives(ctrl, shapes=1, fullPath=1)
    if not shapes:
        cmds.error("No shape nodes found under the control")
    
    # print(f"ctrl name = {ctrl}")
    
    # cr transform node
    if cmds.objExists(f"XFORM_{ctrl[0]}Shape"):
        transform_node = f"XFORM_{ctrl[0]}Shape"
    else:
        transform_node = cmds.group(name=f"XFORM_{ctrl[0]}Shape", em=True)

    # Detach the shape nodes from the original control
    for shp in shapes:
        cmds.parent(shp, transform_node, s=1, relative=1)
    
    # Parent the shape nodes to the original control
    # if not cmds.objExists(f"XFORM_{ctrl[0]}Shape"):
    cmds.parent(transform_node, ctrl, relative=1)
    
    return transform_node

XFORM = expand_curve_shape(selection)

# "XFORM_ctrl_ik_0_clavicle_RShape"

def collapse_curve_shape(transform_node, ctrl):
    print(f"Collapse transform node : {transform_node}")
    
    xform_len = 6
    shape_len = 5
    
    # check for original control transform
    if cmds.objExists(f"{transform_node[xform_len:-shape_len]}"):
        print(f"transform exists :> {transform_node[xform_len:-shape_len]}")

    pos = cmds.getAttr(f"{transform_node}.translate")[0]
    rot = cmds.getAttr(f"{transform_node}.rotate")[0]
    scl = cmds.getAttr(f"{transform_node}.scale")[0]
    # (1.572703563834858, 5.201583350970175, 5.201583350970175)
    print(f"translation = {pos}")
    print(f"rot = {rot}")
    print(f"scale = {scl}")
    #transfrom_dict = {"pos": pos, "rot": rot, "scl":scl}
    #print(transfrom_dict)


    # detach the shape from xform and parent back to the original control transform
    shapes = cmds.listRelatives(transform_node, shapes=1, fullPath=0)
    if not shapes:
        cmds.error("No shape nodes found under the control")
    print(f"xform shape = {shapes}")

    for shp in shapes:
        # Apply transformations to the shape
        cmds.makeIdentity(transform_node, apply=True, t=1, r=1, s=1, n=0)

        cmds.parent(shp, ctrl, s=1, relative=1)
    
    # the attributes on the XFROM are lost, so I need to store them and set them. 
    cmds.setAttr(f"{transform_node}.translate", *pos)
    cmds.setAttr(f"{transform_node}.rotate", *rot)
    cmds.setAttr(f"{transform_node}.scale", *scl)

# collapse_curve_shape(XFORM, selection)

'''
Updated code: `def expand_curve_shape(ctrl):
    # shove a transform node in between the shape node and the control(transform).
    shapes = cmds.listRelatives(ctrl, shapes=1, fullPath=1)
    if not shapes:
        cmds.error("No shape nodes found under the control")
    
    # print(f"ctrl name = {ctrl}")
    
    # cr transform node
    if cmds.objExists(f"XFORM_{ctrl[0]}Shape"):
        transform_node = f"XFORM_{ctrl[0]}Shape"
    else:
        transform_node = cmds.group(name=f"XFORM_{ctrl[0]}Shape", em=True)

    # Detach the shape nodes from the original control
    for shp in shapes:
        cmds.parent(shp, transform_node, s=1, relative=1)
    
    # Parent the shape nodes to the original control
    if not cmds.objExists(f"XFORM_{ctrl[0]}Shape"):
        cmds.parent(transform_node, ctrl, relative=1)
    
    return transform_node

# expand_curve_shape(selection)

XFORM = "XFORM_ctrl_ik_0_clavicle_RShape"

def collapse_curve_shape(transform_node, ctrl):
    print(f"Collapse transform node : {transform_node}")
    
    xform_len = 6
    shape_len = 5
    
    # check for original control transform
    if cmds.objExists(f"{transform_node[xform_len:-shape_len]}"):
        print(f"transform exists :> {transform_node[xform_len:-shape_len]}")

    pos = cmds.getAttr(f"{transform_node}.translate")[0]
    rot = cmds.getAttr(f"{transform_node}.rotate")[0]
    scl = cmds.getAttr(f"{transform_node}.scale")[0]
    # (1.572703563834858, 5.201583350970175, 5.201583350970175)
    print(f"translation = {pos}")
    print(f"rot = {rot}")
    print(f"scale = {scl}")
    #transfrom_dict = {"pos": pos, "rot": rot, "scl":scl}
    #print(transfrom_dict)


    # detach the shape from xform and parent back to the original control transform
    shapes = cmds.listRelatives(transform_node, shapes=1, fullPath=0)
    if not shapes:
        cmds.error("No shape nodes found under the control")
    print(f"xform shape = {shapes}")

    for shp in shapes:
        # Apply transformations to the shape
        cmds.makeIdentity(transform_node, apply=True, t=1, r=1, s=1, n=0)

        cmds.parent(shp, ctrl, s=1, relative=1)
    
    # the attributes on the XFROM are lost, so I need to store them and set them. 
    cmds.setAttr(f"{transform_node}.translate", *pos)
    cmds.setAttr(f"{transform_node}.rotate", *rot)
    cmds.setAttr(f"{transform_node}.scale", *scl)

collapse_curve_shape(XFORM, selection)` -> my 2 functions are A = `expand_curve_shape()` and B = `collapse_curve_shape()`. I don't think function A & B are quite meeting the expectation of what I want. With function A I want to be able to move, rotate and scale the control without effecting the original transform node, thus the intermediate tansform node 'XFORM' and avoid the use of the component mode to shape my control with the cvs. Then for user sake I want to collapse this expanded control with function B. the tricky part is so the transform node is parented to the world, and the shape keeps the transformations from the XFORM, then be able to expand the same control again and the XFORM keeps its transformations data but doesn't change the shape of the control by adding the data onto it which is a problem that happens.  
'''