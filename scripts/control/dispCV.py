import maya.cmds as cmds

def displayCVs():
    Sel = cmds.ls(sl=1)
    
    if not Sel:
        cmds.error("Please select a nurbs curve")
    else:
        newSel = cmds.ls(sl=1)
       
    for x in range(len(newSel)):
        cvinfo = cmds.getAttr(str(newSel[x]) + '.dispCV')
        if cvinfo == 0:
            cmds.setAttr(newSel[x] + '.dispCV', 1)
        else:
            cmds.setAttr(newSel[x] + '.dispCV', 0)

