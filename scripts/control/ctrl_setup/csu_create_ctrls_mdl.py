import maya.cmds as cmds

def csu_create_controls(self, num_controls, axis):
    #creating the control:
        if self.create_cv == True:
            
            print( f"working on {num_controls} controllers" )           
            
            if self.ctrl_type:
                create_ctrls = [cmds.circle( n='ctrl_', nr=axis, c=(0, 0, 0), sw=360, s=8, ut=0 ) for i in range(num_controls)]
            else: #This needs to be 
                ctrlCV = []
                for i in range(int(num_controls)):
                    ctrlCV.append(cmds.curve(n="ctrl_",d=1,p=[(0,0,0),(1,0,0),(1,0,1),(0,0,1),(0,0,0),
                                (0,1,0),(1,1,0),(1,0,0),(1,1,0),
                                (1,1,1),(1,0,1),(1,1,1),
                                (0,1,1),(0,0,1),(0,1,1),(0,1,0)]))
            
                    cmds.CenterPivot()
                cmds.xform(ctrlCV,t=(-.5,-.5,-.5))
                cmds.select(ctrlCV)
                cmds.FreezeTransformations()
                cmds.rename("ctrl_", ignoreShape=1)
                cmds.delete(ctrlCV, ch=1)
                                    
            # Put controls into correct hierarchy 
            if self.ctrl_type:
                ctl_sl = [cmds.ls( create_ctrls[i], type='transform' ) for i in range(num_controls)]
                ctrlCV = [element for sublist in ctl_sl for element in sublist]
                for i in range(num_controls-1): 
                    cmds.parent( ctrlCV[i+1], ctrlCV[i] )
                cmds.select(cl=1)
            else:
                for i in range(num_controls-1): 
                    cmds.parent( ctrlCV[i+1], ctrlCV[i] )
                #cmds.select(cl=1)
        else:
            #put the ctrls into a hierarchy
            print("Didn't create new cvs on purpose, so working on one ctrl")
            ctrlCV = cmds.ls(sl=1, type='transform')
            print("i'm looking for the control I select! -> ", ctrlCV)
        global ctl_ls
        ctl_ls = ctrlCV
        print('HERE_IS_ctrls_ls:', ctl_ls)
        return ctl_ls