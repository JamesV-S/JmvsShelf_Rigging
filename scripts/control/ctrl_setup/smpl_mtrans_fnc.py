import maya.cmds as cmds

def Mtrans(self, fst, scnd, rng):
    print("within mTrans, 'fst' = ", fst)
    print("within mTrans, 'scnd' = ", scnd)
    if not self.create_cv:
        if self.Axis == self.Zaxis:
            cmds.setAttr(f"{fst}.rotateY", 90)
        elif self.Axis == self.Yaxis:
            cmds.setAttr(f"{fst}.rotateZ", 90)
        else:
            pass
        cmds.makeIdentity(fst, apply=1, t=0, r=1, s=0, n=0, pn=1)
        cmds.matchTransform( fst, scnd )
    else:
        for i in range( rng ):
            cmds.matchTransform( fst[i], scnd[i] )
