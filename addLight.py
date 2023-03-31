import pymel.core as pm
import sys
import os

standins = pm.ls(type='aiStandIn')
transforms = [pm.listRelatives(standin, parent=True, f=True)[0] for standin in standins]

ass_xyz = {}
missing = []
light_root = "J:/xkx/work/lib/lig_set/PR/"
for standin, transform in zip(standins, transforms):
    xform_dict = {}
    xform_dict['tx'] = transform.tx.get()
    xform_dict['ty'] = transform.ty.get()
    xform_dict['tz'] = transform.tz.get()
    xform_dict['rx'] = transform.rx.get()
    xform_dict['ry'] = transform.ry.get()
    xform_dict['rz'] = transform.rz.get()
    xform_dict['sx'] = transform.sx.get()
    xform_dict['sy'] = transform.sy.get()
    xform_dict['sz'] = transform.sz.get()

    filename = os.path.basename(standin.dso.get())
    if 'MA' in filename:
        index = filename.find('MA') + 2
        digits = filename[index:index+3]
        if not digits.isdigit(): continue
    else: continue
    ass_name = "MA" + digits + "Night"

    node_name = transform.name().split("_")[-1].split("|")[-1]
    new_name = str(ass_name + "_" + node_name).replace(":", "")

    light_folder = os.path.join(light_root, ass_name)
    if not os.path.isdir(light_folder): continue
    
    ma_file = os.path.join(light_folder, ass_name + "_light.ma")
    ref_node = pm.createReference(ma_file, namespace=new_name)
    light_grp = pm.ls(new_name + ":*", assemblies=True)[0]
    light_grp.setTranslation([xform_dict['tx'], xform_dict['ty'], xform_dict['tz']])
    light_grp.setRotation([xform_dict['rx'], xform_dict['ry'], xform_dict['rz']])
    light_grp.setScale([xform_dict['sx'], xform_dict['sy'], xform_dict['sz']])
