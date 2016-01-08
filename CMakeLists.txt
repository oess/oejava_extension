cmake_minimum_required(VERSION 2.8.9)
project(OpenEye-java-extension)
ENABLE_TESTING()

set (OE_JAVA_DIR ${CMAKE_SOURCE_DIR})

# Find needed SWIG and java stuff
include (FindJava)
find_package(JNI REQUIRED)
find_package(SWIG REQUIRED VERSION 3.0.2 HINT ${HINTPATH})
include(${SWIG_USE_FILE})

include_directories(${JAVA_INCLUDE_PATH})
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/openeye/toolkits/include)

# macro for registering OpenEye shared libraries with CMake so we can link against them
macro( add_openeye_library libname fullpath)
  if ( NOT TARGET ${libname} )
    add_library ( ${libname} SHARED IMPORTED )
    set_target_properties ( ${libname} PROPERTIES IMPORTED_LOCATION ${fullpath})
  endif()
endmacro( add_openeye_library )

# Then find all the shared libraries
set (CMAKE_SHARED_LIBRARY_SUFFIX "jnilib")
set (CMAKE_CXX_FLAGS "-stdlib=libstdc++")
set (CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -unexported_symbols_list ${PROJECT_SOURCE_DIR}/etc/javanew.unexport")

set (OE_JAVA_LIB_DIR ${OE_JAVA_DIR}/openeye/native-libs/MacOSX-x64)
file(GLOB oe_shared_libs "${OE_JAVA_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}*${CMAKE_SHARED_LIBRARY_SUFFIX}")

foreach(fullpathname ${oe_shared_libs})
  if (NOT fullpathname MATCHES "-jni.jnilib")
    # extract the shared library name including version number
    get_filename_component(sharedlibname "${fullpathname}" NAME)
    string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_SUFFIX}" "" sharedlibname "${sharedlibname}")
    string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_PREFIX}" "" sharedlibname "${sharedlibname}")

    # strip the version number
    string(REGEX REPLACE "-java-.*" "" libname "${sharedlibname}")
    message("${libname} = ${fullpathname}")
    # register the shared libraries with CMake
    add_openeye_library(${libname} ${fullpathname})

    execute_process(
      COMMAND ${CMAKE_SOURCE_DIR}/extract_dependencies.py ${fullpathname}
      OUTPUT_STRIP_TRAILING_WHITESPACE
      OUTPUT_VARIABLE dependencies)

    set ( ${libname}_AND_SHARED_DEP_LIBS ${dependencies})
    message("${libname}_AND_SHARED_DEP_LIBS = ${${libname}_AND_SHARED_DEP_LIBS}")
  endif(NOT fullpathname MATCHES "-jni.jnilib")
endforeach(fullpathname)

# Project specific stuff
set(EXAMPLE_SRC
  molwt.cpp
  javanew.cpp)

message("oechem_AND_SHARED_DEP_LIBS = ${oechem_AND_SHARED_DEP_LIBS}")

set_source_files_properties(example.i PROPERTIES CPLUSPLUS ON)
swig_add_module(example java example.i ${EXAMPLE_SRC})
swig_link_libraries(example 
                    ${JAVA_LIBRARIES} 
                    ${oechem_AND_SHARED_DEP_LIBS})

add_custom_command(OUTPUT example.class
  DEPENDS example
  COMMAND ${Java_JAVAC_EXECUTABLE} example.java)

add_custom_target(example_java ALL
  DEPENDS example.class)

add_custom_command(OUTPUT MolWT.class
  DEPENDS example_java
  COMMAND ${Java_JAVAC_EXECUTABLE} -cp . MolWT.java)

add_custom_target(MolWT_java ALL
  DEPENDS MolWT.class)

add_test(ExampleCalcMolWt ${Java_JAVA_EXECUTABLE} -cp . MolWT)