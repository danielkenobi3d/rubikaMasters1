#Arm_rig with Daniel
import pymel.core as pm

# Creating the FK
def arm_rig_FK(*locators):
    joints_list_FK = []
    pm.select(clear=True)
    for each_locator in locators :
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        joints_list_FK.append(new_joint)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

    #Call the create_control functions
    controls_FK = create_control(joints_list_FK)
    pm.parentConstraint(controls_FK,joints_list_FK)

# Creating the output
def arm_rig_output(*locators):
    joints_list_output = []
    pm.select(clear=True)
    for each_locator in locators :
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        joints_list_output.append(new_joint)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

# Creating the IK
def arm_rig_IK(*locators):
    joints_list_IK = []
    pm.select(clear=True)
    for each_locator in locators :
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        joints_list_IK.append(new_joint)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)
    #Call the create_control functions
    controls_IK = create_control(locators[-1])
    #Create IK Handle
    ik_handle, effector = pm.ikHandle(startJoint=joints_list_IK[0], endEffector=joints_list_IK[-1],solver='ikSCsolver')
    pm.parentConstraint(controls_IK,ik_handle)

    #Naming shit
    naming(joints_list_IK, controls_IK)

#Creating controls
def create_control(*points) :
    control_list=[]
    for each_points in points :
        control, make_nurb_circle=pm.circle(normal=[1,0,0])
        control_list.append(control)
        pm.matchTransform(control, each_points)
    return control_list

#My own naming system
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

arm_rig_IK(*locator_list)
arm_rig_FK(*locator_list)
arm_rig_output(*locator_list)

pm.parentConstraint()

