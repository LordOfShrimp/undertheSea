import maya.cmds as cmds


#++ make Mirror ++#
def mirror():
    selecList = cmds.ls(sl=True)
    otherSide = []
    for i, sel in enumerate(selecList):
        if 'L_' in sel:
            otherSide.append(sel.replace('L_', 'R_'))
        elif 'R_' in sel:
            otherSide.append(sel.replace('R_', 'L_'))       
        else:
            break
        rot = cmds.xform(selecList[i], query=True, ro=True, r=True)
        cmds.xform(otherSide[i], ro=rot)
        aPos = cmds.xform(selecList[i], query=True, a=True, t=True)
        cmds.xform(otherSide[i], a=True, t=aPos)

#++ make Initialize ++#
def initialize():
    selecList = cmds.ls(sl=True)
    for sel in selecList:
        cmds.xform(sel, ro=(0, 0, 0))
        cmds.xform(sel, t=(0, 0, 0))

def initializeAll():
    if cmds.objExists('*ctr') is True:
        selecList = cmds.ls('*ctr')
    else:
        selecList = cmds.ls('*ctrl')
    for sel in selecList:
        cmds.xform(sel, ro=(0, 0, 0))
        cmds.xform(sel, t=(0, 0, 0))

