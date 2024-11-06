
# switch_enum_attr
import maya.cmds as cmds

def custom_enum_attr(CtrlEnmOptions, enm_lng_nm):
    
    mstr_ctrl = cmds.ls(sl=1, type="transform")
    
    cmds.addAttr(longName=enm_lng_nm, at="enum", enumName=CtrlEnmOptions )
    cmds.setAttr( f"{mstr_ctrl[0]}.{enm_lng_nm}", e=1, k=1 )

#custom_enum_attr( "Thuki:Arron:Harv", "James")