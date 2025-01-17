
:: Automating the download of usersetup.py to maya directory from my github repo
@echo off

:: Define repo path's
set REPO_URL=https://github.com/JamesV-S/JmvsShelf_Rigging/tree/main/usersetup_file
set DESTINATION_PATH=C:\Docs\maya\scripts\usersetup.py

:: Download the `usersetup.py` file!
powershell -command "(New-Object Net.WebClient).DownloadFile('%REPO_URL%', '%DESTINATION_PATH%')"

echo `usersetup.py` has been downloaded and copied to the Maya scripts directory

pause

