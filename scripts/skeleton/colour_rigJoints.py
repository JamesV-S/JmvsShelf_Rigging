
import maya.cmds as cmds

def rig_jnt_cl():
    all_joints = cmds.ls(type='joint')
    print(f"all_joints = {all_joints}")
    rig_joints = []
    for jnt in all_joints: 
        if jnt.startswith('jnt_rig'):
            rig_joints.append(jnt)
    
    if rig_joints:
        print(f"rig_joints = `{rig_joints}`")
        for jnt in rig_joints:
            rigJnt_Info = cmds.getAttr( (jnt) + '.overrideEnabled' )
            if rigJnt_Info == 0:
                try:
                    cmds.setAttr(f"{jnt}.overrideEnabled", 1)
                    cmds.setAttr(f"{jnt}.overrideColor", 17)
                except Exception as e:
                    print(f"joint `{jnt}` is in a layer therfore colour is locked")
            else:
                try:
                    cmds.setAttr(f"{jnt}.overrideEnabled", 0)
                except Exception as e:
                    print(f"joint `{jnt}` is in a layer therfore colour is locked")
    else:
        print(f"No rig joint found in the scene!!")
    #for x in range(len(joints)):
    #    jntinfo = cmds.getAttr(f"{joints[x]}.visibility")
    #    if jntinfo == 1:
    #        cmds.setAttr(f"{joints[x]}.visibility", 0)
    #    else:
    #        cmds.setAttr(f"{joints[x]}.visibility", 1)
