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


locator_list = pm.ls(selection=True)
arm_rig_fk(*locator_list)
arm_rig_ik(*locator_list)
