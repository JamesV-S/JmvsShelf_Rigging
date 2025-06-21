#Set colours to Nurbs Curves

import maya .cmds as cmds
from pprint import pprint as pp

'''
import importlib
from JmvsShelf_Rigging.scripts.control import cv_green

importlib.reload(cv_green)
cv_green.override_colour_muted_green()
'''

def override_colour_muted_green():
    sel = cmds.ls(selection=True)

    for node in sel:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 27)


