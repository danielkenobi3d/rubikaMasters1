import pymel.core as pm

def arm_rig(*locators):
    joints_list = []
    pm.select(clear=True)
    for each_locator in locators :
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        joints_list.append(new_joint)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

    controls = create_control(locators[-1])
    ik_handle, effector = pm.ikHandle(startJoint=joints_list[0], endEffector=joints_list[-1],solver='ikSCsolver')

    pm.parentConstraint(controls,ik_handle)
    naming(joints_list, controls)


def create_control(*points) :
    control_list=[]
    for each_points in points :
        control, make_nurb_circle=pm.circle(normal=[1,0,0])
        control_list.append(control)
        pm.matchTransform(control, each_points)
    return control_list

def naming(joints_list,controls) :
    naming_joint_list = ['L','shoulder','elbow','hand','CTRL','JNT']
    incr = 0
    for joint in joints_list :
       pm.rename(joint, naming_joint_list[0]+ '_' + naming_joint_list[1+incr]+ '_'+naming_joint_list[-2])
       incr = incr+1

    for control in controls :
       pm.rename(control, naming_joint_list[0]+ '_' + naming_joint_list[1+incr]+ '_'+naming_joint_list[-1])
       incr = incr+1



locator_list=pm.ls(selection=True)
arm_rig(*locator_list)
