# Arm_rig with Daniel
import pymel.core as pm


def arm_rig_fk(*locators):
    joints_list_fk = []
    pm.select(clear=True)

    # Creates an empty group
    fk_arm_group = pm.group(empty=True, name="FK_Arm")

    # Creates a parent_joint to keep track of the last joint created
    parent_joint = None

    for each_locator in locators:
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

        # If the joint is a parent_joint, parent it with the latest joint created
        if parent_joint:
            pm.parent(new_joint, parent_joint)

        parent_joint = new_joint
        joints_list_fk.append(new_joint)

    controls_fk = control_creation(*joints_list_fk)

    for control in controls_fk:
        pm.parent(control, fk_arm_group)


def arm_rig_output(*locators):
    joints_list_output = []
    pm.select(clear=True)

    # Creates an empty group
    output = pm.group(empty=True, name="Output")

    # Creates a parent_joint to keep track of the last joint created
    parent_joint = None

    for each_locator in locators:
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

        # If the joint is a parent_joint, parent it with the latest joint created
        if parent_joint:
            pm.parent(new_joint, parent_joint)

        parent_joint = new_joint
        joints_list_output.append(new_joint)
        pm.parent(output)


def arm_rig_ik(*locators):
    joints_list_ik = []
    pm.select(clear=True)
    for each_locator in locators:
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)
        joints_list_ik.append(new_joint)

    # Call the create_control functions
    controls_ik = control_creation(locators[-1])
    # Create IK Handle
    ik_handle, effector = pm.ikHandle(startJoint=joints_list_ik[0], endEffector=joints_list_ik[-1], solver='ikSCsolver')
    pm.parentConstraint(controls_ik, ik_handle)


def control_creation(*joints):
    control_list = []
    for each_joint in joints:
        control, make_nurb_circle = pm.circle(normal=[1, 0, 0])
        control_list.append(control)
        pm.matchTransform(control, each_joint)
        pm.parentConstraint(control, each_joint)
    return control_list


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
arm_rig_output(*locator_list)

ik_joints_list = pm.ls('ik_joint*')
fk_joints_list = pm.ls('fk_joint*')
constraint_nodes(ik_joints_list, fk_joints_list)
