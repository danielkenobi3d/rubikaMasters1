#Arm_rig with Daniel
import pymel.core as pm

# Creating the FK
def arm_rig_FK(*locators):
    joints_list = []
    pm.select(clear=True)
    for each_locator in locators :
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        joints_list.append(new_joint)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

# Creating the FK
def arm_rig_output(*locators):
    joints_list = []
    pm.select(clear=True)
    for each_locator in locators :
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        joints_list.append(new_joint)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)

# Creating the IK
def arm_rig_IK(*locators):
    joints_list = []
    pm.select(clear=True)
    for each_locator in locators :
        new_joint = pm.joint()
        pm.matchTransform(new_joint, each_locator)
        joints_list.append(new_joint)
        pm.makeIdentity(new_joint, apply=True, translate=True, rotate=True, scale=True)
    #Call the create_control functions
    controls = create_control(locators[-1])
    #Create IK Handle
    ik_handle, effector = pm.ikHandle(startJoint=joints_list[0], endEffector=joints_list[-1],solver='ikSCsolver')
    pm.parentConstraint(controls,ik_handle)

    #Naming shit
    naming(joints_list, controls)

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

