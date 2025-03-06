import maya.cmds as cmds
import maya.cmds as cmds

def get_default_time_node():
    # Find all time nodes in the scene
    time_nodes = cmds.ls(type='time')
    
    for node in time_nodes:
        # Check if the node is the default time node
        if cmds.nodeType(node) == 'time' and cmds.getAttr(node + '.outTime', settable=False):
            return node
    
    return None

# Get the default time node
default_time_node = get_default_time_node()

if default_time_node:
    print(f"Default time node found: {default_time_node}")
else:
    print("No default time node found. You might need to create one.")

axis_ls = ['x', 'y', 'z']
for x in range(3):
    cmds.connectAttr(f"{default_time_node}.outTime", f"PMA_autoMotionShakeOffset.input3D[0].input3D{axis_ls[x]}", f=1)