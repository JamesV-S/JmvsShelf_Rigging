#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#  JMVS RotAxesUpdate_Tool
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import maya.cmds as cmds 
    
def setAxisDisplay():
    
    multiSlList = []
        
    selectionCheck = cmds.ls(sl=1)[0]#, type="joint")
    print(selectionCheck)
    lRA_Info = cmds.getAttr( str(selectionCheck) + '.displayLocalAxis' )
    
      
    # Error check to make sure a joint is selected
    if not selectionCheck:
        cmds.error("Please select the root joint.")
    else:
        rootJnt = cmds.ls(sl=1)
    
    cmds.select(rootJnt, hi=1)
    jointList = cmds.ls(sl=1, type='transform')#, type="joint")
    print(jointList)
        
    # Set the displayLocalAxis attribute to what the user specifies
    if lRA_Info == 0:
        for jnt in jointList:
            cmds.setAttr( jnt + ".displayLocalAxis", 1 )
    else:
        for jnt in jointList:
            cmds.setAttr( jnt + ".displayLocalAxis", 0 )
            
