import maya.cmds as cmds

def Multi_constrain():
    
    multi = 1

    # Get selected objects in the scene
    all_objects = cmds.ls(sl=1)

    # Initialize lists for joints and controls
    selected_controls = []
    selected_joints = []

    # Iterate through all objects
    for obj in all_objects:
        # Check if the object is a joint
        if cmds.nodeType(obj) == 'joint':
            selected_joints.append(obj)
        # Check if the object is a control curve
        elif cmds.nodeType(obj) == 'transform' and cmds.listRelatives(obj, shapes=True, type='nurbsCurve'):
            selected_controls.append(obj)

    # Print the lists
    print("Joints List:", selected_joints)
    print("Controls List:", selected_controls)

    num_control_parents = len(selected_controls)
    print("ctrls:  ", num_control_parents)
    num_joint_parents = len(selected_joints)
    print("jnts:  ",num_joint_parents)

    if multi:
        def get_hierarchy(node):
            hierarchy = [node]
            children = cmds.listRelatives(node, children=True, type="transform") or []
            for child in children:
                hierarchy.extend(get_hierarchy(child))
            return hierarchy
        
        def parent_controls_to_joints(selected_controls, selected_joints):
            for control_parent, joint_parent in zip(selected_controls, selected_joints):
                control_children = get_hierarchy(control_parent)
                joint_children = get_hierarchy(joint_parent)
                print("Joints List:", control_children)
                print("Controls List:", control_children)
                
                for ctrl, jnt in zip(control_children, joint_children):
                    if cmds.objExists(ctrl) and cmds.objExists(jnt):
                        constraint = cmds.parentConstraint( ctrl, jnt, mo=True)[0]
                        print(f"{constraint} - {ctrl} to {jnt}")
                    else:
                        print(f"Error: Target control or joint not found - {ctrl}, {jnt}")
        # Check if the number of selected control and joint parents match
        parent_controls_to_joints(selected_controls, selected_joints)
    else:
        sel = cmds.ls(sl=1, typ="transform")
        ctrl_sel = cmds.listRelatives( sel[0], ad=1, typ="transform" )
        print(ctrl_sel)
        ctrl_sel.append(sel[0])
        ctrl_sel.reverse()
        jnt_sel = cmds.listRelatives( sel[1], ad=1, typ="joint" )
        jnt_sel.append(sel[1])
        jnt_sel.reverse()
        print(jnt_sel)
        for i in range(len(ctrl_sel)):
            cmds.parentConstraint( ctrl_sel[i], jnt_sel[i], mo=1 )