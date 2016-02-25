cmake_minimum_required(VERSION 2.8.9)
project(OpenEye-java-extension)
ENABLE_TESTING()
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_VERBOSE_MAKEFILE ON)

set (OE_JAVA_DIR ${CMAKE_SOURCE_DIR})

if(WIN32)
   set(CMAKE_GENERATOR "Visual Studio 12 Win64")
   set(CMAKE_FIND_LIBRARY_PREFIXES "lib" "")
   set(CMAKE_FIND_LIBRARY_SUFFIXES ".dll.a" ".a" ".lib")
   set(OE_OS "Windows-x64")
   set(OE_TOOLKIT "windows/x64")
   #add_definitions(/DOEBUILDJAVAyes /DBUILDJAVA /DOEDEBUG /DOELIMITEDSTACK=1024)
   add_definitions(/DOEBUILDJAVAyes /DBUILDJAVA /DOEDEBUG /DOE_STREAM_BUFFER_SIZE=32768 /DOE_STATIC_BUFFER_COUNT=32)
elseif(APPLE)
   set(CMAKE_GENERATOR "Unix Makefiles")
   set(OE_OS "MacOSX-x64")
   set(OE_TOOLKIT "openeye/toolkits")
   set(CMAKE_SHARED_LIBRARY_SUFFIX ".jnilib")
   #set(CMAKE_CXX_FLAGS "-stdlib=libstdc++")
   set (CMAKE_CXX_FLAGS "-g -fno-omit-frame-pointer -stdlib=libstdc++")
   set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -unexported_symbols_list ${PROJECT_SOURCE_DIR}/javanew.unexport")
   #add_definitions(-DOEBUILDJAVAyes -DBUILDJAVA -DOEDEBUG -DOELIMITEDSTACK=1024)
   add_definitions(-DOEBUILDJAVAyes -DBUILDJAVA -DOEDEBUG -DOE_STREAM_BUFFER_SIZE=32768 -DOE_STATIC_BUFFER_COUNT=32)
else()
  set (OE_OS "Linux-x64")
endif()

set(OE_JAVA_LIB_DIR ${CMAKE_BINARY_DIR}/openeye/native-libs/${OE_OS})


# Find needed SWIG and java stuff
include (FindJava)
find_package(JNI REQUIRED)
find_package(SWIG REQUIRED VERSION 3.0.2 HINT ${HINTPATH})
include(${SWIG_USE_FILE})

include_directories(${JAVA_INCLUDE_PATH})
include_directories(${JAVA_INCLUDE_PATH2}) # needed for the 'include/linux' subdirectory
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/openeye/toolkits/include)

# macro for registering OpenEye shared libraries with CMake so we can link against them
macro( add_openeye_library libname fullpath)
  if ( NOT TARGET ${libname} )
    add_library ( ${libname} SHARED IMPORTED )
    set_target_properties ( ${libname} PROPERTIES IMPORTED_LOCATION ${fullpath})
	string(REGEX REPLACE ".dll" ".lib" fullpathlib ${fullpath})
	set_target_properties ( ${libname} PROPERTIES IMPORTED_IMPLIB ${fullpathlib})
  endif()
endmacro( add_openeye_library )

file(GLOB oe_shared_libs "${OE_JAVA_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}*${CMAKE_SHARED_LIBRARY_SUFFIX}")
message("${OE_JAVA_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}*${CMAKE_SHARED_LIBRARY_SUFFIX}")

foreach(fullpathname ${oe_shared_libs})
  if (NOT fullpathname MATCHES "-jni${CMAKE_SHARED_LIBRARY_SUFFIX}")
    # extract the shared library name including version number
    get_filename_component(sharedlibname "${fullpathname}" NAME)
    string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_SUFFIX}" "" sharedlibname "${sharedlibname}")
	if(NOT ${CMAKE_SHARED_LIBRARY_PREFIX} STREQUAL "")
      string(REGEX REPLACE "${CMAKE_SHARED_LIBRARY_PREFIX}" "" sharedlibname "${sharedlibname}")
	endif()

    # strip the version number
    string(REGEX REPLACE "-java-.*" "" libname "${sharedlibname}")
    #message("${libname} = ${fullpathname}")
    # register the shared libraries with CMake
    add_openeye_library(${libname} ${fullpathname})

    execute_process(
      COMMAND ${CMAKE_SOURCE_DIR}/extract_dependencies.py ${fullpathname}
      OUTPUT_STRIP_TRAILING_WHITESPACE
      OUTPUT_VARIABLE dependencies)

    set ( ${libname}_AND_SHARED_DEP_LIBS "${libname};${dependencies}")
    #message("${libname}_AND_SHARED_DEP_LIBS = ${${libname}_AND_SHARED_DEP_LIBS}")
  endif()
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
					${oesystem_AND_SHARED_DEP_LIBS}
					${oeplatform_AND_SHARED_DEP_LIBS}
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
