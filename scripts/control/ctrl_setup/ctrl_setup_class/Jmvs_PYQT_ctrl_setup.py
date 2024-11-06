

import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide6.QtCore import *
from PySide6.QtGui import *
#suggested fix from PySide6.QtWidgets import QWidget, QUiLoader, QApplication, QPushButton, QVBoxLayout, QFileDialog, QLabel, QSpinBox
#class main_ui(QWidget):
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *
from shiboken6 import wrapInstance
import os.path

import sys
import importlib
from Jmvs_letter_driver_script import find_driver_letter 
importlib.reload(find_driver_letter)

A_driver = find_driver_letter.get_folder_letter("Jmvs_current_file_path")
custom_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/Jmvs_ctrl_setup_tool/ui_scripts' # Jmvs_ctrl_setup_tool\ui_scripts
another_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/Jmvs_ctrl_setup_tool'
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


mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


class QtSampler(QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSampler,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Jmvs Ctrl Setup Tool")
        self.initUI()
        
        # - location to write commands to activate button..
        #self.ui.qt_button_name.clicked.connect(self.button_function)
        self.ui.scale_spnB.valueChanged.connect(self.scale_of_ctrl)
        self.ui.axs_ddbx.currentIndexChanged.connect(self.axs_dir_ddbox)
        self.ui.zero_out_checkBx.stateChanged.connect(self.clean_ctrls)
        self.ui.num_ctrl_line.textChanged.connect(self.num_ctrl_input)
        self.ui.new_ctrl_ddp.currentIndexChanged.connect(self.cr_nw_ctrl)
        self.ui.type_ctrl_ddbox.currentIndexChanged.connect(self.ctrl_type_func)
        self.ui.sys_type_line.textChanged.connect(self.sys_type)
        self.ui.colour_line.textChanged.connect(self.ctl_colour)
        self.ui.apply_btn.clicked.connect(self.apply_func)
        global create_cv    

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_FILE = f'{A_driver}My_RIGGING/JmvsSCRIPTS/Jmvs_ctrl_setup_tool/ui_scripts/jmvs_ctrl_setup.ui'
        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()
    #---------------------------------------------------------------------------------------------------------------------
    # here are functions I created for the buttons in the ui interface!    
    def scale_of_ctrl(self):
        try:
            self.ctrl_size = self.ui.scale_spnB.value()
            self.ctrl_size = float(self.ctrl_size)# change 'Value' to the right one in script
            print(f"scale: {self.ctrl_size}")
        except ValueError:
            print( 'no string values allowed' )

    # Axis direction, drop_down_box x3        
    def axs_dir_ddbox(self):
        temp_xyz = self.ui.axs_ddbx.currentText()
        self.Xaxis=(1,0,0)
        self.Yaxis=(0,1,0)
        self.Zaxis=(0,0,1)
        if temp_xyz == 'X':
            self.Axis = self.Xaxis
        elif temp_xyz == 'Y':
            self.Axis = self.Yaxis
        else:
            self.Axis = self.Zaxis
        print(str(temp_xyz))
        return self.Xaxis, self.Yaxis, self.Zaxis

    # Zero_out my controls:   
    def clean_ctrls(self):
        temp_zero_out = self.ui.zero_out_checkBx.isChecked()
        if temp_zero_out == True:
            self.ZeroOut_Ctrl = 1
        else:
            self.ZeroOut_Ctrl = 0
        print(temp_zero_out)

    # number of controls to create!     
    def num_ctrl_input(self):
        try: 
            if self.create_cv:
                self.ctrl_num = self.ui.num_ctrl_line.text()
                self.ctrl_num = int(self.ctrl_num)
                print(self.ctrl_num)
            else:
                self.ctrl_num = 1
                self.ctrl_num = int(self.ctrl_num)
        except ValueError:
            print( 'no string values allowed' )
        return self.ctrl_num

    # Master varable:(var dictates a lot decisons within the code ), drop_down x2.
    # Create a new control? + grey out other variables if master = False!!  
    def cr_nw_ctrl(self):
        temp_create_cv = self.ui.new_ctrl_ddp.currentText()
        if temp_create_cv == 'Yes':
            self.create_cv = 1 
            self.ui.num_ctrl_line.setDisabled(False)
        else:
            self.create_cv = 0
            self.ui.num_ctrl_line.setDisabled(True)
        return self.create_cv

    # Type of control, drop_down x2   
    def ctrl_type_func(self):
        temp_type = self.ui.type_ctrl_ddbox.currentText()
        if temp_type == 'Circle':
            self.ctrl_type = 1
        else:
            self.ctrl_type = 0
        print(temp_type)
        return self.ctrl_type

    # naming System type   
    def sys_type(self):
            self.sys = self.ui.sys_type_line.text()
            self.sys = str(self.sys)
            print(self.sys)
    
    # Colour of the control!
    def ctl_colour(self):
        try: 
            self.ctrl_col = self.ui.colour_line.text()
            self.ctrl_col = int(self.ctrl_col)
            print(self.ctrl_col)
        except ValueError:
            print( 'no string values allowed' )
    
    #---------------------------------------------------------------------------------------------------------------------
    # Here are the small functons from the setup_ctrls_tool that i didn't put into modules. 
    def csu_clean_controls(self, obj_sl):
        # Zero out the control with OPM method   
        if self.ZeroOut_Ctrl:
            cmds.select(obj_sl)
            OPM.OpmCleanTool()
            print('cleaned controls: ', obj_sl)
                       
    
    def csu_control_size(self):
        for i in range(self.ctrl_num):
            if self.ctrl_type:
                if self.create_cv:
                    cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, self.ctrl_list[i] + 'Shape.cv[0:7]', r=1 )
                else:
                    cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, self.ctrl_list + 'Shape.cv[0:7]', r=1 )
            else:
                if self.create_cv:
                    cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, (f"curveShape{i+1}") + '.cv[0:15]', r=1 )
                else:
                    cmds.scale(self.ctrl_size,self.ctrl_size,self.ctrl_size, (f"curveShape") + '.cv[0:15]', r=1 )
        
    # change color of ctrl
    def csu_ctrl_colour(self):
        try:
            cmds.select(self.ctrl_list) 
            csu_cv_col_func.override_color_(self.ctrl_col)
            cmds.select(cl=1)
        except:
            cmds.error( "can't change ther colour of this control" )
    #---------------------------------------------------------------------------------------------------------------------
            
    def apply_func(self):

        self.create_cv = self.cr_nw_ctrl()
        self.ctrl_type = self.ctrl_type_func()
        self.Xaxis = self.axs_dir_ddbox()
        self.ctrl_num = self.num_ctrl_input()
        
        self.jnt_sel = cmds.ls(sl=1)
        print("joints selected ", self.jnt_sel)
        
        if self.create_cv:
            cmds.select(cl=1)

        print('apply button pressed')
        # call upon the modules you need to complete the task
        self.ctl_ls = cr_ctls.csu_create_controls(self, self.ctrl_num, self.Axis)
        if self.create_cv:
            self.joint_ls = csu_sel_ctrls_mdl.csu_selecting_controls(self, self.jnt_sel)
        else:
            self.joint_ls, self.ctl_ls  = csu_sel_ctrls_mdl.csu_selecting_controls(self, self.jnt_sel) # called 'self.ctl_ls' because 
        print("J_joint list, ", self.joint_ls)
        print("J_control list, ", self.ctl_ls)
        # i had to return the 'ctl_ls' var again for when 'create_cv=0'!
        smpl_mtrans_fnc.Mtrans(self, self.ctl_ls, self.joint_ls, self.ctrl_num)
        self.ctrl_list = rnm_mdl.csu_rename_controls(self, self.joint_ls, self.ctl_ls, self.ctrl_num, self.sys)
        
        # IF you want to call OPM or not!
        if self.ZeroOut_Ctrl:
            self.csu_clean_controls(self.ctrl_list)
        else:
            pass
        self.csu_control_size()
        self.csu_ctrl_colour()        
       
def main():
    ui = QtSampler()
    ui.show()
    return ui
    
if __name__ == '__main__':
    main()
