import maya.cmds as cmds
 
class curveCube():
    def __init__(self):
        self.var_cube = self.my_cube_()
        print( self.var_cube )
        #return self.var_cube
    def my_cube_(self):
        myCube = cmds.curve(n="ctrl_1",d=1,p=[(0,0,0),(1,0,0),(1,0,1),(0,0,1),(0,0,0),
                                   (0,1,0),(1,1,0),(1,0,0),(1,1,0),
                                   (1,1,1),(1,0,1),(1,1,1),
                                   (0,1,1),(0,0,1),(0,1,1),(0,1,0)])
                
        cmds.CenterPivot()
        cmds.xform(myCube,t=(-.5,-.5,-.5))
        cmds.select(myCube)
        cmds.FreezeTransformations()
        cmds.rename("ctrl_1")
        cmds.delete(myCube, ch=1)
        return myCube
        
            
# This is how you call/u can call from other files, filename, before class name
#myCube = curveCube()