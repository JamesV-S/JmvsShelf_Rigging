#-------------------------------------------------------------------------------------------
#
# JMVS Bind_Skin_Tool 
#
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds

def bindSkinTool():
    
    createQuiSelSet = 1
    
    if createQuiSelSet:
        
        # select joints
        rootJnt = cmds.ls(sl=1)
        cmds.select( rootJnt[0], hi=1 )
        full_joint_list = cmds.ls(sl=1, type='joint')
        
        # Remove unwanted joints from selection
        ignoreJnts = [ '*_upperarm', '*_thigh', '*_hand_twist', '*_foot_twist' ]
        cmds.select( ignoreJnts, d=1 )
        
        # Create quick selection set
        cmds.CreateQuickSelectSet()
        
    else: # Bind Skin tool:
        
        QuickSelSET = 'bindJoints'
        SkinningMesh001 = 'body_game' #The geo af a character will change for every rig 
        
        JOINTS = ['joint1', 'joint2', 'joint3']
        MESH = 'pPlane1'
        
        # Select Bind joints 
        cmds.select( QuickSelSET )
        
        # Add mesh to selection
        cmds.select( SkinningMesh001, tgl=1 )
        
        #Apply SkinCluster to the mesh
        cmds.skinCluster( JOINTS, MESH, dr=4.5 )
        
        '''cmds.skinCluster( QuickSelSET, SkinningMesh001, dr=4.5 )
        cmds.skinCluster( 'joint1', 'pPlane1', dr=4.5)'''
        
bindSkinTool()