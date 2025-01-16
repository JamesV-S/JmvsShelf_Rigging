
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

from JmvsShelf_Rigging.scripts.data import func_path_of_python_file
importlib.reload(func_path_of_python_file)

maya_main_wndwPtr = OpenMayaUI.MQtUtil.mainWindow()
main_window = wrapInstance(int(maya_main_wndwPtr), QWidget)

def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

class pyFilePath(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(pyFilePath, self).__init__(parent)
        version = "001"
        ui_object_name = f"pyFilePath{version}"
        ui_window_name = f"Search for file path V{version}"
        delete_existing_ui(ui_object_name)
        self.setObjectName(ui_object_name)

        # Set flags & dimensions
        self.setParent(main_window)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(ui_window_name)
        self.resize(300, 100)
        
        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                       "..",  "..", "style_interface", "CSS", "geoDB_style_sheet_001.css")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        self.UI()
        self.UI_connect_signals()


    def UI(self):
        main_Vlayout = QtWidgets.QVBoxLayout(self)
        #----------------------------------------------------------------------
        # -- explanation lbl --
        layH_explanation_lbl = QtWidgets.QHBoxLayout()
        layH_explanation_lbl.setContentsMargins(20, 0, 0, 0)
        self.explanation_lbl = QtWidgets.QLabel(
            "Output's the file path of specified python file:"
            )
        layH_explanation_lbl.addWidget(self.explanation_lbl)

        # -- FileName --
        layH_file_name = QtWidgets.QHBoxLayout()
        # layH_file_name.setContentsMargins(100, 0, 0, 0)
        self.pefix_DB_lbl = QtWidgets.QLabel("Name of `.py` file")
        self.fileName_text = QtWidgets.QLineEdit()
        layH_file_name.addWidget(self.pefix_DB_lbl)
        layH_file_name.addWidget(self.fileName_text)
        
        # -- Apply button --
        self.apply_btn = QtWidgets.QPushButton("Apply")

        # add to main layout
        main_Vlayout.addLayout(layH_explanation_lbl)
        main_Vlayout.addLayout(layH_file_name)
        main_Vlayout.addWidget(self.apply_btn)
        
        self.setLayout(main_Vlayout)

    def UI_connect_signals(self):
        # -- FileName --
        self.fileName_text.textChanged.connect(self.sigFunc_fileName)
        # -- Apply Button --
        self.apply_btn.clicked.connect(self.sigFunc_apply)
        

    def sigFunc_fileName(self):
        self.val_fileName_text = str(self.fileName_text.text())
        # return self.val_fileName_text


    def sigFunc_apply(self):
        print(f"sigFunc_apply pressed")
        func_path_of_python_file.getModule_path_tool(self.val_fileName_text)


def py_file_path_main():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])
    ui = pyFilePath()
    ui.show()
    app.exec()
    return ui