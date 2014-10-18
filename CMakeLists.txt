cmake_minimum_required(VERSION 2.8.9)
project(OpenEye-python-extension)
ENABLE_TESTING()

set (OE_PYTHON_DIR ${CMAKE_SOURCE_DIR}/OpenEye-python2.7-osx-10.8-x64-2014.10.2)

# Find needed SWIG and python stuff
find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(SWIG REQUIRED VERSION 3.0.2 HINT ${HINTPATH})
include(${SWIG_USE_FILE})
include_directories(${PYTHON_INCLUDE_DIR})
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/openeye/toolkits/include)

# macro for registering OpenEye shared libraries with CMake so we can link against them
macro( add_openeye_libraries )
  foreach ( libname ${ARGN} )
    if ( NOT TARGET ${libname} )
      add_library ( ${libname} SHARED IMPORTED )
      set_target_properties ( ${libname} PROPERTIES IMPORTED_LOCATION 
        ${OE_PYTHON_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${CMAKE_SHARED_LIBRARY_SUFFIX} )
    endif()
  endforeach ( libname )
endmacro( add_openeye_libraries )

# Figure out our architecture
execute_process(COMMAND ${PYTHON_EXECUTABLE} 
                        ${OE_PYTHON_DIR}/openeye/libs/getarch.py --pythonlibs
                OUTPUT_STRIP_TRAILING_WHITESPACE
                OUTPUT_VARIABLE PY_ARCH)

# Then find all the shared libraries
set (OE_PYTHON_LIB_DIR ${OE_PYTHON_DIR}/openeye/libs/${PY_ARCH}/)
file(GLOB oe_shared_libs "${OE_PYTHON_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}*${CMAKE_SHARED_LIBRARY_SUFFIX}")
foreach(fullpathname ${oe_shared_libs})
  # extract the shared library name including version number
  get_filename_component(sharedlibname "${fullpathname}" NAME)
  string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_SUFFIX}" "" sharedlibname "${sharedlibname}")
  string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_PREFIX}" "" sharedlibname "${sharedlibname}")

  # strip the version number
  string(REGEX REPLACE "-[0-9].[0-9].[0-9]" "" libname "${sharedlibname}")
  set ( ${libname}_AND_SHARED_DEP_LIBS ${sharedlibname})

  # register the shared libraries with CMake
  add_openeye_libraries ( ${${libname}_AND_SHARED_DEP_LIBS} )
endforeach(fullpathname)


# Project specific stuff
set(EXAMPLE_SRC 
    molwt.cpp)

set_source_files_properties(example.i PROPERTIES CPLUSPLUS ON)
swig_add_module(example python example.i ${EXAMPLE_SRC})
swig_link_libraries(example 
                    ${PYTHON_LIBRARIES} 
                    ${oechem_AND_SHARED_DEP_LIBS})

add_test(ExampleCalcMolWt env PYTHONPATH=${OE_PYTHON_DIR}:${CMAKE_BUILD_DIR} ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/molwt.py )