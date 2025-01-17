
# Jmvs user setup file
import maya.cmds as cmds

# basic setup:
def basic_setup_message():
    cmds.confirmDialog(title = 'startup', message='Maya is stating up', button=['OK'])

basic_setup_message()