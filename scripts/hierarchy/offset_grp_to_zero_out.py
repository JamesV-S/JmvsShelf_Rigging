import maya.cmds as cmds

def ofst_grp_to_zero():
    selection = cmds.ls(sl=1, type="transform")
    cmds.select(selection, hi=1)
    full_sel = cmds.ls(sl=1, type="transform")
    print(full_sel)

    for i in range(len(full_sel)):
        offset_grp = cmds.group(n=f"offset_{full_sel[i]}", em=1)
        cmds.matchTransform(offset_grp, full_sel[i])
        cmds.parent(full_sel[i], offset_grp)