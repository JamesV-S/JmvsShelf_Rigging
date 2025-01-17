
# Jmvs user setup file
import maya.cmds as cmds
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_message():
    # for debugging purposes, use logging to track what this script is doing
    logger.info("Maya startup script executed")
log_message() 


# basic setup:
def basic_setup_message():
    cmds.confirmDialog(title = 'startup', 
                       message='Maya is stating up', 
                       button=['OK'])

basic_setup_message()

