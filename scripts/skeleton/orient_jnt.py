import maya.cmds as cmds 

def orient_last_joint():
    
    cmds.ls(sl=1, type='joint')
    
    cmds.joint( e=1, oj="none", ch=1, zso=1 )

    print("jnt orientated to one before it")

