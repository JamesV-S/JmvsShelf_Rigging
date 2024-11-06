
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
import locked_enum_attri_func as DividerAttr
import float_custom_attr_func as floatAttr
import switch_cstm_enum_attr as enumSwitchAttr

importlib.reload(DividerAttr)
importlib.reload(floatAttr)
importlib.reload(enumSwitchAttr)


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
        self.setWindowTitle("Custom Attr Tool")
        self.initUI()
        
        # Lists to hold attribute names
        self.divider_text_list = []
        self.float_text_list = []
        self.enm_text_list = []
        

        # --------
        # Initialize Divider tab UI elements and functionality
        self.vl_sublayout = self.ui.findChild(QtWidgets.QVBoxLayout, "vl_sublayout")
        self.ui.Div_add_name_btn.clicked.connect(self.div_add_name_subwidget_fun)
        self.ui.Div_apply_btn.clicked.connect(self.Div_Apply_func)


        # --------    
        # Initialize Float tab UI elements and functionality
        self.limited_val = False
        self.min_val = 0  
        self.max_val = 0
        self.flt_vl_sublayout = self.ui.findChild(QtWidgets.QVBoxLayout, "flt_vl_sublayout")      
        self.ui.flt_add_name_btn.clicked.connect(self.flt_add_name_subwidget_fun)
        self.ui.flt_Unlimited_radioBtn.clicked.connect(self.flt_unlimited_func)
        self.ui.flt_Min_spnBox.valueChanged.connect(self.flt_min_func)
        self.ui.flt_Max_spnBox.valueChanged.connect(self.flt_max_func)
        self.ui.flt_apply_btn.clicked.connect(self.flt_Apply_func)
        self.ui.flt_Min_spnBox.setEnabled(False)
        self.ui.flt_Max_spnBox.setEnabled(False)
        # Set range for the spin boxes to allow negative values
        self.ui.flt_Min_spnBox.setRange(-999999, 999999)
        self.ui.flt_Max_spnBox.setRange(-999999, 999999)
        

        # --------
        # Initialize Float tab UI elements and functionality
        # this requiers master name & list of name! - nothing is getting disabled
        self.enm_vl_sublayout = self.ui.findChild(QtWidgets.QVBoxLayout, "enm_vl_sublayout") 
        self.ui.enm_add_name_btn.clicked.connect(self.enm_add_name_subwidget_fun)
        self.ui.enm_masterName_line.textChanged.connect(self.enm_master_name_func)
        self.ui.enm_apply_btn.clicked.connect(self.enm_Apply_func)

    def initUI(self):
        loader = QUiLoader()
        UI_FILE = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/custom_Attributes/Custom_attribute_tools/cstm_attr_ui/create_custom_attributes_qt.ui'
        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parentWidget=self)
        file.close()
    
    # functions, connected to above commands   
    def div_add_name_subwidget_fun(self):
        print("button clicked")
        self.subwidget = QtUiTools.QUiLoader().load(f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/custom_Attributes/Custom_attribute_tools/cstm_attr_ui/enmDIV_sub_widget.ui')
        self.vl_sublayout.addWidget(self.subwidget)

        lineEdit = self.subwidget.findChild(QtWidgets.QLineEdit, "div_enm_line")
        lineEdit.textChanged.connect(partial (self.div_handle_text_changed, lineEdit))
        btn_remove = self.subwidget.findChild(QtWidgets.QPushButton, "remove_btn")
        btn_remove.clicked.connect(partial (self.div_removeSubwidget, self.subwidget, lineEdit))
    

    def div_handle_text_changed(self, line, text):
        if ' ' in text:
            self.div_update_divider_list(line)


    def div_update_divider_list(self, line):
        text = line.text().strip() # Remove any leading/trailing spaces
        print("retrieves the text entered: ", text)
        if text:
            self.divider_text_list = [name for name in self.divider_text_list 
                                      if name !=text]
            self.divider_text_list.append(text)
            self.divider_text_list = list(set(self.divider_text_list)) 
            # ^Remove dupliccates^

            print("Updated list: ", self.divider_text_list)


    def div_removeSubwidget(self, subwidget, line):
        # This removes the text from the list, but atm it doesn't remove the 
        # list at all, it should remove a single string depending on the subwidget!
        text = line.text().strip()
        print("text to remove: ", text)
        for item in self.divider_text_list:
            if text in item:
                self.divider_text_list.remove(item)
                break # exit the loop once the item is found and removed
            
        self.vl_sublayout.removeWidget(subwidget)
        subwidget.deleteLater()
        
        print("Updated list after removal: ", self.divider_text_list)
        

    def Div_Apply_func(self):
        if not self.divider_text_list:
            print("No name provided for the divider attribute")
            return
        
        try:
            self.applyied = DividerAttr.locked_enum_attrib(self.divider_text_list) # 'en' is a list, ctrl is cmds.ls
            print(f"Enum divider attribute : {self.applyied}")
        except Exception as e:
            print( f"No name provided for the divider attruubute {e}" )

    # -------------------------------------------------------------------------
    # Float functions
    
    def flt_add_name_subwidget_fun(self):
        print("button clicked")
        self.flt_subwidget = QtUiTools.QUiLoader().load(f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/custom_Attributes/Custom_attribute_tools/cstm_attr_ui/flt_sub_widget.ui')
        self.flt_vl_sublayout.addWidget(self.flt_subwidget)

        flt_lineEdit = self.flt_subwidget.findChild(QtWidgets.QLineEdit, "flt_line")
        flt_lineEdit.textChanged.connect(partial (self.flt_handle_text_changed, flt_lineEdit))
        flt_btn_remove = self.flt_subwidget.findChild(QtWidgets.QPushButton, "flt_remove_btn")
        flt_btn_remove.clicked.connect(partial (self.flt_removeSubwidget, self.flt_subwidget, flt_lineEdit))

    def flt_handle_text_changed(self, line, text):
        if ' ' in text:
            self.flt_update_list(line)

    def flt_update_list(self, line):
        flt_text = line.text().strip() # Remove any leading/trailing spaces
        print("retrieves the text entered: ", flt_text)
        if flt_text:
            self.float_text_list = [name for name in self.float_text_list 
                                      if name !=flt_text]
            self.float_text_list.append(flt_text)
            self.float_text_list = list(set(self.float_text_list)) 
            # ^Remove dupliccates^

            print("Updated list: ", self.float_text_list )
    
    def flt_removeSubwidget(self, subwidget, line):
        flt_text = line.text().strip()
        print("text to remove: ", flt_text)
        for item in self.float_text_list:
            if flt_text in item:
                self.float_text_list.remove(item)
                break # exit the loop once the item is found and removed
            
        self.flt_vl_sublayout.removeWidget(subwidget)
        subwidget.deleteLater()
        
        print("Updated list after removal: ", self.float_text_list)

    def flt_unlimited_func(self):
                      
        self.limited_val = self.ui.flt_Unlimited_radioBtn.isChecked()
        if self.limited_val == True:
            print("unlimited is True")
            self.ui.flt_Min_spnBox.setEnabled(True)
            self.ui.flt_Max_spnBox.setEnabled(True)#  flt_Max_spnBox
        else:
            print("unlimited is False")
            self.limited_val = False
            self.ui.flt_Min_spnBox.setEnabled(False)
            self.ui.flt_Max_spnBox.setEnabled(False)
            #print("unlimited is False")

        return self.limited_val
   
    def flt_min_func(self):
        try:       
            
            self.min_val = self.ui.flt_Min_spnBox.value()
            self.min_val = float(self.min_val)
            print(f"float min value: {self.min_val}")       
        except ValueError:
            print( 'no string values allowed' )
    
    def flt_max_func(self):
        try:
            self.max_val = self.ui.flt_Max_spnBox.value()
            self.max_val = float(self.max_val)
            print(f"float max value: {self.max_val}")
        except ValueError:
            print( 'no string values allowed' )

    def flt_Apply_func(self):
        if not self.float_text_list:
            print("No name provided for the float attribute")
            return

        try:
            self.flt_applyied = floatAttr.add_float_attrib(self.float_text_list, 
                                                           [self.min_val,self.max_val], 
                                                           self.limited_val) 
            print(f"Float attribute : {self.flt_applyied}")
        except Exception as e:
            print( f"No name provided for the float attribute {e}" )
    
    # -------------------------------------------------------------------------
    # Enum functions
    def enm_master_name_func(self):
        self.master_name = self.ui.enm_masterName_line.text()
        self.master_name = str(self.master_name)
        print(f"master name list: {self.master_name}")
    
    
    def enm_add_name_subwidget_fun(self):
        print("button clicked")
        self.enm_subwidget = QtUiTools.QUiLoader().load(f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/custom_Attributes/Custom_attribute_tools/cstm_attr_ui/enm_sub_widget.ui')
        self.enm_vl_sublayout.addWidget(self.enm_subwidget)

        enm_lineEdit = self.enm_subwidget.findChild(QtWidgets.QLineEdit, "enm_line")
        enm_lineEdit.textChanged.connect(partial (self.enm_handle_text_changed, enm_lineEdit))
        btn_remove = self.enm_subwidget.findChild(QtWidgets.QPushButton, "enm_remove_btn")
        btn_remove.clicked.connect(partial (self.enm_removeSubwidget, self.enm_subwidget, enm_lineEdit))
    

    def enm_handle_text_changed(self, line, text):
        if ' ' in text:
            self.enm_update_list(line)

    def enm_update_list(self, line):
        enm_text = line.text().strip() # Remove any leading/trailing spaces
        print("retrieves the text entered: ", enm_text)
        if enm_text:
            self.enm_text_list = [name for name in self.enm_text_list 
                                      if name !=enm_text]
            self.enm_text_list.append(enm_text)
            self.enm_text_list = list(set(self.enm_text_list)) 
            # ^Remove dupliccates^

            print("Updated list: ", self.enm_text_list )
    

    def enm_removeSubwidget(self, subwidget, line):
        enm_text = line.text().strip()
        print("text to remove: ", enm_text)
        for item in self.enm_text_list:
            if enm_text in item:
                self.enm_text_list.remove(item)
                break # exit the loop once the item is found and removed
            
        self.enm_vl_sublayout.removeWidget(subwidget)
        subwidget.deleteLater()
        
        print("Updated list after removal: ", self.enm_text_list)
    

    def enm_Apply_func(self):
        result = ':'.join(self.enm_text_list)

        if not self.enm_text_list:
            print("No name provided for the float attribute")
            return

        try:
            self.enm_applyied = enumSwitchAttr.custom_enum_attr( result, self.master_name)
            print(f"Float attribute : {self.enm_applyied}")
        except Exception as e:
            print( f"No name provided for the enum switch attribute {e}" )


def main():
    ui = QtSamplerWindow()
    ui.show()
    return ui

if __name__ == '__main__':
    main()

