import maya.cmds as cmds

def rename_loc_attributes():
    # Get selected objects
    selected_objects = cmds.ls(selection=True, long=True)

    if not selected_objects:
        cmds.warning("No objects selected. Please select at least one object.")
        return

    for obj in selected_objects:
        # Get all attributes of the object
        attributes = cmds.listAttr(obj, scalar=True)
        if not attributes:
            continue
        
        for attr in attributes:
            # Construct the full attribute name
            full_attr_name = f"{obj}.{attr}"
            
            # Check if the attribute exists and is queryable
            if not cmds.objExists(full_attr_name):
                continue

            try:
                # Check if the attribute is a float attribute and ends with "_Loc"
                if cmds.getAttr(full_attr_name, type=True) == 'double' and attr.endswith('_Loc'):
                    # Create new attribute names with lowercase "_loc"
                    new_long_name = attr[:-4] + '_loc'
                    nice_name = cmds.attributeQuery(attr, node=obj, niceName=True)
                    new_nice_name = nice_name[:-4] + ' loc'
                    print(f"here {new_nice_name}")
                    # Rename the attribute
                    cmds.renameAttr(full_attr_name, new_long_name)
                    
                    # Set the nice name to the new nice name
                    cmds.addAttr(f"{obj}.{new_long_name}", edit=True, niceName=new_nice_name)
                    cmds.select(obj)
                    cmds.select(cl=1)
                    cmds.select(obj)
                
            except Exception as e:
                print(f"Error processing attribute {full_attr_name}: {e}")

# Run the function
rename_loc_attributes()

#cmds.addAttr("ctrl_type_shit_.Helen_Loc", e=1, niceName="Frank")