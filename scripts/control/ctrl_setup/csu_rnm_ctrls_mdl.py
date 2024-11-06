import maya.cmds as cmds

def csu_rename_controls(self, obj_split, fst_name, num_ctrl, sys_pref):
        print("within csu_rename_module this is the joint! -> ", obj_split)
                           
        global ctrl_list
        if self.create_cv:
            rnm_hi_list = []
            for i in range(len(obj_split)):
                rnm_hi_list.append(obj_split[i].split('_')[-2:])    
            print("within rnm_module, renamed name: ", rnm_hi_list) 

            joined_list = ['_'.join(rnm_hi_list[i]) for i in range(len(obj_split))]
            for i in range(num_ctrl):
                print(fst_name[i])
                print(joined_list[i])
                cmds.rename( fst_name[i], (f"ctrl_{sys_pref}_{joined_list[i]}") )
            ctrl_list = [("ctrl_" + sys_pref + '_' + joined_list[i]) for i in range(num_ctrl)]
        else:
             rnm_hi_list = obj_split.split('_')[-2:]
             joined_list = '_'.join(rnm_hi_list)
             print("within rnm_module, renamed name: ", rnm_hi_list)
             print("within rnm_module, fst name: ", fst_name)
             print("within rnm_module, second name: ", joined_list)
             cmds.rename( fst_name, f"ctrl_{sys_pref}_{joined_list}")
             ctrl_list = f"ctrl_{sys_pref}_{joined_list}"
        return ctrl_list