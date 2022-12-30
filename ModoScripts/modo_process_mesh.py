# python
import argparse
import lx
import lxu.command
import lxu.select
import modo
import os
from os import path

# Constants
FBX_EXTENSION = ".fbx"


def storeFBXSettings(self):
    FBX_USERVALUE_PREFIX = 'sceneio.fbx.save.'
    FBX_USERVALUE_COMMAND = 'user.value ' + FBX_USERVALUE_PREFIX
    fbxSettings = {}
    uValCount = self.scrp_svc.UserValueCount()
    for x in range(uValCount):
        try:
            uval = self.scrp_svc.UserValueByIndex(x)
        except IndexError:
            print("Invalid User Value Index: %s (%s total user values)" % (x, uValCount))
        else:
            name = uval.Name()
            if name.startswith('sceneio.fbx.save.'):
                fbxSettings[name] = self.getUserValue(name)
    return fbxSettings


def restoreFBXSettings(self, fbxSettings):
    for name, value in fbxSettings.items():
        lx.eval('user.value %s %s' % (name, value))


def get_args():
    """
    A method to obtain the arguments that came with the triggered Python file - from the .bat file.
    :rtype: object
    :return: An object containing the arguments as properties.
    """
    parser_double_dash = "--"
    parser_path_short_argument = "-p"
    parser_path_long_argument = "--path"
    parser_path_help = "asset path"

    parser = argparse.ArgumentParser()

    _, all_arguments = parser.parse_known_args()
    double_dash_index = all_arguments.index(parser_double_dash)
    script_args = all_arguments[double_dash_index + 1:]

    parser.add_argument(parser_path_short_argument, parser_path_long_argument, help=parser_path_help)
    parsed_script_args, _ = parser.parse_known_args(script_args)
    return parsed_script_args


def setup_and_run_mesh_process():
    """
    Initialize the arguments and run the mesh process.
    """
    args = get_args()
    source_asset_path = args.path
    process_mesh(source_asset_path)


def process_mesh(asset_path):
    """
    Process the mesh at the given asset_path.
    In this sample, processing = Create the UV map with an automatic unwrap based on Sharp Edge Angle
    and export that mesh to the same path, with an added suffix to the name.
    :param string asset_path: The absolute asset path.
    """
    InputFileFormat = "FBX"
    processed_mesh_suffix = "_processed"

    asset_name = os.path.splitext(os.path.basename(asset_path))[0]
    source_asset_directory = os.path.dirname(asset_path)

    # Determine new naming and paths for the processed mesh
    export_asset_name = asset_name + processed_mesh_suffix
    export_asset_path = os.path.join(source_asset_directory, export_asset_name + FBX_EXTENSION)

    print("The source asset path is: " + asset_path)
    print("The source asset name is: " + asset_name)
    print("The source directory path is: " + source_asset_directory)

    fbxSettings = storeFBXSettings()

    # # Import the asset in the Blender scene
    # processing_failed = False
    # try:
    #     ###########################################################################################
    #     # Open the Dialog window to get the Target Path
    #     ###########################################################################################
    #     lx.eval('dialog.setup dir')
    #     lx.eval('dialog.title "Select the target Folder to Analyse and Process"')
    #     # MODO version checks.
    #     modo_ver = int(lx.eval('query platformservice appversion ?'))
    #     if modo_ver == 801:
    #         lx.eval('+dialog.open')
    #     else:
    #         lx.eval('dialog.open')
    #     asset_path = lx.eval('dialog.result ?')
    #     lx.out('Path', asset_path)
    #     ###########################################################################################
    #
    # except Exception as e:
    #     processing_failed = True
    #     print("Could not import asset at : " + asset_path)
    #     print(e)

    # ###########################################################################################
    # # Open FBX Files
    # # lx.eval('loaderOptions.fbx false true true true false false true true false false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport')
    # ###########################################################################################
    #
    # FBXPathList = []
    # CurratedFBXPathList = []
    # for fbx in os.listdir(asset_path):
    #     # if '.fbx' in fbx.lower():                     this one will accept .Fbx .FBx .fbX, etc, because it's case insensitive
    #     if ".fbx" in fbx or ".FBX" in fbx:  # this one will only accept .fbx or .FBX exactly
    #         finalPath = asset_path + "/" + fbx
    #         # print(finalPath)
    #         finalPath_AbsPath = os.path.abspath(finalPath)
    #         # print(finalPath_AbsPath)
    #         FBXPathList.append(finalPath_AbsPath)
    #
    # for item in FBXPathList:
    #     FileSize = os.path.getsize(item)
    #     # print(FileSize)
    #     if FileSize > 128:
    #         # print(item)
    #         # print('File Not Empty')
    #         CurratedFBXPathList.append(item)
    #     if FileSize <= 128:
    #         print('File Considered Empty')
    #
    # if len(CurratedFBXPathList) > 0:
    #     for item in CurratedFBXPathList:
    #         # lx.eval('!!loaderOptions.fbx false true true true false false true true false false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport')
    #         lx.eval('!!loaderOptions.fbx mergeWithExistingItems:false loadGeometry:true loadNormals:true loadMeshSmoothing:true loadBlendShapes:false loadPolygonParts:false loadSelectionSets:true loadMaterials:true invertMatTranAmt:false useMatTranColAsTranAmt:false changeTextureEffect:false loadCameras:false loadLights:false loadAnimation:false loadSampleAnimation:false loadSampleAnimationRate:0 globalScalingFactor:1.0 importUnits:0')
    #
    #         # MergeExistItems =
    #         # LoadGeo =
    #         # LoadNormals =
    #         # LoadMeshSmoothness =
    #         # LoadMorphs =
    #         # LoadParts =
    #         # LoadSelSets =
    #         # LoadMats =
    #         # InvertMatTransp =
    #         # lx.eval('!!loaderOptions.fbx %s %s %s %s %s %s %s %s %s false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport' % MergeExistItems, % LoadGeo, % LoadNormals, % LoadMeshSmoothness, % LoadMorphs, % LoadParts, % LoadSelSets, % LoadMats, % InvertMatTransp)
    #         lx.eval('!!scene.open {%s} normal' % item)
    #         # lx.eval('!!scene.open filename:{%s} mode:normal' % item)
    #         # lx.eval("!!scene.open {%s} import" % finalPath)
    #
    #         scene = modo.Scene()
    #         FullScenePath = scene.filename
    #         # lx.out('Scene Full Path:', FullScenePath)
    #         SceneName = path.splitext(path.basename(scene.filename))[0]
    #         lx.out('Currently Opened Scene:', SceneName)

    lx.eval(
        '!!loaderOptions.fbx mergeWithExistingItems:false loadGeometry:true loadNormals:true loadMeshSmoothing:true loadBlendShapes:false loadPolygonParts:false loadSelectionSets:true loadMaterials:true invertMatTranAmt:false useMatTranColAsTranAmt:false changeTextureEffect:false loadCameras:false loadLights:false loadAnimation:false loadSampleAnimation:false loadSampleAnimationRate:0 globalScalingFactor:1.0 importUnits:0')
    lx.eval('!!scene.open filename:{%s} mode:normal' % asset_path)

    # Process the asset by selecting the meshes and run the Auto Unwrap command
    lx.eval('select.itemType mesh')
    lx.eval('smo.UV.Multi.AutoUnwrapSmartByAngle true true 80.0 180.0')

    # Save the FBX file
    lx.eval('scene.saveAs {%s} fbx false' % export_asset_path)

    # Process the asset
    # In this sample, I'm bevelling the asset and exporting the new mesh right next to the old one.
    # You can add your custom processing here and replace the sample.
    # try:
    #     imported_assets = bpy.context.selected_objects
    #     for asset in imported_assets:
    #         if asset.type != BLENDER_TYPE_MESH:
    #             continue
    #
    #         # Apply a bevel modifier on the mesh
    #         bevel_modifier_name = "Bevel Modifier"
    #         asset.modifiers.new(name=bevel_modifier_name, type=BLENDER_MODIFIER_BEVEL)
    # except Exception as e:
    #     processing_failed = True
    #     print("Could not process asset.")
    #     print(e)
    #
    # # Export the asset from Blender back to Unity, next to the original asset
    # if processing_failed:
    #     return
    # try:
    #     bpy.ops.export_scene.fbx(
    #         filepath=export_asset_path,
    #         use_selection=True)
    # except Exception as e:
    #     print("Could not export to path: " + export_asset_path)
    #     print(e)

    restoreFBXSettings(fbxSettings)


# Triggering the mesh process
setup_and_run_mesh_process()
