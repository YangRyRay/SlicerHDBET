cmake_minimum_required(VERSION 3.13.4)

project(HDBET)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/YangRyRay/SlicerHDBET/")
set(EXTENSION_CATEGORY "Segmentation")
set(EXTENSION_CONTRIBUTORS "Raymond Yang (University of Massachusetts Boston), Lorainne Franke (University of Massachusetts Boston), Steve Pieper (Isomics Inc.), Daniel Haehn (University of Massachusetts Boston), Lipeng Ning (Brigham and Women's Hospital)")
set(EXTENSION_DESCRIPTION "This extension provides a CNN based Brain extracting tool for MRI scans. This is an adaptation of the HD-BET tool by the Department of Neuroradiology at the Heidelberg University Hospital and the Division of Medical Image Computing at the German Cancer Research Center.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/HDBET.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/HDBET/Screenshots/1.png")
set(EXTENSION_DEPENDS "PyTorch") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(HDBET)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
