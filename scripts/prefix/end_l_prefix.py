import maya.cmds as cmds 

def endPrefix():

    selection = cmds.ls(sl=1)
    cmds.select(selection, hi=1)
    full_list = cmds.ls(sl=1, type='transform')

    for i in range(len(full_list)):
        cmds.rename( full_list[i], full_list[i] + '_L' )
    
    
#cmds.rename('sphere1', 'spinning_ball')