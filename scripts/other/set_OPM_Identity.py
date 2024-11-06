
import maya.cmds as cmds

def reset_obj_identity():

    sel = cmds.ls(sl=1)
    
    temp_grp = [ cmds.group(em=1) for x in range(len(sel))]
    
    identity_matrix = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
    #cmds.setAttr('pSphere1.offsetParentMatrix', *identity_matrix, type='matrix')

    for obj in sel:
        cmds.matchTransform(temp_grp, obj)
        cmds.setAttr(f"{obj}.offsetParentMatrix", *identity_matrix, type='matrix')
        cmds.matchTransform(obj, temp_grp)
    cmds.delete(temp_grp)
    cmds.select(sel)
    
reset_obj_identity()