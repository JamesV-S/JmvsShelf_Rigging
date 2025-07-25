
import maya.cmds as cmds


def toggle_wireframe_on_shaded(panel_list):
    '''
    Toggles wireframe-in-shade viewing mode for the specified panel. 
    If no panel is specified, defaults to the currently active panel.
    '''
    for pan in panel_list:
        current_state  = cmds.modelEditor(pan, q=True, wireframeOnShaded=True)
        cmds.modelEditor(pan, edit=True, wireframeOnShaded=not current_state)
    if current_state:
        print(f"FALSE")
        return 0
    else:
        print(f"TRUE")
        return 1


def toggle_wireframe(panel_list):
   for pan in panel_list:
        current_state  = cmds.modelEditor(pan, q=True, displayAppearance=True)
        print(f"current_state = {current_state}")
        if not current_state == "wireframe":
            cmds.modelEditor(pan, edit=True, displayAppearance="wireframe")
        else:
            cmds.modelEditor(pan, edit=True, displayAppearance="smoothShaded")
            cmds.modelEditor(pan, edit=True, wireframeOnShaded=False)


def cycle_viewport():
    # when running this function, the viewport cycles between
        # wireframe | smooth shade all | wireframe on shaded
            # cycling through these & to effect all possible viewports. 
    
    # Get the panel list
    panel_all = cmds.getPanel(all=1)
    panel_list = [model for model in panel_all if "modelPanel" in model]
    
    wire_on_shaded = toggle_wireframe_on_shaded(panel_list)
    print(f"wire_on_shaded = {wire_on_shaded}")
    if wire_on_shaded:
        toggle_wireframe(panel_list)
        toggle_wireframe_on_shaded(panel_list)   
