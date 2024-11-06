
import maya.cmds as cmds

def H_jnts():
    joints = cmds.ls(type='joint')
    for x in range(len(joints)):  
        jntinfo = cmds.getAttr(f"{joints[x]}.visibility")
        if jntinfo == 1:
            cmds.setAttr(f"{joints[x]}.visibility", 0)
        else:
            cmds.setAttr(f"{joints[x]}.visibility", 1)
