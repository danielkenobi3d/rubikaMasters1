import pymel.core as pm

pm.select(d=True)
joint_positions = [( i * 2, 0, 0) for i in range(8)]
joint_chain = [pm.joint(p=position) for position in joint_positions]

curve1 = pm.curve( ep=[(0, 0, 0), (1, 0, 4), (-2, 0, 10), (1, 0, 14),(0, 0, 20), (1, 0, 24)])

pm.ikHandle(sj='joint1', ee='joint8', sol='ikSplineSolver', c=curve1, ccv=False)


curve_info_node = pm.createNode('curveInfo')
pm.connectAttr(curve1 + '.worldSpace[0]', curve_info_node + '.inputCurve')

translate_node = pm.createNode('multiplyDivide')

pm.connectAttr(curve_info_node + '.arcLength', translate_node + '.input1X')
translate_node.input2X.set(7)
translate_node.operation.set(2)

for joint in joint_chain:
    pm.connectAttr(translate_node + '.outputX', joint + '.translateX')
