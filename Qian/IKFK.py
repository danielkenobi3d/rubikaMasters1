import pymel.core as pm

ik_joint1 = pm.joint(name='ik_joint1'，position=(0,10,0))
ik_joint2 = pm.joint(name='ik_joint2'，position=(0,5,5))
ik_end_effector = pm.joint(name='ik_end_effector'，position=(0,1,1))

fk_joint1 = pm.joint(name='fk_joint1')
fk_joint2 = pm.joint(name='fk_joint2')
fk_end_effector = pm.joint(name='fk_end_effector')

ik_control = pm.circle(name='ik_control')[0]

fk_control = pm.circle(name='fk_control')[0]

pm.parentConstraint(ik_control, ik_end_effector, mo=True)

pm.parentConstraint(fk_control, fk_end_effector, mo=True)

switch_control = pm.circle(name='switch_control')[0]

pm.addAttr(switch_control, longName='ik_fk_switch', attributeType='float', min=0, max=1)

ik_fk_switch = switch_control.ik_fk_switch
pm.setDrivenKeyframe(ik_control, attribute='visibility', currentDriver=ik_fk_switch, driverValue=1, value=0)
pm.setDrivenKeyframe(fk_control, attribute='visibility', currentDriver=ik_fk_switch, driverValue=0, value=1)

switch_control.ik_fk_switch >> ik_control.visibility
switch_control.ik_fk_switch >> fk_control.visibility
