
import maya.cmds as cmds
# Delete the scene to start again: 
sel = cmds.ls(sl=1, typ="transform")
shape = cmds.listRelatives(sel, s=1)
print(f"Shape = {shape}")

for shp in shape:
    cmds.setAttr(f"{shp}.aiRenderCurve", 0)
    # cmds.setAttr(f"{shp}.aiSampleRate", 20)