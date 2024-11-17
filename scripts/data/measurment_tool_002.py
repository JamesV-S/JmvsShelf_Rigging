
import maya.cmds as cmds
import os
import sys
import importlib

'''
import importlib
from JmvsShelf_Rigging.scripts.data import measurment_tool_001.py

importlib.reload(measurment_tool_001.py)
measurment_tool_001.py.jmvs_measurment_tool()
'''
from JmvsShelf_Rigging.scripts.data import measurement_dict
importlib.reload(measurement_dict)

from measurement_dict import arm_measurement_dict, head_measurement_dict

class jmvs_measurment_tool():
    def __init__(self):
        
        limb, hand = arm_measurement_dict("Max")
        self.place_locator_measurments(limb, "hand")
        self.place_locator_measurments(hand, "hand")

    def connector_curve(self, top_loc, bttm_loc):
        top_point_loc = cmds.xform(top_loc ,q=1, ws=1, rp=1)
        bttm_point_loc =  cmds.xform(bttm_loc ,q=1, ws=1, rp=1)
        curve_name = f"crv_height_{top_loc}"
        cmds.curve(d=1, p=[top_point_loc, bttm_point_loc], n=curve_name)
        cluster_1 = cmds.cluster(
            f"{curve_name}.cv[0]", n=f"cluster_crv_{top_loc}_cv0"
            )
        cluster_2 = cmds.cluster(
            f" {curve_name}.cv[1]", n=f"cluster_crv_{bttm_loc}_cv0"
            )
        
        cmds.parent(cluster_1, top_loc)
        cmds.parent(cluster_2, bttm_loc)
                
        for x in cmds.ls(typ="cluster"):
            cmds.hide(f"{x}Handle")
            cmds.setAttr(f"{x}Handle.hiddenInOutliner", True)
                
        cmds.setAttr(f"{curve_name}.template", 1)
        cmds.select(cl=1)
        

    def place_locator_measurments(self, dictionary, dict_name, parent_hierachy=True):
        pref = "mes"
        
        rt_parent = f"loc_{pref}_{dict_name}_rt"
        current_path = os.path.dirname(os.path.abspath(__file__))
        SQUID_FILE = os.path.join(current_path, 
                                  "imports",
                                  "sqd_shape_001.abc"
                                  )
        print(f"rt_parent path = {current_path}")
        imported = cmds.file(SQUID_FILE, i=1, namespace="sqd_shape_001", rnn=1)
        print(imported)
        cmds.rename(imported[0], rt_parent)
        cmds.setAttr(f"{rt_parent}.scaleX", 5)
        cmds.setAttr(f"{rt_parent}.scaleY", 5)
        cmds.setAttr(f"{rt_parent}.scaleZ", 5)
        cmds.makeIdentity(rt_parent, apply=True, t=0, r=0, s=1, n=0) 
        
        sqd_shape_list = cmds.listRelatives(rt_parent, shapes=1) 
        sqd_shape = [shape for shape in sqd_shape_list if "sqd" in shape]
        for shape in sqd_shape:
            cmds.setAttr(f"{shape}.overrideEnabled", 1)
            cmds.setAttr(f"{shape}.overrideColor", 17)

        grp_name = f"grp_{pref}_{dict_name}"
        if not cmds.objExists(grp_name):
            cmds.group(empty=True, name=grp_name)
        cmds.setAttr(f"{grp_name}.displayLocalAxis", 1)

        cmds.parent(rt_parent, grp_name)
            
        # Iterate through the dictionary to create locs
        STAR_FILE = os.path.join(current_path, 
                                  "imports",
                                  "star_shape_001.abc"
                                  )

        previous_locator = None
        for key, value in dictionary.items():
            if "name" in key: 
                pass
            else:
                loc_name = f"loc_{pref}_{key}"
                if not cmds.objExists(loc_name):
                    star_imported = cmds.file(
                        STAR_FILE, i=1, namespace="star_shape_001", rnn=1
                        )
                    locator = cmds.rename(star_imported[0], loc_name)
                    cmds.setAttr(f"{locator}.translateY", value)
                    cmds.setAttr(f"{locator}.scaleX", 5)
                    cmds.setAttr(f"{locator}.scaleY", 5)
                    cmds.setAttr(f"{locator}.scaleZ", 5)
                    cmds.makeIdentity(locator, apply=True, t=0, r=0, s=1, n=0) 
                    
                    star_shape_list = cmds.listRelatives(locator, shapes=1) 
                    star_shape = [shape for shape in star_shape_list if "star" in shape]
                    for shape in star_shape:
                        cmds.setAttr(f"{shape}.overrideEnabled", 1)
                        cmds.setAttr(f"{shape}.overrideColor", 20)

            if parent_hierachy and previous_locator:
                cmds.parent(locator, previous_locator)
            else:
                cmds.parent(locator, rt_parent)
            previous_locator = locator

        # Call connector_curve function for each pair of locs
        locs = cmds.listRelatives(rt_parent, children=True) or []
        for x in range(len(locs)-1):
            try:
                if parent_hierachy == True:
                    self.connector_curve(locs[x], locs[x+1])
                else:
                    for loc in locs:
                        self.connector_curve(rt_parent, loc)
            except:
                pass


