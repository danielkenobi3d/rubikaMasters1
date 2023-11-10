from RMPY import nameConvention
import pymel.core as pm
name_conv = nameConvention.NameConvention()
name_conv.defaults_name['system'] = 'reference'
selection = pm.ls(selection=True)


def rename_selection():
	selection = pm.ls(selection=True)
	fix_shapes(*selection)
	for index, each in enumerate(selection):
		side = 'R'
		system_name = 'reference'
		name = 'arm'
		name_conv.rename_name_in_format(each, side=side, system=system_name, name=name)

def fix_shapes(*scene_object_list):
	for index, each_object in enumerate(scene_object_list):
		each_object.rename('geometry{}'.format(65+index))
		shapes_list = each_object.getShapes()
		object_name = str(each_object).split('|')[-1]
		for each in shapes_list:
			each.rename('{}Shape'.format(object_name))

rename_selection()



from RMPY.rig import rigSingleJoint

def rename_selection():
	selection = pm.ls(selection=True)
	fix_shapes(*selection)
	for index, each in enumerate(selection):
		side = 'R'
		system_name = 'reference'
		name = 'test'
		name_conv.rename_name_in_format(each, side=side, system=system_name, name=name)

my_rig = rigSingleJoint.RigSingleJoint()
my_rig.create_point_base('R_arm00_reference_pnt',
                         'R_arm01_reference_pnt',
                         'R_arm02_reference_pnt')
