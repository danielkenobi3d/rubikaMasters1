# Arm_rig with Daniel
import pymel.core as pm


def arm_rig_fk(*locators):
    joints_list_fk = []
    pm.select(clear=True)

    # Creates an empty group
    fk_arm_group = pm.group(empty=True, name="FK_Arm")

    # Creates a parent_joint to keep track of the last joint created
    parent_joint = None

    for index,  each_locator in enumerate(locators):
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

        # If the joint is a parent_joint, parent it with the latest joint created
        # if parent_joint:
        #     pm.parent(new_joint, parent_joint)

        parent_joint = new_joint
        joints_list_fk.append(new_joint)
        pm.rename(new_joint, f'fk_joint{index}')

    reset_control_list, controls_fk = control_creation(*joints_list_fk)
    for each_control, each_joint in zip(controls_fk, joints_list_fk):
        pm.parentConstraint(each_control, each_joint)
    # Parent the reset control to the previous control
    for index, reset_control in enumerate(reset_control_list[1:]):

        pm.parent(reset_control, controls_fk[index])


def arm_rig_ik(*locators):
    joints_list_ik = []
    pm.select(clear=True)
    for index, each_locator in enumerate(locators):
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)
        joints_list_ik.append(new_joint)
        pm.rename(new_joint, f'ik_joint{index}')

        # Call the create_control functions
    reset_controls, controls_ik = control_creation(locators[-1])
    # Create IK Handle
    ik_handle, effector = pm.ikHandle(startJoint=joints_list_ik[0], endEffector=joints_list_ik[-1], solver='ikSCsolver')
    pm.parentConstraint(controls_ik, ik_handle)
    pm.rename(controls_ik, 'ikControl')


def control_creation(*joints):
    control_list = []
    reset_control_list = []
    for index, each_joint in enumerate(joints):
        reset_group = pm.group(name=f'reset{index}', empty=True)
        control, make_nurb_circle = pm.circle(normal=[1, 0, 0])
        control_list.append(control)
        pm.matchTransform(control, each_joint)
        pm.matchTransform(reset_group, each_joint)
        reset_control_list.append(reset_group)
        pm.parent(control, reset_group)
    return reset_control_list, control_list


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


locator_list = pm.ls(selection=True)
arm_rig_fk(*locator_list)
arm_rig_ik(*locator_list)


ik_joints_list = pm.ls('ik_joint*', type='joint')
fk_joints_list = pm.ls('fk_joint*', type='joint')
constraint_nodes(ik_joints_list, fk_joints_list)