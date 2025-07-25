#Set colours to Nurbs Curves

import maya .cmds as cmds
from pprint import pprint as pp

'''
import importlib
from JmvsShelf_Rigging.scripts.control import cv_blue

importlib.reload(cv_blue)
cv_blue.override_colour_lightBlue()
'''

def override_color_blu():
    sel = cmds.ls(selection=True)

    for node in sel:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 6)
        

def override_color_pale_blu():
    sel = cmds.ls(selection=True)

    for node in sel:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 29)


def override_color_turquoise():
    sel = cmds.ls(selection=True)

    for node in sel:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 28)


def override_colour_lightBlue():
    sel = cmds.ls(selection=True)

    for node in sel:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 18)

