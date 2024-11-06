import maya.cmds as cmds

def csu_selecting_controls(self, jnt_sel):
        # select curve if not creating new ones:
        # select the control & joint, putting them in variables
        if not self.create_cv: # working on an existing control
            ctrl_selection = cmds.ls(sl=1, type='transform')
            #print('ctrl_selection right here = ', ctrl_selection)
            #cmds.select(ctrl_selection[0]) 
            ctrlCV = ctrl_selection[0] # cmds.ls(sl=1)
            #print('within csu_sel_controls, control is: ', ctrlCV)
            jnt = ctrl_selection[1]
            #print("within csu_sel_controls, joint is: ", jnt) # ['jnt_rig_base_2']
                        
        else:# select the controls list created  
            cmds.select(jnt_sel, hi=1)
            jnt = cmds.ls(sl=1, type='transform')
            print(jnt) #['jnt_rig_hip_l', 'boneCV_knee_l', 'boneCV_calf_l', 'boneCV_foot_l']
        global joint_ls
        joint_ls = jnt

        print('within csu_SEL, joint is: ', joint_ls)
        
        if self.create_cv:
             return joint_ls
        else:
             print("within csu_SEL, control is: ", ctrlCV)
             return joint_ls, ctrlCV
