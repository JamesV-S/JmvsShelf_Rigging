
# Jmvs user setup file
import os
import maya.cmds as cmds
import logging # debugging
import subprocess # to run any batch scripts
import urllib.request # download online files

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


def run_jmvsShelf_Rigging_batch():
    # Correct raw URL for the batch file
    url = "https://raw.githubusercontent.com/JamesV-S/JmvsShelf_Rigging/main/batch_run_script/Jmvs_shelf_rigging.bat"
    
    # Path for temp folder to download `.bat` to
    temp_script_path = os.path.join(os.getenv('TEMP'), 'Jmvs_shelf_rigging.bat')
    
    try:
        # Download batch file
        urllib.request.urlretrieve(url, temp_script_path)

        # Run the batch script
        subprocess.call([temp_script_path], shell=True)
        
        print("downloading and running the batch script")
    except Exception as e:
        print(f"Error with downloading or running the batch script: {e}")

# run_jmvsShelf_Rigging_batch()


def deferred_setup_tasks():
    # Any tasks for AFTER the ui of maya has loaded.
    print("Deferred setup done.")
    # turn on x-ray joints!
    cmds.modelEditor("modelPanel1", jointXray=True)
deferred_setup_tasks()


