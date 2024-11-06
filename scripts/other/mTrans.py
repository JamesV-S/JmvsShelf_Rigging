import maya.cmds as cmds

def matchsTransform():
    firstSelected = cmds.ls(sl=True)
    firstSelected = firstSelected[1:]
    print("firstSelection: ", firstSelected)

    def matchTrans():
        objList = cmds.ls(sl=True)
        objList = objList[:1]
        print("Other objs: ", objList)
    
        for i in range(len(objList)):
            cmds.matchTransform(objList[i], firstSelected)

    if not firstSelected:
        cmds.error("ERROR: No obj selected")
    else:
        matchTrans()