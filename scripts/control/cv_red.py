#Set colours to Nurbs Curves

import maya .cmds as cmds
from pprint import pprint as pp

def override_color_red():
    sel = cmds.ls(selection=True)

    for node in sel:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 13)

