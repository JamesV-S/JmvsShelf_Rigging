
import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
#suggested fix from PySide2.QtWidgets import QWidget, QUiLoader, QApplication, QPushButton, QVBoxLayout, QFileDialog, QLabel, QSpinBox
#class main_ui(QWidget):
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance
import os.path

import sys
import importlib
import find_driver_letter as driver
importlib.reload(driver)

A_driver = driver.get_folder_letter("Jmvs_current_file_path")
custom_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/mdls_scripts' 
#another_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools/Prefix_Ui_tools' 
print(f"module imported from {custom_path}")
sys.path.append(custom_path)
#sys.path.append(another_path)

# import the tool code!
import Get_module_path_of_python_file as getPath
importlib.reload(getPath)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

class QtSampler(QWidget):
    def __init__(self, *args, **kwargs):
        super(QtSampler,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.initUI()
        
        # - location to write commands to activate button..
        #self.ui.qt_button_name.clicked.connect(self.button_function)
        #self.ui.Bfr_checkBx_3.stateChanged.connect(self.before_checkbox_func)
        #self.ui.Hi_checkBx_3.stateChanged.connect(self.hierarchy_checkbox_func)
#
        self.ui.pythonName_line.textChanged.connect(self.python_name)
        self.ui.getPath_apply_btn.clicked.connect(self.apply_func)
    
    # functions, connected to above commands   
    def initUI(self):
        loader = QUiLoader()
        UI_FILE = f'{A_driver}My_RIGGING/JmvsSCRIPTS/mdls_scripts/ui_scripts/getPath_of_pythonFile.ui'
        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()
    #---------------------------------------------------------------------------------------------------------------------
    # here are functions I created for the buttons in the ui interface!    
    
    # Function for python file name string      
    def python_name(self):
        prefix = self.ui.pythonName_line.text() 
        prefix = str(prefix)
        print("Given python file: ", prefix)
        return prefix
    
    def apply_func(self):

        getPath.getModule_path_tool(self.python_name())
        
def main():
    ui = QtSampler()
    ui.show()
    return ui
    
if __name__ == '__main__':
    main()
