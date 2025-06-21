import maya.cmds as cmds

def my_replace_ctrl():
        curves = cmds.ls(sl=1)
        for x in curves:
            shape = cmds.listRelatives(type="nurbsCurve", c=1)
            shape_grp = cmds.listRelatives(shape, p=1)
            #print(shape[:1])
            #print(shape_grp[1])
            try:
                cmds.parent(shape[:1], shape_grp[1:], s=1, r=1)
                cmds.delete( shape_grp[0], shape[1:] )
            except TypeError:
                print( "replaced the old control!" )
            
my_replace_ctrl()

def big_replace_tool(hi=0):
    if not hi:
        my_replace_ctrl()
    else:
         print("gonna do a madness!")


    # select 1st 
# big_replace_tool()
