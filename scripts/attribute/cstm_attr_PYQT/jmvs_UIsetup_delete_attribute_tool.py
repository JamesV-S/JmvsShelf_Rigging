
import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import *
from PySide6.QtUiTools import *

from shiboken6 import wrapInstance
from PySide6 import QtUiTools, QtWidgets, QtCore
from functools import partial # if you want to include args with UI method calls

import sys
import importlib
from Jmvs_letter_driver_script import find_driver_letter 
importlib.reload(find_driver_letter)

A_driver = find_driver_letter.get_folder_letter("Jmvs_current_file_path")
custom_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/custom_Attributes/Custom_attribute_tools' 
print(f"module imported from {custom_path}")
sys.path.append(custom_path)


# import the tool code!
import Delete_multiple_attributes as delete

importlib.reload(delete)


mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


class QtSamplerWindow(QWidget):
    '''
    Create a default tool window.
    '''
    def __init__(self, *args, **kwargs):
        # Initialise window and load UI file
        super(QtSamplerWindow,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Delete Attr Tool")
        self.initUI()
        
        # Lists to hold attribute names
        self.specify_attr = 0
        self.attrType_call = None
        self.ui.attr_type_ddp.setEnabled(True)

        # --------      
        self.ui.specify_attr_checkBx.stateChanged.connect(self.specify_attrib_func)
        self.ui.attr_type_ddp.currentIndexChanged.connect(self.attr_type_func)
        self.ui.delete_btn.clicked.connect(self.apply_func)
    
    def initUI(self):
        loader = QUiLoader()
        UI_FILE = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/custom_Attributes/Custom_attribute_tools/cstm_attr_ui/delete_attribute_qt.ui'
        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()
    
    # -------------------------------------------------------------------------
    # delete functions
    # if 

    def specify_attrib_func(self):
        self.specify_attr_btn = self.ui.specify_attr_checkBx.isChecked()
        if self.specify_attr_btn == True:
            self.specify_attr = 1
            self.ui.attr_type_ddp.setEnabled(False)
        else:
            self.specify_attr = 0
            self.ui.attr_type_ddp.setEnabled(True)
        print(self.specify_attr)
    
    def attr_type_func(self):
        self.attr_type_btn = self.ui.attr_type_ddp.currentText()
        self.any_attr=None
        self.float_attr="double"
        self.enum_attr="enum"
        if self.attr_type_btn == 'Any':
            self.attrType_call = self.any_attr
            print("chosen attr: ", self.any_attr)
        elif self.attr_type_btn == 'Float':
            self.attrType_call = self.float_attr
            print("chosen attr: ", self.float_attr)
        else:
            self.attrType_call = self.enum_attr
            print("chosen attr: ", self.enum_attr)
        return self.any_attr, self.float_attr, self.enum_attr

    def apply_func(self):
        # self.attrType_call
        self.applyied = delete.delete_custom_attributes(self.attrType_call, self.specify_attr)
        #delete_custom_attributes( None, 0)

def main():
    ui = QtSamplerWindow()
    ui.show()
    return ui

if __name__ == '__main__':
    main()

