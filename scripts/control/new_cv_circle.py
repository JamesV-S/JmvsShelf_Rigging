import maya.cmds as cmds

def nurbsCircle():
    #primary axis for jnt:
    Xaxis=(1,0,0)
    Yaxis=(0,1,0)
    Zaxis=(0,0,1)

    #cmds.curve( n='ctrl_', nr=(1,0,0), sw=360, r=1, d=3, s=8 )
    # create full circle at origin on the x-y plane
    cmds.circle( n='ctrl_type_shit_', nr=Xaxis, c=(0, 0, 0), sw=360, s=8, ut=0 )

