
import maya.cmds as cmds

def sel_Parent_Con_from_jnts():
    sel = cmds.ls(sl=1, type='joint')
    cmds.select(sel, hi=1)
    full_sel = cmds.ls(sl=1)
    cmds.select(cl=1)
    
    skn_jntConLs = cmds.listRelatives(full_sel, type='parentConstraint') # parentConstraint aimConstraint
    print(skn_jntConLs)
    cmds.select(skn_jntConLs)
