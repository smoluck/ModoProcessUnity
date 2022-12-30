@title Run Mesh Process
@echo off

:: This batch file is an example for running a headless version of Modo (Cmd Line) and
:: executing a Python script set of commands in Modo.

:: Establishing the path variables
set modo-directory-path="C:\Program Files\Foundry\Modo\16.0v3"
set mesh-process-script-path="C:\ONEDRIVE\GITHUB\ModoProcessUnity\ModoScripts\modo_process_mesh.py"

:: Switching the current directory to where Modo is installed
cd %modo-directory-path%

:: Echo-ing the data
echo Processing asset at path: "%1"
echo Running ModoCL installed at path: %modo-directory-path%
echo Executing script at path: %mesh-process-script-path%
echo.

:: Triggering the Modo command and passing the current .bat argument as an argument for the .py script
:: modocl.exe -console:python -P %mesh-process-script-path% -- --path %1
modocl.exe -P %mesh-process-script-path% -- --path %1
:: modocl.exe %mesh-process-script-path%

:: Check if the Modo directory exists
if not exist %modo-directory-path% (
    echo Folder %modo-directory-path% does not exist.
    pause
)

:: Check if the Modo script exists
if not exist %mesh-process-script-path% (
    echo File %mesh-process-script-path% does not exist.
    pause
)

:: Check if provided asset path exists
if not exist %1 (
    echo Provided parameter asset path: %1% does not exist.
    pause
)

:: Pause execution on any errors
if not ERRORLEVEL 0 pause