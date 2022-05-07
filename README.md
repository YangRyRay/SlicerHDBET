# SlicerHDBET

This is the code for 'HDBET' extension on [3D Slicer](https://www.slicer.org/), based on [HD-BET](https://github.com/MIC-DKFZ/HD-BET). The main function is to predict and extract the brain from an MRI

![Screenshot of Extracted Brain](https://raw.githubusercontent.com/YangRyRay/SlicerHDBET/master/BrainSeg.png)

# Tutorial
Download [3D Slicer](https://www.slicer.org/) and the install the HD_BET Extension from the Extension Manager.

Load your MRI data to Slicer. This can be done with the Load Data option. You can also download a sample MRI scan from the Download Sample Data option.

Once data is loaded, navigate to the module.

The module has a menu of options to select before applying. First, select the MRI scan to be applied with the MRML Volume dropdown menu. The output node with the extracted brain is called \[MRMLNode\]\_BET by default. This can be modified in the text window. Similarly, if the Save Mask option is selected, the output node with the brain mask is called \[MRMLNode\]\_MASK by default. This can be modified in the text window. Please see [HD-BET](https://github.com/MIC-DKFZ/HD-BET) for the other settings.

Once settings are selected, hit apply and the segmentation will start. Depending on the settings selected and the hardware available, this could take several minutes. Once complete, the output node will be displayed on the 3d render view. 

## References
Isensee F, Schell M, Tursunova I, Brugnara G, Bonekamp D, Neuberger U, Wick A, Schlemmer HP, Heiland S, Wick W, Bendszus M, Maier-Hein KH, Kickingereder P. Automated brain extraction of multi-sequence MRI using artificial neural networks. Hum Brain Mapp. 2019; 1–13. https://doi.org/10.1002/hbm.24750
