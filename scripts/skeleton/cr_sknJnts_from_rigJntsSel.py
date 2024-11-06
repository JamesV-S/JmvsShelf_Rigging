
import sys
import maya.cmds as cmds
import importlib

#-------------------------------------
# Set the path for the Module
from Jmvs_letter_driver_script import find_driver_letter
importlib.reload(find_driver_letter)

A_driver = find_driver_letter.get_folder_letter("Jmvs_current_file_path")
custom_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools'
print(f"module path set to {custom_path}")
sys.path.append(custom_path)
#-------------------------------------

import remove_prefix_returned_list_only as rmv_pref
importlib.reload(rmv_pref)

def produce_sknJnts_from_rig_jnts_sel():
    sel = cmds.ls(sl=1, type='joint')
    cmds.select(sel, hi=1)

    # Get the list of joints in the selection, excluding any parent constraints
    jntList = []
    for obj in cmds.ls(sl=1):
        if cmds.nodeType(obj) == 'joint':
            jntList.append(obj)
    print("rig_jnts = ", jntList)
    
    #------------------------------  
    # Create skn joints from it!
    jnt_name = "jnt_skn_"
    # need a list of the selected joints without their first two prefix!
    base_names_list = rmv_pref.remove_prefix_tool(jntList, 1, 0,  "jnt_rig", 1)
    print(base_names_list)
    
    cmds.select(cl=1)
    skn_jnts_list = [cmds.joint(n=f"{jnt_name}{base_names_list[x]}") for x in range(len(jntList))]
    print("skn_jnts = ", skn_jnts_list)
    for x in range(len(jntList)):
        cmds.matchTransform(skn_jnts_list[x], jntList[x])
        cmds.makeIdentity(skn_jnts_list[x], a=1, t=0, r=1, s=0, n=0, pn=1)
        cmds.parentConstraint( jntList[x], skn_jnts_list[x] )
    cmds.select(cl=1)
    
    # rename parentconstraints on the skn joints
    skn_jntConLs = cmds.listRelatives(skn_jnts_list, type='parentConstraint')
    for x in range(len(skn_jntConLs)):
        cmds.rename( skn_jntConLs[x], f"sknPcons_{base_names_list[x]}")
 
#produce_sknJnts_from_rig_jnts_sel()

    