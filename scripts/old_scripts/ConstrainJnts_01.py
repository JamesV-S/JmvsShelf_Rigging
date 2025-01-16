#----------------------------------------
# parent constrain rig_jnts to skn_jnts
#----------------------------------------  
# Select RigJnt 1st, then  sknJnts 2nd

import sys
import maya.cmds as cmds
import importlib

#-------------------------------------
# Set the path for the Module
import find_driver_letter as driver
importlib.reload(driver)

A_driver = driver.get_folder_letter("current_file_path")[:-1]
custom_path = f'{A_driver}\My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools'
#print(f"module path set to {custom_path}")
sys.path.append(custom_path)
#-------------------------------------

import remove_prefix_tool_04_mdl as rmv_pref 
import add_prefix_name_tool_mdl as add_pref
importlib.reload(rmv_pref)
importlib.reload(add_pref)

def p_constrain():
    
    jntRooty = cmds.ls(sl=1)
    #print(jntRooty)
    rig = cmds.listRelatives( jntRooty[0],
                            ad=1, type="joint"
                            )
    rig.append(jntRooty[0])
    rig.reverse()
    #print(rig)
    
    skn = cmds.listRelatives( jntRooty[1],
                            ad=1, type="joint"
                            )
    skn.append(jntRooty[1])
    skn.reverse()
    #print(skn)
    for i in range(len(rig)):
        cmds.parentConstraint(rig[i],skn[i],mo=1)
    
    cmds.select( cl=1 )
    #print("skin:  ", skn)
    
    jntConLs = []
    for i in range(len(skn)):
        jntConLs.append(cmds.listConnections(skn[i], 
                        type='parentConstraint')[0]
                        )
        
    print("JAMES ----- constraint on selected jnts:  ", jntConLs)
    
    new_nm = []
    for i in range(len(skn)):
        new_nm.append(jntConLs[i].split("_"))
    joined_list = ['_'.join(new_nm[i]) for i in range(len(skn))]
     
    #print("joined list is: ", joined_list)
    
    # Remove the first 2 prefix's from constrain made!
    rmv_pref.remove_prefix_tool(joined_list, True, 1,  "jnt_skn")
    con_name_1 = cmds.ls(sl=1)
    #print(con_name_1)
    
    # adding NAME PREF
    add_pref.front_layout_prefix(con_name_1, True, True, "con_prnt")
    con_name_2 = cmds.ls(sl=1)
    #print(con_name_2)
    
    # remove parent constraint from end
    rmv_pref.remove_prefix_tool(con_name_2, 0, 0,  "one")
    
#p_constrain()

