#-------------------------------------------------------------------------------------------
#
# JMVS controlCreation Tool 
#
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.api.OpenMaya as om

import importlib
import curveCube_class as cCc
import OPM
import csu_cv_col_func
import smpl_mtrans_fnc
#-----------------------------
# new module
import csu_create_ctrls_mdl as cr_ctls
import csu_sel_ctrls_mdl
import csu_rnm_ctrls_mdl as rnm_mdl

importlib.reload(cCc)
importlib.reload(OPM)
importlib.reload(csu_cv_col_func)
importlib.reload(smpl_mtrans_fnc)
#-----------------------------
# new module reload
importlib.reload(cr_ctls)
importlib.reload(csu_sel_ctrls_mdl)
importlib.reload(rnm_mdl)

class jmvs_ctrl_setup():
    def __init__(self):
        
        #global ctl_ls
        #global joint_ls
        # Create a ctrl?
        #----------------------------
        self.create_cv = 1
        #----------------------------
        if self.create_cv:
            print("creating cvs")
        else:
            print("select, cv then joint!")
        # number of ctrls debugging
        if self.create_cv:
            self.ctrl_num = 4
        else:
            self.ctrl_num = 1
        
        #control type
        self.ctrl_type = 0

        if self.ctrl_type:
            print('CRIRCLE')
        else:
            print('CUBE')
        self.Xaxis=(1,0,0)
        self.Yaxis=(0,1,0)
        self.Zaxis=(0,0,1)

        self.sys = "ik"

        self.ZeroOut_Ctrl = 1
        
        self.ctrl_size = 2
        
        self.ctrl_col = 6
        
        self.jnt_sel = cmds.ls(sl=1)
        print('should give me locators ', self.jnt_sel)
        cmds.select(cl=1)
        
        # this works up to here, but the var's 'ctl_ls, joint_ls' are not bing seen by the class
        '''
        cr_ctls.csu_create_controls(self)
        csu_sel_ctrls_mdl.csu_selecting_controls(self)
        '''
        self.ctl_ls = cr_ctls.csu_create_controls(self)
        self.joint_ls = csu_sel_ctrls_mdl.csu_selecting_controls(self)
        smpl_mtrans_fnc.Mtrans(self.ctl_ls, self.joint_ls, self.ctrl_num)
        self.ctrl_list = rnm_mdl.csu_rename_controls(self, self.joint_ls, self.ctl_ls)
        self.csu_clean_controls(self.ctrl_list) 
        #self.csu_create_controls()
        #self.csu_selecting_controls()
        '''
        
        self.csu_rename_controls(joint_ls, ctl_ls)
        #smpl_mtrans_fnc.Mtrans( ctl_ls, joint_ls, self.ctrl_num)
        self.csu_clean_controls(ctrl_list) 
        self.csu_control_size()
        self.csu_ctrl_colour()
        '''

    
    def csu_create_controls(self):
    #creating the control:
        if self.create_cv:
            #put the ctrls into a hierarchy
            if not self.create_cv:
                print('working on one ctrl')
            else:
                print( 'working on ' + str(self.ctrl_num) + ' controllers'  )
            
            if self.ctrl_type:
                create_ctrls = [cmds.circle( n='ctrl_', nr=self.Xaxis, c=(0, 0, 0), sw=360, s=8, ut=0 ) for i in range(self.ctrl_num)]
            else: #This needs to be 
                ctrlCV = []
                for i in range(self.ctrl_num):
                    ctrlCV.append(cmds.curve(n="ctrl_",d=1,p=[(0,0,0),(1,0,0),(1,0,1),(0,0,1),(0,0,0),
                                (0,1,0),(1,1,0),(1,0,0),(1,1,0),
                                (1,1,1),(1,0,1),(1,1,1),
                                (0,1,1),(0,0,1),(0,1,1),(0,1,0)]))
            
                    cmds.CenterPivot()
                cmds.xform(ctrlCV,t=(-.5,-.5,-.5))
                cmds.select(ctrlCV)
                cmds.FreezeTransformations()
                cmds.rename("ctrl_", ignoreShape=1)
                cmds.delete(ctrlCV, ch=1)
                                    
            # Put controls into correct hierarchy 
            if self.ctrl_type:
                ctl_sl = [cmds.ls( create_ctrls[i], type='transform' ) for i in range(self.ctrl_num)]
                ctrlCV = [element for sublist in ctl_sl for element in sublist]
                for i in range(self.ctrl_num-1): 
                    cmds.parent( ctrlCV[i+1], ctrlCV[i] )
                cmds.select(cl=1)
            else:
                for i in range(self.ctrl_num-1): 
                    cmds.parent( ctrlCV[i+1], ctrlCV[i] )
                cmds.select(cl=1)
        else:
            print("didn't create new cvs on purpose")
        global ctl_ls
        ctl_ls = ctrlCV
        
        print('HERE_IS_ctrls_ls:', ctl_ls)

    def csu_selecting_controls(self):
        # select curve if not creating new ones:
        # select the control & joint, putting them in variables
        if not self.create_cv:
            ctrl_selection = cmds.ls(sl=1, type='transform')
            print(ctrl_selection)
            cmds.select(ctrl_selection[0]) 
            ctrlCV = cmds.ls(sl=1)
            print('selecting cv then joint', ctrlCV)
            jnt = cmds.ls(ctrl_selection[1])
            print(jnt)
                        
        else:# select the controls list created  
            cmds.select(self.jnt_sel, hi=1)
            jnt = cmds.ls(sl=1, type='transform')
            print(jnt) #['jnt_rig_hip_l', 'boneCV_knee_l', 'boneCV_calf_l', 'boneCV_foot_l']
        global joint_ls
        joint_ls = jnt

        for i in range( self.ctrl_num ):
          cmds.matchTransform( ctl_ls[i], joint_ls[i] )
    
    #----------------------------
    def csu_rename_controls(self, obj_split, fst_name):
        rnm_hi_list = []
        for i in range(len(obj_split)):
            rnm_hi_list.append(obj_split[i].split('_')[-2:])    
                            
        joined_list = ['_'.join(rnm_hi_list[i]) for i in range(len(obj_split))]
                
        for i in range(self.ctrl_num):
            print(fst_name[i])
            print(joined_list[i])
            cmds.rename( fst_name[i], ("ctrl_" + self.sys + '_' + joined_list[i]) )
        global ctrl_list
        ctrl_list = [("ctrl_" + self.sys + '_' + joined_list[i]) for i in range(self.ctrl_num)]
      
    
    def csu_clean_controls(self, obj_sl):
        # Zero out the control with OPM method   
        if self.ZeroOut_Ctrl:
            cmds.select(obj_sl)
            OPM.OpmCleanTool()
            print('cleaned controls: ', obj_sl)
            #cmds.select(cl=1)
           
    
    def csu_control_size(self):
        # Scale the curve or curves
        #ctrl_size = 4
        for i in range(self.ctrl_num):
            #cmds.scale(.25,.25,.25, ctrl_list[i] + 'Shape.cv[0:7]', r=1 )
            if self.ctrl_type:
                cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, self.ctrl_list[i] + 'Shape.cv[0:7]', r=1 )
            else:
                pass
                cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, (f"curveShape{i+1}") + '.cv[0:15]', r=1 )
        
    # change color of ctrl
    def csu_ctrl_colour(self):
        try:
            cmds.select(self.ctrl_list) 
            csu_cv_col_func.override_color_(self.ctrl_col)
            cmds.select(cl=1)
        except:
            cmds.error( "can't change ther colour of this control" )
     
jmvs_ctrl_setup()        
     