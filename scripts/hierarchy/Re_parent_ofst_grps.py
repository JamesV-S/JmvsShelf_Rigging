import maya.cmds as cmds

def Re_parent_Ofset_grps():

    # Get the selected groups
    selected_groups = cmds.ls(selection=True)
    selected_groups.reverse()
    list_relative = [ cmds.listRelatives(selected_groups[i], children=True) for i in range(len(selected_groups))] 
    children = ['_'.join(list_relative[i]) for i in range(len(list_relative))]

    print("children: ", children)
    print("groups: ", selected_groups)
    minus_child = children[1:]

    for x in range(len(selected_groups)-1):
        #print('Parented {} to {}'.format(selected_groups[x], minus_child[x]))
        cmds.parent( selected_groups[x], minus_child[x] )