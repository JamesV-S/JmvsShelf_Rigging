
import maya.cmds as cmds 
    
def cr_new_display_layer():
    obj  = cmds.ls(sl=1)
    try:
        cmds.select(obj)
    except:
        pass
    try:
        layer = cmds.createDisplayLayer(nr=1, n=f"lay_{obj[0]}_auto")
        cmds.setAttr(f"{layer}.displayType", 2)
        cmds.select(cl=1)
    except:
        cmds.error("Select an object!")
