cmake_minimum_required(VERSION 3.13.4)

project(HDBET)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/YangRyRay/SlicerHDBET/")
set(EXTENSION_CATEGORY "Segmentation")
set(EXTENSION_CONTRIBUTORS "")
set(EXTENSION_DESCRIPTION "Brain Masking using CNN")
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
