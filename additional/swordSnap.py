import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

def aligner(driven, driver, Const=False):

    cmds.select(driver, r=1)
    cmds.select(driven, add=1)

    if Const == 'parent':
        cmds.delete(cmds.parentConstraint(mo=False, sr="none", st="none"))
    elif Const == 'orient':
        cmds.delete(cmds.orientConstraint(mo=False))
    elif Const == 'point':
        cmds.delete(cmds.pointConstraint(mo=False))


def window():

    window_widget = omui.MQtUtil.mainWindow()
    return wrapInstance(long(window_widget), QtWidgets.QWidget)

class SwordSnap(QtWidgets.QDialog):

    def __init__(self, parent=window()):
        super(SwordSnap, self).__init__(parent)


    def create(self):
        self.setWindowTitle("SNAP")
        self.setWindowFlags(QtCore.Qt.Tool)

        self.functions()
        self.layouts()
        self.connections()

    def functions(self):

        self.getSelect = QtWidgets.QPushButton("  Select  ")
        self.snapCopy = QtWidgets.QPushButton("   COPY   ")
        self.snapPaste = QtWidgets.QPushButton("   PASTE   ")


    def layouts(self):
      

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(20, 10, 20, 20)
        mainLayout.addWidget(self.getSelect)
        mainLayout.addWidget(self.snapCopy)
        mainLayout.addWidget(self.snapPaste)

        mainLayout.addStretch()
        
        self.setLayout(mainLayout)


    def connections(self):
        self.getSelect.clicked.connect(self.selectCtrl)
        self.snapCopy.clicked.connect(self.defSnapCopy)
        self.snapPaste.clicked.connect(self.defSnapPaste)

    def selectCtrl(self):
        self.selected = cmds.ls(sl=True)[0]

    def defSnapCopy(self):
        self.tempNode = cmds.group(n=self.selected+'_temp', w=True, empty=True)
        aligner(self.tempNode, self.selected, Const='parent')
        cmds.select(self.selected, r=True)


    def defSnapPaste(self):
        aligner(self.selected, self.tempNode, Const='parent')
        cmds.delete(self.tempNode)






ui = SwordSnap()
ui.create()
ui.show()




