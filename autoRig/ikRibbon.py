#-*- coding: euc-kr -*-

import maya.cmds as cmds


def addCustomAttribute(main_=None):
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


def makeOwnGRP(lonelyNode, style='Pos'):
    if type(lonelyNode) == list:
        lonelyNode = lonelyNode[0]
    cmds.select(cl=True)
    if style == 'Pos':
        grp = cmds.group(em=True, n=lonelyNode+'_Pos')
    elif style == 'GRP':
        grp = cmds.group(em=True, n=lonelyNode+'_GRP')

    cmds.select(lonelyNode, r=1)
    cmds.select(grp, add=1)

    cmds.delete(cmds.parentConstraint(mo=0, sr="none", st="none"))
    cmds.parent(lonelyNode, grp)
    return grp


def getRoot(nodType, sel=None):
    if sel is None:
        cmds.select(sl=True, r=True)
    else:
        cmds.select(sel, r=True)
    sel = cmds.ls(sl=True, l=True)[0].split('|')
    cmds.select(cl=True)
    for i, j in enumerate(sel):
        if cmds.nodeType(sel[i+1]) == str(nodType):
            root = sel[i+1]

            return root


def controllerColor(ctrl, color):
    if type(ctrl) == list:
        ctrl = ctrl[0]

    colorSet = {'yellow':17, 'red':13, 'default':5, 'pink':9, 'white':16, 'blue':6}
    color = colorSet.get(color, 'darkblue')
    cmds.setAttr("{0}.overrideEnabled".format(ctrl), True)
    cmds.setAttr("{0}.overrideColor".format(ctrl), color)


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


def aligner(driven, driver, Const=False):

    cmds.select(driver, r=1)
    cmds.select(driven, add=1)

    if Const == 'parent':
        cmds.delete(cmds.parentConstraint(mo=False, sr="none", st="none"))
    elif Const == 'orient':
        cmds.delete(cmds.orientConstraint(mo=False))
    elif Const == 'point':
        cmds.delete(cmds.pointConstraint(mo=False))





def limbsSetUp(initialSelec):    
    #++ functions ++# 
    def makeIKRibbon(selectedName):

        
        rollNamingFirst = '_roll_1_skin_joint'
        rollNamingEnd = '_roll_end_joint'
        selecRollFirst = selectedName+rollNamingFirst
        selecRollEnd = selectedName+rollNamingEnd



        if cmds.objExists('spik_GRP') is False:
            spikGRP = cmds.group(empty=True, w=True, n='spik_GRP')
        else:
            spikGRP = cmds.ls('spik_GRP')[0]


        #!!!!!!!!!
        sideName = selectedName

        if selectedName.split('_')[0] == 'shoulder':
            sideName = sideName.replace('shoulder', 'arm')
        elif selectedName.split('_')[0] == 'elbow':
            sideName = sideName.replace('elbow', 'arm')

        elif selectedName.split('_')[0] == 'thigh':
            sideName = sideName.replace('thigh', 'leg')
        elif selectedName.split('_')[0] == 'knee':
            sideName = sideName.replace('knee', 'leg')

        sideName = sideName.replace('_joint', '')
        #!!!!!!!!!

        spikHandle = cmds.ikHandle(sj=selecRollFirst, ee=selecRollEnd, sol='ikSplineSolver', pcv=False, ns=4, n=selectedName + '_spik_handle')
        spikCRV = selectedName+'_spik_curve'
        cmds.rename('curve1', spikCRV)

        curvePoint = cmds.pointOnCurve(spikCRV, p=True)


        jointNum = 1
        spikJNTList = []
        for i in range(7):
            spikJntPos = cmds.pointPosition(spikCRV+'.cv['+str(i)+']')
            cmds.select(cl=True)
            if i != 1 and i != 5:
                spikJNT = cmds.joint(p=spikJntPos, n=selectedName+'_spik_'+str(jointNum)+'_joint', rad=2)
                cmds.hide(spikJNT)
                if i == 6:            
                    aligner(spikJNT, selecRollEnd, Const='orient')
                else:
                    aligner(spikJNT, selecRollFirst, Const='orient')
                cmds.makeIdentity(spikJNT, apply=True, t=0, r=1, s=0, n=1, pn=1)
                spikJNTList.append(spikJNT)
                jointNum += 1



        cmds.select(spikJNTList, r=True)
        cmds.select(spikCRV, add=True)
        cmds.skinCluster(tsb=True, dr=4.0)

        spikCtrlList = makeController(spikJNTList, parent=True, )



        crvInfoNode = cmds.createNode('curveInfo', n=spikCRV+'_crvINFO')
        cmds.connectAttr(spikCRV+'.worldSpace[0]', crvInfoNode+'.inputCurve')

        mdNode1 = cmds.createNode('multiplyDivide', n=spikCRV+'_MD1')
        cmds.setAttr(mdNode1+'.operation', 2)
        mdNode2 = cmds.createNode('multiplyDivide', n=spikCRV+'_MD2')
        cmds.setAttr(mdNode2+'.operation', 2)
        crvLength = cmds.getAttr(crvInfoNode+'.arcLength')
        cmds.setAttr(mdNode2+'.input2X', crvLength)
        cmds.connectAttr(crvInfoNode+'.arcLength', mdNode1+'.input1X')
        cmds.connectAttr(mdNode1+'.outputX', mdNode2+'.input1X')


        rollList = cmds.listRelatives(selecRollFirst, c=True, ad=True, type='joint')
        list.reverse(rollList)
        rollList.insert(0, selecRollFirst)
    

        for i in range(len(rollList)):
            cmds.connectAttr(mdNode2+'.outputX', rollList[i]+'.scaleX')

        val1 = 0.75
        val2 = 0.25

        for i in range(1,4):
            cmds.select(spikCtrlList[0], r=True)
            cmds.select(spikCtrlList[-1], add=True)
            
            ctrlConst = cmds.listRelatives(spikCtrlList[i], parent=True)[0]
            cmds.select(ctrlConst, add=True)
            
            cmds.pointConstraint(mo=False, weight=1)
            
            cmds.setAttr(ctrlConst+'_pointConstraint1.'+spikCtrlList[0]+'W0', val1)
            cmds.setAttr(ctrlConst+'_pointConstraint1.'+spikCtrlList[-1]+'W1', val2)

            val1 -= 0.25 
            val2 += 0.25 

        rotJNT1 = cmds.duplicate(rollList[0], po=True, n=selectedName+'_rot_1_ik_joint')
        rotJNT2 = cmds.duplicate(rollList[-1], po=True, n=selectedName+'_rot_2_ik_joint')

        cmds.parent(rotJNT1, w=True)
        cmds.parent(rotJNT2, rotJNT1)

        rotSCik = cmds.ikHandle(sj=rotJNT1[0], ee=rotJNT2[0], sol='ikSCsolver', n=selectedName + '_rot_SCik_handle')

        cmds.parent(selectedName + '_rot_SCik_handle', spikCtrlList[-1])

        rotGRP = cmds.group(empty=True, n=selectedName+'_rot_GRP', w=True)
        aligner(rotGRP, spikCtrlList[0], Const='parent')


        for i in range(1,4):
            spikCtrlPos = cmds.listRelatives(cmds.listRelatives(spikCtrlList[i], ap=True, p=True), p=True)
            cmds.parent(spikCtrlPos, rotGRP)

        cmds.select(rotJNT1, r=True)
        cmds.select(rotGRP, add=True)
        cmds.orientConstraint(mo=True)

        cmds.parent(rotJNT1, spikCtrlList[0])

        cmds.hide(rotJNT1)
        cmds.hide(rotSCik)
        cmds.hide(spikHandle[0])

        #!!!!!!!!!
        if cmds.objExists(sideName+'_spik_GRP') is False:
            sidespikGRP = cmds.group(empty=True, w=True, n=sideName+'_spik_GRP')
        else:
            sidespikGRP = cmds.ls(sideName+'_spik_GRP')[0]
        #!!!!!!!!!

        selectedspikGRP = cmds.group(empty=True, w=True, n=selectedName+'_spik_GRP')
        cmds.parent(spikHandle[0], spikCRV, selectedspikGRP)
        cmds.parent(selectedspikGRP, sidespikGRP)

        return spikCtrlList


    #++ MAIN ++#

    
    print(initialSelec)
    side = initialSelec.split('_')[1]
    selecFirst = initialSelec
    selecSecond = (cmds.listRelatives(selecFirst, c=True))[0]
    selecThird = (cmds.listRelatives(selecSecond, c=True))[0]

    #* make IK set
    dup = cmds.duplicate(initialSelec, renameChildren=True, n=initialSelec.replace('_joint', '_IK_joint'))
    cmds.rename(dup[1], dup[1].replace('_joint1', '_IK_joint'))
    cmds.rename(dup[2], dup[2].replace('_joint1', '_IK_joint'))

    #* make FK set
    dup = cmds.duplicate(initialSelec, renameChildren=True, n=initialSelec.replace('_joint', '_FK_joint'))
    cmds.rename(dup[1], dup[1].replace('_joint1', '_FK_joint'))
    cmds.rename(dup[2], dup[2].replace('_joint1', '_FK_joint'))


    selectedIKFirst = initialSelec.replace('_joint', '_IK_joint')
    selectedIKMiddle = (cmds.listRelatives(selectedIKFirst, c=True))[0]
    selectedIKLast = (cmds.listRelatives(selectedIKMiddle, c=True))[0]

    selectedFKFirst = initialSelec.replace('_joint', '_FK_joint')
    selectedFKMiddle = (cmds.listRelatives(selectedFKFirst, c=True))[0]
    selectedFKLast = (cmds.listRelatives(selectedFKMiddle, c=True))[0]



    selectedName1 = selecFirst.replace('_joint', '')
    ribbonCtrls1 = makeIKRibbon(selectedName1)

    selectedName2 = selecSecond.replace('_joint', '')
    ribbonCtrls2 = makeIKRibbon(selectedName2)

    selectedName3 = selecThird.replace('_joint', '')




    #++ get Side GRP name ++#

    sideGRPName = initialSelec

    if initialSelec.split('_')[0] == 'shoulder':
        sideGRPName = sideGRPName.replace('shoulder', 'arm')

    elif initialSelec.split('_')[0] == 'thigh':
        sideGRPName = sideGRPName.replace('thigh', 'leg')

    sideGRPName = sideGRPName.replace('_joint', '')




    #++ initial classify +##

    rollShoulderGRP = makeOwnGRP(selectedName1+'_roll_1_skin_joint', style='GRP')
    rollElbowGRP = makeOwnGRP(selectedName2+'_roll_1_skin_joint', style='GRP')


    skinJointGRP = cmds.group(empty=True, p='joint_GRP', n=sideGRPName+'_joint_GRP')
    # cmds.parent(rollShoulderGRP, rollElbowGRP, skinJointGRP)


    if cmds.objExists('global_GRP') is False:
        globalGRP = cmds.group(empty=True, w=True, n='global_GRP')
    else:
        globalGRP = cmds.ls('global_GRP')[0]

    if cmds.objExists('Extras') is False:
        extras = cmds.group(empty=True, w=True, n='Extras')
    else:
        extras = cmds.ls('Extras')[0]
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cmds.select(cl=True)
    cmds.select(globalGRP, hi=True)
    check = cmds.ls(sl=True)

    if ('joint_GRP' in check) is False:
        cmds.parent('joint_GRP', globalGRP)
        cmds.parent('spik_GRP', extras)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    #++ func ELbow Lock ++#

    upCtrlPosLast = selecFirst.replace('_joint', '_spik_5_Pos')
    lowCtrlPosFirst = selecSecond.replace('_joint', '_spik_1_Pos')

    lockGRP = cmds.group(empty=True, n=selectedName2+'_lock_ctrl_GRP')
    aligner(lockGRP, lowCtrlPosFirst, Const='parent')

    lockCtrl = makeController(lockGRP, shape='star')

    cmds.parent(upCtrlPosLast, lowCtrlPosFirst, lockGRP)
    # cmds.delete(lockGRP)

    addCustomAttribute(lockCtrl)

    cmds.addAttr(lockCtrl, ln='Sub_Controller_Visibility', nn="Sub Controller Visibility", at="enum", en="Off:On")
    cmds.setAttr(lockCtrl[0]+'.Sub_Controller_Visibility', e=1, keyable=1)

    cmds.connectAttr(lockCtrl[0]+'.Sub_Controller_Visibility', ribbonCtrls1[-1]+'.visibility')
    cmds.connectAttr(lockCtrl[0]+'.Sub_Controller_Visibility', ribbonCtrls2[0]+'.visibility')

    # cmds.parentConstraint(lockCtrl[0], lockGRP, mo=True)




    #++ Follow Codes Belongs Main ++#

    lockCtrlPos = getRoot(nodType='transform', sel=lockCtrl)
    cmds.parentConstraint(selectedIKMiddle, lockCtrlPos, mo=True)

    cmds.parentConstraint(selectedIKFirst, getRoot(nodType='transform', sel=ribbonCtrls1[0]))
    cmds.parentConstraint(selectedIKLast, getRoot(nodType='transform', sel=ribbonCtrls2[-1]))





    #:: Main classify ::#

    sideIKGRP = cmds.group(empty=True, w=True, n=sideGRPName+'_IK_GRP')
    ribbonCtrlPos1 = getRoot(nodType='transform', sel=ribbonCtrls1[0])
    ribbonCtrlPos2 = getRoot(nodType='transform', sel=ribbonCtrls1[1])
    ribbonCtrlPos4 = getRoot(nodType='transform', sel=ribbonCtrls2[-2])
    ribbonCtrlPos5 = getRoot(nodType='transform', sel=ribbonCtrls2[-1])


    sideBendctrlGRP = cmds.group(empty=True, w=True, n=sideGRPName+'_bend_ctrl_GRP')
    cmds.parent(ribbonCtrlPos2, ribbonCtrlPos4, sideBendctrlGRP)




    #++ Make IK controller ++# 

    wristIKsubCtrl = makeController(selectedIKLast, shape='star', addName='_sub', scale=0.8)
    wristIKmainCtrl = makeController(selectedIKLast, shape='star', addName='_main', scale=1.1)
    cmds.parent(getRoot(sel=wristIKsubCtrl, nodType='transform'), wristIKmainCtrl)

    shoulderIKCtrl = makeController(selectedIKFirst, shape='star')

    rpIKHandle = cmds.ikHandle(sj=selectedIKFirst, ee=selectedIKLast, sol='ikRPsolver', n=selectedName1+'_IK_handle')
    cmds.parent(rpIKHandle[0], wristIKsubCtrl)
    cmds.hide(rpIKHandle)

    controllerColor(shoulderIKCtrl, 'red')
    controllerColor(wristIKmainCtrl, 'red')
    controllerColor(wristIKsubCtrl, 'red')

    cmds.parent(getRoot(sel=wristIKmainCtrl, nodType='transform'), sideIKGRP)
    cmds.parent(getRoot(sel=shoulderIKCtrl, nodType='transform'), sideIKGRP)


    #++ make FK Controllers ++#

    shoulderFKctrl = makeController(selectedFKFirst, scale=1.2)
    controllerColor(shoulderFKctrl, 'yellow')
    shoulderFKctrlPos = getRoot(sel=shoulderFKctrl, nodType='transform')
    addCustomAttribute(shoulderFKctrl)
    cmds.addAttr(shoulderFKctrl, ln='stretch', nn='stretch', at='float', minValue=0, defaultValue=1)
    cmds.setAttr(shoulderFKctrl[0]+'.stretch', e=1, keyable=1)

    elbowFKctrl = makeController(selectedFKMiddle, scale=1.2)
    controllerColor(elbowFKctrl, 'yellow')
    elbowFKctrlPos = getRoot(sel=elbowFKctrl, nodType='transform')
    addCustomAttribute(elbowFKctrl)
    cmds.addAttr(elbowFKctrl, ln='stretch', nn='stretch', at='float', minValue=0, defaultValue=1)
    cmds.setAttr(elbowFKctrl[0]+'.stretch', e=1, keyable=1)

    wristFKctrl = makeController(selectedFKLast, scale=1.2)
    controllerColor(wristFKctrl, 'yellow')
    wristFKctrlPos = getRoot(sel=wristFKctrl, nodType='transform')

    sideFKGRP = cmds.group(empty=True, w=True, n=sideGRPName+'_FK_GRP')
    cmds.parent(shoulderFKctrlPos, elbowFKctrlPos, wristFKctrlPos, sideFKGRP)


    #++ make fk connections ++#

    cmds.parentConstraint(selectedFKMiddle, lockCtrlPos, mo=True) 
    cmds.parentConstraint(selectedFKLast, ribbonCtrlPos5, mo=True)
    cmds.parentConstraint(selectedFKFirst, ribbonCtrlPos1, mo=True)

    cmds.parentConstraint(selectedIKMiddle, rollElbowGRP, mo=True)
    cmds.parentConstraint(selectedFKMiddle, rollElbowGRP, mo=True)

    cmds.parentConstraint(shoulderFKctrl, selectedFKFirst, mo=True)
    cmds.orientConstraint(elbowFKctrl, selectedFKMiddle)

    cmds.pointConstraint(selectedFKLast, cmds.listRelatives(wristFKctrl, p=True)[0], mo=True)
    cmds.pointConstraint(selectedFKMiddle, cmds.listRelatives(elbowFKctrl, p=True)[0])

    #* fk shoulder controller drives elbow controller GRP by orient Constraining
    cmds.orientConstraint(shoulderFKctrl, cmds.listRelatives(elbowFKctrl, p=True)[0], mo=True)
    cmds.orientConstraint(elbowFKctrl, cmds.listRelatives(wristFKctrl, p=True)[0], mo=True)

    #* fk shoulder and elbow stretch connections
    cmds.connectAttr(shoulderFKctrl[0]+'.stretch', selectedFKFirst+'.scaleX')
    cmds.connectAttr(elbowFKctrl[0]+'.stretch', selectedFKMiddle+'.scaleX')


    #++ hands and finger setUp ++#
    wristRootJNT = selectedName3+'_root_joint'
    wristRootGRP = makeOwnGRP(wristRootJNT, style='GRP')
    cmds.parent(wristRootGRP, 'joint_GRP')
    cmds.pointConstraint(selectedIKLast, wristRootGRP, mo=True)
    cmds.pointConstraint(selectedFKLast, wristRootGRP, mo=True)


    #++ Set Orientation Buffer Locators ++#
    ikWristLoc = cmds.spaceLocator(n=selectedName3+'_ik_loc')
    aligner(ikWristLoc, wristIKsubCtrl, Const='parent')
    cmds.parent(ikWristLoc, wristIKsubCtrl)

    fkWristLoc = cmds.spaceLocator(n=selectedName3+'_fk_loc')
    aligner(fkWristLoc, wristFKctrl, Const='parent')
    cmds.parent(fkWristLoc, wristFKctrl)

    cmds.orientConstraint(ikWristLoc, fkWristLoc, wristRootGRP, mo=True)




    #++ pole Vector Controller ++#

    polVecCtrl = makeController(selectedIKMiddle, addName='_poleVector', shape='cube', scale=1.1)
    controllerColor(polVecCtrl, 'pink')
    poleVecPoly = cmds.polyCreateFacet(p=[cmds.xform(selectedIKFirst, q=True, t=True, ws=True), cmds.xform(selectedIKMiddle, q=True, t=True, ws=True), 
                            cmds.xform(selectedIKLast, q=True, t=True, ws=True)], ch=True, tx=1, n='poleVecPoly')

    cmds.select(cl=True)
    poleVtx = '{0}.vtx[1]'.format(poleVecPoly[0])
    poleVecPos = getRoot(sel=polVecCtrl, nodType='transform')
    cmds.normalConstraint(poleVtx, poleVecPos)

    cmds.delete(poleVecPoly)
    cmds.poleVectorConstraint(polVecCtrl, rpIKHandle[0])

    cmds.parent(poleVecPos, sideIKGRP)




    def fingerSetUp(side, sidectrlGRP):        

        #++ make FK finger Controllers ++#
        fingerFKJNTLists = cmds.ls('finger_*'+side+'*_FK_joint', type='joint')
        fingerFKJNTLists = list(filter(lambda x: 'end' not in x, fingerFKJNTLists)) #* or -> [f for f in fingerFKJNTLists if '_end_' not in f]

        fingerAllCtrlLists = makeController(selec=fingerFKJNTLists, scale=0.3)

        for i in fingerAllCtrlLists:
            controllerColor(i, 'yellow')

        for i in range(len(fingerFKJNTLists)):
            cmds.parentConstraint(fingerAllCtrlLists[i], fingerFKJNTLists[i], mo=True)

        #* separate finger Controller Lists by 3 then make child the later(-1) to the former(-2) 
        fingerCtrlLists = list(filter(lambda x: 'root' not in x and '0' not in x, fingerAllCtrlLists))
        fingerCtrlLists = [fingerCtrlLists[f:f+3] for f in range(0, len(fingerCtrlLists), 3)]

        cmds.parent(getRoot(sel=fingerCtrlLists[0][-1], nodType='transform'), fingerCtrlLists[0][-2])
        cmds.parent(getRoot(sel=fingerCtrlLists[0][-2], nodType='transform'), fingerCtrlLists[0][-3])

        cmds.parent(getRoot(sel=fingerCtrlLists[1][-1], nodType='transform'), fingerCtrlLists[1][-2])
        cmds.parent(getRoot(sel=fingerCtrlLists[1][-2], nodType='transform'), fingerCtrlLists[1][-3])

        cmds.parent(getRoot(sel=fingerCtrlLists[2][-1], nodType='transform'), fingerCtrlLists[2][-2])
        cmds.parent(getRoot(sel=fingerCtrlLists[2][-2], nodType='transform'), fingerCtrlLists[2][-3])

        cmds.parent(getRoot(sel=fingerCtrlLists[3][-1], nodType='transform'), fingerCtrlLists[3][-2])
        cmds.parent(getRoot(sel=fingerCtrlLists[3][-2], nodType='transform'), fingerCtrlLists[3][-3])

        cmds.parent(getRoot(sel=fingerCtrlLists[4][-1], nodType='transform'), fingerCtrlLists[4][-2])
        # cmds.parent(getRoot(sel=fingerCtrlLists[4][-2], nodType='transform'), fingerCtrlLists[4][-3])

        if filter(lambda x: '0' in x, fingerAllCtrlLists) is not 0:
            #fingerAllCtrlLists = [fingerAllCtrlLists[f:f+4] for f in range(0, len(fingerAllCtrlLists), 4)]
            cmds.parent(getRoot(sel=fingerCtrlLists[0][-3], nodType='transform'), fingerAllCtrlLists[0])
            cmds.parent(getRoot(sel=fingerCtrlLists[1][-3], nodType='transform'), fingerAllCtrlLists[4])
            cmds.parent(getRoot(sel=fingerCtrlLists[2][-3], nodType='transform'), fingerAllCtrlLists[8])
            cmds.parent(getRoot(sel=fingerCtrlLists[3][-3], nodType='transform'), fingerAllCtrlLists[13])
            cmds.parent(getRoot(sel=fingerCtrlLists[4][-2], nodType='transform'), fingerAllCtrlLists[18])
            if filter(lambda x: 'root' in x, fingerAllCtrlLists) is not 0:
                cmds.parent(getRoot(sel=fingerAllCtrlLists[8], nodType='transform'), fingerAllCtrlLists[12])
                cmds.parent(getRoot(sel=fingerAllCtrlLists[13], nodType='transform'), fingerAllCtrlLists[17])
                cmds.parent(getRoot(sel=fingerAllCtrlLists[12], nodType='transform'), fingerAllCtrlLists[17])
                
        fingerFKctrlGRP = cmds.group(empty=True, w=True, n='finger_FK_ctrl_GRP')
        aligner(fingerFKctrlGRP, wristRootJNT, Const='parent')

        if cmds.objExists('finger_'+side+'_ctrl_GRP') is False:
            fingerCtrlGRP = cmds.group(empty=True, w=True, n='finger_'+side+'_ctrl_GRP')
            aligner(fingerCtrlGRP, wristRootJNT, Const='parent')
        else: 
            fingerCtrlGRP = cmds.ls('finger_'+side+'_ctrl_GRP')[0]

        cmds.parent(getRoot(sel=fingerCtrlLists[0][0], nodType='transform'), fingerFKctrlGRP)
        cmds.parent(getRoot(sel=fingerCtrlLists[1][0], nodType='transform'), fingerFKctrlGRP)
        cmds.parent(getRoot(sel=fingerCtrlLists[2][0], nodType='transform'), fingerFKctrlGRP)
        # cmds.parent(getRoot(sel=fingerCtrlLists[3][0], nodType='transform'), fingerFKctrlGRP)
        cmds.parent(getRoot(sel=fingerCtrlLists[4][0], nodType='transform'), fingerFKctrlGRP)

        cmds.parent(fingerFKctrlGRP, fingerCtrlGRP)

        cmds.parentConstraint(wristRootJNT, fingerCtrlGRP, mo=True)


        #++ make IK finger Controllers ++#
        fingerIKJNTLists = cmds.ls('finger_*'+side+'*_IK_joint', type='joint')
        fingerIKJNTLists = [f for f in fingerIKJNTLists if '_0_' not in f]

        fingerIKJNTLists = [fingerIKJNTLists[f:f+4] for f in range(0, len(fingerIKJNTLists), 4)]

        fingerIKhandle1 = cmds.ikHandle(sj=fingerIKJNTLists[0][0], ee=fingerIKJNTLists[0][-1], solver='ikSCsolver', n=fingerIKJNTLists[0][0].split('_')[1]+side+'_IK_handle')
        fingerIKhandle2 = cmds.ikHandle(sj=fingerIKJNTLists[1][0], ee=fingerIKJNTLists[1][-1], solver='ikSCsolver', n=fingerIKJNTLists[1][0].split('_')[1]+side+'_IK_handle')
        fingerIKhandle3 = cmds.ikHandle(sj=fingerIKJNTLists[2][0], ee=fingerIKJNTLists[2][-1], solver='ikSCsolver', n=fingerIKJNTLists[2][0].split('_')[1]+side+'_IK_handle')
        fingerIKhandle4 = cmds.ikHandle(sj=fingerIKJNTLists[3][0], ee=fingerIKJNTLists[3][-1], solver='ikSCsolver', n=fingerIKJNTLists[3][0].split('_')[1]+side+'_IK_handle')
        fingerIKhandle5 = cmds.ikHandle(sj=fingerIKJNTLists[4][0], ee=fingerIKJNTLists[4][-1], solver='ikSCsolver', n=fingerIKJNTLists[4][0].split('_')[1]+side+'_IK_handle')

        cmds.hide(fingerIKhandle1[0])
        cmds.hide(fingerIKhandle2[0])
        cmds.hide(fingerIKhandle3[0])
        cmds.hide(fingerIKhandle4[0])
        cmds.hide(fingerIKhandle5[0])


        for i in range(0, 5):
            for j in range(len(fingerIKJNTLists[i])-1):
                cmds.connectAttr(fingerIKJNTLists[i][j]+'.rotate', cmds.listRelatives(fingerCtrlLists[i][j], p=True)[0]+'.rotate')

        fingerIKctrl1 = makeController(fingerIKJNTLists[0][-1], shape='cube', scale=0.6)
        controllerColor(fingerIKctrl1, 'red')
        fingerIKctrl2 = makeController(fingerIKJNTLists[1][-1], shape='cube', scale=0.6)
        controllerColor(fingerIKctrl2, 'red')
        fingerIKctrl3 = makeController(fingerIKJNTLists[2][-1], shape='cube', scale=0.6)
        controllerColor(fingerIKctrl3, 'red')
        fingerIKctrl4 = makeController(fingerIKJNTLists[3][-1], shape='cube', scale=0.6)
        controllerColor(fingerIKctrl4, 'red')
        fingerIKctrl5 = makeController(fingerIKJNTLists[4][-1], shape='cube', scale=0.6)
        controllerColor(fingerIKctrl5, 'red')

        cmds.parent(fingerIKhandle1[0], fingerIKctrl1)
        cmds.parent(fingerIKhandle2[0], fingerIKctrl2)
        cmds.parent(fingerIKhandle3[0], fingerIKctrl3)
        cmds.parent(fingerIKhandle4[0], fingerIKctrl4)
        cmds.parent(fingerIKhandle5[0], fingerIKctrl5)

        fingerIKctrlGRP = cmds.group(empty=True, w=True, n='finger_IK_ctrl_GRP')
        aligner(fingerIKctrlGRP, wristRootJNT, Const='parent')

        cmds.parent(getRoot(sel=fingerIKctrl1[0], nodType='transform'), fingerIKctrlGRP)
        cmds.parent(getRoot(sel=fingerIKctrl2[0], nodType='transform'), fingerIKctrlGRP)
        cmds.parent(getRoot(sel=fingerIKctrl3[0], nodType='transform'), fingerIKctrlGRP)
        cmds.parent(getRoot(sel=fingerIKctrl4[0], nodType='transform'), fingerIKctrlGRP)
        cmds.parent(getRoot(sel=fingerIKctrl5[0], nodType='transform'), fingerIKctrlGRP)

        cmds.parent(fingerIKctrlGRP, fingerCtrlGRP)
        cmds.parent(fingerCtrlGRP, sidectrlGRP)



    #++ make Twist SetUp ++# 
    twistJNT = cmds.duplicate(selecFirst, parentOnly=True, n=selectedName1+'_twist_joint')
    twistEndJNT = cmds.duplicate(selecSecond, parentOnly=True, n=selectedName1+'_twist_end_joint')
    twistRotJNT = cmds.duplicate(selecFirst, parentOnly=True, n=selectedName1+'_twist_rot_joint')

    cmds.parent(twistJNT, w=True)
    cmds.parent(twistEndJNT, twistJNT)
    upTwistJNTGRP = makeOwnGRP(twistJNT, style='GRP')


    upTwistikHandle = cmds.ikHandle(sj=twistJNT[0], ee=twistEndJNT[0], solver='ikRPsolver', n=twistJNT[0].replace('_joint', '_ik_handle'))
    upTwistikHandleGRP = makeOwnGRP(upTwistikHandle[0], style='GRP')
   
    cmds.setAttr(upTwistikHandle[0]+'.poleVectorX', 0)
    cmds.setAttr(upTwistikHandle[0]+'.poleVectorY', 0)
    cmds.setAttr(upTwistikHandle[0]+'.poleVectorZ', 0)

    cmds.pointConstraint(selectedIKFirst, upTwistJNTGRP, mo=True)
    cmds.pointConstraint(selectedFKFirst, upTwistJNTGRP, mo=True)
    cmds.pointConstraint(selectedIKMiddle, upTwistikHandleGRP, mo=True)
    cmds.pointConstraint(selectedFKMiddle, upTwistikHandleGRP, mo=True)

    cmds.parent(twistRotJNT, w=True)
    upTwistRotGRP = makeOwnGRP(twistRotJNT, style='GRP')
    cmds.parentConstraint(selectedIKFirst, upTwistRotGRP, mo=True)
    cmds.parentConstraint(selectedFKFirst, upTwistRotGRP, mo=True)
    cmds.orientConstraint(twistJNT, twistRotJNT, mo=True)

    uptwistMD = cmds.createNode('multiplyDivide', n=twistJNT[0]+'_MD')
    if side == 'R':
        cmds.setAttr(uptwistMD+'.input2X', 1)
    else:
        cmds.setAttr(uptwistMD+'.input2X', -1)
        
    cmds.connectAttr(twistRotJNT[0]+'.rotateX', uptwistMD+'.input1X')
    cmds.connectAttr(uptwistMD+'.outputX', selectedName1+'_spik_handle.twist')

    #* Make Wrist Twist SetUp from here
    wristTwistJNT = cmds.duplicate(wristRootJNT, po=True, n=wristRootJNT.replace('_root_joint', '_twist_root_joint'))
    wristTwistRotJNT = cmds.duplicate(wristRootJNT, po=True, n=wristRootJNT.replace('_root_joint', '_rot_joint'))
    wristTwistEndJNT = cmds.duplicate(wristRootJNT.replace('_root_joint', '_end_joint'), po=True, n=wristRootJNT.replace('_end_joint', '_twist_end_joint'))

    cmds.parent(wristTwistJNT, w=True)
    cmds.parent(wristTwistEndJNT, wristTwistJNT)

    lowTwistikHandle = cmds.ikHandle(sj=wristTwistJNT[0], ee=wristTwistEndJNT[0], solver='ikRPsolver', n=wristTwistJNT[0].replace('_root_joint', '_ik_handle'))
    cmds.setAttr(lowTwistikHandle[0]+'.poleVectorX', 0)
    cmds.setAttr(lowTwistikHandle[0]+'.poleVectorY', 0)
    cmds.setAttr(lowTwistikHandle[0]+'.poleVectorZ', 0)
    lowTwistikHandleGRP = makeOwnGRP(lowTwistikHandle[0], style='GRP')
    cmds.parentConstraint(wristIKsubCtrl, lowTwistikHandleGRP, mo=True)
    cmds.parentConstraint(wristFKctrl, lowTwistikHandleGRP, mo=True)

    wristTwistJNTGRP = makeOwnGRP(wristTwistJNT, style='GRP')
    wristTwistRotJNTGRP = makeOwnGRP(wristTwistRotJNT, style='GRP')
    cmds.pointConstraint(selectedIKLast, wristTwistJNTGRP, mo=True)
    cmds.pointConstraint(selectedFKLast, wristTwistJNTGRP, mo=True)
    cmds.parentConstraint(wristRootJNT, wristTwistRotJNTGRP, mo=True)
    cmds.orientConstraint(wristTwistJNT, wristTwistRotJNT, mo=True)

    lowtwistMD = cmds.createNode('multiplyDivide', n=wristTwistJNT[0]+'_MD')
    cmds.setAttr(lowtwistMD+'.input2X', -1)
    cmds.connectAttr(wristTwistRotJNT[0]+'.rotateX', lowtwistMD+'.input1X')
    cmds.connectAttr(lowtwistMD+'.outputX', selectedName2+'_spik_handle.twist')


    #* classify hierarchy and make lowArm fk controlls whole lowArmtwist System to prevent double transform 
    upJNTsGRP = cmds.group(empty=True, w=True, n=selectedName1+'_joint_GRP')
    lowJNTsGRP = cmds.group(empty=True, w=True, n=selectedName2+'_joint_GRP')
    aligner(lowJNTsGRP, selectedFKMiddle, Const='parent')


    cmds.parent(upTwistJNTGRP, upJNTsGRP)
    cmds.parent(upTwistRotGRP, upJNTsGRP)
    cmds.parent(rollShoulderGRP, upJNTsGRP)

    cmds.parent(rollElbowGRP, lowJNTsGRP)
    cmds.parent(wristTwistJNTGRP, lowJNTsGRP)
    cmds.parent(wristRootGRP, lowJNTsGRP)
    cmds.parent(wristTwistRotJNTGRP, lowJNTsGRP)

    cmds.parent(upJNTsGRP, skinJointGRP)
    cmds.parent(lowJNTsGRP, skinJointGRP)

    cmds.parentConstraint(selectedIKMiddle, lowJNTsGRP, mo=True)
    cmds.parentConstraint(selectedFKMiddle, lowJNTsGRP, mo=True)



    #++ make ik fk Switcher ++#

    ikfkSwitcher = makeController(selectedIKLast, shape='cube', addName='_FK_switch', scale=1.1)
    addCustomAttribute(ikfkSwitcher)
    cmds.addAttr(ikfkSwitcher, ln='IKFK', nn="IKFK", at="float", maxValue=1, minValue=0)
    cmds.setAttr(ikfkSwitcher[0]+'.IKFK', e=1, keyable=1)

    controllerColor(ikfkSwitcher, 'white')
    IKFKswitchREV = cmds.createNode('reverse', n='IKFKswitchREV')
    cmds.connectAttr('{0}.IKFK'.format(ikfkSwitcher[0]), '{0}.inputX'.format(IKFKswitchREV))

    #* ik - fk visibility 
    cmds.connectAttr('{0}.outputX'.format(IKFKswitchREV), '{0}.visibility'.format(sideIKGRP))
    cmds.connectAttr('{0}.outputX'.format(IKFKswitchREV), '{0}.visibility'.format(selectedIKFirst))
    cmds.connectAttr('{0}.IKFK'.format(ikfkSwitcher[0]), '{0}.visibility'.format(sideFKGRP))
    cmds.connectAttr('{0}.IKFK'.format(ikfkSwitcher[0]), '{0}.visibility'.format(selectedFKFirst))

    #* ik connections
    cmds.connectAttr(IKFKswitchREV+'.outputX', ribbonCtrlPos1+'_parentConstraint1.'+selectedIKFirst+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', lockCtrlPos+'_parentConstraint1.'+selectedIKMiddle+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', ribbonCtrlPos5+'_parentConstraint1.'+selectedIKLast+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', rollElbowGRP+'_parentConstraint1.'+selectedIKMiddle+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', wristRootGRP+'_orientConstraint1.'+ikWristLoc[0]+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', wristRootGRP+'_pointConstraint1.'+selectedIKLast+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', lowJNTsGRP+'_parentConstraint1.'+selectedIKMiddle+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', wristTwistJNTGRP+'_pointConstraint1.'+selectedIKLast+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', lowTwistikHandleGRP+'_parentConstraint1.'+wristIKsubCtrl[0]+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', upTwistJNTGRP+'_pointConstraint1.'+selectedIKFirst+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', upTwistikHandleGRP+'_pointConstraint1.'+selectedIKMiddle+'W0')
    cmds.connectAttr(IKFKswitchREV+'.outputX', upTwistRotGRP+'_parentConstraint1.'+selectedIKFirst+'W0')

    #* fk connections 
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', rollElbowGRP+'_parentConstraint1.'+selectedFKMiddle+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', ribbonCtrlPos1+'_parentConstraint1.'+selectedFKFirst+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', lockCtrlPos+'_parentConstraint1.'+selectedFKMiddle+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', ribbonCtrlPos5+'_parentConstraint1.'+selectedFKLast+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', wristRootGRP+'_orientConstraint1.'+fkWristLoc[0]+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', wristRootGRP+'_pointConstraint1.'+selectedFKLast+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', lowJNTsGRP+'_parentConstraint1.'+selectedFKMiddle+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', wristTwistJNTGRP+'_pointConstraint1.'+selectedFKLast+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', lowTwistikHandleGRP+'_parentConstraint1.'+wristFKctrl[0]+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', upTwistJNTGRP+'_pointConstraint1.'+selectedFKFirst+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', upTwistikHandleGRP+'_pointConstraint1.'+selectedFKMiddle+'W1')
    cmds.connectAttr(ikfkSwitcher[0]+'.IKFK', upTwistRotGRP+'_parentConstraint1.'+selectedFKFirst+'W1')





    #++ IK stretch SetUp ++#

    lenCRV = cmds.curve(d=1, 
            p=[cmds.xform(selectedIKFirst, query=True, t=True, ws=True), cmds.xform(selectedIKMiddle, query=True, t=True, ws=True), cmds.xform(selectedIKLast, query=True, t=True, ws=True)], 
            k=(0, 1, 2), n=selectedName1+'_arcLength_curve')


    cmds.select(clear=True)
    cmds.select(selectedIKFirst, r=True)
    cmds.select(selectedIKMiddle, selectedIKLast, add=True)
    cmds.select(lenCRV, add=True)
    arcLenSkinCluster = cmds.skinCluster(tsb=True, dr=4.0)
    cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[0]', transformValue=[(selectedIKFirst, 1)])
    cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[1]', transformValue=[(selectedIKMiddle, 1)])
    cmds.skinPercent(arcLenSkinCluster[0], lenCRV+'.cv[2]', transformValue=[(selectedIKLast, 1)])

    arcLen = cmds.arclen(lenCRV)
    distanceNode = cmds.createNode('distanceBetween', n=selectedIKFirst+'_DIST')
    cmds.connectAttr(shoulderIKCtrl[0]+'.worldMatrix', distanceNode+'.inMatrix1')
    cmds.connectAttr(wristIKsubCtrl[0]+'.worldMatrix', distanceNode+'.inMatrix2')

    distanceMD = cmds.createNode('multiplyDivide', n='stretchIK_Dist_MD')
    cmds.setAttr(distanceMD+'.operation', 2)
    cmds.connectAttr(distanceNode+'.distance', distanceMD+'.input1X')

    distanceCOND = cmds.createNode('condition', n='stretchIK_Dist_COND')
    cmds.setAttr(distanceCOND+'.operation', 2)
    cmds.connectAttr(distanceMD+'.outputX', distanceCOND+'.firstTerm')
    cmds.connectAttr(distanceMD+'.outputX', distanceCOND+'.colorIfTrueR')
    cmds.setAttr(distanceCOND+'.secondTerm', arcLen)
    cmds.setAttr(distanceCOND+'.colorIfFalseR', arcLen)

    distanceMD2 = cmds.createNode('multiplyDivide', n='stretchIK_Dist_MD2')
    cmds.setAttr(distanceMD2+'.operation', 2)
    cmds.setAttr(distanceMD2+'.input2X', arcLen)
    cmds.delete(lenCRV)


    #* Add ik stretch OnOff Attribute to ik wrist Controller 
    addCustomAttribute(wristIKmainCtrl)
    cmds.addAttr(wristIKmainCtrl[0], ln='Stretch_On_Off', nn="Stretch_On_Off", at="float", maxValue=1, minValue=0, defaultValue=0)
    cmds.addAttr(wristIKmainCtrl[0], ln='Up_Stretch', nn="Up_Stretch", at="float", minValue=0, defaultValue=1)
    cmds.addAttr(wristIKmainCtrl[0], ln='Low_Stretch', nn="Low_Stretch", at="float", minValue=0, defaultValue=1)
    cmds.setAttr(wristIKmainCtrl[0]+'.Stretch_On_Off', e=1, keyable=1)
    cmds.setAttr(wristIKmainCtrl[0]+'.Up_Stretch', e=1, keyable=1)
    cmds.setAttr(wristIKmainCtrl[0]+'.Low_Stretch', e=1, keyable=1)

    stretchBLND = cmds.createNode('blendColors', n='stretchIK_BLND')

    cmds.connectAttr(distanceCOND+'.outColorR', stretchBLND+'.color1R')
    cmds.setAttr(stretchBLND+'.color2R', arcLen)

    cmds.connectAttr(stretchBLND+'.outputR', distanceMD2+'.input1X')
    cmds.connectAttr(wristIKmainCtrl[0]+'.Stretch_On_Off', stretchBLND+'.blender')

    stretchUpMD = cmds.createNode('multiplyDivide', n='stretch_IK_Up_MD')
    stretchLowMD = cmds.createNode('multiplyDivide', n='stretch_IK_Low_MD')
    cmds.setAttr(stretchUpMD+'.operation', 1)
    cmds.setAttr(stretchLowMD+'.operation', 1)

    cmds.connectAttr(wristIKmainCtrl[0]+'.Up_Stretch', stretchUpMD+'.input1X')
    cmds.connectAttr(wristIKmainCtrl[0]+'.Low_Stretch', stretchLowMD+'.input1X')

    cmds.connectAttr(distanceMD2+'.outputX', stretchUpMD+'.input2X')
    cmds.connectAttr(distanceMD2+'.outputX', stretchLowMD+'.input2X')


    #* Now Connects to joint's scaleX
    cmds.connectAttr(stretchUpMD+'.outputX', selectedIKFirst+'.scaleX')
    cmds.connectAttr(stretchLowMD+'.outputX', selectedIKMiddle+'.scaleX')


    #* Add poleVector Twist Attribute
    addCustomAttribute(wristIKmainCtrl)
    cmds.addAttr(wristIKmainCtrl[0], ln='Twist', nn="Twist", at="float", defaultValue=0)
    cmds.setAttr(wristIKmainCtrl[0]+'.Twist', e=1, keyable=1)
    cmds.connectAttr(wristIKmainCtrl[0]+'.Twist', rpIKHandle[0]+'.twist')



    #++ later classify ++#

    if cmds.objExists('ctrl_GRP') is False:
        ctrlGRP = cmds.group(empty=True, w=True, n='ctrl_GRP')
        cmds.parent(ctrlGRP, globalGRP)
    else:
        ctrlGRP = cmds.ls('ctrl_GRP')[0]

    bendRootGRP = cmds.group(empty=True, w=True, n=sideGRPName+'_bend_root_GRP')
    sidectrlGRP = cmds.group(empty=True, w=True, n=sideGRPName+'_ctrl_GRP')
    sideTwistIKhandleGRP = cmds.group(empty=True, w=True, n=sideGRPName+'_twist_ik_handle_GRP')

    if cmds.objExists('twist_ik_handle_GRP') is False:
        twistIKhandleGRP = cmds.group(empty=True, w=True, n='twist_ik_handle_GRP')
        cmds.parent(twistIKhandleGRP, extras)
    else:
        twistIKhandleGRP = cmds.ls('twist_ik_handle_GRP')[0]


    if cmds.objExists('twist_ik_handle_GRP') is False:
        twistIKhandleGRP = cmds.group(empty=True, w=True, n='twist_ik_handle_GRP')
        cmds.parent(twistIKhandleGRP, extras)
    else:
        twistIKhandleGRP = cmds.ls('twist_ik_handle_GRP')[0]

    cmds.parent(sideGRPName+'_spik_GRP', 'spik_GRP')

    cmds.parent(lockGRP, lockCtrl)
    cmds.parent(ribbonCtrlPos5, ribbonCtrlPos1, bendRootGRP)
    cmds.parent(bendRootGRP, sideBendctrlGRP)

    cmds.parent(sideIKGRP, sideFKGRP, getRoot(nodType='transform', sel=ikfkSwitcher), sidectrlGRP)
    cmds.parent(sideBendctrlGRP, sidectrlGRP)
    cmds.parent(lockCtrlPos, sidectrlGRP)

    cmds.parent(sidectrlGRP, ctrlGRP)


    cmds.parent(upTwistikHandleGRP, sideTwistIKhandleGRP)
    cmds.parent(lowTwistikHandleGRP, sideTwistIKhandleGRP)
    cmds.parent(sideTwistIKhandleGRP, twistIKhandleGRP)




    #++ Do finger SetUp if finger exists ++#
    for i in cmds.listRelatives(wristRootJNT, children=True):
        if 'finger' == i.split('_')[0]:
            print('fingerGRP Found')
            fingerSetUp(side, sidectrlGRP)


def doLimbsSetUp():
    initialSelecList = cmds.ls(sl=True)

    for i in initialSelecList:
        limbsSetUp(i)
       

    #++ hide Extras ++#

    cmds.hide('Extras')




def doSpineSetUp():
    #++ Spine SetUp ++#

    waistJNTs = cmds.ls('waist_*')
    cmds.hide(waistJNTs)
    waistMidJNT = waistJNTs.pop(0)
    waistJNTs.insert(1, waistMidJNT)

    spineJNTs = cmds.ls('spine_*')
    chestJNTs = [f for f in cmds.ls('chest_*') if not '_IK_' in f]
    chestRootJNT = chestJNTs.pop(1)
    chestJNTs.insert(0, chestRootJNT)

    hipJNTs = cmds.ls('hip_*')[::-1]


    spineIKhandle = cmds.ikHandle(sj=spineJNTs[0], ee=spineJNTs[-1], sol='ikSplineSolver', pcv=False, ns=4, n='spine_spik_handle')
    spineIKCRV = cmds.rename(spineIKhandle[-1], 'spine_spik_curve')

    cmds.skinCluster(waistJNTs, spineIKCRV, toSelectedBones=True, dropoffRate=4.0)

    waistMidctrl = makeController(selec=waistJNTs[1], pointConst=True, normalPlane='xz')
    waistRootctrl = makeController(selec=waistJNTs[0], pointConst=True, normalPlane='xz')
    chestLowctrl = makeController(selec=waistJNTs[2], newName='chest_Low', pointConst=True, normalPlane='xz')
    hipctrl = makeController(selec=waistJNTs[0], shape='cube', newName='hip', scale=7, pointConst=True, normalPlane='xz')
    pelvisctrl = makeController(selec=waistJNTs[0], newName='pelvis', scale=3, pointConst=True, normalPlane='xz')
    chestUpctrl = makeController(selec=chestJNTs[1], newName='chest_Up', pointConst=True, normalPlane='xz')
    waistIKctrl = makeController(selec=waistJNTs[1], shape='cross', addName='_IK', pointConst=True, scale=6, parent=True, normalPlane='xz')
    waistIKctrlGRP = getRoot(sel=waistIKctrl, nodType='transform')
    controllerColor(waistIKctrl, color='red')
    controllerColor(pelvisctrl, color='blue')
    controllerColor(hipctrl, color='yellow')
    controllerColor(waistRootctrl, color='default')
    controllerColor(waistMidctrl, color='default')
    controllerColor(chestLowctrl, color='default')
    controllerColor(chestUpctrl, color='default')


    cmds.parentConstraint(waistJNTs[0], waistJNTs[2], waistIKctrlGRP, mo=True)
    cmds.parent(waistIKctrlGRP, waistMidctrl)
    cmds.parent(getRoot(sel=chestLowctrl, nodType='transform'), waistMidctrl)
    cmds.parent(getRoot(sel=waistMidctrl, nodType='transform'), waistRootctrl)

    cmds.parent(waistJNTs[2], chestLowctrl)
    cmds.parent(getRoot(sel=chestUpctrl, nodType='transform'), chestLowctrl)

    waistRootJNT_GRP = cmds.group(empty=True, w=True, n=waistJNTs[0]+'_GRP')
    waistRootJNT_Pos = makeOwnGRP(waistRootJNT_GRP, style='Pos')
    aligner(waistRootJNT_Pos, waistJNTs[0], Const='point')
    cmds.connectAttr(waistRootctrl[0]+'.translate', waistRootJNT_GRP+'.translate')
    cmds.connectAttr(waistRootctrl[0]+'.rotate', waistRootJNT_GRP+'.rotate')
    cmds.parent(waistJNTs[0], waistRootJNT_GRP)
    cmds.parent(waistRootJNT_Pos, hipctrl)

    cmds.parentConstraint(hipctrl, hipJNTs[0], mo=True)


    #* Add hip rotation offset Attribute to hip controller 
    addCustomAttribute(hipctrl)
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
    cmds.parent(getRoot(sel=waistRootctrl, nodType='transform'), pelvisctrl)
    cmds.parent(getRoot(sel=hipctrl, nodType='transform'), pelvisctrl)

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


    #* reverse Twist SetUp 




#++ set all constraints .interpType to 2 
allOrientList = cmds.ls('*orientConstraint1')
allParentList = cmds.ls('*parentConstraint1')

for o in allOrientList:
    cmds.setAttr('{0}.interpType'.format(o), 2)
for p in allParentList:
    cmds.setAttr('{0}.interpType'.format(p), 2)
 
 
#++ progressBar ++#

