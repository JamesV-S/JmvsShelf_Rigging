import maya.cmds as cmds

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

def add_float_attrib(flt, val, limited):
    
    ctrl = cmds.ls(sl=1, type="transform")

    MinVal = val[0]
    MaxVal = val[1]
    
    if limited:
        for target in ctrl:
                for x in range(len(flt)):
                    cmds.addAttr(target, longName=flt[x], at='double', dv=0, 
                                min= MinVal, max = MaxVal)
                    cmds.setAttr(f"{target}.{flt[x]}", e=1, k=1 )
    else:
        for target in ctrl:
                for x in range(len(flt)):
                    cmds.addAttr(target, longName=flt[x], at='double', dv=0, 
                                )
                    cmds.setAttr(f"{target}.{flt[x]}", e=1, k=1 )

def noise_add_attr(ctrl):
    noise_attr_ls = ["Up_Down_Noise", "Fwd_Tilt_Noise", "Side_Tilt_Noise", "Noise_Speed", "Noise_Offset"]
    shake_attr_ls = ["Up_Down_Amount", "Fwd_Tilt_Amount", "Side_Tilt_Amount", "Up_Down_Speed", "Fwd_Speed", "Side_Speed", "Up_Down_Offset", "Fwd_Offset", "Side_Offset"]
    
    cmds.select(ctrl)
    #locked_enum_attrib(["NOISE"])
    #add_float_attrib(noise_attr_ls, [0,1] , False)

    locked_enum_attrib(["SHAKE"])
    add_float_attrib(shake_attr_ls, [0,1] , False)
        
noise_add_attr("ctrl_fk_0_spine_2")
