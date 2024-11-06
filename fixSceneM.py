import maya.cmds as cmds

def fixSccene():
    cmds.jointDisplayScale(1.5)
    cmds.ikHandleDisplayScale(5)
    cmds.manipPivot(mto=0)

    print("Scene Fixed")
