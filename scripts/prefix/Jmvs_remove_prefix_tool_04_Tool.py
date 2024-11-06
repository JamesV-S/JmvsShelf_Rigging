#-------------------------------------------------#
#                     CODE                        #
#-------------------------------------------------#
import maya.cmds as cmds 

# searchReplaceNames "rig_" "\n" "hierarchy"
# IF there is a Letter in another part of name, like 'r', and you try to remove it, it bugs out.  

def remove_prefix_tool(bfr, hi, prefix):
    before = bfr
    
    hierarchy = hi

    pref_val = prefix

    # Must ALWAYS split the selected name at the very beginning no matter what 
    obj_name = cmds.ls(sl=1)
    #['jnt_rig_hip_l']
    
    if hierarchy:
        cmds.select(obj_name, hi=1)
        
    full_selection_ls = cmds.ls( sl=1, type='transform' )
    undo_num = len(full_selection_ls) 
    #print("joints selected - ", full_selection_ls)# ['jnt_rig_hip_l', 'jnt_rig_knee_l', 'jnt_rig_calf_l', 'jnt_rig_foot_l']
    
    def rename_controls(obj_split):
        if before:
            rnm_hi_list = []
            for i in range(len(obj_split)):
                rnm_hi_list.append(obj_split[i].split('_')[pref_val:])  
        else:
            rnm_hi_list = []
            for i in range(len(obj_split)):
                rnm_hi_list.append(obj_split[i].split('_')[:-pref_val])   
                            
        joined_list = ['_'.join(rnm_hi_list[i]) for i in range(len(obj_split))]
        #print("split list: ", rnm_hi_list)
        #print("joined list: ", joined_list)
        
                
        for i in range(len(obj_split)): # number of joints selected
            cmds.rename( obj_split[i], (joined_list[i]) ) # self.sys = 'ik'
        #global ctrl_list
        [("ctrl_" + joined_list[i]) for i in range(len(obj_split))]
        
        #return ctrl_list
    rename_controls(full_selection_ls)

    return undo_num

    
#remove_prefix_tool( 1, 1, 2)
