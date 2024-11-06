import maya.cmds as cmds

def override_color_(clr_num):
    sel = cmds.ls(selection=True)
    shape = cmds.listRelatives( sel, shapes = True )
    #add = cmds.select( add=True )
    for node in shape:
        cmds.setAttr (node + ".overrideEnabled" ,True)
        cmds.setAttr (node + ".overrideColor" , clr_num)