import maya.cmds as cmds

def front_layout_prefix(obj, before, hi, prefix):
    side = before
    hierarchy = hi
    fst_selection = obj
    
    if hierarchy:
        cmds.select(fst_selection, hi=1)
    else:
        pass
    
    full_list = cmds.ls(sl=1, type='transform')
    
    if side == 1:
        [cmds.rename(full_list[i], prefix + '_' + full_list[i]) for i in range(len(full_list))]
    else:
        [cmds.rename(full_list[i], full_list[i] + '_' + prefix) for i in range(len(full_list))]
    
#front_layout_prefix(cmds.ls(sl=1), True, True, "jnt_rig")

