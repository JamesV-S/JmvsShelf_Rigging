
import maya.cmds as cmds

def connector_curve(obj_item, single_obj):
        print(f"connector_cruve: {obj_item}")
        top_point_loc = cmds.xform(obj_item ,q=1, ws=1, rp=1)
        bttm_point_loc =  cmds.xform(single_obj ,q=1, ws=1, rp=1)
        curve_name = f"crv_mes_{obj_item}"
        cmds.curve(d=1, p=[top_point_loc, bttm_point_loc], n=curve_name)
        cluster_1 = cmds.cluster(
            f"{curve_name}.cv[0]", n=f"cluster_crv_{obj_item}_cv0"
            )
        cluster_2 = cmds.cluster(
            f" {curve_name}.cv[1]", n=f"cluster_crv_{single_obj}_cv0"
            )
        # cmds.setAttr(f"{curve_name}.hiddenInOutliner", True)
        cmds.parent(cluster_1, obj_item)
        cmds.parent(cluster_2, single_obj)
             
        for x in cmds.ls(typ="cluster"):
            cmds.hide(f"{x}Handle")
            cmds.setAttr(f"{x}Handle.hiddenInOutliner", True)
        if cmds.objExists(curve_name):
            if cmds.attributeQuery('template', node=curve_name, exists=True):
                cmds.setAttr(f"{curve_name}.template", 1)
        cmds.select(cl=1)

        return curve_name

def connector_curve_sep(single_obj, list_obj):
    curve_ls = []
    for obj_item in list_obj:
        top_point_loc = cmds.xform(obj_item, q=1, ws=1, rp=1)
        bttm_point_loc = cmds.xform(single_obj, q=1, ws=1, rp=1)
        
        curve_name = f"crv_mes_{obj_item}"
        cmds.curve(d=1, p=[top_point_loc, bttm_point_loc], n=curve_name)
        
        cluster_1 = cmds.cluster(f"{curve_name}.cv[0]", n=f"cluster_crv_{obj_item}_cv0")
        cluster_2 = cmds.cluster(f"{curve_name}.cv[1]", n=f"cluster_crv_{single_obj}_cv0")
        
        cmds.parent(cluster_1, obj_item)
        cmds.parent(cluster_2, single_obj)
        
        for x in cmds.ls(typ="cluster"):
            cmds.hide(f"{x}Handle")
            cmds.setAttr(f"{x}Handle.hiddenInOutliner", True)
        
        cmds.setAttr(f"{curve_name}.template", 1)
        cmds.select(cl=1)
        curve_ls.append(curve_name)
    print(f"curve_ls > {curve_ls}")
