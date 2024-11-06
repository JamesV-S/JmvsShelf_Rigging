
import maya.cmds as cmds 

def freeze_rot():
    
    sel = cmds.ls(sl=1, type="transform")
    
    for selecetion in sel:
        cmds.makeIdentity(selecetion, a=1, t=0, r=1, s=0, n=0, pn=1)
    print("did it update?")
        