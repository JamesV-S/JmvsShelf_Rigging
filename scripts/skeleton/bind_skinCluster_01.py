
import maya.cmds as cmds


def retrieve_jnt_and_geo_list():
    jnt_list = []
    geo_list = []

    selection = cmds.ls(sl=1)
    if selection:
        print(f"sel = {selection}")
        for sel in selection:
            obj_type = cmds.nodeType(sel)
            if obj_type == "joint":
                jnt_list.append(sel)
            elif obj_type in ["transform"]:
                geo_list.append(sel)
    return jnt_list, geo_list


def bind_joints_to_geos():
    # retrieve the joints and geo selected
    jnt_list, geo_list = retrieve_jnt_and_geo_list()
    print(f"retrieved joint sel `{jnt_list}` & geo sel `{geo_list}`")
    
    all_bound = True
    for geo in geo_list:
        skn_clus = cmds.ls(cmds.listHistory(geo), type='skinCluster')
        print(f"skin_cluster")
        try: # # handle attempting to bind a jnts that's alr influencing the geo
            if skn_clus:
                print(f"ZZ SkinCluster is True")
                existing_jnt_influence = cmds.skinCluster( skn_clus[0], q=1, inf=1 )
                for jnt in jnt_list:
                    if jnt not in existing_jnt_influence:
                        cmds.skinCluster(skn_clus[0], edit=1, addInfluence=jnt, wt=0)
                        print(f"Added influence `{jnt}` to geo `{geo}`")
                        all_bound = False
            else:
                cmds.skinCluster(jnt_list, geo, tsb=True, wd=1)
                print(f"binded skin: geo `{geo}`, to jnt `{jnt_list}`")
                all_bound = False
        except RuntimeError as e:
            print(f"RuntimeError: in bind_skin {e}")
    
    if all_bound:
        print(f"All bind joints r already skinned to the geometry with skincluster")
    