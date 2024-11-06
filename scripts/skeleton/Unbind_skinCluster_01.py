
import maya.cmds as cmds

# Unbind_skin_script

def Unbind_skin():
    
    selected_objects = cmds.ls(sl=1)

    for obj in selected_objects:
        skn_clus = cmds.ls(cmds.listHistory(obj), type='skinCluster')
        if skn_clus:
            cmds.skinCluster(skn_clus[0], edit=True, unbind=True)
  
#Unbind_skin()