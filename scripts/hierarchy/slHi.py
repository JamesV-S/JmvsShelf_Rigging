import maya.cmds as cmds

def selectHi():
    sel = cmds.ls(sl=1, type="transform")
    cmds.select(sel, hi=1)
    newSel = cmds.ls(sl=1, type='transform')
    print(newSel)