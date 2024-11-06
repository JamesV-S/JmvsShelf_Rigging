import maya.cmds as cmds

def select_skinCluster():

    sel = cmds.ls(sl=1)

    jnts = cmds.skinCluster( sel, inf=1, q=1 )

    cmds.select(jnts)


