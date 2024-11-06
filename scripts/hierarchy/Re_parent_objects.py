
import maya.cmds as cmds

def re_parent_objects():
    sel = cmds.ls(sl=1)
    sel.reverse()

    for i in range(len(sel)):
        if sel[i] == sel[-1]:
            continue
        cmds.parent(sel[i], sel[i+1])

