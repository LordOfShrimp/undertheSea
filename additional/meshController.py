import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance



def window():

    window_widget = omui.MQtUtil.mainWindow()
    return wrapInstance(long(window_widget), QtWidgets.QWidget)

class MeshController(QtWidgets.QDialog):

    def __init__(self, parent=window()):
        super(MeshController, self).__init__(parent)


    def create(self):
        self.setWindowTitle("Auto Mesh Controller")
        self.setWindowFlags(QtCore.Qt.Tool)

        self.functions()
        self.layouts()
        self.connections()

    def functions(self):

        self.getPartsBTN = QtWidgets.QPushButton("     Get Parts    ")
        self.getCtrlBTN = QtWidgets.QPushButton("   Get Controller   :")
        self.ctrlLabel = QtWidgets.QLabel("                               ")
        self.makeMeshCtrlBTN = QtWidgets.QPushButton("   Make Mesh Controller   ")


    def layouts(self):
      
        getCtrlLayout = QtWidgets.QHBoxLayout()
        getCtrlLayout.setContentsMargins(0, 0, 0, 0)
        getCtrlLayout.addWidget(self.getCtrlBTN)
        getCtrlLayout.addWidget(self.ctrlLabel)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.addLayout(getCtrlLayout)
        mainLayout.addWidget(self.getPartsBTN)
        mainLayout.addWidget(self.makeMeshCtrlBTN)

        mainLayout.addStretch()
        
        self.setLayout(mainLayout)


    def connections(self):
        self.getPartsBTN.clicked.connect(self.getParts)
        self.getCtrlBTN.clicked.connect(self.ctrlUpDateLabel)
        self.makeMeshCtrlBTN.clicked.connect(self.makeMeshCtrl)


    def getParts(self):
        self.selectedFaces = cmds.ls(sl=True)
        print(self.selectedFaces)
        self.initialMesh = self.selectedFaces[0].split('.')[0]
        print(self.initialMesh)


    def ctrlUpDateLabel(self):        
        self.ctrlLabel.setText(cmds.ls(sl=True)[0])
        self.selectedCtrl = self.ctrlLabel.text()
        self.newCtrlName = self.selectedCtrl.replace('_ctrl', '_meshCtrl')


    def makeMeshCtrl(self):
        newMesh = cmds.duplicate(self.initialMesh, n=self.newCtrlName)[0]
        newMeshParts = [item.replace(self.initialMesh, newMesh) for item in self.selectedFaces]
        print(newMesh)
        print(newMeshParts)
        cmds.setAttr(newMesh+'.tx', lock=False)
        cmds.setAttr(newMesh+'.ty', lock=False)
        cmds.setAttr(newMesh+'.tz', lock=False)
        cmds.setAttr(newMesh+'.rx', lock=False)
        cmds.setAttr(newMesh+'.ry', lock=False)
        cmds.setAttr(newMesh+'.rz', lock=False)
        cmds.setAttr(newMesh+'.sx', lock=False)
        cmds.setAttr(newMesh+'.sy', lock=False)
        cmds.setAttr(newMesh+'.sz', lock=False)
        cmds.editDisplayLayerMembers('defaultLayer', newMesh, noRecurse=True)

        newMeshShape = cmds.listRelatives(newMesh, shapes=True)[0]
        oldMeshShape = cmds.listRelatives(self.initialMesh, shapes=True)[0]
        ctrlShape = cmds.listRelatives(self.selectedCtrl, shapes=True)[0]

        cmds.connectAttr(oldMeshShape+'.outMesh', newMeshShape+'.inMesh')

        cmds.parent(newMesh, self.selectedCtrl)
        cmds.makeIdentity(newMesh, apply=True, r=True, t=True, s=True)
        cmds.select(newMesh+'.f[*]', r=True)
        cmds.select(newMeshParts, tgl=True)
        cmds.delete()

        cmds.select(cl=True)

        cmds.parent(newMeshShape, self.selectedCtrl, shape=True, relative=True)

        newMeshHistory = cmds.listHistory(newMeshShape)
        for item in newMeshHistory:
            if cmds.nodeType(item) == 'transformGeometry':
                transGeoNode = item

        cmds.setAttr(transGeoNode+'.invertTransform', 1)
        cmds.connectAttr(self.selectedCtrl+'.worldMatrix', transGeoNode+'.transform')
        cmds.delete(newMesh)

        cmds.hide(ctrlShape)
        cmds.select(cl=True)







ui = MeshController()
ui.create()
ui.show()




