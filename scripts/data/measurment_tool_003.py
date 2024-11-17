import configparser
import maya.cmds as cmds
import os
import sys
import importlib

from JmvsShelf_Rigging.scripts import utils as util

importlib.reload(util)

'''
import importlib
from JmvsShelf_Rigging.scripts.data import measurment_tool_001.py

importlib.reload(measurment_tool_001.py)
measurment_tool_001.py.jmvs_measurment_tool()
'''

class jmvs_measurment_tool():
    def __init__(self):
        config = configparser.ConfigParser()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ini_list = ['leg_measurements_Max.ini', 'arm_measurements_Max.ini', 'head_measurements_Max.ini', 'head_measurements_Jae.ini']# ['leg_measurements_Max.ini'] #, 'leg_measurements_Max.ini', 'arm_measurements_Max.ini', 'head_measurements_Max.ini', 'head_measurements_Jae.ini']# ['leg_measurements_Max.ini']# ['leg_measurements_Max.ini'] #, 'leg_measurements_Max.ini', 'arm_measurements_Max.ini', 'head_measurements_Max.ini', 'head_measurements_Jae.ini']# ['leg_measurements_Max.ini'] #, 'leg_measurements_Max.ini', 'arm_measurements_Max.ini', 'head_measurements_Max.ini', 'head_measurements_Jae.ini']# ['leg_measurements_Max.ini'] #, 'leg_measurements_Max.ini', 'arm_measurements_Max.ini', 'head_measurements_Max.ini', 'head_measurements_Jae.ini']# ['leg_measurements_Max.ini']# ['leg_measurements_Max.ini'] #, 'leg_measurements_Max.ini', 'arm_measurements_Max.ini', 'head_measurements_Max.ini', 'head_measurements_Jae.ini']# ['leg_measurements_Max.ini']
            # 
        
        # create the .ini fole path then read
        for ini in ini_list:
            config_file = os.path.join(current_dir, '..', '..', 'config', ini)
            config.read(config_file)        
        print(config.sections())
        # output = ['limb', 'hand', 'handknuWidth', ...]
        
        ''' * Method to load all avalable ini_files: '''
        # get the boolean val for parent_hierarchy read on the .ini file
        mes_guide_list = []
        for section in config.sections():
            print(f"processing section: {section}")
            part = {key: float(value) for key, value in config[section].items()
                     if key != 'parent_hierachy'}
            # if `parent_hierachy` is not specified, it defaults to `True`
            prnt_hi = config.getboolean(section, 'parent_hierachy', fallback=True)
            mes_guide = self.place_locator_measurments(part, section, prnt_hi)
            mes_guide_list.append(mes_guide)
        
        # Create dictionary's from specified ini sections
        # limb = {key: float(value) for key, value in config['limb'].items()}
        
        ''' DO NOT DELETE
        * This is the individual method, for sepcific. 
        neckLengthM = {
                key: float(value) for key, value in config['neckLengthM'].items()}
        neckLengthJ = {
                key: float(value) for key, value in config['neckLengthJ'].items()}
        handknuWidth = {
                key: float(value) for key, value in config['handknuWidth'].items()}

        self.place_locator_measurments(limb, "limb")
        self.place_locator_measurments(neckLengthM, "neckLengthM")
        self.place_locator_measurments(neckLengthJ, "neckLengthJ")
        self.place_locator_measurments(handknuWidth, "handknuWidth")
        '''
        # group the measurement guides all in one grp, 
        print(f"self.grp_connectors: {mes_guide_list}")
        if "grp_gds_mesurements" in cmds.ls("grp_gds_mesurements"):
            cmds.parent(self.grp_connectors, mes_guide_list, "grp_gds_mesurements")
        else: 
            cmds.group(self.grp_connectors, mes_guide_list, n="grp_gds_mesurements", w=1)
        cmds.select(cl=1)


    def place_locator_measurments(self, dictionary, dict_name, parent_hierachy):
        pref = "mes"
        
        # import the squid alembic shape
        first_key = next(iter(dictionary))
        print(f"first key: {first_key}")
        suffix = first_key[first_key.rfind('_'):]
        print(f"suffix: {suffix}")
        rt_parent = f"sqd_rt_{dict_name}{suffix}"
        current_path = os.path.dirname(os.path.abspath(__file__))
        SQUID_FILE = os.path.join(current_path, 
                                  "imports",
                                  "sqd_shape_001.abc"
                                  )
        print(f"rt_parent path = {current_path}")
        imported = cmds.file(SQUID_FILE, i=1, namespace="sqd_shape_001", rnn=1)
        print(imported)
        cmds.rename(imported[0], rt_parent)
        
        # scale the shape
        num = []
        for key, value in dictionary.items():
            num.append(value)
        if num[0] < 14:
            cmds.setAttr(f"{rt_parent}.scaleX", 2.5)
            cmds.setAttr(f"{rt_parent}.scaleY", 2.5)
            cmds.setAttr(f"{rt_parent}.scaleZ", 2.5)
        else:
            cmds.setAttr(f"{rt_parent}.scaleX", 5)
            cmds.setAttr(f"{rt_parent}.scaleY", 5)
            cmds.setAttr(f"{rt_parent}.scaleZ", 5)
        cmds.makeIdentity(rt_parent, apply=True, t=0, r=0, s=1, n=0) 

        yellow_colour = (1.0, 1.0, 0.0)
        cmds.setAttr(f"{rt_parent}.useOutlinerColor", 1)
        cmds.setAttr(f"{rt_parent}.outlinerColor", yellow_colour[0], yellow_colour[1], yellow_colour[2], type="double3")


        # rename the shapes to avoid duplicates
        squid_shape_list = cmds.listRelatives(rt_parent, shapes=1)
        for x, shape in enumerate(squid_shape_list):
            squid_shape_name = f"rt_{dict_name}_squidShape_{x}"
            cmds.rename(shape, squid_shape_name)
            cmds.setAttr(f"{squid_shape_name}.overrideEnabled", 1)
            cmds.setAttr(f"{squid_shape_name}.overrideColor", 17)

        self.grp_name = f"grp_{pref}_{dict_name}{suffix}"
        if not cmds.objExists(self.grp_name):
            cmds.group(empty=True, name=self.grp_name)
        cmds.setAttr(f"{self.grp_name}.displayLocalAxis", 1)
        white = (1.0, 1.0, 1.0)
        cmds.setAttr(f"{self.grp_name}.useOutlinerColor", 1)
        cmds.setAttr(f"{self.grp_name}.outlinerColor", white[0], white[1], white[2], type="double3")
        
        cmds.parent(rt_parent, self.grp_name)
        
        #----------------------------------------------------------------------
        # Iterate through the dictionary to create locs
        STAR_FILE = os.path.join(current_path, 
                                  "imports",
                                  "star_shape_001.abc"
                                  )

        previous_locator = None
        for key, value in dictionary.items():
            
            loc_name = f"str_{pref}_{key}"
            # if not cmds.objExists(loc_name):
            star_imported = cmds.file(
                STAR_FILE, i=1, namespace="star_shape_001", rnn=1
                )
            locator = cmds.rename(star_imported[0], loc_name)
                
            if parent_hierachy and previous_locator:
                cmds.parent(locator, previous_locator)
            else:
                cmds.parent(locator, rt_parent)
            previous_locator = locator
                
            cmds.setAttr(f"{locator}.translateY", value)
            light_blue = (0.68, 0.85, 0.90)
            cmds.setAttr(f"{locator}.useOutlinerColor", 1)
            cmds.setAttr(f"{locator}.outlinerColor", light_blue[0], light_blue[1], light_blue[2], type="double3")

            if value < 14:
                cmds.setAttr(f"{locator}.scaleX", 2.5)
                cmds.setAttr(f"{locator}.scaleY", 2.5)
                cmds.setAttr(f"{locator}.scaleZ", 2.5)
            else:
                cmds.setAttr(f"{locator}.scaleX", 5)
                cmds.setAttr(f"{locator}.scaleY", 5)
                cmds.setAttr(f"{locator}.scaleZ", 5)
            cmds.makeIdentity(locator, apply=True, t=0, r=0, s=1, n=0) 

            # rename the shapes to avoid duplicates
            star_shape_list = cmds.listRelatives(locator, shapes=1)
            for x, shape in enumerate(star_shape_list):
                star_shape_name = f"str_{key}_starShape_{x}"
                cmds.rename(shape, star_shape_name)
                cmds.setAttr(f"{star_shape_name}.overrideEnabled", 1)
                cmds.setAttr(f"{star_shape_name}.overrideColor", 28) # 20
                
        # Call connector_curve function for each pair of locs
        locs = cmds.listRelatives(rt_parent, ad=True, type="transform") or []
        print(f"rt_parent: {rt_parent}, locs from rt_parent = {locs}" )
        locs.append(rt_parent)
        locs.reverse()
        # ['loc_mes_knee_ankle_max', 'loc_mes_hip_knee_max']
        
        for x in range(len(locs)-1):
            #try:
            if parent_hierachy:
                print(f"parent TRUE")
                util.connector_curve(locs[x], locs[x + 1])
        if not parent_hierachy:
            print(f"parent FALSE")
            sep_locs = cmds.listRelatives(rt_parent, ad=True, type="transform") or []
            print(f"FFFFF>> {sep_locs}")
            util.connector_curve_sep(rt_parent, sep_locs)
        
        connector_pref = cmds.ls("crv_mes_*", type="transform")
        print(f"CONNECTOR pref >> {connector_pref}")
        self.grp_connectors = "grp_mes_connectors"
        if "grp_mes_connectors" in cmds.ls("grp_mes_connectors"):
            cmds.parent(connector_pref, "grp_mes_connectors")
        else:
            cmds.group(connector_pref, n="grp_mes_connectors", w=1)
        cmds.select(cl=1)

        return self.grp_name


