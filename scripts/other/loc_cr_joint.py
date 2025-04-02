import maya.cmds as cmds

def cr_jnt_from_locator(sel, group_name):
    cmds.group(n=group_name, em=1)
    for s in sel:
        cmds.select(cl=1)
        jnt_nm = s.replace('ctrl', 'jnt_skn')
        cmds.joint(n=jnt_nm)
        cmds.matchTransform(jnt_nm, s)
        cmds.makeIdentity(jnt_nm, a=1, t=0, r=1, s=0, n=0, pn=1)
        cmds.parent(jnt_nm, group_name)

cr_jnt_from_locator(cmds.ls(sl=1, typ="transform"), "grp_jnts_head_switches")