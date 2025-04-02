
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
import importlib
import os.path

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

'''
import importlib
from JmvsShelf_Rigging.scripts.prefix import Jmvs_UIsetup_rename_tool_001

importlib.reload(Jmvs_UIsetup_rename_tool_001)
Jmvs_UIsetup_rename_tool_001.main()
'''
def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

class rename_obj_interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(rename_obj_interface,self).__init__(*args, **kwargs)
        version = "001"
        delete_existing_ui(f"rename_obj_interface{version}")
        self.setObjectName(f"rename_obj_interface{version}")
        self.initUI()

        self.setParent(mayaMainWindow)
        # self.setWindowFlags(Qt.Window)   
        self.setWindowFlags(Qt.Window)
   
        self.setWindowTitle(f"Jmvs_rename_obj_{version}")

        self.resize(290, 100)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        stylesheet_path = os.path.join(current_dir,
            "..",  
            "..",  
            "style_interface",
            "CSS",
            "geoDB_style_sheet_001.css"
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
        # description label
        self.descrip_layout = QtWidgets.QVBoxLayout()
        self.descrip_label = QtWidgets.QLabel("Replace object's existing name:")
        self.descrip_layout.addWidget(self.descrip_label)
        #----------------------
        # Label & LineEdit layout
        self.label_line_layout = QtWidgets.QHBoxLayout()
        self.text_label = QtWidgets.QLabel("Prefix:")
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("new_name_")
        self.label_line_layout.addWidget(self.text_label)
        self.label_line_layout.addWidget(self.lineEdit)
        self.label_line_layout.setAlignment(Qt.AlignCenter)
        # self.lineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
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
        self.main_layout.addLayout(self.label_line_layout)
        self.main_layout.addLayout(self.button_layout)
        
        #----------------------
        self.setLayout(self.main_layout)  
        
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


    def connect_signals(self):
        # Add this variable to track the state of the Undo button
        self.undo_btn.setEnabled(False)
        self.undo_clicked = False
        self.lineEdit.textChanged.connect(self.new_name)
        self.apply_btn.clicked.connect(self.apply_func)
        self.undo_btn.clicked.connect(self.undo_func)


    def new_name(self):
        new_name_input = self.lineEdit.text()
        self.new_name_str= str(new_name_input)
        print(f"new_name_input: {self.new_name_str}")
        # return new_name_str
       

    def apply_func(self):     
        # rename the selected objects:
        selection = cmds.ls(sl=True, type="transform")
        print(f"selection = {selection}")
        print(f"number of selecte ditems: {len(selection)}")
        
        # get number of sel for undo function
        self.num_of_sel = len(selection)

        renamed_list = []
        for index, obj in enumerate(selection):
            new_obj_name = f"{self.new_name_str}{index}"
            renamed_list.append(cmds.rename(obj, new_obj_name))
        print(f"renamed list = {renamed_list}")

        # Re-enable the Undo button
        self.undo_btn.setEnabled(True)
        self.undo_clicked = False


    def undo_func(self):
        if self.undo_clicked:
            return
        # Disable the Undo button
        self.undo_btn.setEnabled(False)
        
        self.undo_clicked = True
        #print(f"undo this many times: _ {self.applyied+1} _ ")
        for x in range(self.num_of_sel):
            cmds.undo()
        
        
def main():
    ui = rename_obj_interface()
    ui.show()
    return ui
    
if __name__ == '__main__':
    main()
