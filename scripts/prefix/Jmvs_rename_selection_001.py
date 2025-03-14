import maya.cmds as cmds

def rename_list(new_name):
    selection = cmds.ls(sl=True, type="transform")
    print(f"selection = {selection}")
    
    renamed_list = []
    for index, obj in enumerate(selection):
        new_obj_name = f"{new_name}{index}"
        renamed_list.append(cmds.rename(obj, new_obj_name))
    
    print(f"renamed list = {renamed_list}")

rename_list("new_name_")