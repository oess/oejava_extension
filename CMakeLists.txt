cmake_minimum_required(VERSION 2.8.9)
project(OpenEye-java-extension)
ENABLE_TESTING()

set (OE_JAVA_DIR ${CMAKE_SOURCE_DIR}/)

# Find needed SWIG and java stuff
include (FindJava)
find_package(JNI REQUIRED)
find_package(SWIG REQUIRED VERSION 3.0.2 HINT ${HINTPATH})
include(${SWIG_USE_FILE})

include_directories(${JAVA_INCLUDE_PATH})
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/openeye/toolkits/include)

# macro for registering OpenEye shared libraries with CMake so we can link against them
macro( add_openeye_libraries )
  foreach ( libname ${ARGN} )
    if ( NOT TARGET ${libname} )
      add_library ( ${libname} SHARED IMPORTED )
      set_target_properties ( ${libname} PROPERTIES IMPORTED_LOCATION 
        ${OE_JAVA_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${CMAKE_SHARED_LIBRARY_SUFFIX} )
    endif()
  endforeach ( libname )
endmacro( add_openeye_libraries )

# Then find all the shared libraries
set (CMAKE_SHARED_LIBRARY_SUFFIX "jnilib")

set (OE_JAVA_LIB_DIR ${OE_JAVA_DIR}/openeye/native-libs/MacOSX-x64/)
file(GLOB oe_shared_libs "${OE_JAVA_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}*${CMAKE_SHARED_LIBRARY_SUFFIX}")
message("oe_shared_libs = ${oe_shared_libs}")

foreach(fullpathname ${oe_shared_libs})
  message("fullpathname = ${fullpathname}")
  # extract the shared library name including version number
  get_filename_component(sharedlibname "${fullpathname}" NAME)
  string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_SUFFIX}" "" sharedlibname "${sharedlibname}")
  string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_PREFIX}" "" sharedlibname "${sharedlibname}")

  # strip the version number
  string(REGEX REPLACE "-java-.*" "" libname "${sharedlibname}")
  message("libname = ${libname}")
  set ( ${libname}_AND_SHARED_DEP_LIBS ${sharedlibname})

  # register the shared libraries with CMake
  add_openeye_libraries ( ${${libname}_AND_SHARED_DEP_LIBS} )
endforeach(fullpathname)

# Project specific stuff
set(EXAMPLE_SRC 
    molwt.cpp)

message("oechem_AND_SHARED_DEP_LIBS = ${oechem_AND_SHARED_DEP_LIBS}")

set_source_files_properties(example.i PROPERTIES CPLUSPLUS ON)
swig_add_module(example java example.i ${EXAMPLE_SRC})
swig_link_libraries(example 
                    ${JAVA_LIBRARIES} 
                    ${oechem_AND_SHARED_DEP_LIBS})

add_test(ExampleCalcMolWt env JAVAPATH=${OE_JAVA_DIR}:${CMAKE_BUILD_DIR} ${JAVA_EXECUTABLE} ${CMAKE_SOURCE_DIR}/molwt.py )