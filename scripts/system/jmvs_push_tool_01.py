
# Jmvs_push_system
import maya.cmds as cmds
import importlib

class jmvs_push_tool():
    def __init__(self):
        
        # MUST select 1)Push_jnt, 2)rig_jnnt, 3)bind_jnt
        self.sel = cmds.ls(sl=1, type="joint")
        print(self.sel)
        cmds.select(cl=1)
        self.pusher_jnt = self.sel[0] # jnt_driver
        self.pushed_Inp_jnt = self.sel[1] # driven rig_jnt
        self.output_jnt = self.sel[2] # driven skn_jnt
        
        self.ctrl = f"ctrl_{self.pusher_jnt.split('_')[2:][0]}"
        print(self.ctrl)

        print(self.output_jnt)

        def get_other_axis(lst, axis):
            other_axis = [element for element in lst if element != axis]
            return other_axis
        my_list = ["X", "Y", "Z"]
        self.push_axis = "Y"
        self.other_axis = get_other_axis(my_list, self.push_axis)
        print(self.other_axis)  # Output will be ['X', 'Z']

        self.matrix_from_jnts()
        self.push_cond()
        self.calculate_push_diff()
        self.connect_to_skn_jnt()

    def matrix_from_jnts(self):
        
        # Compose a matrix from the driver joint
        pusher_Mmtx = cmds.shadingNode(
            "multMatrix", au=1, 
            n=f"{self.pusher_jnt.split('_')[2:][0]}_pusher_MltMtx")
        self.pusher_Dmtx = cmds.createNode(
            "decomposeMatrix", 
            n=f"{self.pusher_jnt.split('_')[2:][0]}_self.pusher_Dmtx")
        
        cmds.connectAttr((f"{self.pusher_jnt}.worldMatrix[0]"), 
                         (f"{pusher_Mmtx}.matrixIn[0]"), f=1)
        cmds.connectAttr((f"{pusher_Mmtx}.matrixSum"), 
                         (f"{self.pusher_Dmtx}.inputMatrix"), f=1)

        
        # Compose a matrix from the pushed_Inp joint
        pushed_InpMmtx = cmds.shadingNode(
            "multMatrix", au=1, 
            n=f"{self.pushed_Inp_jnt.split('_')[2:][0]}_pushed_MltMtx")
        self.pushed_InpDmtx = cmds.createNode(
            "decomposeMatrix", 
            n=f"{self.pushed_Inp_jnt.split('_')[2:][0]}_pushed_Dmtx")
        print(f"{self.pushed_Inp_jnt.split('_')[2:][0]}_pushed_Dmtx")

        cmds.connectAttr((f"{self.pushed_Inp_jnt}.worldMatrix[0]"), 
                         (f"{pushed_InpMmtx}.matrixIn[0]"), f=1)
        cmds.connectAttr((f"{pushed_InpMmtx}.matrixSum"), 
                         (f"{self.pushed_InpDmtx}.inputMatrix"), f=1)
    
    def push_cond(self):
        
        # -----------------------------------
        # Condition node
        self.pushCond = cmds.shadingNode( 
            "condition", au=1, 
            n=f"{self.pusher_jnt.split('_')[2:][0]}_push_Cond")
        # Wire up for if statement with nodes to create the method that push 
        # the output joint!
        
        # cushion controls
        def enum_attrib(ctrl, ln, en, flt):
                
            dividerNN = "------------" 
            atrrType = "enum"
            MaxVal = 25
            MinVal = -25
            # Divivder 
            cmds.addAttr(ctrl, longName=ln, niceName=dividerNN, 
                         attributeType=atrrType, enumName=en, k=True)
            cmds.setAttr( ctrl + '.' + ln, lock=True, keyable=False, 
                         channelBox=True)
            # Float
            cmds.addAttr(ctrl, longName=flt, at='double', min=MinVal, 
                         max=MaxVal, dv=MinVal )
            cmds.setAttr(ctrl + '.' + flt, e=1, k=1 )
        enum_attrib(self.ctrl, "push_dvdr", 
                    "PUSH", "Cushion")
        cmds.setAttr(f"{self.ctrl}.Cushion" , 0)

        self.drvrCush_pma = cmds.shadingNode(
            "plusMinusAverage", au=1,
            n=f"{self.pusher_jnt.split('_')[2:][0]}_pshrCushion_pma")
        
        # Driver to cushion, then to cond
        cmds.connectAttr((f"{self.pusher_Dmtx}.outputTranslate{self.push_axis}"), 
                         (f"{self.drvrCush_pma}.input1D[0]"), f=1)
        cmds.connectAttr((f"{self.ctrl}.Cushion"),
                         (f"{self.drvrCush_pma}.input1D[1]"), f=1)
        
        cmds.connectAttr((f"{self.drvrCush_pma}.output1D"),
                         (f"{self.pushCond}.firstTerm"), f=1)
        
        # pushed to cond 
        cmds.connectAttr((f"{self.pushed_InpDmtx}.outputTranslate{self.push_axis}"), 
                         (f"{self.pushCond}.secondTerm"), f=1)
        cmds.connectAttr((f"{self.pushed_InpDmtx}.outputTranslate{self.push_axis}"), 
                         (f"{self.pushCond}.colorIfFalseR"), f=1)
        cmds.setAttr( f"{self.pushCond}.operation", 2 )
        
    def calculate_push_diff(self):
        
        # -----------------------------------
        # Calculate the difference
        self.sub_pma = cmds.shadingNode(
            "plusMinusAverage", au=1, 
            n=f"{self.pusher_jnt.split('_')[2:][0]}_sub_pma")
        
        self.add_pma = cmds.shadingNode(
            "plusMinusAverage", au=1, 
            n=f"{self.pusher_jnt.split('_')[2:][0]}_add_pma")
        
        # subtract pusher_drv val from pushed rest_val
        # connect input_jnts
        cmds.connectAttr((f"{self.pusher_Dmtx}.outputTranslate{self.push_axis}"), 
                         (f"{self.sub_pma}.input1D[0]"), f=1) 
        cmds.connectAttr((f"{self.pushed_InpDmtx}.outputTranslate{self.push_axis}"), 
                         (f"{self.sub_pma}.input1D[1]"), f=1)
        
        # add up the result to get the pushed value for rig_input_jnt
        cmds.connectAttr((f"{self.sub_pma}.output1D"), 
                         (f"{self.add_pma}.input1D[0]"), f=1) 
        cmds.connectAttr((f"{self.pushed_InpDmtx}.outputTranslate{self.push_axis}"), 
                         (f"{self.add_pma}.input1D[1]"), f=1)
        
        # Connect to cushion, then to condition node

        self.inputCush_pma = cmds.shadingNode(
            "plusMinusAverage", au=1,
            n=f"{self.pusher_jnt.split('_')[2:][0]}_pshdCushion_pma")

        cmds.connectAttr((f"{self.add_pma}.output1D"), 
                         (f"{self.inputCush_pma}.input1D[0]"), f=1)
        cmds.connectAttr((f"{self.ctrl}.Cushion"), 
                         (f"{self.inputCush_pma}.input1D[1]"), f=1)
        
        cmds.connectAttr((f"{self.inputCush_pma}.output1D"),
                         (f"{self.pushCond}.colorIfTrueR"), f=1)
               
        cmds.setAttr( f"{self.sub_pma}.operation", 1 )
        cmds.setAttr( f"{self.sub_pma}.operation", 2 )

    def connect_to_skn_jnt(self):
        
        cmds.connectAttr( (f"{self.pushCond}.outColorR"), 
                         (f"{self.output_jnt}.translate{self.push_axis}"), f=1 )
        
        for i in range(2):
            cmds.connectAttr(
                (f"{self.pushed_InpDmtx}.outputTranslate{self.other_axis[i]}"), 
                (f"{self.output_jnt}.translate{self.other_axis[i]}"), f=1 )
        

jmvs_push_tool()

