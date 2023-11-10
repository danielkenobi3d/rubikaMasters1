import pymel.core as pm

def create_ik_joints():
    ik_joint1=pm.joint(name='ik_joint1', position=(0,10,0))
    ik_joint2=pm.joint(name='ik_joint2', position=(0,5,5))
    ik_joint3=pm.joint(name='ik_joint3', position=(0,1,1))

    ik_handle=pm.ikHandle(name='ik_handle',startJoint=ik_joint1, endEffector=ik_joint3)

    return ik_handle



def create_fk_joints():
    pm.select(clear=True)
    fk_joint1=pm.joint(name='fk_joint1', position=(5,10,0))
    fk_joint2=pm.joint(name='fk_joint2', position=(5,5,5))
    fk_joint3=pm.joint(name='fk_joint3', position=(5,1,1))
def create_control_on_transform(maya_node):
    control, create_circle = pm.circle(name='reset_control')
    reset_control = pm.group(empty=True, name='reset_control')
    pm.matchTransform(control, maya_node)
    pm.matchTransform(reset_control, maya_node)
    pm.parent(control, reset_control)
    return reset_control, control


def constraint_nodes(source_list, destination_list):
    # creates a control on the first element of the source_list
    reset_control, control = create_control_on_transform(source_list[0])
    pm.addAttr(control, longName='ikControl', keyable=True, min=0, max=1)
    reverse_node = pm.createNode('reverse', name='flip_value')

    # this is connecting the attributes of the control to the reverse node
    control.ikControl >> reverse_node.inputX

    # zip cycles through 2 iterables, and matches one on one the content of the lists
    parent_constraints_list = []
    for source, destination in zip(source_list, destination_list):
        output = pm.joint(name='output')
        pm.parentConstraint(source, output, mo=False)
        parent_constraint_node = pm.parentConstraint(destination, output, mo=False)
        parent_constraints_list.append(parent_constraint_node)
        weight_alias = parent_constraint_node.getWeightAliasList()
        # connecting the control to the first weight
        control.ikControl >> weight_alias[0]
        # connecting the reverse to the second weight
        reverse_node.outputX >> weight_alias[1]


create_ik_joints()
create_fk_joints()
ik_joints_list = pm.ls('ik_joint*')
fk_joints_list = pm.ls('fk_joint*')
constraint_nodes(ik_joints_list, fk_joints_list)
