import pymel.core as pm
#    Homework
#  fix the orientation of the joints, They are flipping because there is no angle at the begginning
#  There is no control for the IK control
# Remove the driven key and do a direct connection


def create_arm_rig():
    # Create joints
    shoulder_joint = pm.joint(p=(0, 5, 0), n='shoulder_joint')
    elbow_joint = pm.joint(p=(4, 5, 0), n='elbow_joint')
    wrist_joint = pm.joint(p=(8, 5, 0), n='wrist_joint')

    # Create IK handle
    ik_handle, effector = pm.ikHandle(sj=shoulder_joint, ee=wrist_joint, sol='ikRPsolver', n='arm_ikHandle')

    # Create controllers
    shoulder_ctrl = pm.circle(n='shoulder_ctrl', r=1)[0]
    elbow_ctrl = pm.circle(n='elbow_ctrl', r=1)[0]
    wrist_ctrl = pm.circle(n='wrist_ctrl', r=1)[0]

    # Position controllers
    pm.matchTransform(shoulder_ctrl, shoulder_joint)
    pm.matchTransform(elbow_ctrl, elbow_joint)
    pm.matchTransform(wrist_ctrl, wrist_joint)

    # Create control hierarchy
    shoulder_ctrl_grp = pm.group(shoulder_ctrl, n='shoulder_ctrl_grp')
    elbow_ctrl_grp = pm.group(elbow_ctrl, n='elbow_ctrl_grp')
    wrist_ctrl_grp = pm.group(wrist_ctrl, n='wrist_ctrl_grp')

    pm.parent(elbow_ctrl_grp, shoulder_ctrl)
    pm.parent(wrist_ctrl_grp, elbow_ctrl)

    # Set up IK/FK switch attribute
    pm.addAttr(shoulder_ctrl, ln='IK_FK_Switch', at='double', min=0, max=1, dv=0, k=True)

    # Set up constraints
    pm.parentConstraint(shoulder_ctrl, shoulder_joint, mo=True)
    pm.parentConstraint(elbow_ctrl, elbow_joint, mo=True)
    pm.parentConstraint(wrist_ctrl, wrist_joint, mo=True)

    # Set driven key for IK/FK switch
    pm.setDrivenKeyframe(ik_handle + '.ikBlend', cd=shoulder_ctrl + '.IK_FK_Switch', dv=0, v=1)
    pm.setDrivenKeyframe(ik_handle + '.ikBlend', cd=shoulder_ctrl + '.IK_FK_Switch', dv=1, v=0)

    print("Arm rig with IK switch created.")


# Run the function to create the arm rig
create_arm_rig()
