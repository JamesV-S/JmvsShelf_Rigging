@echo off
setlocal

:: Define repo path
set REPO_PATH=C:\Docs\maya\scripts\JmvsShelf_Rigging

:: Check if directory exists & for changes to the repo.
if exist "%REPO_PATH%" (
    echo Directory exists.
    cd /d "%REPO_PATH%" || (
        echo Unable to change directory to %REPO_PATH%. Exiting...
        exit /b
    )

    :: Check for changes
    :: git diff-index --quiet HEAD --

    :: Check for changes, including untracked files
    git status --porcelain | findstr /r "^\(M\| M\|A\|??\)" >nul

    :: Commit changes and publish to GitHub
    if errorlevel 1 (
        echo Changes detected in repository at "%REPO_PATH%". Committing...
        git add .
        git commit -m "Cloning 'JmvsShelf_Rigging' Automated commit"
        git push origin main
        echo Commit and push successful for repository at "%REPO_PATH%".
    ) else (
        echo No changes to commit for repository at "%REPO_PATH%".
    )

    REM Remove the existing repo if it exists, to clone it from new. 
    echo Directory exists, removing it...
    cd ..
    rmdir /S /Q "%REPO_PATH%"
) else (
    echo Directory does not exist.
)

:: ------------------------------------------------------------------------------------------
::COPY REPO
git config --global user.name "JamesV-S"
git config --global user.email "hamzvilelas@gmail.com"

git clone https://github.com/JamesV-S/JmvsShelf_Rigging "%REPO_PATH%"

:: ------------------------------------------------------------------------------------------
:: COPY SHELF
robocopy "C:\Docs\maya\scripts\JmvsShelf_Rigging\shelf" "C:\Docs\maya\2025\prefs\shelves"

:: ------------------------------------------------------------------------------------------
:: COPY Mayaenv & Workspace
robocopy "C:\Docs\maya\scripts\JmvsShelf_Rigging\mayaenv" "C:\Docs\maya\2025"
robocopy "C:\Docs\maya\scripts\JmvsShelf_Rigging\workspace" "C:\Docs\maya\2025\prefs\workspaces"

:: Start Maya 
start /d "C:\Program Files\Autodesk\Maya2025\bin" maya.exe

echo [script complete, close window.]

pause

