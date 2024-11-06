
# locked enum attribute function:
import maya.cmds as cmds

enum_attrib_list = ["MUM"]

def locked_enum_attrib(en):
    ctrl = cmds.ls(sl=1, type="transform")
              
    dividerNN = "------------" 
    atrrType = "enum"
    
    ln = [f"{en[x].lower()}_dvdr" for x in range(len(en))]
    print(ln[0])

    for target in ctrl:
        for x in range(len(ln)):
            cmds.addAttr(target, longName=ln[x], niceName=dividerNN, 
                        attributeType=atrrType, enumName=en[x], k=True
                        )
            
            cmds.setAttr(f"{target}.{ln[x]}", lock=True, keyable=False, 
                        channelBox=True
                        )

#locked_enum_attrib(enum_attrib_list)