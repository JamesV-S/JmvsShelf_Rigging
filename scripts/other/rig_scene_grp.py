import maya.cmds as cmds

#def rig_grp(): 

hi_name_list = ['JMVS_rig', 'controls', 'DO_NOT_TOUCH', 
                'rig_buffer', 'geo', 'skeleton', 'rig_systems', 
                'blendshapes', 'misc', 'grp_ctrl_arm_l', 
                'grp_ctrl_arm_r', 'grp_ctrl_leg_l', 
                'grp_ctrl_leg_r', 'grp_ctrl_torso'
                ]

def create_group_hierarchy(the_range=range(len(hi_name_list))):

    hi_list = []
        
    for i in the_range:
                   
        agrp = cmds.group(em=1, n=hi_name_list[i])
            
        hi_list.append(agrp)
            
    return hi_list

def parent_hi_groups():

    grp_list = create_group_hierarchy()

        # parent 'controls' & 'DO_NOT_TOUCH' to 'JMVS_rig'
    cmds.parent(grp_list[1:3], grp_list[0])

        # parent 'rig_buffer' to 'DO_NOT_TOUCH'
    cmds.parent(grp_list[3], grp_list[2])
        
        # parent ['controls', 'skeleton', 'rig_systems', 'blendshapes', 'misc' to 'rig':
    cmds.parent( grp_list[4:9], grp_list[3] )
    
    cmds.parent(grp_list[9:14],  grp_list[1] )

    cmds.select(cl=1)
    print("RIG GRP REPO")

