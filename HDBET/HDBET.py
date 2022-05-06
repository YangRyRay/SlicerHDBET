import os
import qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from Lib.run import run_hd_bet
from Lib.utils import maybe_mkdir_p, subfiles

#
# HDBET
#

class HDBET(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "HD-BET"
        self.parent.categories = ["Masking"]
        self.parent.dependencies = []
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]
        self.parent.helpText = """ Module masks out brain from MRI scans"""
        self.parent.acknowledgementText = """Isensee F, Schell M, Tursunova I, Brugnara G, Bonekamp D, Neuberger U, Wick A, Schlemmer HP, Heiland S, Wick W,"
           "Bendszus M, Maier-Hein KH, Kickingereder P. Automated brain extraction of multi-sequence MRI using artificial"
           "neural networks. arXiv preprint arXiv:1901.11341, 2019. """


#
# HDBETWidget
#

class HDBETWidget(ScriptedLoadableModuleWidget):
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

        # new layout for collapsible button
        self.formLayout = qt.QFormLayout(collapsibleGB)

        ############
        # Input volume selector
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

        # Select Output Node Name
        self.NOutName = qt.QLineEdit(self.inputSelector1.currentNode().GetName()+"_BET")
        self.formLayout.addRow("Enter Output Name:", self.NOutName)

        # Select processor
        self.procSelector = qt.QComboBox()
        self.procSelector.addItem("cpu")
        self.procSelector.addItem("gpu")
        self.procSelector.setToolTip("Select which device to predict with")
        self.formLayout.addRow("Select device:", self.procSelector)

        # Select mode
        self.modeSelector = qt.QComboBox()
        self.modeSelector.addItem("accurate")
        self.modeSelector.addItem("fast")
        self.modeSelector.setToolTip("Select which mode to predict with")
        self.formLayout.addRow("Select prediction mode:", self.modeSelector)

        # Select TTA
        self.ttaSelector = qt.QComboBox()
        self.ttaSelector.addItem("1")
        self.ttaSelector.addItem("0")
        self.ttaSelector.setToolTip("Switch to 0 for faster processing with CPU")
        self.formLayout.addRow("Select TTA:", self.ttaSelector)

        # Select PostProcessing
        self.ppSelector = qt.QComboBox()
        self.ppSelector.addItem("1")
        self.ppSelector.addItem("0")
        self.ppSelector.setToolTip("Switch to 0 for faster processing with CPU")
        self.formLayout.addRow("Select Post Processing:", self.ppSelector)

        # Select Overwrite
        self.oSelector = qt.QComboBox()
        self.oSelector.addItem("1")
        self.oSelector.addItem("0")
        self.oSelector.setToolTip("Switch to 0 for faster processing with CPU")
        self.formLayout.addRow("Overwrite existing predictions:", self.oSelector)

        # Select save mask
        self.sSelector = qt.QComboBox()
        self.sSelector.addItem("1")
        self.sSelector.addItem("0")
        self.sSelector.setToolTip("Switch to 0 for faster processing with CPU")
        self.formLayout.addRow("Save Mask:", self.sSelector)

        # Select Output Node Name
        self.MOutName = qt.QLineEdit(self.inputSelector1.currentNode().GetName() + "_Mask")
        self.formLayout.addRow("Enter Mask Name:", self.MOutName)

        # Apply Button
        self.applyButton = qt.QPushButton("Apply")
        self.applyButton.toolTip = "Run Brain Masking"
        self.applyButton.enabled = True
        self.formLayout.addRow(self.applyButton)

        # connections
        self.applyButton.clicked.connect(self.onApplyButton)
        self.inputSelector1.currentNodeChanged.connect(self.onNewNode)
        self.sSelector.currentTextChanged.connect(self.onSChange)


    def cleanup(self):
        """
        Called when the application closes and the module widget is destroyed.
        """
        print('Closed Mod')
        # self.removeObservers()

    def onNewNode(self):
        self.NOutName.clear()
        self.NOutName.insert(self.inputSelector1.currentNode().GetName()+"_BET")
        self.MOutName.clear()
        self.MOutName.insert(self.inputSelector1.currentNode().GetName() + "_Mask")

    def onSChange(self):
        if int(self.sSelector.currentText) == 0: self.MOutName.setVisible(False)
        else: self.MOutName.setVisible(True)

    def onApplyButton(self):
        try:
            input_file_or_dir = self.inputSelector1.currentNode().GetName()
            output_file_or_dir = self.NOutName.text


            if output_file_or_dir.strip() is "":
                output_file_or_dir = self.inputSelector1.currentNode().GetName()+"_BET"


            mode = self.modeSelector.currentText
            device = self.procSelector.currentText
            tta = int(self.ttaSelector.currentText)
            pp = int(self.ppSelector.currentText)
            overwrite_existing = int(self.oSelector.currentText)
            save_mask = int(self.sSelector.currentText)
            mask_file = self.MOutName.text

            if device == "gpu":
                device = 0

            params_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_final.py")
            config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Lib/config.py")

            if os.path.isdir(input_file_or_dir):
                maybe_mkdir_p(output_file_or_dir)
                input_files = subfiles(input_file_or_dir, suffix='.nii.gz', join=False)

                if len(input_files) == 0:
                    raise RuntimeError("input is a folder but no nifti files (.nii.gz) were found in here")

                output_files = [os.path.join(output_file_or_dir, i) for i in input_files]
                input_files = [os.path.join(input_file_or_dir, i) for i in input_files]
            else:
                if not output_file_or_dir.endswith('.nii.gz'):
                    # output_file_or_dir += '.nii.gz'
                    assert os.path.abspath(input_file_or_dir) != os.path.abspath(
                        output_file_or_dir), "output must be different from input"

                output_files = [output_file_or_dir]
                input_files = [input_file_or_dir]

            if tta == 0:
                tta = False
            elif tta == 1:
                tta = True
            else:
                raise ValueError("Unknown value for tta: %s. Expected: 0 or 1" % str(tta))

            if overwrite_existing == 0:
                overwrite_existing = False
            elif overwrite_existing == 1:
                overwrite_existing = True
            else:
                raise ValueError("Unknown value for overwrite_existing: %s. Expected: 0 or 1" % str(overwrite_existing))

            if pp == 0:
                pp = False
            elif pp == 1:
                pp = True
            else:
                raise ValueError("Unknown value for pp: %s. Expected: 0 or 1" % str(pp))

            if save_mask == 0:
                save_mask = False
            elif save_mask == 1:
                save_mask = True
            else:
                raise ValueError("Unknown value for save mask: %s. Expected: 0 or 1" % str(pp))

            from Lib.paths import folder_with_parameter_files

            run_hd_bet(input_files, output_files, mask_file, mode, config_file, device, pp, tta, save_mask, overwrite_existing)


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
