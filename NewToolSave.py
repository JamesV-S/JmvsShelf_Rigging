import subprocess

import maya.cmds as cmds
import maya.mel as mel
import os
import shutil

saveFile = ""
tempFile = False

def runMEL():
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
    value = mel.eval('confirmDialog -title "Confirm" -message "Save Preferences BEFORE clicking ok" -button "OK" -button "Cancel" -defaultButton "OK" -cancelButton "Cancel" -dismissString "Cancel";')
    

    # If Ok button is clicked in check box #
    if value == "OK":
        destShelfFile = "E:/YR2/Maya/MayaSetup/shelf/shelf_WD_Tools.mel"
        shelfFile = "C:/Docs/maya/2024/prefs/shelves/shelf_WD_Tools.mel"
        shutil.copyfile(shelfFile, destShelfFile)
        
        destPrefFile = "E:/YR2/Maya/MayaSetup/pref/userPrefs.mel"
        prefFile = "C:/Docs/maya/2024/prefs/userPrefs.mel"
        shutil.copyfile(prefFile, destPrefFile)
        
        # Optional temp save #
        if tempFile == True:
            cmds.file(rename=newFileName)
            
        cmds.file(save=True, typ=newFileType)
        tempFileLoc = cmds.file(q=True, sn=True)
        print("File Saved To:", tempFileLoc)
        
        # runs batch process to copy shelves to maya #
        subprocess.run([r"E:\YR2\Maya\MayaSetup\copyShelfDontTouch.bat"])
    
        # runs and shuts current maya session #
        os.spawnl(os.P_NOWAIT, loc, '-file', tempFileLoc)
        cmds.quit()
    else:
        pass
        
runMEL()
