#Set colours to Nurbs Curves

import maya .cmds as cmds
from pprint import pprint as pp

def override_col_yel():
    sel = cmds. ls (selection=True)

    shape = cmds.listRelatives ( sel, shapes = True )
    #add = cmds.select( add=True )

    for node in shape:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 17)

    print("yellow_edited!")


