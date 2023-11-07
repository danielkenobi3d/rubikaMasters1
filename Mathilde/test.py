# Arm_rig with Daniel
import pymel.core as pm

def arm_rig_ik(*locators):
    joints_list_ik = []
    pm.select(clear=True)

    # Create joints and add them to the joints_list_ik
    for each_locator in locators:
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)
        joints_list_ik.append(new_joint)

    # Call the create_control function
    controls_ik = control_creation(joints_list_ik[-1])

    # Create IK Handle
    ik_handle, effector = pm.ikHandle(startJoint=joints_list_ik[0], endEffector=joints_list_ik[-1], solver='ikSCsolver')

    # Create a group to hold the IK handle
    ik_handle_group = pm.group(empty=True, name='IK_Handle_Group')
    pm.parent(ik_handle, ik_handle_group)

    # Parent the control to the IK handle group
    for control in controls_ik:
        pm.parent(control, ik_handle_group)

    # Create a parent constraint between the control and the joint at the wrist
    pm.parentConstraint(controls_ik, joints_list_ik[-1])

def control_creation(joints):
    control_list = []
    for each_joint in joints:
        control, make_nurb_circle = pm.circle(normal=[1, 0, 0])
        control_list.append(control)
        pm.matchTransform(control, each_joint)
        pm.parentConstraint(control, each_joint)
    return control_list

locator_list = pm.ls(selection=True)
arm_rig_ik(*locator_list)
