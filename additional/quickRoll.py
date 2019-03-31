import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance


def window():

    window_widget = omui.MQtUtil.mainWindow()
    return wrapInstance(long(window_widget), QtWidgets.QWidget)

class QuickRoll(QtWidgets.QDialog):

    def __init__(self, parent=window()):
        super(QuickRoll, self).__init__(parent)


    def create(self):
        self.setWindowTitle("QuickRoll")
        self.setWindowFlags(QtCore.Qt.Tool)

        self.functions()
        self.layouts()
        self.connections()

    def functions(self):
        
        self.num_label = QtWidgets.QLabel("Divide by")
        self.num_line = QtWidgets.QLineEdit("")
        self.make_roll = QtWidgets.QPushButton("Make Rolls")
        self.rename_label = QtWidgets.QLabel("Rename")
        self.rename_line = QtWidgets.QLineEdit("")
        self.proxy_label = QtWidgets.QLabel("Select every Joints \nyou want to attach proxy to")
        self.make_proxy = QtWidgets.QPushButton("Make Proxy Cubes")
        self.divide_line = QtWidgets.QSplitter()


    def layouts(self):
        numLayout = QtWidgets.QHBoxLayout()
        numLayout.addWidget(self.num_label)
        numLayout.addWidget(self.num_line)
        numLayout.setContentsMargins(2,2,2,2)
        nameLayout = QtWidgets.QHBoxLayout()
        nameLayout.addWidget(self.rename_label)
        nameLayout.addWidget(self.rename_line)
        

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(4,4,4,4)
        mainLayout.addLayout(numLayout)
        mainLayout.addLayout(nameLayout)
        mainLayout.addWidget(self.make_roll)
        mainLayout.addWidget(self.divide_line)
        mainLayout.addWidget(self.proxy_label)
        mainLayout.addWidget(self.make_proxy)
        mainLayout.addStretch()
        
        self.setLayout(mainLayout)


    def connections(self):

        self.make_roll.clicked.connect(self.makeRolls)
        self.make_proxy.clicked.connect(self.makeProxy)


    def makeRolls(self):  
        try:
            num = int(self.num_line.text())          
            sel = cmds.ls(sl=True)
            dis = cmds.getAttr(str(sel[1])+'.translateX')

            posX = dis/num
            cmds.select(sel[0], r=True)
            jointList = [cmds.joint(p=(posX, 0, 0), r=True) for j in range(num-1)]

            jointList.insert(0, sel[0])
            jointList.append(sel[1])

            cmds.parent(jointList[-1], jointList[-2])

            if len(self.rename_line.text()) != 0:
                self.renamer(jointList)
        except:
            if len(self.num_line.text()) == 0 or self.num_line.text() == 1:
                cmds.confirmDialog(title='Warning', message="Put an integer number greater than one", button=['Ok'], defaultButton='Ok')
                raise ValueError("Put an integer number greater than one")
            else:
                cmds.confirmDialog(title='Warning', message="Must select two joints in the same hierarchy", button=['Ok'], defaultButton='Ok')
                raise IndexError("Select Start and End joints")
            


    def renamer(self, jointList):
        getName = self.rename_line.text()+'_'
        for count in range(len(jointList)-1):
            cmds.rename(jointList[count], getName + str(count+1) + '_skin_joint')
        cmds.rename(jointList[-1], getName + 'end' + '_joint')

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
            


ui = QuickRoll()
ui.create()
ui.show()


