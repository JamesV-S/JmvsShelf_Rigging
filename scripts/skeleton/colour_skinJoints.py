
import maya.cmds as cmds

def skn_jnt_cl():
    all_joints = cmds.ls(type='joint')
    print(f"all_joints = {all_joints}")
    skn_joints = []
    for jnt in all_joints: 
        if jnt.startswith('jnt_skn'):
            skn_joints.append(jnt)
    
    if skn_joints:
        print(f"skn_joints = `{skn_joints}`")
        for jnt in skn_joints:
            sknJnt_Info = cmds.getAttr( (jnt) + '.overrideEnabled' )
            if sknJnt_Info == 0:
                try:
                    cmds.setAttr(f"{jnt}.overrideEnabled", 1)
                    cmds.setAttr(f"{jnt}.overrideColor", 4)
                except Exception as e:
                    print(f"joint `{jnt}` is in a layer therfore colour is locked")
            else:
                try:
                    cmds.setAttr(f"{jnt}.overrideEnabled", 0)
                except Exception as e:
                    print(f"joint `{jnt}` is in a layer therfore colour is locked")
    else:
        print(f"No skn joint found in the scene!!")
    #for x in range(len(joints)):
    #    jntinfo = cmds.getAttr(f"{joints[x]}.visibility")
    #    if jntinfo == 1:
    #        cmds.setAttr(f"{joints[x]}.visibility", 0)
    #    else:
    #        cmds.setAttr(f"{joints[x]}.visibility", 1)
