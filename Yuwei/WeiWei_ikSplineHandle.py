import pymel.core as pm

pm.select(d=True)
joints = []
pm.joint(n='IKS_Joint01_Start', p=(0,0,0))
pm.joint(n='IKS_Joint02',p=(0,0,4))
pm.joint(n='IKS_Joint03',p=(0,0,8))
pm.joint(n='IKS_Joint04',p=(0,0,12))
pm.joint(n='IKS_Joint05',p=(0,0,16))
pm.joint(n='IKS_Joint06_End',p=(0,0,20))

pm.curve(n='IKS_Curve',pw=[(1,0,-1,1),(3,3,6,1),(10,5,10,1),(20,10,5,1)])

pm.ikHandle(n='ikHandleSpline',
            sj='IKS_Joint01_Start', ee='IKS_Joint06_End',
            sol='ikSplineSolver',
            ccv=False,
            curve='IKS_Curve')

curve_info = pm.createNode('curveInfo')
pm.connectAttr('IKS_CurveShape.ws[0]','curveInfo1.inputCurve')

multiply_divide = pm.createNode('multiplyDivide')
pm.connectAttr(curve_info.arcLength, multiply_divide.input1X)
# pm.setAttr(multiply_divide.input2X, 5)
multiply_divide.input2X.set(5)
multiply_divide.operation.set(2)
for each_joint in ['IKS_Joint02', 'IKS_Joint03', 'IKS_Joint04','IKS_Joint05', 'IKS_Joint06_End']:
    pm.connectAttr(multiply_divide.outputX, f'{each_joint}.translateZ')

#Question: What is ikSplineHandleCtx?
#if pm.ikSplineHandleCtx('ik Spline HandleCtx', q=True, ex=True):
#    pm.ikSplineHandleCtx('ik Spline HandleCtx', e=True, parentCurve=True)


#Daniel Tips:
#scale_node=pm.createNode('multiplyDivide')
#pm.connectAttr('samplerInfo.curveLength','name_of_scale.input1X')
#scale_node.operation.set(2)
