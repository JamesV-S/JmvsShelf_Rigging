
# Delete multiple custom attributes.

import maya.cmds as cmds

def delete_custom_attributes(attr_type, specific):
    ctrl = cmds.ls(sl=1, type="transform")
    if specific:
        for target in ctrl:
            try:
                attrs = cmds.listAttr(target, userDefined=True) or []
                for attr in attrs:
                    if attr_type is None or cmds.getAttr(F"{target}.{attr}", type=True) == attr_type:
                        try:
                            cmds.setAttr(f"{target}.{attr}", lock=0)
                        except:
                            print(f"Failed unlock{target}.{attr}")                        
            except:
                print(f"No custom attributes of type {attr_type} found on {target}")
        cmds.DeleteAttribute()
    else:
        for target in ctrl:
            try:
                attrs = cmds.listAttr(target, userDefined=True) or []
                for attr in attrs:
                    if attr_type is None or cmds.getAttr(F"{target}.{attr}", type=True) == attr_type:
                        try:
                            cmds.setAttr(f"{target}.{attr}", lock=0)
                            cmds.deleteAttr(f"{target}.{attr}")
                            print(f"{target}.{attr}")
                        except:
                            print(f"Failed to unlock & delete {target}.{attr}")
            except:
                print(f"No custom attributes of type {attr_type} found on {target}")
#delete_custom_attributes( None, 0) # None = Any , double = Float, enum = enum