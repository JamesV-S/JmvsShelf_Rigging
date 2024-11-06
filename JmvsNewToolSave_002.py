
import subprocess

import maya.cmds as cmds
import maya.mel as mel
import os
import shutil
import sys
import importlib

import find_driver_letter as driver
importlib.reload(driver)



def runMEL():

    A_driver = driver.get_folder_letter("Jmvs_current_file_path")
    print("0", A_driver[0])
    #custom_path = f'{A_driver}My_RIGGING/MayaSetup/toolSetup.txt' # 
    #another_path = f'{A_driver}My_RIGGING/JmvsSCRIPTS/JMVS_Working_Scripts/JMVS_Rigging_Tools/prefix_tools/Prefix_Ui_tools/ui_scripts' 
    #print(f"module imported from {custom_path}")
    #sys.path.append(custom_path)

    saveFile = ""
    tempFile = 1
    
    setup = open(f'{A_driver}My_RIGGING/MayaSetup/toolSetup.txt', "r") # 
    path = setup.readline()
    tempFileT = setup.readline()
    
    print("path: ",path)
    print("Need a temp file: ",tempFileT)
    
    
    #runMEL()
    # Gathers mayas run exe into a path string #
    loc = mel.eval("getenv maya_location")
    loc = loc + "/bin/maya.exe"
    print("loc",loc)
    
    # Gathers scene name #
    sceneName = mel.eval("file -q -sn -shn;")
    print("sceneName", sceneName)

    # Gets the file type .mb or .ma #
    fileName = sceneName[:-3]
    fileType = sceneName[-3:]
    print("fileType", fileType)
    
    # Adds a temperory name to file name if file needs saving #
    fileName = fileName + "_TEMPORARY"
    print("fileName",fileName)
    newFileName = fileName + fileType
    print("newFileName",newFileName)
    
    # File destination #
    destination = cmds.file(q=True, sn=True)
    print("dest",destination)
    
    if fileType == ".mb":
        newFileType = "mayaBinary"
    else:
        newFileType = "mayaAscii"
           
    print("newFileType", newFileType)
    # Check box to ask user to save preferenecs #
    value = mel.eval(
        'confirmDialog -title "Confirm" -message "Save Preferences BEFORE clicking ok" -button "OK" -button "Cancel" -defaultButton "OK" -cancelButton "Cancel" -dismissString "Cancel";'
        )
    

    # If Ok button is clicked in check box #
    if value == "OK":
        destShelfFile = path + "/shelf/shelf_Jmvs_Tools.mel"
        print("2", destShelfFile)
        shelfFile = "C:/Docs/maya/2024/prefs/shelves/shelf_Jmvs_Tools.mel"
        #shutil.copyfile(shelfFile, destShelfFile)
        
        destPrefFile = path + "/pref/userPrefs.mel"
        print("1", destPrefFile)
        prefFile = "C:/Docs/maya/2024/prefs/userPrefs.mel"
        #shutil.copyfile(prefFile, destPrefFile)
        
        if A_driver[0] == "E":
            print(f"{path}/MayaSetup/EcopyShelfDontTouch.bat")

        
        # Optional temp save #
        if tempFile == True:
            cmds.file(rename=newFileName)
            
        cmds.file(save=True, typ=newFileType)
        tempFileLoc = cmds.file(q=True, sn=True)
        print("File Saved To:", tempFileLoc)
         
        # runs batch process to copy shelves to maya #
        if A_driver[0] == "E":
            #print(r"{path}\MayaSetup\EcopyShelfDontTouch.bat")
            subprocess.run([r"{path}\MayaSetup\EcopyShelfDontTouch.bat"])
        else: # D
            subprocess.run([r"{path}\MayaSetup\DcopyShelfDontTouch.bat"])

        # runs and shuts current maya session #
        os.spawnl(os.P_NOWAIT, loc, '-file', tempFileLoc)
        cmds.quit()
    else:
        pass
        
runMEL()