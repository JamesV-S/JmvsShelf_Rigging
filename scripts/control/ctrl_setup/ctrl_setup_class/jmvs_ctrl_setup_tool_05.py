
#-------------------------------------------------------------------------------------------
#
# JMVS controlCreation Tool 
#
#-------------------------------------------------------------------------------------------

import sys

import maya.cmds as cmds
import maya.api.OpenMaya as om

import importlib

import find_driver_letter as driver
importlib.reload(driver)

A_driver = driver.get_folder_letter("Jmvs_current_file_path")
custom_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/Jmvs_ctrl_setup_tool'
another_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/shelf_tools' # for the OPM module
print(f"module imported from {custom_path}") 
sys.path.append(custom_path)
sys.path.append(another_path)

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
        #----------------------------
        self.create_cv = 0
        
        if self.create_cv:
            print("creating cvs")
        else:
            print("select, cv then joint!")
        
        # number of ctrls debugging
        if self.create_cv:
            self.ctrl_num = 5
        else:
            self.ctrl_num = 1
        
        self.ctrl_type = 1

        self.Xaxis=(1,0,0)
        self.Yaxis=(0,1,0)
        self.Zaxis=(0,0,1)
        self.Axis = self.Yaxis

        self.sys = "ik"

        self.ZeroOut_Ctrl = 1
        
        self.ctrl_size = 1.5
        
        self.ctrl_col = 6
        #-----------------------------------------
        self.jnt_sel = cmds.ls(sl=1)
        print("joints selected ", self.jnt_sel)
        
        if self.create_cv:
            cmds.select(cl=1)
        #-----------------------------------------

        # 'self.ctl_ls' is a global variable from 'cr_ctls' module, that i returned in the fnction and assigning it here so it's known
        self.ctl_ls = cr_ctls.csu_create_controls(self, self.ctrl_num, self.Axis)[0]
        self.joint_ls= csu_sel_ctrls_mdl.csu_selecting_controls(self, self.jnt_sel)[0]
        print("J_joint list, ", self.joint_ls) # should be a single 'jnt_rig_base_#'
        print("J_control list, ", self.ctl_ls) # should be a single 'ctrl_type_shit_'
        smpl_mtrans_fnc.Mtrans(self, self.ctl_ls, self.joint_ls, self.ctrl_num)
        self.ctrl_list = rnm_mdl.csu_rename_controls(self, self.joint_ls, self.ctl_ls, self.ctrl_num, self.sys)
        self.csu_clean_controls(self.ctrl_list)
        self.csu_control_size()
        self.csu_ctrl_colour()    
    #-----------------------------------------
    def csu_clean_controls(self, obj_sl):
        # Zero out the control with OPM method   
        if self.ZeroOut_Ctrl:
            cmds.select(obj_sl)
            OPM.OpmCleanTool()
            print('cleaned controls: ', obj_sl)
    
    def csu_control_size(self):
        for i in range(self.ctrl_num):
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
     