#Set colours to Nurbs Curves

import maya .cmds as cmds
from pprint import pprint as pp

# Make a ui tha tlets me scroll & pick any colour for the objectts selected

def override_color():
    sel = cmds. ls (selection=True)

    shape = cmds.listRelatives ( sel, shapes = True )
    #add = cmds.select( add=True )

    for node in shape:
        cmds. setAttr (node + ".overrideEnabled" ,True)
        cmds. setAttr (node + ".overrideColor" , 7)

override_color()

#Main colours = BLUE > 6/18 RED > 13/4. YELLOW > 17. GREEN > 7/14/23/26

#0-grey/1-black/2-dark_grey/3-mid_grey/4-red/5-dark_blue/6-light_blue/7-dark_green/
#8-darkest_blue/9-light_purple/10-light_brown/11-dark_brown/12-browny_red/13-vivid_red/14-bright_green/15-blue_norm
#16-white/17-yellow/18-light_blue/19-muted_green....

