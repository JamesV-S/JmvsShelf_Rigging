
import maya.cmds as cmds

ctrls = cmds.ls(sl=1, type="transform")

N_of_Ctrl = 'ctrl_COG'
N_of_Attr = 'ik_fk_Switch'

NewAttrLname = "ik_fk_Switch"
cmds.addAttr( ln=NewAttrLname, proxy=f"{N_of_Ctrl}.{N_of_Attr}" )









