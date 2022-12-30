# Modo Process Unity (NOT WORKING - UNDER DEVELOPMENT) [![License](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat)](http://mit-license.org)
![](/UnityProject/Assets/Screenshots/ModoProcessTitle.png)

Repository that show how to trigger a headless Modo (via Modo Command Line) operation from inside Unity.
This repository is based on [BlenderProcessUnity](https://github.com/razluta/BlenderProcessUnity) project from [Razvan Luta](https://github.com/razluta).

## Using the tool
The tool will only run on Windows currently, as it uses a .bat file to trigger Modo.
Since there is no UI to define local path variables, the user will need to modify the scripts to point Unity, Windows and Modo to the right paths. Follow the setup instructions below.

### Step 01 of 02 - Setup
a) In the Unity Project, in the _Scripts/Editor_ folder, you'll need to modify the **MeshModoProcess.cs** script to:
- (mandatory) point the two constants to your Modo .bat file (or the example provided)   
- (optional) change where the script can be launched from in the menus

The .bat process path is defined on this line:

`private const string ModoScriptPath = "D:\\example-repos\\ModoProcessUnity\\ModoScripts\\RunMeshProcess.bat";`

The context menu for the tools is defined on this line:

`private const string MenuItemModoToolsRunMeshProcess = "Assets/Modo Tools/Run Mesh Process";`

b) In the .bat file, currently called **RunMeshProcess.bat**, you'll need to edit:
- (mandatory) the local path for where Modo is installed
- (mandatory) the local path for where the Modo script you want to run is located

The Modo path is defined on this line:

`set modo-directory-path="D:\SteamGames\steamapps\common\Modo"`

The local path for the Modo script to run is on this line:

`set mesh-process-script-path="D:\example-repos\ModoProcessUnity\ModoScripts\process_mesh.py"`

c) Lastly, in the Python script currently called **process_mesh.py**, you can easily change the following:
- (optional) the suffix of the newly exported asset
- (optional) the operation to put the mesh through
- (optional) the entire behavior of the script ... 

The suffix is defined on this line:

`processed_mesh_suffix = "_processed"`

The operations ran on the mesh are defined on these lines:

```
# Create the UV map with an automatic unwrap based on Sharp Edge Angle and export that mesh to the same path, with an added suffix to the name
lx.eval('smo.UV.Multi.AutoUnwrapSmartByAngle true true 80.0 180.0')
```


### Step 02 of 02 - Running the tool
To run the tool in Unity, the user needs to just **right-click** on a mesh in the Project view and select _Modo Tools > Run  Mesh Process_.

The image sequence below showcase how the tool currently works.
![](/UnityProject/Assets/Screenshots/BlenderProcessUnityDemo.gif)

## How it works
- When the user triggers the tool from Unity (it can only be triggered on GameObjects), the code will launch a Process that runs a .bat file with a parameter (in this case, the parameter is the absolute file path for the .fbx mesh).
- The .bat file that gets executed opens a headless version of Modo and passes the path to the .fbx as an argument as well as instructing Modo on what Python script to execute for the mesh processing.
- The Python file that gets executed in Modo uses the headless version of Modo, opens a new scene and receives the argument as a path to the mesh to import. After importing the mesh, in this sample, the script applies a Modo custom Wrapped command (in this case a AutoUnwrap based on Sharp Edge Angle) and exports the mesh right next to the original mesh back in Unity.

## Extending the tool
The scripts can be easily modified to include several arguments from Unity or perform more complex edit operations inside Modo.

### Resources
- [Unity MenuItem](https://docs.unity3d.com/ScriptReference/MenuItem.html)
- [C# Process](https://docs.microsoft.com/en-us/dotnet/api/system.diagnostics.process.start?view=net-5.0)
- [Windows Batch Scripting](https://en.wikibooks.org/wiki/Windows_Batch_Scripting)
- [BlenderProcessUnity](https://github.com/razluta/BlenderProcessUnity)
- [Modo SDK Headless](https://learn.foundry.com/modo/developers/latest/sdk/pages/general/systems/Headless.html#)
- [Modo Python Reference](https://learn.foundry.com/modo/developers/latest/sdk/python/python.html)
