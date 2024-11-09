
import maya.cmds as cmds
from maya import OpenMayaUI as omui

# 'PySide' module provides access to the Qt APIs as its submodule, 
# & importing the following:
try:
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import (QWidget)
    from shiboken6 import wrapInstance
except ModuleNotFoundError:
    from PySide2 import QtCore, QtWidgets, QtGui
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import (QWidget)
    from shiboken2 import wrapInstance

# from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random
import importlib
import os.path

# import the tool code!
from JmvsShelf_Rigging.scripts.prefix import Jmvs_add_prefix_tool_01_Tool as add_pref
importlib.reload(add_pref)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

'''
import importlib
from JmvsShelf_Rigging.scripts.prefix import Jmvs_UIsetup_Addprefix_tool_002

importlib.reload(Jmvs_UIsetup_Addprefix_tool_002)
Jmvs_UIsetup_Addprefix_tool_002.main()
'''

def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

class add_pref_interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(add_pref_interface,self).__init__(*args, **kwargs)
        version = "002"
        delete_existing_ui(f"Jmvs_add_pref_interface{version}")
        self.setObjectName(f"Jmvs_add_pref_interface{version}")
        self.initUI()

        self.setParent(mayaMainWindow)
        # self.setWindowFlags(Qt.Window)   
        self.setWindowFlags(Qt.Window)
   
        self.setWindowTitle(f"Jmvs_add_pref_{version}")

        self.resize(200, 150)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        stylesheet_path = os.path.join(current_dir,
            "..",  
            "..",  
            "style_interface",
            "CSS",
            "style_shelf_ui_001.css"
        )

        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

        # Add this variable to track the state of the Undo button
        self.undo_clicked = False      
        
        self.connect_signals()

    # functions, connected to above commands   
    def initUI(self):  
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
       
        #----------------------
        self.descrip_layout = QtWidgets.QVBoxLayout()
        self.descrip_label = QtWidgets.QLabel("Add prefix to selection:")
        self.descrip_layout.addWidget(self.descrip_label)

        #----------------------
        # checkbox layout
        self.checkbox_layout = QtWidgets.QGridLayout() 
        self.before_checkBx = QtWidgets.QCheckBox("Before")
        self.before_checkBx.setChecked(False)
        self.before_checkBx.setToolTip("if checked, places the prefix before the selection. Otherwise prefix goes behind.")
        self.Hi_checkBx = QtWidgets.QCheckBox("Hierarchy")
        self.Hi_checkBx.setChecked(False)
        self.Hi_checkBx.setToolTip("check if you want to add prefix to selection's Hierarchy")
        self.checkbox_layout.addWidget(self.before_checkBx, 0, 0)
        self.checkbox_layout.addWidget(self.Hi_checkBx, 0, 1)
        
        #----------------------
        # Label & LineEdit layout
        self.label_line_layout = QtWidgets.QHBoxLayout()
        self.text_label = QtWidgets.QLabel("Prefix:")
        self.pref_line = QtWidgets.QLineEdit()
        self.pref_line.setPlaceholderText("type_sys_obj_side/num")
        self.label_line_layout.addWidget(self.text_label)
        self.label_line_layout.addWidget(self.pref_line)
        self.label_line_layout.setAlignment(Qt.AlignCenter)
        # self.pref_line.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
   
        '''
        self.label_line_layout = QtWidgets.QGridLayout()
        self.text_label = QtWidgets.QLabel("Prefix:")
        self.pref_line = QtWidgets.QLineEdit()
        self.pref_line.setPlaceholderText("type_sys_obj_side/num")
        self.label_line_layout.addWidget(self.text_label)
        self.label_line_layout.addWidget(self.pref_line)
        self.label_line_layout.addWidget(self.text_label, 0, 1)
        self.label_line_layout.addWidget(self.pref_line, 0, 0)
        ''' 
        #----------------------
        # Button layout
        self.button_layout = QtWidgets.QGridLayout()
        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.undo_btn = QtWidgets.QPushButton("Undo")
        self.button_layout.addWidget(self.apply_btn, 0, 0)
        self.button_layout.addWidget(self.undo_btn, 0, 1)

        #----------------------
        # Add checkbox layout and button layout to the main layout
        self.main_layout.addLayout(self.descrip_layout)
        self.main_layout.addLayout(self.checkbox_layout)
        self.main_layout.addLayout(self.label_line_layout)
        self.main_layout.addLayout(self.button_layout)
        
        #----------------------
        self.setLayout(self.main_layout)
        '''
                col#0        col#1        col#2
        row#0   cell         cell         cell
        row#1   cell         cell         cell
        '''    
        
        #----------------------
        special_button_true = [self.apply_btn, self.undo_btn]
        special_button_False = []
        for item in special_button_true:
            item.setProperty("specialButton", True)
        for item in special_button_False:
            item.setProperty("specialButton", False)

        decrip_label_style = [self.descrip_label]
        for item in decrip_label_style:
            item.setProperty("descripLabel", True)

    #----------------------
    def connect_signals(self):
        self.before_checkBx.stateChanged.connect(self.before_checkbox_func)
        self.Hi_checkBx.stateChanged.connect(self.hierarchy_checkbox_func)
        self.pref_line.textChanged.connect(self.prefix_name)
        self.apply_btn.clicked.connect(self.apply_func)
        self.undo_btn.clicked.connect(self.undo_func)

    def before_checkbox_func(self):
        before_arg = self.before_checkBx.isChecked()
        if  before_arg == True:
            print(f"add prefix to front: {before_arg}")
        else:
            print(f"add prefix to behind: {before_arg}")
        return before_arg
        
      
    def hierarchy_checkbox_func(self):
        hi_arg = self.Hi_checkBx.isChecked()
        if hi_arg == True:
            print(f"added prefix to hierachy: {hi_arg}")
        else:
            print(f"added to no hierarchy: {hi_arg}")
        return hi_arg

           
    def prefix_name(self):
        prefix = self.pref_line.text()
        prefix = str(prefix)
        print("added a new prefix: ", prefix)
        return prefix
    
  
    def apply_func(self):

        self.applyied = add_pref.front_layout_prefix(self.before_checkbox_func(), self.hierarchy_checkbox_func(), self.prefix_name())
        print("returned function!!!! ", self.applyied)
        
        # Re-enable the Undo button
        self.undo_btn.setEnabled(True)
        self.undo_clicked = False


    def undo_func(self):
        if self.undo_clicked:
            return
        # Disable the Undo button
        self.undo_btn.setEnabled(False)
        
        self.undo_clicked = True
        print(f"undo this many times: _ {self.applyied+1} _ ")
        
        for x in range(self.applyied+1):
            cmds.undo()
        
        
def main():
    app = QtWidgets.QApplication.instance()
    if not app: # If there is no 
        app = QtWidgets.QApplication([])# Use an empty list for maya

    ui = add_pref_interface()
    ui.show()
    app.exec()
    return ui
    
# if __name__ == '__main__':
    # main()