

import maya.cmds as cmds
from maya import OpenMayaUI

try:
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem
    from PySide6.QtWidgets import (QWidget)
    from shiboken6 import wrapInstance
except ModuleNotFoundError:
    from PySide2 import QtCore, QtWidgets, QtGui
    from PySide2.QtCore import Qt, Signal
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import (QWidget)
    from shiboken2 import wrapInstance

import sys
import importlib
import os.path

# from JmvsShelf_Rigging.scripts. import utils as util

from JmvsShelf_Rigging.scripts.data import func_path_of_python_file as getpath
from JmvsShelf_Rigging.scripts.other import OPM

from JmvsShelf_Rigging.scripts.control.ctrl_setup import (
    csu_cv_col_func,
    smpl_mtrans_fnc,
    curveCube_class,

    csu_create_ctrls_mdl,
    csu_sel_ctrls_mdl,
    csu_rnm_ctrls_mdl
)

importlib.reload(getpath)
importlib.reload(OPM)

importlib.reload(csu_cv_col_func)
importlib.reload(smpl_mtrans_fnc)
importlib.reload(curveCube_class)
importlib.reload(csu_create_ctrls_mdl)
importlib.reload(csu_sel_ctrls_mdl)
importlib.reload(csu_rnm_ctrls_mdl)

maya_main_wndwPtr = OpenMayaUI.MQtUtil.mainWindow()
main_window = wrapInstance(int(maya_main_wndwPtr), QWidget)

def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

class ctrlSetupTool(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ctrlSetupTool, self).__init__(parent)
        version = "001"
        ui_object_name = f"ctrlSetupTool{version}"
        ui_window_name = f"ctrl setup tool V{version}"
        delete_existing_ui(ui_object_name)
        self.setObjectName(ui_object_name)

        # Set flags & dimensions
        self.setParent(main_window)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(ui_window_name)
        self.resize(350, 150)
        
        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                       "..",  "..", "style_interface", "CSS", "geoDB_style_sheet_001.css")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        self.ZeroOut_Ctrl = 1
        self.ctrl_size = 5
        self.ctrl_col = 13
        self.UI()
        self.UI_connect_signals()
        

    def UI(self):
        main_Vlayout = QtWidgets.QVBoxLayout(self)
        #----------------------------------------------------------------------
        # ---- grid layout ----
        layH_grids = QtWidgets.QHBoxLayout()
        layGrid_left = QtWidgets.QGridLayout()
        layGrid_right = QtWidgets.QGridLayout()
        layGrid_right.setContentsMargins(10, 0, 0, 0)
        layH_grids.addLayout(layGrid_left)
        layH_grids.addLayout(layGrid_right)
        
        # -- grid content L --
        new_ctrl_lbl = QtWidgets.QLabel("New control?")
        self.new_ctrl_comboBox = QtWidgets.QComboBox()
        self.new_ctrl_comboBox.addItems(["Yes", "No"])
        layGrid_left.addWidget(new_ctrl_lbl, 0,0 )
        layGrid_left.addWidget(self.new_ctrl_comboBox, 0,1 )

        num_ctrls_lbl = QtWidgets.QLabel("number of controls")
        self.num_ctrl_text = QtWidgets.QLineEdit()
        self.num_ctrl_text.setText("4")
        layGrid_left.addWidget(num_ctrls_lbl, 1,0 )
        layGrid_left.addWidget(self.num_ctrl_text, 1,1 )

        clean_ctrls_lbl = QtWidgets.QLabel("Clean controls:")
        self.clean_ctrls_checkBox = QtWidgets.QCheckBox()
        self.clean_ctrls_checkBox.setChecked(True)
        layGrid_left.addWidget(clean_ctrls_lbl, 2,0 )
        layGrid_left.addWidget(self.clean_ctrls_checkBox, 2,1 )

        scale_value_lbl = QtWidgets.QLabel("Control scale:")
        self.scale_value_dSpinBox = QtWidgets.QDoubleSpinBox()
        self.scale_value_dSpinBox.setValue(5)
        layGrid_left.addWidget(scale_value_lbl, 3,0 )
        layGrid_left.addWidget(self.scale_value_dSpinBox, 3,1 )

        # -- grid content R --
        ctrl_type_lbl = QtWidgets.QLabel("Control type?")
        self.ctrl_type_comboBox = QtWidgets.QComboBox()
        self.ctrl_type_comboBox.addItems(["Circle", "Cube"])
        layGrid_right.addWidget(ctrl_type_lbl, 0,0 )
        layGrid_right.addWidget(self.ctrl_type_comboBox, 0,1 )

        sys_type_lbl = QtWidgets.QLabel("Sys type: ")
        self.sys_type_text = QtWidgets.QLineEdit()
        self.sys_type_text.setText("fk")
        layGrid_right.addWidget(sys_type_lbl, 1,0 )
        layGrid_right.addWidget(self.sys_type_text, 1,1 )

        axis_direction_lbl = QtWidgets.QLabel("Axis direction:")
        self.axis_direction_comboBox = QtWidgets.QComboBox()
        self.axis_direction_comboBox.addItems(["X", "Y", "Z"])
        layGrid_right.addWidget(axis_direction_lbl, 2,0 )
        layGrid_right.addWidget(self.axis_direction_comboBox, 2,1 )

        colour_lbl = QtWidgets.QLabel("Colour:")
        self.colour_text = QtWidgets.QLineEdit()
        self.colour_text.setText("13")
        layGrid_right.addWidget(colour_lbl, 3,0 )
        layGrid_right.addWidget(self.colour_text, 3,1 )
        
        # -- Apply button --
        self.apply_btn = QtWidgets.QPushButton("Apply")

        # add to main layout
        main_Vlayout.addLayout(layH_grids)
        main_Vlayout.addWidget(self.apply_btn)
        
        self.setLayout(main_Vlayout)

    def UI_connect_signals(self):
        # -- grid L --
        self.new_ctrl_comboBox.currentIndexChanged.connect(self.sigFunc_cr_nw_ctrl)
        self.num_ctrl_text.textChanged.connect(self.sigFunc_num_ctrl_input)
        self.clean_ctrls_checkBox.stateChanged.connect(self.sigFunc_clean_ctrls)
        self.scale_value_dSpinBox.valueChanged.connect(self.sigFunc_scale_of_ctrl)
        # -- grid R --
        self.ctrl_type_comboBox.currentIndexChanged.connect(self.sigFunc_ctrl_type_func)
        self.sys_type_text.textChanged.connect(self.sigFunc_sys_type)
        self.axis_direction_comboBox.currentIndexChanged.connect(self.sigFunc_axs_dir_ddbox)
        self.colour_text.textChanged.connect(self.sigFunc_ctl_colour)
        # -- Apply Button --
        self.apply_btn.clicked.connect(self.sigFunc_apply)
    
    # -- grid L functions --
    def sigFunc_cr_nw_ctrl(self):
        temp_create_cv = self.new_ctrl_comboBox.currentText()
        if temp_create_cv == 'Yes':
            self.create_cv = 1 
            self.num_ctrl_text.setDisabled(False)
        else:
            self.create_cv = 0
            self.num_ctrl_text.setDisabled(True)
        return self.create_cv
    
    def sigFunc_num_ctrl_input(self):
        try: 
            if self.create_cv:
                self.ctrl_num = self.num_ctrl_text.text()
                self.ctrl_num = int(self.ctrl_num)
                print(self.ctrl_num)
            else:
                self.ctrl_num = 1
                self.ctrl_num = int(self.ctrl_num)
        except ValueError:
            print( 'no string values allowed' )
        return self.ctrl_num

    def sigFunc_clean_ctrls(self):
        temp_zero_out = self.clean_ctrls_checkBox.isChecked()
        if temp_zero_out == True:
            self.ZeroOut_Ctrl = 1
        else:
            self.ZeroOut_Ctrl = 0
        print(temp_zero_out)

    def sigFunc_scale_of_ctrl(self):
        try:
            self.ctrl_size = self.scale_value_dSpinBox.value()
            self.ctrl_size = float(self.ctrl_size)# change 'Value' to the right one in script
            print(f"scale: {self.ctrl_size}")
        except ValueError:
            print( 'no string values allowed' )
    
    # -- grid R functions --
    def sigFunc_ctrl_type_func(self):
        temp_type = self.ctrl_type_comboBox.currentText()
        if temp_type == 'Circle':
            self.ctrl_type = 1
            self.sys_type_text.setText("fk")
            self.num_ctrl_text.setText("4")
        else:
            self.ctrl_type = 0
            self.sys_type_text.setText("ik")
            self.num_ctrl_text.setText("1")
        print(temp_type)
        return self.ctrl_type
    
    def sigFunc_sys_type(self):
            self.sys = self.sys_type_text.text()
            self.sys = str(self.sys)
            return self.sys

    def sigFunc_axs_dir_ddbox(self):
        temp_xyz = self.axis_direction_comboBox.currentText()
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

    def sigFunc_ctl_colour(self):
        try: 
            self.ctrl_col = self.colour_text.text()
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
        
   
    def csu_ctrl_colour(self):
        # change color of ctrl
        try:
            cmds.select(self.ctrl_list) 
            csu_cv_col_func.override_color_(self.ctrl_col)
            cmds.select(cl=1)
        except Exception as e:
            cmds.error( f"ctrl colour error: {e}" )
    
    #---------------------------------------------------------------------------------------------------------------------  
    def sigFunc_apply(self):
        self.create_cv = self.sigFunc_cr_nw_ctrl()
        self.ctrl_type = self.sigFunc_ctrl_type_func()
        self.Xaxis = self.sigFunc_axs_dir_ddbox()
        self.ctrl_num = self.sigFunc_num_ctrl_input()
        sys_type = self.sigFunc_sys_type()
        
        self.jnt_sel = cmds.ls(sl=1)
        print("joints selected ", self.jnt_sel)
        
        if self.create_cv:
            cmds.select(cl=1)

        print('apply button pressed')
        # call upon the modules you need to complete the task
        self.ctl_ls = csu_create_ctrls_mdl.csu_create_controls(self, self.ctrl_num, self.Axis)
        if self.create_cv:
            self.joint_ls = csu_sel_ctrls_mdl.csu_selecting_controls(self, self.jnt_sel)
        else:
            self.joint_ls, self.ctl_ls  = csu_sel_ctrls_mdl.csu_selecting_controls(self, self.jnt_sel) # called 'self.ctl_ls' because 
        print("J_joint list, ", self.joint_ls)
        print("J_control list, ", self.ctl_ls)
        # i had to return the 'ctl_ls' var again for when 'create_cv=0'!
        smpl_mtrans_fnc.Mtrans(self, self.ctl_ls, self.joint_ls, self.ctrl_num)
        self.ctrl_list = csu_rnm_ctrls_mdl.csu_rename_controls(self, self.joint_ls, self.ctl_ls, self.ctrl_num, sys_type)
        
        # IF you want to call OPM or not!
        if self.ZeroOut_Ctrl:
            self.csu_clean_controls(self.ctrl_list)
        else:
            pass
        self.csu_control_size()
        self.csu_ctrl_colour() 


def ctrlSetupTool_main():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])
    ui = ctrlSetupTool()
    ui.show()
    app.exec()
    return ui