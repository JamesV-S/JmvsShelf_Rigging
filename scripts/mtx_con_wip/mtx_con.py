import maya.cmds as cmds
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

def pickMatrix_attributes(pm_node_name, dict):
    for attr, value in dict.items():
        if attr == "t":
            cmds.setAttr(f"{pm_node_name}.useTranslate", value)
        if attr == "r":
            cmds.setAttr(f"{pm_node_name}.useRotate", value)
        if attr == "s":
            cmds.setAttr(f"{pm_node_name}.useScale", value)

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

    Argumnts: 
        -> Driver object/s (locator/s)
        -> Constrained Object (cube)
        -> constrained object PARENT (cube parent)
        -> BlendMatrix = switch between drivers
        -> MultMatrix = fixes double transform
    '''
    
    # core matrix xonstraint setup:
    if mo:
        driven_attr = "mtxCon_MO"
        suffix = "mxco"
    else:
        driven_attr = "mtxCon"
        suffix = "mxc"

    # look for parent, if doesn't exist make one!
    prnt = cmds.listRelatives(driven, p=1)
    print(f"parent = {prnt}")
    if prnt == None:
        offset_grp = cmds.createNode("transform", n=f"offset_{driven}")
        cmds.matchTransform(offset_grp, driven)
        cmds.parent(driven, offset_grp)
        driven_parent = offset_grp
    else:
        driven_parent = prnt[0]
    
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
    
    # MM & PM
    MM_mtxCon = f"MM_{driven}_{suffix}"
    cr_node_if_not_exists(1, "multMatrix", MM_mtxCon)
    PM_mtxCon = f"PM_{driven}_{suffix}"
    cr_node_if_not_exists(1, "pickMatrix", PM_mtxCon)
    
    if mo: 
        cstm_ofs_attr = "offsetMatrix"
        cmds.addAttr(driven_parent, ln="offsetMatrix", at="matrix")
        
        # grp_store_ofs
        grp_store_mtxConOff = f"grp_store_{driven}_{suffix}"
        cr_node_if_not_exists(0, "transform", grp_store_mtxConOff)
        cmds.matchTransform(grp_store_mtxConOff, driven, pos=1, rot=1, scl=1)
        cmds.parent(grp_store_mtxConOff, driven_parent)
        cmds.setAttr (f"{grp_store_mtxConOff}.overrideEnabled" ,True)
        cmds.setAttr (f"{grp_store_mtxConOff}.hiddenInOutliner" ,True)
        
        # MM_store_ofs
        MM_store_mtxConOff = f"MM_store_{driven}_{suffix}"
        cr_node_if_not_exists(1, "multMatrix", MM_store_mtxConOff)

        # store connections
        connect_attr(f"{grp_store_mtxConOff}{wld_mtx_plg}", f"{MM_store_mtxConOff}{mtx_in_plgs[0]}")
        connect_attr(f"{driver}{wld_inv_mtx_plg}", f"{MM_store_mtxConOff}{mtx_in_plgs[1]}")  

        # add the mtx to the 'driven_parent' cstm attr
        connect_attr(f"{MM_store_mtxConOff}{mtx_sum_plg}", f"{driven_parent}.{cstm_ofs_attr}")
        cmds.disconnectAttr(f"{MM_store_mtxConOff}{mtx_sum_plg}", f"{driven_parent}.{cstm_ofs_attr}")

    # MM connections
    if mo: 
        connect_attr(f"{driven_parent}.{cstm_ofs_attr}", f"{MM_mtxCon}{mtx_in_plgs[0]}")
        connect_attr(f"{driver}{wld_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[1]}")
        connect_attr(f"{driven_parent}{wld_inv_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[2]}")
    else:
        connect_attr(f"{driver}{wld_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[0]}")
        connect_attr(f"{driven_parent}{wld_inv_mtx_plg}", f"{MM_mtxCon}{mtx_in_plgs[1]}")

    # PM connection
    connect_attr(f"{MM_mtxCon}{mtx_sum_plg}", f"{PM_mtxCon}{inp_mtx_plg}")
    if con_type:
        pickMatrix_attributes(PM_mtxCon, con_type)

    # driven connection
    connect_attr(f"{PM_mtxCon}{out_mtx_plg}", f"{driven}{opm_plg}")
    # set the driven values to 0
    for x in range(3):
        cmds.setAttr(f"{driven}.translate{axis_plgs[x]}", 0)
        cmds.setAttr(f"{driven}.rotate{axis_plgs[x]}", 0)
        cmds.setAttr(f"{driven}.scale{axis_plgs[x]}", 1)

    # add custom attr to driven to id it with a matrix constraint!
    cmds.addAttr(driven, longName=driven_attr, niceName="CONSTRAINT > ", 
                        attributeType="enum", enumName=driven_attr, k=True
                        )
            
    cmds.setAttr(f"{driven}.{driven_attr}", lock=True, keyable=False, 
                channelBox=False
                )
   
    # Show ther user it's succesful: 
    cmds.select(cl=1)
    cmds.select(driven)

selection = cmds.ls(sl=1, type="transform")

matrix_constraint(selection[0], selection[1], con_type={"r":0}, mo=0)





