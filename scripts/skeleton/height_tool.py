
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
from JmvsShelf_Rigging.scripts.skeleton import height_tool

importlib.reload(height_tool)
height_tool.main()
'''



def delete_existing_ui(ui_name):
    if cmds.window(ui_name, exists=True):
        cmds.deleteUI(ui_name, window=True)

class height_tool_interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(height_tool_interface,self).__init__(*args, **kwargs)
        version = "001"
        delete_existing_ui(f"height_tool_{version}")
        self.setObjectName(f"height_tool_{version}")
        self.initUI()

        self.setParent(mayaMainWindow)
        # self.setWindowFlags(Qt.Window)   
        self.setWindowFlags(Qt.Window)
   
        self.setWindowTitle(f"height_tool_{version}")

        self.resize(290, 100)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"rt_parent path = {current_dir}") 
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
        # description label
        self.descrip_layout = QtWidgets.QVBoxLayout()
        self.descrip_label = QtWidgets.QLabel("Replace object's existing name:")
        self.descrip_layout.addWidget(self.descrip_label)
        #----------------------
        # Label & LineEdit layout
        self.label_line_layout = QtWidgets.QHBoxLayout()
        self.text_label = QtWidgets.QLabel("height_num:")
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("cm please")
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
        self.lineEdit.textChanged.connect(self.height_num)
        self.apply_btn.clicked.connect(self.apply_func)
        self.undo_btn.clicked.connect(self.undo_func)


    def height_num(self):
        height_num_input = self.lineEdit.text()
        self.height_num_int = float(height_num_input)
        print(f"height_num_input: {self.height_num_int}")
        # return height_num_str
    

    def position_cube(self):
        # cr_cube
        top_loc_name = f"loc_height_cube_top_#"
        bttm_loc_name = f"loc_height_cube_bttm_#"
 
        top_loc = cmds.spaceLocator(n=top_loc_name)[0]
        bttm_loc = cmds.spaceLocator(n=bttm_loc_name)[0]
        print(f"topLoc: {top_loc}, bttm_loc: {bttm_loc}")
        
        # Set the cube's scale to 1 cm in height
        cmds.setAttr(f"{top_loc}.scaleY", 1)
        
        # Calculate the translate Y position # 175.3
        translate_y = self.height_num_int - (1 / 2.0)  # Assuming the cube height is now 1 cm
        
        '''
        Here's the breakdown:
        175.3 cm is the desired height for the top of the object.
        1 cm is the height of the object.
        1 / 2.0 calculates the adjustment needed to position the center 
        of a 1 cm object so its top reaches 175.3 cm.
        This calculation sets the base of the object at 175.3 - 0.5, 
        ensuring the top reaches exactly 175.3 cm.
        '''
        # Apply the translation
        cmds.setAttr(f"{top_loc}.translateY", translate_y, lock=1)
        cmds.setAttr(f"{bttm_loc}.translateY", 0, lock=1)

        top_point_loc = cmds.xform(top_loc ,q=1, ws=1, rp=1)
        bttm_point_loc =  cmds.xform(bttm_loc ,q=1, ws=1, rp=1)
        curve_name = f"crv_height_{top_loc}"
        cmds.curve(d=1, p=[top_point_loc, bttm_point_loc], n=curve_name)
        cluster_1 = cmds.cluster(f"{curve_name}.cv[0]", n=f"cluster_crv_{top_loc}_cv0")
        cluster_2 = cmds.cluster(f" {curve_name}.cv[1]", n=f"cluster_crv_{bttm_loc}_cv0")
        
        cmds.parent(cluster_1, top_loc)
        cmds.parent(cluster_2, bttm_loc)
               
        for x in cmds.ls(typ="cluster"):
            cmds.hide(f"{x}Handle")
            cmds.setAttr(f"{x}Handle.hiddenInOutliner", True)
                
        cmds.setAttr(f"{curve_name}.template", 1)
        cmds.select(cl=1)
    

    def set_units_to_centimeters():
        # Set the linear unit to centimeters
        cmds.currentUnit(linear='cm')
        
        current_unit = cmds.currentUnit(query=True, linear=True)
        print(f"Current linear unit: {current_unit}")


    def apply_func(self):  
        # get number of sel for undo function
        print(f"Apply_func")
        self.position_cube()
        self.num_of_sel = 1

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
    ui = height_tool_interface()
    ui.show()
    return ui
    
if __name__ == '__main__':
    main()

