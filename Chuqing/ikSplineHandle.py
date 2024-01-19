import pymel.core as pm

joints = [pm.joint(p=(5, 0, i*2)) for i in range(1, 9)]

curve1=pm.curve(ep=[(0,0,0),(2,0,5),(-2,0,10),(2,0,15),(0,0,20)])

pm.ikHandle(sj='joint1',ee='joint8', n='ikSplineHandle', c=curve1,ccv=False,sol='ikSplineSolver')

curve_info_node = pm.createNode('curveInfo')
curve1.getShape().worldSpace[0].connect(curve_info_node.inputCurve)

multiply_node = pm.createNode('multiplyDivide')

curve_info_node.arcLength >> multiply_node.input1X
multiply_node.operation.set(2.0)
multiply_node.input2X.set(7.0)

for joint in joints:
    multiply_node.outputX >> joint.translateX
