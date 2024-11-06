
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
#another_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools/Prefix_Ui_tools' 
print(f"module imported from {custom_path}")
sys.path.append(custom_path)
#sys.path.append(another_path)

# import the tool code!
import Jmvs_remove_prefix_tool_04_Tool as rmv_pref
importlib.reload(rmv_pref)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


class QtSampler(QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSampler,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Remove Prefix Tool")
        self.initUI()
        
        # Add this variable to track the state of the Undo button
        self.undo_clicked = False 

        # - location to write commands to activate button..
        #self.ui.qt_button_name.clicked.connect(self.button_function)
        self.ui.Bfr_checkBx_3.stateChanged.connect(self.before_checkbox_func)
        self.ui.Hi_checkBx_3.stateChanged.connect(self.hierarchy_checkbox_func)
#
        self.ui.pref_spnBox.valueChanged.connect(self.prefix_num)
        self.ui.addPref_apply_btn_3.clicked.connect(self.apply_func)
        self.ui.undo_btn_1.clicked.connect(self.undo_func)

    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_FILE = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools/Prefix_Ui_tools/ui_scripts/jmvs_remove_prefix.ui'
        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()
    #---------------------------------------------------------------------------------------------------------------------
    # here are functions I created for the buttons in the ui interface!    
    
    # Function for before checkbox   
    def before_checkbox_func(self):
        before_arg = self.ui.Bfr_checkBx_3.isChecked()
        if  before_arg == True:
            print(f"add prefix to front: {before_arg}")
        else:
            print(f"add prefix to behind: {before_arg}")
        return before_arg
        
    # Function for hierarchy checkbox   
    def hierarchy_checkbox_func(self):
        hi_arg = self.ui.Hi_checkBx_3.isChecked()
        if hi_arg == True:
            print(f"added prefix to hierachy: {hi_arg}")
        else:
            print(f"added to no hierarchy: {hi_arg}")
        return hi_arg

    # Function for prefix string        
    def prefix_num(self):
        prefix = self.ui.pref_spnBox.text()
        prefix = int(prefix)
        print("added a new prefix: ", prefix)
        return prefix
    
    
          
    def apply_func(self):

        self.applyied = rmv_pref.remove_prefix_tool(self.before_checkbox_func(), 
                                     self.hierarchy_checkbox_func(), 
                                     self.prefix_num())
        print("returned function!!!! ", self.applyied)
        # Re-enable the Undo button
        self.ui.undo_btn_1.setEnabled(True)
        self.undo_clicked = False
        
    def undo_func(self):
        if self.undo_clicked:
            return
        # Disable the Undo button
        self.ui.undo_btn_1.setEnabled(False)
        
        self.undo_clicked = True
        print(f"undo this many times: _ {self.applyied+1} _ ")
        
        for x in range(self.applyied+1):
            cmds.undo()
        
def main():
    ui = QtSampler()
    ui.show()
    return ui
    
if __name__ == '__main__':
    main()
