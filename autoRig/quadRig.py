#-*- coding: euc-kr -*-

import maya.cmds as cmds

class General():
    def __init__(self):
        pass

    def getRoot(self, sel, nodeName):
        sel = cmds.ls(sel, l=True)[0].split('|')
        for item in sel:
            if nodeName in item:
                root = item

                return root

    def makeOwnGRP(self, lonelyNode, style='Pos', removeCtrl=False):

        grpName = lonelyNode
        if removeCtrl is True:
            grpName = grpName.replace('_ctrl', '')
        if style == 'Pos':
            grp = cmds.group(em=True, n=grpName+'_Pos', w=True)
        elif style == 'GRP':
            grp = cmds.group(em=True, n=grpName+'_GRP', w=True)
        elif style == 'Buf':
            grp = cmds.group(em=True, n=grpName+'_Buf', w=True)


        cmds.delete(cmds.parentConstraint(lonelyNode, grp, mo=0, sr="none", st="none"))
        if cmds.listRelatives(lonelyNode, p=True) != None:
            cmds.parent(grp, cmds.listRelatives(lonelyNode, p=True)[0])
        cmds.parent(lonelyNode, grp)

        return grp


    def aligner(self, driven, driver, Const='parent'):

        if Const == 'parent':
            cmds.delete(cmds.parentConstraint(driver, driven, mo=False, sr="none", st="none"))
        elif Const == 'orient':
            cmds.delete(cmds.orientConstraint(driver, driven, mo=False))
        elif Const == 'point':
            cmds.delete(cmds.pointConstraint(driver, driven, mo=False))


    def makeController(self, selec, parent=False, shape='circle', addName=None, scale=1, newName=None, pointConst=False, normalPlane='yz', color=None, only=None, sameSpace=False):
        ctrlList = []

        if type(selec) != list:
            selec = selec.split()

        for i in range(len(selec)):
            if '_joint' in selec[i]:
                name = selec[i].replace('_joint', '')
                if '_end' in name:
                    name = name.replace('_end', '')
            else:
                name = selec[i]

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
                ctrl = cmds.circle(nr=normalPlane, c=(0, 0, 0), r=2, n=name+'_ctrl')[0]

            elif shape == 'star':
                ctrl = cmds.circle(nr=normalPlane, c=(0, 0, 0), r=2, n=name+'_ctrl')[0]

                cmds.select(cl=True)
                for j in [1, 3, 5, 7]:
                    cmds.select(ctrl+'.cv['+str(j)+']', add=True)
                cmds.scale(2, 2, 2, r=True, ocp=True)

            elif shape == 'cube':
                ctrl = cmds.curve(d=1, p=[(0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
                                (0.5, 0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5),
                                (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5),
                                (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5)],
                            k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], n=name+'_ctrl')

            elif shape == 'cross':
                print(normalPlane)
                if normalPlane == (0, 0, 1):
                    ctrl = cmds.curve(d=1, p=[(0, 1.001567, 0), (0.336638, 0.751175, 0), (0.0959835, 0.751175, 0), (0.0959835, 0.0987656, 0), (0.751175, 0.0987656, 0), (0.751175, 0.336638, 0), (1.001567, 0, 0), 
                (0.751175, -0.336638, 0), (0.751175, -0.0987656, 0), (0.0959835, -0.0987656, 0), (0.0959835, -0.751175, 0), (0.336638, -0.751175, 0), (0, -1.001567, 0), 
                (-0.336638, -0.751175, 0), (-0.0959835, -0.751175, 0), (-0.0959835, -0.0987656, 0), (-0.751175, -0.0987656, 0), (-0.751175, -0.336638, 0), (-1.001567, 0, 0), 
                (-0.751175, 0.336638, 0), (-0.751175, 0.0987656, 0), (-0.0959835, 0.0987656, 0), (-0.0959835, 0.751175, 0), (-0.336638, 0.751175, 0), (0, 1.001567, 0)], 
                k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], n=name+'_ctrl')

                else:
                    ctrl = cmds.curve(d=1, p=[(-0.0959835, 0, -0.751175), (-0.0959835, 0, -0.0987656), (-0.751175, 0, -0.0987656), (-0.751175, 0, -0.336638), 
                (-1.001567, 0, 0), (-0.751175, 0, 0.336638), (-0.751175, 0, 0.0987656), (-0.0959835, 0, 0.0987656), (-0.0959835, 0, 0.751175), 
                (-0.336638, 0, 0.751175), (0, 0, 1.001567), (0.336638, 0, 0.751175), (0.0959835, 0, 0.751175), (0.0959835, 0, 0.0987656), 
                (0.751175, 0, 0.0987656), (0.751175, 0, 0.336638), (1.001567, 0, 0), (0.751175, 0, -0.336638), (0.751175, 0, -0.0987656), 
                (0.0959835, 0, -0.0987656), (0.0959835, 0, -0.751175), (0.336638, 0, -0.751175), (0, 0, -1.001567), (-0.336638, 0, -0.751175), (-0.0959835, 0, -0.751175)], 
                k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], n=name+'_ctrl')

            if scale != 1:
                cmds.select(cl=True)

                spans = cmds.getAttr(ctrl+'.spans')
                if shape == 'cube' or shape == 'cross': 
                    spans += 1
                for k in range(spans):
                    cmds.select(ctrl+'.cv['+str(k)+']', add=True)
                cmds.scale(scale, scale, scale, r=True, ocp=True)
                cmds.select(cl=True)
            
            if only == 'Buf':
                posGrp = cmds.group(ctrl, n=name+'_Buf')
            elif only == 'Pos':
                posGrp = cmds.group(ctrl, n=name+'_Pos')
            else:
                posGrp = cmds.group(ctrl, n=name+'_Pos')
                cmds.group(ctrl, n=name+'_Const')
                
            if pointConst is True:
                cmds.delete(cmds.pointConstraint(selec[i], posGrp, mo=False))
            else:
                cmds.delete(cmds.parentConstraint(selec[i], posGrp, mo=False))

            if sameSpace is True:
                cmds.parent(posGrp, cmds.listRelatives(selec[i], p=True)[0])

            if parent is True:
                cmds.parent(selec[i], ctrl)

            ctrlList.append(ctrl)

            if color != None:
                self.ctrlColor(ctrl, color)
        
        return ctrlList

    def addCustomAttribute(self, main_=None):
        if main_ is None:
            main_ = cmds.ls(sl=1)
        else:
            main_ = cmds.ls(main_)
        for x in main_:
            name_ = '.Add__Ctr__'
            if cmds.objExists(x+name_)== False:
                cmds.addAttr (x, ln = 'Add__Ctr__' ,nn = "Add__Ctr__",at = "enum",en = "___________:")
                cmds.setAttr (x+name_,e=1,keyable = 1)
                cmds.setAttr (x+name_,lock = 1)
            else:
                cmds.setAttr ('%s.Add__Ctr__'%x,e=1,keyable = 1)


    def ctrlColor(self, ctrl, color):
        if type(ctrl) == list:
            ctrl = ctrl[0]

        colorSet = {'yellow':17, 'red':13, 'default':5, 'pink':9, 'white':16, 'blue':6, 'skyblue':18}
        color = colorSet.get(color, 'default')
        cmds.setAttr("{0}.overrideEnabled".format(ctrl), True)
        cmds.setAttr("{0}.overrideColor".format(ctrl), color)
                


class LegSetUP(General):
    def __init__(self, initJNT):
        self.initJNT = initJNT
        self.initJNTchain = cmds.listRelatives(self.initJNT, c=True, ad=True)
        self.initJNTchain.append(self.initJNT)
        self.initJNTchain.reverse()

        #* make nameSet
        self.initNamechain = []
        for item in self.initJNTchain:
            self.initNamechain.append(item.replace('_joint','')) 

        #* make IK set
        self.ikJNTchain = cmds.duplicate(self.initJNT, rc=True)
        for i, item in enumerate(self.ikJNTchain):
            self.ikJNTchain[i] = cmds.rename(item, item.replace("_joint1", "_IK_joint"))

        #* make FK set
        self.fkJNTchain = cmds.duplicate(self.initJNT, rc=True)
        for i, item in enumerate(self.fkJNTchain):
            self.fkJNTchain[i] = cmds.rename(item, item.replace("_joint1", "_FK_joint"))

        #* define side
        self.side = self.initJNT.split("_")[1]
    
        #* define fore or rear
        if 'shoulder' in str(self.initJNT):
            self.frontOrBack = 'foreLeg'
            self.sideForB = self.frontOrBack+'_'+self.side
        elif 'thigh' in str(self.initJNT):
            self.frontOrBack = 'rearLeg'
            self.sideForB = self.frontOrBack+'_'+self.side

        

        #* find ankle or foot joint 
        self.footJNT = self.initJNTchain[-1].replace('_joint', '_skin_joint')

        self.letsClassify()

        print(self.initNamechain)



    def letsClassify(self):
        if cmds.objExists('global_GRP') is False:
            self.globalGRP = cmds.group(empty=True, w=True, n='global_GRP')
        else:
            self.globalGRP = cmds.ls('global_GRP')[0]

        if cmds.objExists('Extras') is False:
            self.extras = cmds.group(empty=True, w=True, n='Extras')
        else:
            self.extras = cmds.ls('Extras')[0]
        
        if cmds.objExists('spik_GRP') is False:
            self.spikGRP = cmds.group(empty=True, w=True, n='spik_GRP')
        else:
            self.spikGRP = cmds.ls('spik_GRP')[0]

        if cmds.objExists('joint_GRP') is False:
            self.jointGRP = cmds.group(empty=True, w=True, n='joint_GRP')
        else:
            self.jointGRP = cmds.ls('joint_GRP')[0]

        if cmds.objExists(self.frontOrBack+'_bend_GRP') is False:
            self.bendGRP = cmds.group(empty=True, w=True, n=self.frontOrBack+'_bend_GRP')
        else:
            self.bendGRP = cmds.ls(self.frontOrBack+'_bend_GRP')[0]

        if cmds.objExists(self.frontOrBack+'_IK_GRP') is False:
            self.ikGRP = cmds.group(empty=True, w=True, n=self.frontOrBack+'_IK_GRP')
        else:
            self.ikGRP = cmds.ls(self.frontOrBack+'_IK_GRP')

        if cmds.objExists(self.frontOrBack+'_FK_GRP') is False:
            self.fkGRP = cmds.group(empty=True, w=True, n=self.frontOrBack+'_FK_GRP')
        else:
            self.fkGRP = cmds.ls(self.frontOrBack+'_FK_GRP')

        if cmds.objExists(self.sideForB+'_IK_GRP') is False:
            self.sideIKGRP = cmds.group(empty=True, w=True, n=self.sideForB+'_IK_GRP')
        else:
            self.sideIKGRP = cmds.ls(self.sideForB+'_IK_GRP')

        if cmds.objExists(self.sideForB+'_FK_GRP') is False:
            self.sideFKGRP = cmds.group(empty=True, w=True, n=self.sideForB+'_FK_GRP')
        else:
            self.sideFKGRP = cmds.ls(self.sideForB+'_FK_GRP')


        if cmds.objExists(self.sideForB+'_bend_ctrl_GRP') is False:
            self.sideBendGRP = cmds.group(empty=True, w=True, n=self.sideForB+'_bend_ctrl_GRP')
        else:
            self.sideBendGRP = cmds.ls(self.sideForB+'_bend_ctrl_GRP')[0]

        if cmds.listRelatives(self.spikGRP, p=True) is None:
            cmds.parent(self.spikGRP, self.extras)
        if cmds.listRelatives(self.jointGRP, p=True) is None:
            cmds.parent(self.jointGRP, self.globalGRP)


    def keepClassify(self):
        for i in range(len(self.spikCtrlList)-1):

            #++ func ELbow Lock ++#
            upCtrlPosLast = self.getRoot(self.spikCtrlList[i][-1], '_Pos')
            lowCtrlPosFirst = self.getRoot(self.spikCtrlList[i+1][0], '_Pos')

            lockGRP = cmds.group(empty=True, n=self.initNamechain[i+1]+'_lock_ctrl_GRP')
            self.aligner(lockGRP, lowCtrlPosFirst, Const='parent')

            self.lockCtrl = self.makeController(lockGRP, shape='star', newName=lockGRP.replace('_ctrl_GRP', ''))[0]

            cmds.parent(upCtrlPosLast, lowCtrlPosFirst, lockGRP)

            self.addCustomAttribute(self.lockCtrl)

            cmds.addAttr(self.lockCtrl, ln='Sub_Controller_Visibility', nn="Sub Controller Visibility", at="enum", en="Off:On")
            cmds.setAttr(self.lockCtrl+'.Sub_Controller_Visibility', e=1, keyable=1)

            cmds.connectAttr(self.lockCtrl+'.Sub_Controller_Visibility', upCtrlPosLast+'.visibility')
            cmds.connectAttr(self.lockCtrl+'.Sub_Controller_Visibility', lowCtrlPosFirst+'.visibility')

            cmds.parentConstraint(self.lockCtrl, lockGRP, mo=True)


            self.lockCtrlConst = self.getRoot(self.lockCtrl, '_Const')

            elbowLock = cmds.group(empty=True, w=True, n=self.initNamechain[i+1]+'_elbow_lock_GRP')
            cmds.parent(self.getRoot(self.lockCtrl, nodeName='_Pos'), lockGRP, elbowLock)
            cmds.parent(elbowLock, self.sideBendGRP)


            #* make ik and fk joint Controlls spik ctrls so that it can effect skin joints
            if len(self.spikCtrlList) != 2 and i == 0:
                cmds.parentConstraint(self.ikJNTchain[0], self.getRoot(self.spikCtrlList[0][0], '_Const'))
                cmds.parentConstraint(self.fkJNTchain[0], self.getRoot(self.spikCtrlList[0][0], '_Const'))       

            cmds.parentConstraint(self.ikJNTchain[i+1], self.lockCtrlConst, mo=True)
            cmds.parentConstraint(self.fkJNTchain[i+1], self.lockCtrlConst, mo=True)

            if i == len(self.spikCtrlList)-2:
                
                cmds.parentConstraint(self.ikJNTchain[i+2], self.getRoot(self.spikCtrlList[i+1][-1], '_Const'))
                cmds.parentConstraint(self.fkJNTchain[i+2], self.getRoot(self.spikCtrlList[i+1][-1], '_Const'))
            
            if len(self.spikCtrlList) == 2:
                cmds.parentConstraint(self.ikJNTchain[i], self.getRoot(self.spikCtrlList[i][0], '_Const'))
                cmds.parentConstraint(self.fkJNTchain[i], self.getRoot(self.spikCtrlList[i][0], '_Const'))
                if i != len(self.spikCtrlList)-2:
                    cmds.parentConstraint(self.ikJNTchain[i+2], self.getRoot(self.spikCtrlList[i+1][-1], '_Const'))
                    cmds.parentConstraint(self.fkJNTchain[i+2], self.getRoot(self.spikCtrlList[i+1][-1], '_Const'))




    def fire(self):
        self.spikCtrlList = [self.ikRibbon(self.initNamechain[i]) for i in range(len(self.initNamechain)-1)] 

        self.keepClassify()
        self.footSetUp()
        if len(self.initNamechain) == 4:
            self.ikSpringSet()
            self.ikSet()
        else:
            self.ikSet()
        self.fkSet()
        self.ikfkSwitch()

        cmds.hide(self.initJNT)
        self.finalTouch()

        # self.doBind()


    def ikRibbon(self, initName):
        #* find roll skin joint
        RollJNTstart = initName+"_roll_1_skin_joint"
        RollJNTend = initName+"_roll_end_joint"

        #++ first, make a ribbon setup
        spikHandle = cmds.ikHandle(sj=RollJNTstart, ee=RollJNTend, pcv=False, ns=4, solver='ikSplineSolver', n=initName+'_spik_handle')[0]
        spikCRV = cmds.rename('curve1', initName+'_spik_curve')

        spikJNTlist = []
        jointNum = 1
        for i in range(0, 7):            
            if i == 0 or i % 3 == 0:
                spikJNTPos = cmds.pointPosition(spikCRV+'.cv['+str(i)+']')
                cmds.select(cl=True)
                spikJNT = cmds.joint(p=spikJNTPos, n=initName+'_spik_'+str(jointNum)+'_joint') 
                jointNum += 1
                if i == 6:            
                    self.aligner(spikJNT, RollJNTend, Const='orient')
                else:
                    self.aligner(spikJNT, RollJNTstart, Const='orient')
                spikJNTlist.append(spikJNT)

        cmds.skinCluster(spikCRV, spikJNTlist, tsb=True, dr=4.0)

        spikJNTctrlList = self.makeController(spikJNTlist, parent=True, shape='circle')
        

        #* make stretch by scaling roll joints
        crvInfoNode = cmds.createNode('curveInfo', n=spikCRV+'_crvINFO')
        cmds.connectAttr(spikCRV+'.worldSpace[0]', crvInfoNode+'.inputCurve')

        mdNode1 = cmds.createNode('multiplyDivide', n=spikCRV+'_MD1')
        cmds.setAttr(mdNode1+'.operation', 2)
        mdNode2 = cmds.createNode('multiplyDivide', n=spikCRV+'_MD2')
        cmds.setAttr(mdNode2+'.operation', 2)
        crvLength = cmds.arclen(spikCRV)
        cmds.setAttr(mdNode2+'.input2X', crvLength)
        cmds.connectAttr(crvInfoNode+'.arcLength', mdNode1+'.input1X')
        cmds.connectAttr(mdNode1+'.outputX', mdNode2+'.input1X')

        rollList = cmds.listRelatives(RollJNTstart, c=True, ad=True, type='joint')
        rollList.reverse()
        rollList.insert(0, RollJNTstart)
    
        for item in rollList:
            cmds.connectAttr(mdNode2+'.outputX', item+'.scaleX')


        #* make middle ribbon controller follow its both side controllers
        ctrlConst = self.getRoot(spikJNTctrlList[1], '_Const')
        cmds.pointConstraint(spikJNTctrlList[0], spikJNTctrlList[2], ctrlConst, mo=False)

        cmds.setAttr(ctrlConst+'_pointConstraint1.'+spikJNTctrlList[0]+'W0', 0.5)
        cmds.setAttr(ctrlConst+'_pointConstraint1.'+spikJNTctrlList[2]+'W1', 0.5)

        rotJNT1 = cmds.duplicate(RollJNTstart, po=True, n=initName+'_rot_1_ik_joint')[0]
        rotJNT2 = cmds.duplicate(RollJNTend, po=True, n=initName+'_rot_2_ik_joint')[0]

        cmds.parent(rotJNT2, rotJNT1)
        rotJNThandle = cmds.ikHandle(sj=rotJNT1, ee=rotJNT2, solver='ikSCsolver', n=rotJNT1.replace('_joint', '_SCik_handle'))[0]
        cmds.parent(rotJNThandle, spikJNTctrlList[2])

        cmds.orientConstraint(rotJNT1, ctrlConst, mo=True)


        #* make classify
        rotGRP = cmds.group(empty=True, n=initName+'_rot_GRP', w=True)
        self.aligner(rotGRP, spikJNTctrlList[0], Const='parent')

        for item in spikJNTctrlList:
            spikCtrlPos = self.getRoot(item, '_Pos')
            cmds.parent(spikCtrlPos, rotGRP)

        cmds.parent(rotJNT1, spikJNTctrlList[0])

        cmds.hide(rotJNT1)
        cmds.hide(rotJNThandle)
        cmds.hide(spikJNTlist)
        cmds.hide(spikCRV)
        cmds.hide(spikHandle)


        if cmds.objExists(initName+'_spik_GRP') is False:
            spikGRPc = cmds.group(empty=True, w=True, n=initName+'_spik_GRP')
        else:
            spikGRPc = cmds.ls(initName+'_spik_GRP')[0]



        cmds.parent(rotGRP, self.sideBendGRP)

        if cmds.listRelatives(self.sideBendGRP, p=True) is None:
            cmds.parent(self.sideBendGRP, self.bendGRP)
        cmds.parent(spikHandle, spikCRV, spikGRPc)
        cmds.parent(spikGRPc, self.spikGRP)

        return spikJNTctrlList


    def ikSet(self):
        ikHandle = cmds.ikHandle(sj=self.ikJNTchain[-3], ee=self.ikJNTchain[-1], solver='ikRPsolver', n=self.sideForB+'_IK_Handle')[0]
        cmds.hide(ikHandle)
        ikCtrl = self.makeController(ikHandle, newName=ikHandle.replace('_Handle', ''))[0]
        self.ctrlColor(ikCtrl, color='red')

        rootIKctrl = self.makeController(self.ikJNTchain[0], scale=1.5)[0]
        self.ctrlColor(rootIKctrl, color='red')

        cmds.parent(self.getRoot(ikCtrl, nodeName='_Pos'), self.sideIKGRP)
        cmds.parent(self.getRoot(rootIKctrl, nodeName='_Pos'), self.sideIKGRP)

        cmds.parent(self.sideIKGRP, self.ikGRP)

        cmds.parentConstraint(ikCtrl, self.getRoot(self.footCtrl, nodeName='_Const'), mo=True)
        cmds.parentConstraint(self.ikJNTchain[-1], cmds.listRelatives(self.footJNT, p=True)[0], mo=True)


        if len(self.ikJNTchain) == 4:
            
            upLoc = cmds.spaceLocator(n=self.sideForB+'_upVector_loc')[0]
            self.aligner(upLoc, self.ikJNTchain[0], Const='parent')
            cmds.xform(upLoc, r=True, os=True, t=(0, -10, 0))
            cmds.aimConstraint(self.ikJNTchain[1].replace("_IK_joint", "_SpringIK_joint"), self.getRoot(self.ikJNTchain[0].replace('_joint', '_ctrl'), '_Const'), worldUpObject=upLoc, mo=True)
            
            self.makePoleVector(ikHandle, 2)
        else:
            self.makePoleVector(ikHandle, 1)
       
        if len(self.ikJNTchain) == 3:
            cmds.pointConstraint(rootIKctrl, self.ikJNTchain[0], mo=True)
        if len(self.ikJNTchain) == 4:
            cmds.parentConstraint(rootIKctrl, self.ikJNTchain[0], mo=True)

        cmds.parent(ikHandle, self.sideForB+'_footRoll_ctrl')

        

        #* make IK Stretch
        posSet = [cmds.xform(i, q=True, t=True, ws=True) for i in self.ikJNTchain]

        if len(posSet) == 3:                    
            lenCRV = cmds.curve(d=1, p=[posSet[0], posSet[1], posSet[2]], k=(0, 1, 2), n=self.sideForB+'_arcLength_curve')
            arcLenSkinCluster = cmds.skinCluster(lenCRV, self.ikJNTchain, tsb=True, dr=4.0)
            cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[0]', transformValue=[(self.ikJNTchain[0], 1)])
            cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[1]', transformValue=[(self.ikJNTchain[1], 1)])
            cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[2]', transformValue=[(self.ikJNTchain[2], 1)])
        elif len(posSet) == 4:
            lenCRV = cmds.curve(d=1, p=[posSet[0], posSet[1], posSet[2], posSet[3]], k=(0, 1, 2, 3), n=self.sideForB+'_arcLength_curve')
            arcLenSkinCluster = cmds.skinCluster(lenCRV, self.ikJNTchain, tsb=True, dr=4.0)
            cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[0]', transformValue=[(self.ikJNTchain[0], 1)])
            cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[1]', transformValue=[(self.ikJNTchain[1], 1)])
            cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[2]', transformValue=[(self.ikJNTchain[2], 1)])
            cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[3]', transformValue=[(self.ikJNTchain[3], 1)])
        
        arcLen = cmds.arclen(lenCRV)
        distanceNode = cmds.createNode('distanceBetween', n=self.sideForB+'_IK_DIST')
        cmds.connectAttr(rootIKctrl+'.worldMatrix', distanceNode+'.inMatrix1')
        cmds.connectAttr(ikCtrl+'.worldMatrix', distanceNode+'.inMatrix2')

        distanceMD = cmds.createNode('multiplyDivide', n=self.sideForB+'_stretchIK_Dist_MD')
        cmds.setAttr(distanceMD+'.operation', 2)
        cmds.connectAttr(distanceNode+'.distance', distanceMD+'.input1X')

        distanceCOND = cmds.createNode('condition', n=self.sideForB+'_stretchIK_Dist_COND')
        cmds.setAttr(distanceCOND+'.operation', 2)
        cmds.connectAttr(distanceMD+'.outputX', distanceCOND+'.firstTerm')
        cmds.connectAttr(distanceMD+'.outputX', distanceCOND+'.colorIfTrueR')
        cmds.setAttr(distanceCOND+'.secondTerm', arcLen)
        cmds.setAttr(distanceCOND+'.colorIfFalseR', arcLen)

        distanceMD2 = cmds.createNode('multiplyDivide', n=self.sideForB+'_stretchIK_Dist_MD2')
        cmds.setAttr(distanceMD2+'.operation', 2)
        cmds.setAttr(distanceMD2+'.input2X', arcLen)
        cmds.delete(lenCRV)

        self.addCustomAttribute(ikCtrl)
        cmds.addAttr(ikCtrl, ln='Stretch_On_Off', nn="Stretch_On_Off", at="float", maxValue=1, minValue=0, defaultValue=0)

        for i in self.initNamechain[:-1]:
            cmds.addAttr(ikCtrl, ln=i+'_Stretch', nn=i+'_Stretch', at="float", minValue=0, defaultValue=1)
            cmds.setAttr(ikCtrl+'.'+i+'_Stretch', e=1, keyable=1)

        cmds.setAttr(ikCtrl+'.Stretch_On_Off', e=1, keyable=1)
        
        stretchBLND = cmds.createNode('blendColors', n=self.sideForB+'_stretchIK_BLND')

        cmds.connectAttr(distanceCOND+'.outColorR', stretchBLND+'.color1R')
        cmds.setAttr(stretchBLND+'.color2R', arcLen)

        cmds.connectAttr(stretchBLND+'.outputR', distanceMD2+'.input1X')
        cmds.connectAttr(ikCtrl+'.Stretch_On_Off', stretchBLND+'.blender')

        stretchChain = [cmds.createNode('multiplyDivide', n=self.initNamechain[i]+'_stretch_IK_MD') for i in range(len(self.ikJNTchain)-1)]

        for i, item in enumerate(stretchChain):
            cmds.setAttr(item+'.operation', 1)
            cmds.connectAttr(ikCtrl+'.'+self.initNamechain[i]+'_Stretch', item+'.input1X')
            cmds.connectAttr(distanceMD2+'.outputX', item+'.input2X')
            #* Now Connects to joint's scaleX
            cmds.connectAttr(item+'.outputX', self.ikJNTchain[i]+'.scaleX')




    def ikSpringSet(self):
        self.ikSpringJNTchain = cmds.duplicate(self.initJNT, rc=True)
        for i, item in enumerate(self.ikSpringJNTchain):
            self.ikSpringJNTchain[i] = cmds.rename(item, item.replace("_joint1", "_SpringIK_joint"))

        handle = cmds.ikHandle(sj=self.ikSpringJNTchain[0], ee=self.ikSpringJNTchain[3], solver='ikSpringSolver', n=self.sideForB+'_SpringIK_handle')[0]

        self.makePoleVector(handle, 1)
        # cmds.setAttr(handle+'.twist', 180)
        cmds.parent(handle, self.sideForB+'_footRoll_ctrl')
        cmds.hide(self.ikSpringJNTchain[0])




    def makePoleVector(self, pvIKhandle, num):
        #++ pole Vector Controller ++#

        polVecCtrl = self.makeController(self.ikJNTchain[num], addName='_poleVector', shape='cube', scale=1.1)
        self.ctrlColor(polVecCtrl, 'pink')
        poleVecPoly = cmds.polyCreateFacet(p=[cmds.xform(self.ikJNTchain[num-1], q=True, t=True, ws=True), cmds.xform(self.ikJNTchain[num], q=True, t=True, ws=True), 
        cmds.xform(self.ikJNTchain[num+1], q=True, t=True, ws=True)], ch=True, tx=1, n='poleVecPoly')

        cmds.select(cl=True)
        poleVtx = '{0}.vtx[1]'.format(poleVecPoly[0])
        poleVecPos = self.getRoot(polVecCtrl, nodeName='_Pos')
        cmds.normalConstraint(poleVtx, poleVecPos)

        cmds.delete(poleVecPoly)
        cmds.poleVectorConstraint(polVecCtrl, pvIKhandle)

        cmds.xform(poleVecPos, r=True, os=True, t=(0, 0, 10))
        cmds.parent(poleVecPos, self.sideIKGRP)



    def fkSet(self):
        #* make controllers 

        if len(self.fkJNTchain) == 4:
            fkCtrlList = [self.makeController(item, color='blue', scale=1.2)[0] for item in self.fkJNTchain[:-1]]
        elif len(self.fkJNTchain) == 3:
            fkCtrlList = [self.makeController(item, color='blue', scale=1.2)[0] for item in self.fkJNTchain]
                   
        
        for item in fkCtrlList:
            cmds.parent(self.getRoot(item, '_Pos'), self.sideFKGRP)
        
        #* Set Constraints

        cmds.pointConstraint(self.fkJNTchain[1], self.getRoot(fkCtrlList[1], '_Const'), mo=True)
        cmds.orientConstraint(fkCtrlList[0], self.getRoot(fkCtrlList[1], '_Const'), mo=True)

        cmds.pointConstraint(self.fkJNTchain[2], self.getRoot(fkCtrlList[2], '_Const'), mo=True)
        cmds.orientConstraint(fkCtrlList[1], self.getRoot(fkCtrlList[2], '_Const'), mo=True)

        cmds.parentConstraint(fkCtrlList[0], self.fkJNTchain[0], mo=True)
        cmds.orientConstraint(fkCtrlList[1], self.fkJNTchain[1], mo=True)
        if len(self.initJNTchain) == 4:
            cmds.orientConstraint(fkCtrlList[2], self.fkJNTchain[2], mo=True)

        cmds.parentConstraint(fkCtrlList[-1], self.getRoot(self.footCtrl, nodeName='_Const'), mo=True)
        cmds.parentConstraint(self.fkJNTchain[-1], cmds.listRelatives(self.footJNT, p=True)[0], mo=True)

        cmds.parent(self.sideFKGRP, self.fkGRP)

        #* make Stretch setup
        for i, item in enumerate(fkCtrlList):                
            self.addCustomAttribute(item)
            cmds.addAttr(item, ln='Stretch', nn="Stretch", at="float", minValue=0, defaultValue=1)
            cmds.setAttr(item+'.Stretch', e=1, keyable=1)
            cmds.connectAttr(item+'.Stretch', self.fkJNTchain[i]+'.scaleX')



    def footSetUp(self):
        footJNTList = cmds.listRelatives(self.footJNT, ad=True, c=True)
        
        footJNTList.reverse()
        footJNTList.insert(0, self.footJNT)
        footIKhandleList = []
        for i in range(len(footJNTList)-1):
            handle = cmds.ikHandle(sj=footJNTList[i], ee=footJNTList[i+1], solver='ikSCsolver', n=footJNTList[i+1].replace('_skin_joint', '_IK_handle'))[0]
            footIKhandleList.append(handle)
            cmds.hide(handle)
        
        self.footCtrl = self.makeController(footJNTList[1], pointConst=True, shape='cube', color='yellow', scale=1.2, newName=self.sideForB+'_foot', only='Buf')[0]

        footCtrlConst = cmds.group(empty=True, w=True, n=self.footCtrl.replace('_ctrl', '_Const'))
        footCtrlPos = cmds.group(empty=True, w=True, n=self.footCtrl.replace('_ctrl', '_Pos'))

        self.aligner(footCtrlConst, footJNTList[0], Const='parent')
        self.aligner(footCtrlPos, footJNTList[0], Const='parent')

        cmds.parent(footIKhandleList, self.footCtrl)
        cmds.parent(footCtrlConst, footCtrlPos)
        cmds.parent(self.getRoot(self.footCtrl, nodeName='_Buf'), footCtrlConst)


        #* Let's foot 
        footLocGRP = self.sideForB+'_foot_Loc_GRP'
        footLocList = cmds.listRelatives(footLocGRP, ad=True, c=True, type='transform')
        footLocList.reverse()
        footSubCtrlList = []
        for i, item in enumerate(footLocList):
            currentCtrl = self.makeController(item, color='skyblue', newName=item.replace('_loc', ''), scale=0.2, only='Pos')[0]
            footSubCtrlList.append(currentCtrl) 
            if i > 0 and i < len(footLocList)-1:
                cmds.parent(self.getRoot(currentCtrl, 'Pos'), footSubCtrlList[i-1])
            if i == len(footLocList)-1:
                cmds.parent(self.getRoot(currentCtrl, 'Pos'), footSubCtrlList[i-2])
            
        cmds.delete(footLocGRP)

        if len(footIKhandleList) == 3:
            cmds.parent(footIKhandleList[1], footSubCtrlList[-3])
            cmds.parent(footIKhandleList[0], footSubCtrlList[-1])
            cmds.parent(footIKhandleList[-1], footSubCtrlList[-2])
        elif len(footIKhandleList) == 2:
            cmds.parent(footIKhandleList[0], footSubCtrlList[-3])
            cmds.parent(footIKhandleList[1], footSubCtrlList[-2])
            
        cmds.parent(self.getRoot(footSubCtrlList[0], 'Pos'), self.footCtrl)



    def ikfkSwitch(self):
        switchCtrl = self.makeController(self.footCtrl, shape='cube', color='white', scale=0.8, newName=self.sideForB+'_IKFK_Switch')[0]
        if self.side == 'L':
            cmds.xform(self.getRoot(switchCtrl, '_Pos'), r=True, os=True, t=(5, 0, 0))
        else:
            cmds.xform(self.getRoot(switchCtrl, '_Pos'), r=True, os=True, t=(-5, 0, 0))
        self.addCustomAttribute(switchCtrl)
        cmds.addAttr(switchCtrl, ln='IK_to_FK', nn="IK_to_FK", at="float", maxValue=1, minValue=0)
        cmds.setAttr(switchCtrl+'.IK_to_FK', e=1, keyable=1)

        switchCtrlREV = cmds.createNode('reverse', n=self.sideForB+'_IKFKswitch_REV')
        cmds.connectAttr('{0}.IK_to_FK'.format(switchCtrl), '{0}.inputX'.format(switchCtrlREV))

        #* ik - fk visibility 
        cmds.connectAttr('{0}.outputX'.format(switchCtrlREV), '{0}.visibility'.format(self.sideIKGRP))
        cmds.connectAttr('{0}.outputX'.format(switchCtrlREV), '{0}.visibility'.format(self.ikJNTchain[0]))
        cmds.connectAttr('{0}.IK_to_FK'.format(switchCtrl), '{0}.visibility'.format(self.sideFKGRP))
        cmds.connectAttr('{0}.IK_to_FK'.format(switchCtrl), '{0}.visibility'.format(self.fkJNTchain[0]))



        #* ik connections
        cmds.connectAttr(switchCtrlREV+'.outputX', self.getRoot(self.spikCtrlList[0][0], '_Const')+'_parentConstraint1.'+self.ikJNTchain[0]+'W0')
        cmds.connectAttr(switchCtrlREV+'.outputX', self.initNamechain[1]+'_lock_Const_parentConstraint1.'+self.ikJNTchain[1]+'W0')

        if len(self.initJNTchain) == 4:
            cmds.connectAttr(switchCtrlREV+'.outputX', self.initNamechain[2]+'_lock_Const_parentConstraint1.'+self.ikJNTchain[2]+'W0')

        cmds.connectAttr(switchCtrlREV+'.outputX', self.getRoot(self.spikCtrlList[-1][-1], '_Const')+'_parentConstraint1.'+self.ikJNTchain[-1]+'W0')

        cmds.connectAttr(switchCtrlREV+'.outputX', self.footCtrl.replace('_ctrl', '_Const')+'_parentConstraint1.'+self.sideForB+'_IK_ctrl'+'W0')
        cmds.connectAttr(switchCtrlREV+'.outputX', cmds.listRelatives(self.footJNT, p=True)[0]+'_parentConstraint1.'+self.ikJNTchain[-1]+'W0')

        #* fk connections 
        cmds.connectAttr(switchCtrl+'.IK_to_FK', self.getRoot(self.spikCtrlList[0][0], '_Const')+'_parentConstraint1.'+self.fkJNTchain[0]+'W1')
        cmds.connectAttr(switchCtrl+'.IK_to_FK', self.initNamechain[1]+'_lock_Const_parentConstraint1.'+self.fkJNTchain[1]+'W1')

        if len(self.initJNTchain) == 4:
            cmds.connectAttr(switchCtrl+'.IK_to_FK', self.initNamechain[2]+'_lock_Const_parentConstraint1.'+self.fkJNTchain[2]+'W1')

        cmds.connectAttr(switchCtrl+'.IK_to_FK', self.getRoot(self.spikCtrlList[-1][-1], '_Const')+'_parentConstraint1.'+self.fkJNTchain[-1]+'W1')

        cmds.connectAttr(switchCtrl+'.IK_to_FK', self.footCtrl.replace('_ctrl', '_Const')+'_parentConstraint1.'+self.fkJNTchain[2].replace('_joint', '_ctrl')+'W1')
        cmds.connectAttr(switchCtrl+'.IK_to_FK', cmds.listRelatives(self.footJNT, p=True)[0]+'_parentConstraint1.'+self.fkJNTchain[-1]+'W1')        



    def stretchSetUp(self):
        pass


    def finalTouch(self):
        handles = cmds.ls('*handle')
        cmds.select(handles, r=True)
        cmds.hide()
        cmds.select(cl=True)




class SpineSetUP(General):
    def doSpineSetUp(self):
        #++ Spine SetUp ++#

        waistJNTs = cmds.ls('waist_*')
        cmds.hide(waistJNTs)
        waistMidJNT = waistJNTs.pop(0)
        waistJNTs.insert(1, waistMidJNT)

        spineJNTs = cmds.ls('spine_*')
        chestJNTs = [f for f in cmds.ls('chest_*', type='joint') if not '_IK_' in f and not 'skin' in f]
        chestRootJNT = chestJNTs.pop(-1)
        chestJNTs.insert(0, chestRootJNT)


        hipJNTs = cmds.ls('hip_*')[::-1]


        spineIKhandle = cmds.ikHandle(sj=spineJNTs[0], ee=spineJNTs[-1], sol='ikSplineSolver', pcv=False, ns=4, n='spine_spik_handle')
        spineIKCRV = cmds.rename(spineIKhandle[-1], 'spine_spik_curve')

        cmds.skinCluster(waistJNTs, spineIKCRV, toSelectedBones=True, dropoffRate=4.0)

        waistMidctrl = self.makeController(selec=waistJNTs[1], pointConst=True, normalPlane='xy')
        waistRootctrl = self.makeController(selec=waistJNTs[0], pointConst=True, normalPlane='xy')
        chestLowctrl = self.makeController(selec=waistJNTs[2], newName='chest_Low', pointConst=True, normalPlane='xy')
        hipctrl = self.makeController(selec=waistJNTs[0], shape='cube', newName='hip', scale=7, pointConst=True, normalPlane='xy')
        pelvisctrl = self.makeController(selec=waistJNTs[0], newName='pelvis', scale=3, pointConst=True, normalPlane='xy')
        chestUpctrl = self.makeController(selec=chestJNTs[1], newName='chest_Up', pointConst=True, normalPlane='xy')
        waistIKctrl = self.makeController(selec=waistJNTs[1], shape='cross', addName='_IK', pointConst=True, scale=6, parent=True, normalPlane='xy')
        waistIKctrlGRP = self.getRoot(sel=waistIKctrl, nodeName='Pos')
        self.ctrlColor(waistIKctrl, color='red')
        self.ctrlColor(pelvisctrl, color='blue')
        self.ctrlColor(hipctrl, color='yellow')
        self.ctrlColor(waistRootctrl, color='default')
        self.ctrlColor(waistMidctrl, color='default')
        self.ctrlColor(chestLowctrl, color='default')
        self.ctrlColor(chestUpctrl, color='default')


        cmds.parentConstraint(waistJNTs[0], waistJNTs[2], waistIKctrlGRP, mo=True)
        cmds.parent(waistIKctrlGRP, waistMidctrl)
        cmds.parent(self.getRoot(sel=chestLowctrl, nodeName='Pos'), waistMidctrl)
        cmds.parent(self.getRoot(sel=waistMidctrl, nodeName='Pos'), waistRootctrl)

        cmds.parent(waistJNTs[2], chestLowctrl)
        cmds.parent(self.getRoot(sel=chestUpctrl, nodeName='Pos'), chestLowctrl)

        waistRootJNT_GRP = cmds.group(empty=True, w=True, n=waistJNTs[0]+'_GRP')
        waistRootJNT_Pos = self.makeOwnGRP(waistRootJNT_GRP, style='Pos')
        self.aligner(waistRootJNT_Pos, waistJNTs[0], Const='point')
        cmds.connectAttr(waistRootctrl[0]+'.translate', waistRootJNT_GRP+'.translate')
        cmds.connectAttr(waistRootctrl[0]+'.rotate', waistRootJNT_GRP+'.rotate')
        cmds.parent(waistJNTs[0], waistRootJNT_GRP)
        cmds.parent(waistRootJNT_Pos, hipctrl)

        cmds.parentConstraint(hipctrl, hipJNTs[0], mo=True)


        #* Add hip rotation offset Attribute to hip controller 
        self.addCustomAttribute(hipctrl)
        cmds.addAttr(hipctrl, ln='Rotation_OffSet', nn="Rotation_OffSet", at="float", defaultValue=0)
        cmds.setAttr(hipctrl[0]+'.Rotation_OffSet', e=1, keyable=1)

        hipRotOffset_MD = cmds.createNode('multiplyDivide', n='hip_Rot_Offset_MD')
        cmds.connectAttr(hipctrl[0]+'.rotateX', hipRotOffset_MD+'.input1X')
        cmds.connectAttr(hipctrl[0]+'.rotateY', hipRotOffset_MD+'.input1Y')
        cmds.connectAttr(hipctrl[0]+'.rotateZ', hipRotOffset_MD+'.input1Z')

        cmds.connectAttr(hipctrl[0]+'.Rotation_OffSet', hipRotOffset_MD+'.input2X')
        cmds.connectAttr(hipctrl[0]+'.Rotation_OffSet', hipRotOffset_MD+'.input2Y')
        cmds.connectAttr(hipctrl[0]+'.Rotation_OffSet', hipRotOffset_MD+'.input2Z')

        cmds.connectAttr(hipRotOffset_MD+'.outputX', waistJNTs[0]+'.rotateX')
        cmds.connectAttr(hipRotOffset_MD+'.outputY', waistJNTs[0]+'.rotateY')
        cmds.connectAttr(hipRotOffset_MD+'.outputZ', waistJNTs[0]+'.rotateZ')



        #* chest SetUp
        chestIKhandle = cmds.ikHandle(sj=chestJNTs[0], ee=chestJNTs[-1], solver='ikSplineSolver', pcv=False, ns=4, n='chest_spik_handle')
        chestIKCRV = cmds.rename(chestIKhandle[-1], 'chest_spik_curve')
        chestIKJNTs = cmds.ls('chest_*_IK_joint')
        chestIKJNTs.reverse()
        cmds.skinCluster(chestIKJNTs, chestIKCRV, toSelectedBones=True, dropoffRate=4.0)


        #* more classify
        cmds.parent(self.getRoot(sel=waistRootctrl, nodeName='Pos'), pelvisctrl)
        cmds.parent(self.getRoot(sel=hipctrl, nodeName='Pos'), pelvisctrl)

        bodySpikGRP = cmds.group(empty=True, w=True, n='body_spik_GRP')
        cmds.parent(chestIKhandle[0], chestIKCRV, bodySpikGRP)
        cmds.parent(spineIKhandle[0], spineIKCRV, bodySpikGRP)

        cmds.setAttr(waistMidctrl[0]+'.rotateOrder', 1)
        cmds.setAttr(waistRootctrl[0]+'.rotateOrder', 1)
        cmds.setAttr(chestLowctrl[0]+'.rotateOrder', 1)
        cmds.setAttr(hipctrl[0]+'.rotateOrder', 1)
        cmds.setAttr(pelvisctrl[0]+'.rotateOrder', 1)
        cmds.setAttr(chestUpctrl[0]+'.rotateOrder', 1)
        cmds.setAttr(waistIKctrl[0]+'.rotateOrder', 1)


        cmds.parentConstraint(chestLowctrl, cmds.listRelatives(chestRootJNT, parent=True)[0], mo=True)

        cmds.parent(bodySpikGRP, 'Extras')


        #* waist Twist SetUp 
        waistTwistPMA = cmds.createNode('plusMinusAverage', n='waistTwist_PMA')
        waistTwistMD = cmds.createNode('multiplyDivide', n='waistTwist_MD')
        hipTwistMD = cmds.createNode('multiplyDivide', n='hipTwist_MD')
        cmds.addAttr(waistRootctrl, ln='Twist_Offset', nn="Twist_Offset", at="float", minValue=0, defaultValue=1)
        cmds.setAttr(waistRootctrl[0]+'.Twist_Offset', e=1, keyable=1)
        cmds.addAttr(waistMidctrl, ln='Twist_Offset', nn="Twist_Offset", at="float", minValue=0, defaultValue=1)
        cmds.setAttr(waistMidctrl[0]+'.Twist_Offset', e=1, keyable=1)
        cmds.addAttr(chestLowctrl, ln='Twist_Offset', nn="Twist_Offset", at="float", minValue=0, defaultValue=1)
        cmds.setAttr(chestLowctrl[0]+'.Twist_Offset', e=1, keyable=1)

        cmds.connectAttr(waistRootctrl[0]+'.rotateY', waistTwistMD+'.input1X')
        cmds.connectAttr(waistMidctrl[0]+'.rotateY', waistTwistMD+'.input1Y')
        cmds.connectAttr(chestLowctrl[0]+'.rotateY', waistTwistMD+'.input1Z')
        cmds.connectAttr(hipctrl[0]+'.rotateY', hipTwistMD+'.input1X')

        cmds.connectAttr(waistRootctrl[0]+'.Twist_Offset', waistTwistMD+'.input2X')
        cmds.connectAttr(waistMidctrl[0]+'.Twist_Offset', waistTwistMD+'.input2Y')
        cmds.connectAttr(chestLowctrl[0]+'.Twist_Offset', waistTwistMD+'.input2Z')

        cmds.connectAttr(waistTwistMD+'.outputX', waistTwistPMA+'.input2D[0].input2Dx')
        cmds.connectAttr(waistTwistMD+'.outputY', waistTwistPMA+'.input2D[1].input2Dx')
        cmds.connectAttr(waistTwistMD+'.outputZ', waistTwistPMA+'.input2D[2].input2Dx')
        cmds.connectAttr(hipTwistMD+'.outputX', waistTwistPMA+'.input2D[3].input2Dx')

        cmds.connectAttr(waistTwistPMA+'.output2Dx', spineIKhandle[0]+'.twist')


        handles = cmds.ls('*handle')
        cmds.select(handles, r=True)
        cmds.hide()
        cmds.select(cl=True)



    #* reverse Twist SetUp 







    def doBind(self):
        cmds.select(cl=True)
        cmds.select('*_skin_joint')
        cmds.select('Dog', add=True)
        cmds.skinCluster(tsb=True, dr=4.0)




class ForeLeg(General):

    def __init__(self):
        pass




    def rearLeg(self, initJNT):
        pass






