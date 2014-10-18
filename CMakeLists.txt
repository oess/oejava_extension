cmake_minimum_required(VERSION 2.8.9)
project(OpenEye-python-extension)
ENABLE_TESTING()

set (OE_PYTHON_DIR ${CMAKE_SOURCE_DIR}/OpenEye-python2.7-osx-10.8-x64-2014.10.2)

# Figure out our architecture
execute_process(COMMAND ${PYTHON_EXECUTABLE} 
                        ${OE_PYTHON_DIR}/openeye/libs/getarch.py --pythonlibs
                OUTPUT_STRIP_TRAILING_WHITESPACE
                OUTPUT_VARIABLE PY_ARCH)

set (OE_PYTHON_LIB_DIR ${OE_PYTHON_DIR}/openeye/libs/${PY_ARCH}/)

# hack for now... figure out how to call gen_cmake_shared_library_deps.py automagically later
include(${CMAKE_SOURCE_DIR}/OELibs.cmake)

# Find SWIG and the python stuff it needs
find_package(SWIG REQUIRED VERSION 3.0.2 HINT ${HINTPATH})
include(${SWIG_USE_FILE})
include_directories(${OE_PYTHON_DIR}/extension)
include_directories(${OE_PYTHON_DIR}/openeye/include)

# Project specific stuff
set(EXAMPLE_SRC 
    molwt.cpp)

set_source_files_properties(example.i PROPERTIES CPLUSPLUS ON)
swig_add_module(example python example.i ${EXAMPLE_SRC})
swig_link_libraries(example 
                    ${PYTHON_LIBRARIES} 
                    ${oechem_AND_SHARED_DEP_LIBS})
