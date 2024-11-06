
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
custom_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools/Prefix_Ui_tools' 
#print(f"module imported from {custom_path}")
sys.path.append(custom_path)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

class QtSampler(QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSampler,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Rename Sel Tool")
        self.initUI()
        
        # Add this variable to track the state of the Undo button
        self.ui.newName_undo_btn.setEnabled(False)
        self.undo_clicked = False
        self.ui.newName_lineEdit.textChanged.connect(self.new_name)
        self.ui.newName_apply_btn.clicked.connect(self.apply_func)
        self.ui.newName_undo_btn.clicked.connect(self.undo_func)
        
        
    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_FILE = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools/Prefix_Ui_tools/ui_scripts/jmvs_rename_selection_001.ui'
        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()

        
    def new_name(self):
        new_name_input = self.ui.newName_lineEdit.text()
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
        self.ui.newName_undo_btn.setEnabled(True)
        self.undo_clicked = False


    def undo_func(self):
        if self.undo_clicked:
            return
        # Disable the Undo button
        self.ui.newName_undo_btn.setEnabled(False)
        
        self.undo_clicked = True
        #print(f"undo this many times: _ {self.applyied+1} _ ")
        for x in range(self.num_of_sel):
            cmds.undo()
        
        
def main():
    ui = QtSampler()
    ui.show()
    return ui
    
if __name__ == '__main__':
    main()
