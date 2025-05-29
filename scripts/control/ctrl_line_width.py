#Set colours to Nurbs Curves

import maya .cmds as cmds
from pprint import pprint as pp

'''
import importlib
from JmvsShelf_Rigging.scripts.control import ctrl_line_width

importlib.reload(ctrl_line_width)
ctrl_line_width.line_width(2)
'''

def line_width(num):
    sel = cmds.ls(selection=True)
    
    width_info = cmds.getAttr(f"{sel[0]}.lineWidth")
    if width_info == -1:
        for node in sel:
            cmds. setAttr (f"{node}.lineWidth", num)
    else:
        for node in sel:
            cmds. setAttr (f"{node}.lineWidth", -1)

