import pymel.core as pm
import json
import sys
import os

def ReplaceAssPath(standin):
    # Define the directory where the asset files are located
    asset_dir = "J:/xkx/work/lib/asset/PR/"
    assPath = standin.dso.get()
    if asset_dir in assPath: 
        return assPath
    
    assName = standin.dso.get().split("/")[-1].split("_")[-1].split(".")[0]
    assNightDir = asset_dir + assName + "Night/shd/ass/"
    assDir = asset_dir + assName + "/shd/ass/"

    if os.path.isdir(assNightDir): 
        version = max([f for f in os.listdir(assNightDir) if f.startswith("v")])
        assPath = "%s%sNight/shd/ass/%s/PR%sNight_shd_%s.ass" % (asset_dir, assName, version, assName, version)
    elif os.path.isdir(assDir):
        version = max([f for f in os.listdir(assDir) if f.startswith("v")])
        assPath = "%s%s/shd/ass/%s/PR%s_shd_%s.ass" % (asset_dir, assName, version, assName, version)
    else:
        if assDir in missing: 
            return assPath
        missing.append(assDir)
        return assPath
    
    # Remove the "Night" from the assPath
    assPath = assPath.replace("Night/", "")
    standin.dso.set(assPath)
    
    return assPath

standins = pm.ls(type='aiStandIn')
standinTransforms = [pm.listRelatives(standin, parent=True, f=True)[0] for standin in standins]

assXYZ = {}
missing = []
for standin, transform in zip(standins, standinTransforms):
    xformDict = {}
    xformDict['tx'] = transform.tx.get()
    xformDict['ty'] = transform.ty.get()
    xformDict['tz'] = transform.tz.get()
    xformDict['rx'] = transform.rx.get()
    xformDict['ry'] = transform.ry.get()
    xformDict['rz'] = transform.rz.get()
    xformDict['sx'] = transform.sx.get()
    xformDict['sy'] = transform.sy.get()
    xformDict['sz'] = transform.sz.get()

    # Get the asset name from the standin file path
    # assPath = standin.dso.get()
    assPath = ReplaceAssPath(standin)
    nodeName = transform.name()
    print(nodeName)
    if assPath not in assXYZ:
        assXYZ[assPath] = {}
    assXYZ[assPath][nodeName] = xformDict

json_str = json.dumps(assXYZ, indent=4)
with open('D:/assXYZ.json', 'w') as f:
    json.dump(assXYZ, f, indent=4)
