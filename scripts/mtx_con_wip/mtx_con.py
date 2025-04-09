import maya.cmds as cmds
from maya.api import OpenMaya as om

#------------------------------ UTILITY ---------------------------------------
def cr_node_if_not_exists(util_type, node_type, node_name, set_attrs=None):
    if not cmds.objExists(node_name):
        if util_type:
            cmds.shadingNode(node_type, au=1, n=node_name)
        else:
            cmds.createNode(node_type, n=node_name)
        if set_attrs:
            for attr, value in set_attrs.items():
                cmds.setAttr(f"{node_name}.{attr}", value)


def connect_attr(source_attr, target_attr):
    connections = cmds.listConnections(target_attr, destination=False ,source=True)
    #print(f"here is the listed connection: {connections}")
    if not connections:
        cmds.connectAttr(source_attr, target_attr, force=True)
    else:
        print(f" CON {source_attr} is already connected to {target_attr} ")
#------------------------------------------------------------------------------

def add_matrix_attr(node, attr_name):
    cmds.addAttr(node, ln=attr_name, at="matrix")


def constraint_type_matrix_setup(drivewn_obj, MM_node, BM_node, list):
    # matrix node on MM to storte driven's orig mtx
    orig_mtx_attr = f"orig_{drivewn_obj}_mtx"
    add_matrix_attr(MM_node, orig_mtx_attr)    
    
    # Don't connect translate 
    for attr in list:
        if not attr == "t":
            connect_attr(f"{MM_node}.{orig_mtx_attr}", f"{BM_node}.target[0].targetMatrix")
        else:
            connect_attr(f"{drivewn_obj}.worldMatrix[0]", f"{MM_node}.{orig_mtx_attr}")
            cmds.disconnectAttr(f"{drivewn_obj}.worldMatrix[0]", f"{MM_node}.{orig_mtx_attr}")
            connect_attr(f"{MM_node}.{orig_mtx_attr}", f"{BM_node}.target[0].targetMatrix")

    # set the appropriate attr on BM for user requested constraint
    BM_attr_ls = ["scaleWeight", "translateWeight", "rotateWeight"]
    for x in range(len(BM_attr_ls)):
        cmds.setAttr(f"{BM_node}.target[0].{BM_attr_ls[x]}", 1)
    for attr in list:
        if attr == "t":
            cmds.setAttr(f"{BM_node}.target[0].translateWeight", 0)
        if attr == "r":
            cmds.setAttr(f"{BM_node}.target[0].rotateWeight", 0)
        if attr == "s":
            cmds.setAttr(f"{BM_node}.target[0].scaleWeight", 0)


def mtxCon_attr_id(driven, driven_attr, list):
    for attr in list:
        if attr == "t":
            niceName = f"R_S_{driven_attr}"
        elif attr == "r":
            niceName = f"T_S_{driven_attr}"
        elif attr == "s":
            niceName = f"T_R_{driven_attr}"
        else:
            niceName = f"All_{driven_attr}"
    cmds.addAttr(driven, longName=niceName, niceName="Constraint", 
                        attributeType="enum", enumName=niceName, k=True
                        )
            
    cmds.setAttr(f"{driven}.{niceName}", lock=False, keyable=False, 
                 channelBox=True
                 )


def matrix_constraint(driver, driven, con_type=None, mo=None):
    '''
    naming:
        mxc = matrixConstraint
        mxco = matrixConstraintOffset
        mo = maintainOffset

    # if drivers is a single object: 
        # 1 MM / 1 PM

    # if multiple drivers
        # number of drivers MM / 1 BM

    # if offset, ONLY:
        # 1 MM / 1 PM / 1 store MM / 1 store grp

    # PM should work for use to pick the type of consraint: 
        # default: {t: True, r:True, s:True}

        
    # Working on: 
        > mxc / t:1, r:0, s:1 / mo=0 [NO ROTATE]
            WORKS PERFECTLY WITHOUT CHANGING ANYTHING!
    
        > mxc / t:0, r:1, s:1 / mo=0 [NO TRANSLATE] > Must zero out the matrix attrbute on the MM
            (BEFORE = driven snaps to 0 translater mtx,  translate pos affected not constrained)
            (update needed = driven snaps to driver pos, translate pos affected not constrained)
            SOLUTION = add orig mtx to attr on MM/ 1 BM / /blendMatrix.targetMatrix = orig_attr, t=1 else 0 

        > mxc / t:1, r:1, s:0 / mo=0 [NO SCALE]
            (BEFORE = driven snaps to 0 translater mtx,  translate pos affected not constrained)
            (update needed = driven snaps to driver pos, translate pos affected not constrained)
            SOLUTION = add orig mtx to attr on MM/ 1 BM / /blendMatrix.targetMatrix = orig_attr, s=1 else 0 

    Argumnts: 
        -> Driver object/s (locator/s)
        -> Constrained Object (cube)
        -> constrained object PARENT (cube parent)
        -> BlendMatrix = switch between drivers
        -> MultMatrix = fixes double transform
    '''
    # plugs
    axis_plgs = ['X', 'Y', 'Z']
    mtx_in_plgs = []
    for x in range(3):
        plg = f".matrixIn[{x}]"
        mtx_in_plgs.append(plg)
    mtx_sum_plg = ".matrixSum"
    wld_mtx_plg = ".worldMatrix[0]"
    wld_inv_mtx_plg = ".worldInverseMatrix[0]"
    inp_mtx_plg = ".inputMatrix"
    out_mtx_plg = ".outputMatrix"
    opm_plg = ".offsetParentMatrix"
    
    # mtxCon attr name
    if mo:
        driven_attr = "mtxCon_MO"
        suffix = "mxco"
    else:
        driven_attr = "mtxCon"
        suffix = "mxc"
    
    # m = om.MMatrix(driven)
    # print(F"MMatrix = {m}")
    # driven_orig_wld = cmds.getAttr(f"{driven}{wld_mtx_plg}") # Output: list of floats
    # print(f"driven_orig_wld = {driven_orig_wld}")
    # # [0.9639752234005823, 0.0, 0.0, 0.0, 0.0, 0.9639752234005823, 0.0, 0.0, 0.0, 0.0, 0.9639752234005823, 0.0, -5.668618234121337, 0.0, 5.7217731105811644, 1.0]

    # look for parent, if doesn't exist make one!
    prnt = cmds.listRelatives(driven, p=1)
    print(f"parent = {prnt}")
    if prnt == None:
        offset_grp = cmds.createNode("transform", n=f"prnt_{driven}")
        cmds.matchTransform(offset_grp, driven)
        cmds.parent(driven, offset_grp)
        driven_parent = offset_grp
    else:
        driven_parent = prnt[0]
    
    
    # MM & PM
    MM_mtxCon = f"MM_{driven}_{suffix}"
    cr_node_if_not_exists(1, "multMatrix", MM_mtxCon)
    # orig_mtx_attr = f"orig_{driven}_mtx"
    # add_matrix_attr(MM_mtxCon, orig_mtx_attr)    
    
    BM_mtxCon = f"BM_{driven}_{suffix}"
    cr_node_if_not_exists(0, "blendMatrix", BM_mtxCon)
    
    
    # Store driven original mtx
    # connect_attr(f"{driven}.worldMatrix[0]", f"{MM_mtxCon}.{orig_mtx_attr}")
    # cmds.disconnectAttr(f"{driven}.worldMatrix[0]", f"{MM_mtxCon}.{orig_mtx_attr}")
    # connect_attr(f"{MM_mtxCon}.{orig_mtx_attr}", f"{BM_mtxCon}.target[0].targetMatrix")
    # # turn it off for now, to constrain all attr by default. 
    # BM_attr_ls = ["scaleWeight", "translateWeight", "rotateWeight"]
    # for x in range(len(BM_attr_ls)):
    #     cmds.setAttr(f"{BM_mtxCon}.target[0].{BM_attr_ls[x]}", 0)

    if mo: 
        cstm_ofs_attr = f"offsetMatrix_{driven}_{suffix}"
        print(f"driven_parent  ==  {driven_parent}")
        cmds.addAttr(driven_parent, ln=cstm_ofs_attr, at="matrix")
        
        # MM_store_ofs
        MM_store_mtxConOff = f"MM_store_{driven}_{suffix}"
        cr_node_if_not_exists(1, "multMatrix", MM_store_mtxConOff)

        # store connections
        connect_attr(f"{driven}{wld_mtx_plg}", f"{MM_store_mtxConOff}{mtx_in_plgs[0]}")
        connect_attr(f"{driver}{wld_inv_mtx_plg}", f"{MM_store_mtxConOff}{mtx_in_plgs[1]}")  

        # add the mtx to the 'driven_parent' cstm attr
        connect_attr(f"{MM_store_mtxConOff}{mtx_sum_plg}", f"{driven_parent}.{cstm_ofs_attr}")
        cmds.disconnectAttr(f"{MM_store_mtxConOff}{mtx_sum_plg}", f"{driven_parent}.{cstm_ofs_attr}")
        cmds.delete(MM_store_mtxConOff)

    # MM connections
    if mo: 
        connect_attr(f"{driven_parent}.{cstm_ofs_attr}", f"{MM_mtxCon}{mtx_in_plgs[0]}")
        connect_attr(f"{driver}{wld_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[1]}")
        connect_attr(f"{driven_parent}{wld_inv_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[2]}")
    else:
        connect_attr(f"{driver}{wld_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[0]}")
        connect_attr(f"{driven_parent}{wld_inv_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[1]}")

    # PM connection
    connect_attr(f"{MM_mtxCon}{mtx_sum_plg}", f"{BM_mtxCon}{inp_mtx_plg}")
    if con_type:
        constraint_type_matrix_setup(driven, MM_mtxCon, BM_mtxCon, con_type)

    # driven connection
    connect_attr(f"{BM_mtxCon}{out_mtx_plg}", f"{driven}{opm_plg}")
    # set the driven values to 0
    try:
        for x in range(3):
            cmds.setAttr(f"{driven}.translate{axis_plgs[x]}", 0)
            cmds.setAttr(f"{driven}.rotate{axis_plgs[x]}", 0)
            cmds.setAttr(f"{driven}.scale{axis_plgs[x]}", 1)
    except Exception as e:
        print(f"setting driven attr to default: {e}")

    # # add custom attr to driven to id it with a matrix constraint!
    # mtxCon_attr_id(driven=driven , driven_attr=driven_attr, list=con_type)
   
    # Show ther user it's succesful: 
    cmds.select(cl=1)
    cmds.select(driven)

    return driver, driven
selection = cmds.ls(sl=1, type="transform")
driver, driven = matrix_constraint(selection[0], selection[1], con_type=["t"], mo=0)

''' USELESS 
def check_all_true(dictionary):
    if all(dictionary.values()):
        return True
    return False


def get_False_key(dictionary):    
    false_attribute = [key for key, val in dictionary.items() if not val]
    return false_attribute


def set_mtxCon_type(driver, driven, con_type_dict):
    # what needs to be done for specific options!
    # if all items are True, then ignore function
    if check_all_true(con_type_dict):
        "All matrix constraint attribute values are set to True"
    else:
        false_mtx_attr = get_False_key(con_type_dict)
        for attr in false_mtx_attr:
            # translate == False
            if attr == 't':
                print("change mtx constriant setup to ignore the driver's translate")
            # rotate == False
            elif attr == 'r':
                print("change mtx constriant setup to ignore the driver's rotate")
            # scale == False
            elif attr == 's':
                print("change mtx constriant setup to ignore the driver's scale")
            # Otherwise don't do anything

selection = cmds.ls(sl=1, type="transform")
driver, driven = matrix_constraint(selection[0], selection[1], con_type=["t"], mo=0)
set_mtxCon_type(driver, driven, {"t":0, "s":True, "r":True})
'''

'''

# Deleting function must looks for, 
    > attr on driven parent
    > attr om driven
    > MM
    > BM
^Delete them^

options for positioning the driven obj, 
> stay in place constrainted
> go back to state before constraint
> go back to parent origin! (completely zeroed out!)
'''

def delete_matrix_constraint(driven):
    pass
    # get custom attr on driven to check if this has a mtxConstraint
    cmds.getAttr(driven)
    # get driven parent
    
    # get attr on driven parent 

    # 