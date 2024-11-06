import maya.cmds as cmds

def createLocator():
    amount = 4
    xPos = 0
    locList = []

    for x in range(amount):
        loc = cmds.spaceLocator(n="loc_"+str(x+1),a=True)
        cmds.move(xPos)
        xPos = xPos + 5
        locList.append(loc)
    
    #amount = amount - 1
    locList.reverse()
    
    try:
        for i in range(amount):
            cmds.parent(locList[i],locList[i+1])
    except IndexError:
        pass
    
    cmds.select(locList[-1])

    print("ON THE REPO")
