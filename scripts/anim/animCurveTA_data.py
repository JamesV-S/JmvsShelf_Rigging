import maya.cmds as cmds

def gather_keyframes(anim_curve_name):
    """
    Gathers keyframe data from the specified AnimCurveTA node.
    
    :param anim_curve_name: Name of the AnimCurveTA node.
    :return: List of tuples containing (frame, value) for each keyframe.
    """
    if not cmds.objExists(anim_curve_name):
        raise ValueError(f"AnimCurveTA node '{anim_curve_name}' does not exist.")
    
    keyframes = cmds.keyframe(anim_curve_name, query=True, timeChange=True)
    values = cmds.keyframe(anim_curve_name, query=True, valueChange=True)
    
    return list(zip(keyframes, values))

def create_anim_curve(name, keyframe_data):
    """
    Creates a new AnimCurveTA node and sets keyframes based on the provided data.
    
    :param name: Name for the new AnimCurveTA node.
    :param keyframe_data: List of tuples containing (frame, value) for keyframes.
    :return: Name of the newly created AnimCurveTA node.
    """
    new_anim_curve = cmds.createNode('animCurveTA', name=name)
    
    for frame, value in keyframe_data:
        cmds.setKeyframe(new_anim_curve, time=frame, value=value)
    
    # Set pre-infinity and post-infinity to cycle
    cmds.setAttr(f"{new_anim_curve}.preInfinity", 3)  # 3 corresponds to cycle
    cmds.setAttr(f"{new_anim_curve}.postInfinity", 3)  # 3 corresponds to cycle
    
    # Disable weighted tangents
    cmds.keyTangent(new_anim_curve, edit=True, weightedTangents=False)
    
    return new_anim_curve

# Example usage:
keyframes = gather_keyframes('UACR1:UACR_body_ctrl_sideTiltAmountCurve')
print(f"keyframes = {keyframes}")

keyframes = [(0.0, 0.0), (0.8, 0.06875), (1.6, 0.1), (2.4, 0.06875), (4.0, -0.06875), (4.8, -0.1), (5.6, -0.06875), (6.4, 0.0)]
new_curve = create_anim_curve('AC_sideAmountCurve', keyframes)
