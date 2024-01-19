import pymel.core as pm
num_joints = 5

joints = []
for i in range(num_joints):
    joint_name = "joint_{0}".format(i + 1)
    joint = pm.joint(name=joint_name, p=(i+20,0,0))
    joints.append(joint)

ik_handle = pm.ikHandle(sj='joint_1', ee='joint_5', solver="ikSplineSolver", curve='curve1', createCurve=False)
ik_handle[0].rename('splineIKHandle')

curve_info = pm.arclen('curve1', ch=True)

multiply_divide_node = pm.createNode('multiplyDivide')
pm.connectAttr(curve_info.arcLength, multiply_divide_node.input1X)
multiply_divide_node.operation.set(2)

multiply_divide_node.outputX >> joints[0].tx
multiply_divide_node.outputX >> joints[-1].tx

