import maya.cmds as cmds


def makeController(selec, parent=False, shape='circle', addName=None, scale=1, newName=None, pointConst=False, normalPlane='yz'):
    ctrlList = []
    if selec is None:
        selec = cmds.ls(sl=True)

    if type(selec) != list:
        selec = selec.split()


    for j in range(len(selec)):
        #if name is None:
        if '_joint' in selec[j]:
            name = selec[j].replace('_joint', '')
            if '_end' in name:
                name = name.replace('_end', '')
        else:
            name = selec[j]

        if addName != None:
            name = name + addName
        if newName != None:
            name = newName

        if normalPlane == 'yz':
            normalPlane = (1, 0, 0)
        elif normalPlane == 'xz':
            normalPlane = (0, 1, 0)
        elif normalPlane == 'xy':
            normalPlane = (0, 0, 1)

        if shape == 'circle':
            ctrl = cmds.circle(nr=normalPlane, c=(0, 0, 0), r=2, n=name+'_ctrl')

        elif shape=='star':
            ctrl = cmds.circle(nr=normalPlane, c=(0, 0, 0), r=2, n=name+'_ctrl')

            cmds.select(cl=True)
            for i in [1, 3, 5, 7]:                

                cmds.select(ctrl[0]+'.cv['+str(i)+']', add=True)
            cmds.scale(2, 2, 2, r=True, ocp=True)

        elif shape=='cube':
            ctrl = cmds.curve(d=1, p=[(0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
                             (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
                              (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5),
                             (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5)],
                        k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], n=name+'_ctrl')

        elif shape=='cross':
            ctrl = cmds.curve(d=1, p=[(-0.0959835, 0, -0.751175), (-0.0959835, 0, -0.0987656), (-0.751175, 0, -0.0987656), (-0.751175, 0, -0.336638), 
            (-1.001567, 0, 0), (-0.751175, 0, 0.336638), (-0.751175, 0, 0.0987656), (-0.0959835, 0, 0.0987656), (-0.0959835, 0, 0.751175), 
            (-0.336638, 0, 0.751175), (0, 0, 1.001567), (0.336638, 0, 0.751175), (0.0959835, 0, 0.751175), (0.0959835, 0, 0.0987656), 
            (0.751175, 0, 0.0987656), (0.751175, 0, 0.336638), (1.001567, 0, 0), (0.751175, 0, -0.336638), (0.751175, 0, -0.0987656), 
            (0.0959835, 0, -0.0987656), (0.0959835, 0, -0.751175), (0.336638, 0, -0.751175), (0, 0, -1.001567), (-0.336638, 0, -0.751175), (-0.0959835, 0, -0.751175)], 
            k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], n=name+'_ctrl')

        if scale != 1:
            cmds.select(cl=True)

            if type(ctrl) != list: ctrl = ctrl.split()
            spans = cmds.getAttr(ctrl[0]+'.spans')
            if shape=='cube' or shape=='cross': spans += 1
            for i in range(spans):

                cmds.select(ctrl[0]+'.cv['+str(i)+']', add=True)
            cmds.scale(scale, scale, scale, r=True, ocp=True)
            cmds.select(cl=True)
        
        posGrp = cmds.group(ctrl, n=name+'_Pos')
        cmds.group(ctrl, n=name+'_Const')
        
        if pointConst is True:
            cmds.delete(cmds.pointConstraint(selec[j], posGrp))
        else:
            cmds.delete(cmds.parentConstraint(selec[j], posGrp))

        if parent is True:
            cmds.parent(selec[j], ctrl[0])

        ctrlList.append(ctrl[0])
    
    return ctrlList

def getRoot(sel, nodeName):
    sel = cmds.ls(sel, l=True)[0].split('|')
    for item in sel:
        if nodeName in item:
            root = item

            return root

def ctrlColor(ctrl, color):
    if type(ctrl) == list:
        ctrl = ctrl[0]

    colorSet = {'yellow':17, 'red':13, 'default':5, 'pink':9, 'white':16, 'blue':6, 'skyblue':18}
    color = colorSet.get(color, 'default')
    cmds.setAttr("{0}.overrideEnabled".format(ctrl), True)
    cmds.setAttr("{0}.overrideColor".format(ctrl), color)


class Foot():
    def __init__(self, leg):


        initAnkleJNT = cmds.listRelatives(leg, c=True, ad=True)[0]
        ankleJNT = initAnkleJNT.replace('_joint', '_root_joint')
        ballJNT = [item for item in cmds.listRelatives(ankleJNT, c=True, ad=True) if 'ball' in item][0]
        toeJNT = cmds.listRelatives(ballJNT, c=True)[0]
        legIKhandle = leg.replace('_joint', '_IK_handle')


        Footside = 'foot_'+initAnkleJNT.split('_')[1]

        locGRP = cmds.ls(Footside+'_loc_GRP')[0]
        footLocs = cmds.listRelatives(locGRP, c=True, ad=True, type='transform')
        footLocs.reverse()


        ballIKhandle = cmds.ikHandle(sj=ankleJNT, ee=ballJNT, solver='ikSCsolver', n=ankleJNT.replace('_joint', '_IK_handle'))[0]
        toeIKhandle = cmds.ikHandle(sj=ballJNT, ee=toeJNT, solver='ikSCsolver', n=ballJNT.replace('_joint', '_IK_handle'))[0]

        toeFKctrl = makeController(ballJNT)[0]
        cmds.parentConstraint(footLocs[-4], getRoot(toeFKctrl, nodeName='Const'), mo=True)
        cmds.parentConstraint(toeFKctrl, footLocs[-1], mo=True)

        footCtrl = makeController(ankleJNT, shape='cube', newName=Footside, scale=3)[0]
        ctrlColor(footCtrl, color='skyblue')

        cmds.parent(ballIKhandle, footLocs[-2])
        cmds.parent(toeIKhandle, footLocs[-1])
        

        cmds.parent(getRoot(toeFKctrl, nodeName='Pos'), footCtrl)



        #* now add Costom Attributes to foot ctrl
        
        cmds.addAttr(footCtrl, ln='Foot_Control_Options' ,nn="Foot_Control_Options", at="enum", en="___________:")
        cmds.setAttr(footCtrl+'.Foot_Control_Options', e=1, keyable=1)
        cmds.setAttr(footCtrl+'.Foot_Control_Options', lock=1)

        cmds.addAttr(footCtrl, ln='Heel_Raise', nn="Heel_Raise", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Heel_Raise', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Toes_Raise', nn="Toes_Raise", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Toes_Raise', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Ball_Raise', nn="Ball_Raise", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Ball_Raise', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Ankle_Raise', nn="Ankle_Raise", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Ankle_Raise', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Toe_Tip_Raise', nn="Toe_Tip_Raise", at="float", minValue=0, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Toe_Tip_Raise', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Heel_Twist', nn="Heel_Twist", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Heel_Twist', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Ball_Twist', nn="Ball_Twist", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Ball_Twist', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Toe_Tip_Twist', nn="Toe_Tip_Twist", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Toe_Tip_Twist', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Side_Roll', nn="Side_Roll", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Side_Roll', e=1, keyable=1)

        cmds.addAttr(footCtrl, ln='Foot_Roll', nn="Foot_Roll", at="float", minValue=-10, maxValue=10, defaultValue=0)
        cmds.setAttr(footCtrl+'.Foot_Roll', e=1, keyable=1)



        #* Now Connects each Attributes

        footInRollMD = cmds.createNode('multiplyDivide', n=Footside+'_inRoll_MD')
        footInRollCOND = cmds.createNode('condition', n=Footside+'_inRoll_COND')
        cmds.setAttr(footInRollMD+'.input2X', 9)
        cmds.setAttr(footInRollCOND+'.operation', 4)
        cmds.connectAttr(footCtrl+'.Side_Roll', footInRollMD+'.input1X')
        cmds.connectAttr(footInRollMD+'.outputX', footInRollCOND+'.colorIfTrueR')
        cmds.connectAttr(footCtrl+'.Side_Roll', footInRollCOND+'.firstTerm')
        cmds.connectAttr(footInRollCOND+'.outColorR', footLocs[1]+'.rotateZ')

        footOutRollMD = cmds.createNode('multiplyDivide', n=Footside+'_outRoll_MD')
        footOutRollCOND = cmds.createNode('condition', n=Footside+'_outRoll_COND')
        cmds.setAttr(footOutRollMD+'.input2X', 9)
        cmds.setAttr(footOutRollCOND+'.operation', 2)
        cmds.connectAttr(footCtrl+'.Side_Roll', footOutRollMD+'.input1X')
        cmds.connectAttr(footOutRollMD+'.outputX', footOutRollCOND+'.colorIfTrueR')
        cmds.connectAttr(footCtrl+'.Side_Roll', footOutRollCOND+'.firstTerm')
        cmds.connectAttr(footOutRollCOND+'.outColorR', footLocs[0]+'.rotateZ')

        footRollMD = cmds.createNode('multiplyDivide', n=Footside+'_roll_MD')
        footRollCOND = cmds.createNode('condition', n=Footside+'_roll_COND')
        cmds.setAttr(footRollMD+'.input2X', -7)
        cmds.setAttr(footRollCOND+'.operation', 2)
        cmds.connectAttr(footCtrl+'.Foot_Roll', footRollMD+'.input1X')
        cmds.connectAttr(footRollMD+'.outputX', footRollCOND+'.colorIfTrueR')
        cmds.connectAttr(footCtrl+'.Foot_Roll', footRollCOND+'.firstTerm')
        cmds.connectAttr(footRollCOND+'.outColorR', footLocs[2]+'.rotateX')

        heelRoll1MD = cmds.createNode('multiplyDivide', n=Footside+'_heelRoll_1_MD')
        heelRoll2MD = cmds.createNode('multiplyDivide', n=Footside+'_heelRoll_2_MD')
        cmds.setAttr(heelRoll1MD+'.input2X', -7)
        cmds.setAttr(heelRoll2MD+'.input2X', 5)
        cmds.connectAttr(footCtrl+'.Heel_Raise', heelRoll1MD+'.input1X')
        cmds.connectAttr(heelRoll1MD+'.outputX', footLocs[3]+'.rotateX')
        cmds.connectAttr(footCtrl+'.Heel_Twist', heelRoll2MD+'.input1X')
        cmds.connectAttr(heelRoll2MD+'.outputX', footLocs[3]+'.rotateY')

        toeRoll1MD = cmds.createNode('multiplyDivide', n=Footside+'_toeRoll_1_MD')
        toeRoll2MD = cmds.createNode('multiplyDivide', n=Footside+'_toeRoll_2_MD')
        cmds.setAttr(toeRoll1MD+'.input2X', 9)
        cmds.setAttr(toeRoll2MD+'.input2X', -7)
        cmds.connectAttr(footCtrl+'.Toe_Tip_Raise', toeRoll1MD+'.input1X')
        cmds.connectAttr(toeRoll1MD+'.outputX', footLocs[4]+'.rotateX')
        cmds.connectAttr(footCtrl+'.Toe_Tip_Twist', toeRoll2MD+'.input1X')
        cmds.connectAttr(toeRoll2MD+'.outputX', footLocs[4]+'.rotateY')

        ballMD = cmds.createNode('multiplyDivide', n=Footside+'_ball_MD')
        cmds.setAttr(ballMD+'.input2X', 4.5)
        cmds.connectAttr(footCtrl+'.Ankle_Raise', ballMD+'.input1X')
        cmds.connectAttr(ballMD+'.outputX', footLocs[5]+'.rotateX')

        ballHingeMD = cmds.createNode('multiplyDivide', n=Footside+'_ballHinge_MD')
        ballHingeCOND = cmds.createNode('condition', n=Footside+'_ballHinge_COND')
        cmds.setAttr(ballHingeMD+'.input2X', -9)
        cmds.setAttr(ballHingeCOND+'.operation', 4)
        cmds.connectAttr(footCtrl+'.Foot_Roll', ballHingeMD+'.input1X')
        cmds.connectAttr(ballHingeMD+'.outputX', ballHingeCOND+'.colorIfTrueR')
        cmds.connectAttr(footCtrl+'.Foot_Roll', ballHingeCOND+'.firstTerm')
        cmds.connectAttr(ballHingeCOND+'.outColorR', footLocs[6]+'.rotateX')

        ballTwist1MD = cmds.createNode('multiplyDivide', n=Footside+'_heelRoll_1_MD')
        ballTwist2MD = cmds.createNode('multiplyDivide', n=Footside+'_heelRoll_2_MD')
        cmds.setAttr(ballTwist1MD+'.input2X', 4.5)
        cmds.setAttr(ballTwist2MD+'.input2X', 5)
        cmds.connectAttr(footCtrl+'.Ball_Raise', ballTwist1MD+'.input1X')
        cmds.connectAttr(ballTwist1MD+'.outputX', footLocs[7]+'.rotateX')
        cmds.connectAttr(footCtrl+'.Ball_Twist', ballTwist2MD+'.input1X')
        cmds.connectAttr(ballTwist2MD+'.outputX', footLocs[7]+'.rotateY')



        cmds.parentConstraint(footCtrl, locGRP, mo=True)
        
        if cmds.objExists(legIKhandle) == True:
            print('found IK Handle for ', footCtrl)
            cmds.parent(legIKhandle, footLocs[-2])

    def footSet(self):
        pass
