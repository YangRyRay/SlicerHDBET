import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *


#
# MyMod
#

class MyMod(ScriptedLoadableModule):

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "MyMod"
        self.parent.categories = ["Def Testing"]
        self.parent.dependencies = []
        self.parent.contributors = ["For Testing"]
        self.parent.helpText = """Testing of created modules help"""
        self.parent.acknowledgementText = """Testing of created modules ack"""


#
# MyModWidget
#

class MyModWidget(ScriptedLoadableModuleWidget):
    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.logic = None
        self._parameterNode = None
        self._updatingGUIFromParameterNode = False

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # GUI
        collapsibleGB = ctk.ctkCollapsibleGroupBox()
        self.layout.addWidget(collapsibleGB)

        # new layout for collpsible button
        self.formLayout = qt.QFormLayout(collapsibleGB)

        ############
        # First input volume selector
        #
        self.inputSelector1 = slicer.qMRMLNodeComboBox()
        self.inputSelector1.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
        self.inputSelector1.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", 0)
        self.inputSelector1.selectNodeUponCreation = True
        self.inputSelector1.addEnabled = False
        self.inputSelector1.removeEnabled = False
        self.inputSelector1.noneEnabled = False
        self.inputSelector1.showHidden = False
        self.inputSelector1.showChildNodeTypes = False
        self.inputSelector1.setMRMLScene(slicer.mrmlScene)
        self.inputSelector1.setToolTip("Select Volume to filter")
        self.formLayout.addRow("MRML Volume: ", self.inputSelector1)

        # Dial selection for percent
        self.hiPassSel = qt.QDial()
        self.hiPassSel.setMinimum(0)
        self.hiPassSel.setMaximum(100)
        self.hiPassSel.toolTip = "Converts voxels less than __% of the maximum voxel value into minimum values (Can filter again with a higher percent, but need to reset data in order to filter with lower percent)"
        self.hiPassSel.setNotchesVisible(True)
        self.formLayout.addRow(self.hiPassSel)


        # Apply Button
        #
        self.applyButton = qt.QPushButton("Select percent of voxels to highpass WRT max val using above dial, then click here")
        self.applyButton.toolTip = "Converts voxels less than __% of the maximum voxel value into minimum values (Can filter again with a higher percent, but need to reset data in order to filter with lower percent)"
        self.applyButton.enabled = True
        self.formLayout.addRow(self.applyButton)


        self.textfield = qt.QTextEdit()
        self.textfield.setReadOnly(True)
        self.formLayout.addRow(self.textfield)
        # connections
        self.hiPassSel.valueChanged.connect(self.onDialChange)
        self.applyButton.clicked.connect(self.onApplyButton)

    def cleanup(self):
        """
    Called when the application closes and the module widget is destroyed.
    """
        print('Closed Mod')
        #self.removeObservers()

    def onDialChange(self):
        try:
            self.textfield.undo()
            self.textfield.insertPlainText(str(self.hiPassSel.value)+ '%')

        except Exception as e:
            slicer.util.errorDisplay("Failed to compute results: " + str(e))
            import traceback
            traceback.print_exc()

    def onApplyButton(self):
        try:
            self.textfield.undo()
            self.textfield.insertPlainText("Applied")
            name = self.inputSelector1.currentNode().GetName()
            n = slicer.util.getNode(name)
            a = slicer.util.array(name)
            a[a < self.hiPassSel.value*max(a.flatten())/100] = min(a.flatten())
            slicer.util.arrayFromVolumeModified(n)

        except Exception as e:
            slicer.util.errorDisplay("Failed to compute results: " + str(e))
            import traceback
            traceback.print_exc()
#
# MyModLogic
#
class MyModLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
    def __init__(self):
        ScriptedLoadableModuleLogic.__init__(self)
