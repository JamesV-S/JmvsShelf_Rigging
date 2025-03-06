
# float_custom_attr_func
import maya.cmds as cmds

attrib_list = ["James" ,"HArv", "Thuki", "Arron"]
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
   

#add_float_attrib(cmds.ls(attrib_list, [0,1] , False)


