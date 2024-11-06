#------------------------------------------------------------------
# JMVS - rename_MatchTransforms
#------------------------------------------------------------------
import maya.cmds as cmds 

class rnm_mTrans():
    def __init__(self):
        self.objMatch = cmds.ls(sl=True)
        print("obj match: ", self.objMatch)
        
        print("location to match to: ", self.objMatch[1])

        if not self.objMatch:
            cmds.error("ERROR: No obj selected")
        else:
            self.matchTrans()
        
        self.csu_rename_controls(self.objMatch[0])

    def matchTrans(self):
        objList = cmds.ls(sl=True)
        print("obj ls: ", objList)

        firstSel = objList[0]
        print("objs to move: ", firstSel)
        
        print("length:", len(objList))

        global glob_fstSel
        glob_fstSel = firstSel
    
        cmds.matchTransform(firstSel, self.objMatch, pos=1, rot=1)

    def csu_rename_controls(self, old_name):
        fstSl = glob_fstSel
        example = ["loc", "pelvis", "0"]
        print("HEEEEE: ", example[:-2]) # = 'loc' 
        
        list_1 = list(fstSl.split("_")[:-2])
        print("loc nm lenght: ", len(list_1))
        
        joined_ls_1 = '_'.join(list_1)  
        joined_ls_1 = '_'.join(list_1) 
        print("loc_pelvis_0 === ", joined_ls_1) # = 'loc' 

        list_2 = list(self.objMatch[1].split("_")[-2:])
        joined_ls_2 = '_'.join(list_2) 
        print("jnt_rig_spine_12 === ", joined_ls_2) # = 'spine_12'

        newNM = joined_ls_1 + "_" + joined_ls_2
        print(newNM)
        cmds.rename( old_name, newNM)
    
#rnm_mTrans()