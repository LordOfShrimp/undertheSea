import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import ikRibbon
import bipedFootSetUP
import quadRig

def window():

    window_widget = omui.MQtUtil.mainWindow()
    return wrapInstance(long(window_widget), QtWidgets.QWidget)

class SetReady(QtWidgets.QDialog):

    def __init__(self, parent=window()):
        super(SetReady, self).__init__(parent)
        


    def create(self):
        self.setWindowTitle("Auto Rigging Tool ")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 550)

        self.functions()
        self.layouts()
        self.connection()


    def functions(self):
        self.information = QtWidgets.QLabel("\n\n   Biped & Quadruped Auto Rigging Tool \n   v.01  \n\n   Yeon Kim \n   @ March 2019 \n\n")
        self.loadReadySetBtn = QtWidgets.QPushButton("     Load Initial Human Joint Set     ")
        self.loadReadySetBtn.setStyleSheet("background-color: rgb(70, 70, 70)")

        self.leftArmJNTBtn = QtWidgets.QPushButton("Left Arm Joint")
        self.leftArmJNTBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.leftArmJNTLabel = QtWidgets.QLabel(":NULL")

        self.rightArmJNTBtn = QtWidgets.QPushButton("Right Arm Joint")
        self.rightArmJNTBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.rightArmJNTLabel = QtWidgets.QLabel(":NULL")

        self.leftLegJNTBtn = QtWidgets.QPushButton("Left Leg Joint")
        self.leftLegJNTBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.leftLegJNTLabel = QtWidgets.QLabel(":NULL")

        self.rightLegJNTBtn = QtWidgets.QPushButton("Right Leg Joint")
        self.rightLegJNTBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.rightLegJNTLabel = QtWidgets.QLabel(":NULL")

        self.armQuickRollBtn = QtWidgets.QPushButton("    Make Roll Joints    ")
        self.armQuickRollBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.legQuickRollBtn = QtWidgets.QPushButton("    Make Roll Joints    ")
        self.legQuickRollBtn.setStyleSheet("background-color: rgb(70, 70, 70)")

        self.armProxyCubeBtn = QtWidgets.QPushButton("Make Proxy Cubes")
        self.armProxyCubeBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.armRemvProxyCubeBtn = QtWidgets.QPushButton("Delete Proxy Cubes")
        self.armRemvProxyCubeBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.legProxyCubeBtn = QtWidgets.QPushButton("Make Proxy Cubes")
        self.legProxyCubeBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.legRemvProxyCubeBtn = QtWidgets.QPushButton("Delete Proxy Cubes")
        self.legRemvProxyCubeBtn.setStyleSheet("background-color: rgb(70, 70, 70)")

        self.armNumLabel = QtWidgets.QLabel("Rolls : ")
        self.armNumSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.armNumSlider.setMinimum(2)
        self.armNumSlider.setMaximum(30)
        self.armNumSlider.setValue(15)
        self.armNumSlider.setSingleStep(1)
        self.armNumSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.armSliderValue = QtWidgets.QLabel("15")

        self.legNumLabel = QtWidgets.QLabel("Rolls : ")
        self.legNumSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.legNumSlider.setMinimum(2)
        self.legNumSlider.setMaximum(30)
        self.legNumSlider.setValue(15)
        self.legNumSlider.setSingleStep(1)
        self.legNumSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.legSliderValue = QtWidgets.QLabel("15")

        self.rigIcon1 = QtWidgets.QLabel("")
        pixmap1 = QtGui.QPixmap('C:/Users/Ana/Documents/maya/2018/scripts/autorig/test3.jpg')
        self.rigIcon1.setPixmap(pixmap1)

        self.rigIcon2 = QtWidgets.QLabel("")
        pixmap2 = QtGui.QPixmap('C:/Users/Ana/Documents/maya/2018/scripts/autorig/test2.jpg')
        self.rigIcon2.setPixmap(pixmap2)

        self.lArmCBox = QtWidgets.QCheckBox("   Left Arm   ")
        self.rArmCBox = QtWidgets.QCheckBox("   Right Arm   ")
        self.lLegCBox = QtWidgets.QCheckBox("   Left Leg   ")
        self.rLegCBox = QtWidgets.QCheckBox("   Right Leg   ")
        self.spineCBox = QtWidgets.QCheckBox("   Spine   ")
        self.neckCBox = QtWidgets.QCheckBox("   Neck   ")
        self.lFootCBox = QtWidgets.QCheckBox("   Left Foot   ")
        self.rFootCBox = QtWidgets.QCheckBox("   Right Foot   ")


        self.doRig = QtWidgets.QPushButton("    Do Rig    ")
        self.doRig.setStyleSheet("background-color: rgb(60, 60, 60)")
        
        self.loadQuadReadySetBtn = QtWidgets.QPushButton("     Load Initial Dog Joint Set     ")
        self.loadQuadReadySetBtn.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.foreQuadLegCBox = QtWidgets.QCheckBox("   Fore Leg   ")
        self.rearQuadLegCBox = QtWidgets.QCheckBox("   Rear Leg   ")
        self.quadNeckCBox = QtWidgets.QCheckBox("    Neck    ")
        self.quadTailCBox = QtWidgets.QCheckBox("    Tail    ")
        self.quadSpineCBox = QtWidgets.QCheckBox("   Spine   ")
        self.quadRig = QtWidgets.QPushButton("    Do Quad Rig    ")
        self.quadRig.setStyleSheet("background-color: rgb(60, 60, 60)")
 

    def layouts(self):
        initLayout = QtWidgets.QVBoxLayout()
        initLayout.setContentsMargins(2,2,2,15)
        initLayout.addWidget(self.information)
        initLayout.addWidget(self.loadReadySetBtn)
        initLayout.addWidget(self.loadQuadReadySetBtn)


        lArmJNTLayout = QtWidgets.QHBoxLayout()
        lArmJNTLayout.setContentsMargins(0,0,0,0)
        lArmJNTLayout.addWidget(self.leftArmJNTBtn)
        lArmJNTLayout.addWidget(self.leftArmJNTLabel)

        rArmJNTLayout = QtWidgets.QHBoxLayout()
        rArmJNTLayout.setContentsMargins(0,0,0,0)
        rArmJNTLayout.addWidget(self.rightArmJNTBtn)
        rArmJNTLayout.addWidget(self.rightArmJNTLabel)

        armSliderLayout = QtWidgets.QHBoxLayout()
        armSliderLayout.setContentsMargins(0,0,0,0)
        armSliderLayout.addWidget(self.armSliderValue)
        armSliderLayout.addWidget(self.armNumSlider)

        armProxyLayout = QtWidgets.QHBoxLayout()
        armProxyLayout.addWidget(self.armProxyCubeBtn)
        armProxyLayout.addWidget(self.armRemvProxyCubeBtn)

        armLayout = QtWidgets.QVBoxLayout()
        armLayout.addLayout(lArmJNTLayout)
        armLayout.addLayout(rArmJNTLayout)
        armLayout.addWidget(self.armQuickRollBtn)
        armLayout.addWidget(self.armNumLabel)
        armLayout.addLayout(armSliderLayout)
        armLayout.addLayout(armProxyLayout)
        

        lLegJNTLayout = QtWidgets.QHBoxLayout()
        lLegJNTLayout.setContentsMargins(0,0,0,0)
        lLegJNTLayout.addWidget(self.leftLegJNTBtn)
        lLegJNTLayout.addWidget(self.leftLegJNTLabel)

        rLegJNTLayout = QtWidgets.QHBoxLayout()
        rLegJNTLayout.setContentsMargins(0,0,0,0)
        rLegJNTLayout.addWidget(self.rightLegJNTBtn)
        rLegJNTLayout.addWidget(self.rightLegJNTLabel)

        legSliderLayout = QtWidgets.QHBoxLayout()
        legSliderLayout.setContentsMargins(0,0,0,0)
        legSliderLayout.addWidget(self.legSliderValue)
        legSliderLayout.addWidget(self.legNumSlider)

        legProxyLayout = QtWidgets.QHBoxLayout()
        legProxyLayout.addWidget(self.legProxyCubeBtn)
        legProxyLayout.addWidget(self.legRemvProxyCubeBtn)

        legLayout = QtWidgets.QVBoxLayout()
        legLayout.addLayout(lLegJNTLayout)
        legLayout.addLayout(rLegJNTLayout)
        legLayout.addWidget(self.legQuickRollBtn)
        legLayout.addWidget(self.legNumLabel)
        legLayout.addLayout(legSliderLayout)
        legLayout.addLayout(legProxyLayout)

        armCheckBoxLayout = QtWidgets.QHBoxLayout()
        armCheckBoxLayout.addWidget(self.lArmCBox)
        armCheckBoxLayout.addWidget(self.rArmCBox)
        

        legCheckBoxLayout = QtWidgets.QHBoxLayout()
        legCheckBoxLayout.addWidget(self.lLegCBox)
        legCheckBoxLayout.addWidget(self.rLegCBox)

        footCheckBoxLayout = QtWidgets.QHBoxLayout()
        footCheckBoxLayout.addWidget(self.lFootCBox)
        footCheckBoxLayout.addWidget(self.rFootCBox)

        spineCheckBoxLayout = QtWidgets.QHBoxLayout()
        spineCheckBoxLayout.addWidget(self.spineCBox)
        spineCheckBoxLayout.addWidget(self.neckCBox)


        autoRigLayout = QtWidgets.QVBoxLayout()
        autoRigLayout.addLayout(armCheckBoxLayout)
        autoRigLayout.addLayout(legCheckBoxLayout)
        autoRigLayout.addLayout(footCheckBoxLayout)
        autoRigLayout.addLayout(spineCheckBoxLayout)
        autoRigLayout.addWidget(self.doRig)

        tempLayout = QtWidgets.QVBoxLayout()
        tempLayout.addWidget(self.rigIcon2)

        dynamicLayout = QtWidgets.QVBoxLayout()
        # dynamicLayout.addWidget(self.rigIcon2)

        legQuadCheckBoxLayout = QtWidgets.QHBoxLayout()
        legQuadCheckBoxLayout.addWidget(self.foreQuadLegCBox)
        legQuadCheckBoxLayout.addWidget(self.rearQuadLegCBox)

        spineQuadCheckBoxLayout = QtWidgets.QHBoxLayout()
        spineQuadCheckBoxLayout.addWidget(self.quadSpineCBox)
        spineQuadCheckBoxLayout.addWidget(self.quadTailCBox)


        quadruLayout = QtWidgets.QVBoxLayout()
        quadruLayout.addLayout(legQuadCheckBoxLayout)
        quadruLayout.addLayout(spineQuadCheckBoxLayout)
        quadruLayout.addWidget(self.quadRig)

        armWidget = QtWidgets.QWidget()
        armWidget.setLayout(armLayout)
        legWidget = QtWidgets.QWidget()
        legWidget.setLayout(legLayout)
        initWidget = QtWidgets.QWidget()
        initWidget.setLayout(initLayout)

        autoRigWidget = QtWidgets.QWidget()
        autoRigWidget.setLayout(autoRigLayout)

        tempWidget = QtWidgets.QWidget()
        tempWidget.setLayout(tempLayout)

        dynamicWidget = QtWidgets.QWidget()
        dynamicWidget.setLayout(dynamicLayout)

        quadruWidget = QtWidgets.QWidget()
        quadruWidget.setLayout(quadruLayout)

        self.limbsToolBox = QtWidgets.QToolBox()
        self.limbsToolBox.addItem(initWidget, 'INFO ')
        self.limbsToolBox.addItem(armWidget, 'Make Arm Roll Joints')
        self.limbsToolBox.addItem(legWidget, 'Make Leg Roll Joints')
        self.limbsToolBox.addItem(autoRigWidget, 'Biped SetUP')
        self.limbsToolBox.addItem(dynamicWidget, 'Dynamic SetUP')
        self.limbsToolBox.addItem(quadruWidget, 'Quadruped SetUP')
        # self.limbsToolBox.addItem(tempWidget, 'Temp ..')
        

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(30,30,30,70)
        mainLayout.addLayout(initLayout)
        mainLayout.addWidget(self.limbsToolBox)

        mainLayout.addStretch()
        
        self.setLayout(mainLayout)


    def connection(self):
        self.loadReadySetBtn.clicked.connect(self.loadReadySet)        

        self.leftArmJNTBtn.clicked.connect(self.lArmUpDateLabel)
        self.rightArmJNTBtn.clicked.connect(self.rArmUpDateLabel)
        
        self.leftLegJNTBtn.clicked.connect(self.lLegUpDateLabel)
        self.rightLegJNTBtn.clicked.connect(self.rLegUpDateLabel)

        self.armQuickRollBtn.clicked.connect(self.makeArmRollsPre)
        self.armNumSlider.valueChanged.connect(self.armSliderValue.setNum)
        self.armNumSlider.valueChanged.connect(self.makeArmRollsPre)

        self.legQuickRollBtn.clicked.connect(self.makeLegRollsPre)
        self.legNumSlider.valueChanged.connect(self.legSliderValue.setNum)
        self.legNumSlider.valueChanged.connect(self.makeLegRollsPre)

        self.lArmCBox.toggled.connect(self.isCBoxToggled)
        self.rArmCBox.toggled.connect(self.isCBoxToggled)
        self.lLegCBox.toggled.connect(self.isCBoxToggled)
        self.rLegCBox.toggled.connect(self.isCBoxToggled)
        self.spineCBox.toggled.connect(self.isCBoxToggled)
        self.neckCBox.toggled.connect(self.isCBoxToggled)

        self.doRig.clicked.connect(self.doRigPre)


        #* dog Rig from here
        self.loadQuadReadySetBtn.clicked.connect(self.loadQaudReadySet)
        self.quadRig.clicked.connect(self.doQuadRigPre)




    def loadReadySet(self):
        cmds.file( 'D:/_Working3D/_Projects/Rigging Studies/AutoRig/CapUltraJointReadySet.ma', i=True, usingNamespaces=False )


    def loadQaudReadySet(self):
        cmds.file('D:/_Working3D/_Projects/Rigging Studies/Dog Rig/readySetTest.ma', i=True, usingNamespaces=False)


    def lArmUpDateLabel(self):        
        self.leftArmJNTLabel.setText(cmds.ls(sl=True)[0])
        self.currentinitJNT = self.leftArmJNTLabel.text()

    def rArmUpDateLabel(self):        
        self.rightArmJNTLabel.setText(cmds.ls(sl=True)[0])
        self.currentinitJNT = self.rightArmJNTLabel.text()

    def lLegUpDateLabel(self):        
        self.leftLegJNTLabel.setText(cmds.ls(sl=True)[0])
        self.currentinitJNT = self.leftLegJNTLabel.text()

    def rLegUpDateLabel(self):        
        self.rightLegJNTLabel.setText(cmds.ls(sl=True)[0])
        self.currentinitJNT = self.rightLegJNTLabel.text()


#!!!!!!!!!!!!!!!
        # self.make_proxy.clicked.connect(self.makeProxy)     

    def makeArmRollsPre(self):
        lArmJNTL = self.leftArmJNTLabel.text()
        if lArmJNTL != ':NULL':
            lArmJNTList = cmds.listRelatives(lArmJNTL, c=True)
            lArmJNTList.insert(0, lArmJNTL)
            self.makeRolls(lArmJNTList[0], 'arm')
            self.makeRolls(lArmJNTList[1], 'arm')

        rArmJNTL = self.rightArmJNTLabel.text()
        if rArmJNTL != ':NULL':
            rArmJNTList = cmds.listRelatives(rArmJNTL, c=True)
            rArmJNTList.insert(0, rArmJNTL)
            self.makeRolls(rArmJNTList[0], 'arm')
            self.makeRolls(rArmJNTList[1], 'arm')

    def makeLegRollsPre(self):
        lLegJNT = self.leftLegJNTLabel.text()
        if lLegJNT != ':NULL':
            lLegJNTList = cmds.listRelatives(lLegJNT, c=True, ad=True)
            lLegJNTList.reverse()
            lLegJNTList.insert(0, lLegJNT)
            for i in range(len(lLegJNTList)-1):
                self.makeRolls(lLegJNTList[i], 'leg')

        rLegJNT = self.rightLegJNTLabel.text()
        if rLegJNT != ':NULL':
            rLegJNTList = cmds.listRelatives(rLegJNT, c=True, ad=True)
            rLegJNTList.reverse()
            rLegJNTList.insert(0, rLegJNT)
            for i in range(len(rLegJNTList)-1):
                self.makeRolls(rLegJNTList[i], 'leg')




    def makeRolls(self, initJNT, limb):

        if limb == 'arm':
            num = int(self.armNumSlider.value())
        elif limb == 'leg':
            num = int(self.legNumSlider.value())
        cmds.showHidden(initJNT)    

        rollJNTQuery = initJNT.replace('_joint', '_roll_1_skin_joint')
        if cmds.objExists(rollJNTQuery) is True:
            # print("RollJNT Already Exists ! ")
            cmds.delete(rollJNTQuery)
    
        dupJNTList = cmds.duplicate(initJNT, renameChildren=True)
        
        if len(dupJNTList) == 3:
            cmds.delete(dupJNTList[-1])
            dupJNTList.pop()
        elif len(dupJNTList) == 4:
            cmds.delete(dupJNTList[-2])
            dupJNTList.pop()
            dupJNTList.pop()

        dis = cmds.getAttr(str(dupJNTList[1])+'.translateX')
        posX = dis/num
    
        cmds.select(dupJNTList[0], r=True)
        jointList = [cmds.joint(p=(posX, 0, 0), r=True) for j in range(num-1)]

        jointList.insert(0, dupJNTList[0])
        jointList.append(dupJNTList[1])

        cmds.parent(jointList[-1], jointList[-2])
        cmds.parent(jointList[0], w=True)
        
        cmds.hide(initJNT)

        self.renamer(jointList)



    def renamer(self, jointList):
        getName = jointList[0].replace('_joint1', '_roll_')
        for count in range(len(jointList)-1):
            cmds.rename(jointList[count], getName + str(count+1) + '_skin_joint')
        cmds.rename(jointList[-1], getName + 'end' + '_joint')
        cmds.parent(jointList[0].replace('_joint1', '_roll_1_skin_joint'), 'limbs_joint_GRP')


    def makeProxy(self):
        sel = cmds.ls(sl=1)
        proxyCubes = []
        for i in sel:
            cube = cmds.polyCube()
            proxyCubes.append(cube[0])
            cmds.select(i, replace=True)
            cmds.select(cube, add=True)
            cmds.parentConstraint(weight = True)
        print(proxyCubes)
        cmds.select(proxyCubes, r=True)
        cmds.group(n='proxyCube_GRP')
            
            
    def isCBoxToggled(self):
        sender = self.sender()
        
    
    def doRigPre(self):
        if self.lArmCBox.isChecked() == True:
            cmds.select(cl=True)
            cmds.select(self.leftArmJNTLabel.text(), r=True)
            ikRibbon.doLimbsSetUp()

        if self.rArmCBox.isChecked() == True:
            cmds.select(cl=True)
            cmds.select(self.rightArmJNTLabel.text(), r=True)
            ikRibbon.doLimbsSetUp()

        if self.lLegCBox.isChecked() == True:
            cmds.select(cl=True)
            cmds.select(self.leftLegJNTLabel.text(), r=True)
            ikRibbon.doLimbsSetUp()

        if self.rLegCBox.isChecked() == True:
            cmds.select(cl=True)
            cmds.select(self.rightLegJNTLabel.text(), r=True)
            ikRibbon.doLimbsSetUp()

        if self.spineCBox.isChecked() == True:
            cmds.select(cl=True)
            ikRibbon.doSpineSetUp()

        # self.neckCBox.isChecked()

        if self.lFootCBox.isChecked() == True:
            cmds.select(cl=True)
            bipedFootSetUP.Foot(self.leftLegJNTLabel.text())

        if self.rFootCBox.isChecked() == True:
            cmds.select(cl=True)
            bipedFootSetUP.Foot(self.rightLegJNTLabel.text())


    def doQuadRigPre(self):
        if self.quadSpineCBox.isChecked() == True:
            quad = quadRig.SpineSetUP()
            quad.doSpineSetUp()

        if self.rearQuadLegCBox.isChecked() == True:
            quadLeftLeg = quadRig.LegSetUP(self.leftLegJNTLabel.text())
            quadLeftLeg.fire()
            quadRightLeg = quadRig.LegSetUP(self.rightLegJNTLabel.text())
            quadRightLeg.fire()

        if self.rearQuadLegCBox.isChecked() == True:
            quadLeftArm = quadRig.LegSetUP(self.leftArmJNTLabel.text())
            quadLeftArm.fire()
            quadRightArm = quadRig.LegSetUP(self.rightArmJNTLabel.text())
            quadRightArm.fire()

        if self.quadTailCBox.isChecked() == True:
            pass





    def doQuadRig(self):
        pass

    def doQuadLegRig(self):
        pass










ui = SetReady()
ui.create()
ui.show()