


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
importlib.reload(getpath)

maya_main_wndwPtr = OpenMayaUI.MQtUtil.mainWindow()
main_window = wrapInstance(int(maya_main_wndwPtr), QWidget)

def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

class crCustomAttrTool(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(crCustomAttrTool, self).__init__(parent)
        version = "001"
        ui_object_name = f"crCustomAttrTool{version}"
        ui_window_name = f"Create custom attr tool V{version}"
        delete_existing_ui(ui_object_name)
        self.setObjectName(ui_object_name)

        # Set flags & dimensions
        self.setParent(main_window)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(ui_window_name)
        self.resize(300, 250)
        
        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                       "..",  "..", "style_interface", "CSS", "geoDB_style_sheet_001.css")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        ''''''
        self.UI()
        self.UI_connect_signals()
        ''''''

    def UI(self):
        pass

    def UI_connect_signals(self):
        pass
        
def crCustomAttrTool_main():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])
    ui = crCustomAttrTool()
    ui.show()
    app.exec()
    return ui