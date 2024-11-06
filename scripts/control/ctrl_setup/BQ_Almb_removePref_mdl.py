#-------------------------------------------------#
#                     CODE                        #
#-------------------------------------------------#
import maya.cmds as cmds 

# searchReplaceNames "rig_" "\n" "hierarchy"
# IF there is a Letter in another part of name, like 'r', and you try to remove it, it bugs out.  

def remove_prefix_tool(root_obj, bfr, hi, prefix):
    before = bfr
    
    hierarchy = hi
    #fst_selection = cmds.ls(sl=1)
    
    #check for prefix:
    pref_check = prefix[-1:]
    print('does the prefix have an "_"? = ', pref_check)# '_'
    
    # Make sure the prefix is usable 
    if "_" in pref_check:
        print( 'this prefix has underscore at the end' )
        val_01 = prefix.split('_') #['jnt', 'rig', '']
        pref_val = len(val_01)-1
        print('number of specified prefix = ', pref_val) # 3, i need it to be 2 if in this condition!
    else:
        print( 'this prefix does NOT hv underscore at the end' )
        val_01 = prefix.split('_') #['jnt', 'rig']
        pref_val = len(val_01)
        print('number of specified prefix = ', pref_val)# 2, this is good
    
    # Must ALWAYS split the selected name at the very beginning no matter what 
    obj_name = root_obj
    #['jnt_rig_hip_l']
    
    if hierarchy:
        cmds.select(obj_name, hi=1)
        
    full_selection_ls = cmds.ls( sl=1, type='transform' )
    print("joints selected - ", full_selection_ls)# ['jnt_rig_hip_l', 'jnt_rig_knee_l', 'jnt_rig_calf_l', 'jnt_rig_foot_l']
 
    def csu_rename_controls(obj_split):
        if before:
            rnm_hi_list = []
            for i in range(len(obj_split)):
                rnm_hi_list.append(obj_split[i].split('_')[pref_val:])  
        else:
            rnm_hi_list = []
            for i in range(len(obj_split)):
                rnm_hi_list.append(obj_split[i].split('_')[:-pref_val])   
                            
        joined_list = ['_'.join(rnm_hi_list[i]) for i in range(len(obj_split))]
        print("split list: ", rnm_hi_list)
        print("joined list: ", joined_list)
        
                
        for i in range(len(obj_split)): # number of joints selected
            cmds.rename( obj_split[i], (joined_list[i]) ) # self.sys = 'ik'
        #global ctrl_list
        [("ctrl_" + joined_list[i]) for i in range(len(obj_split))]
        
        #return ctrl_list
    csu_rename_controls(full_selection_ls)

    
#remove_prefix_tool(cmds.ls(sl=1), 0, 0,  "jnt")
