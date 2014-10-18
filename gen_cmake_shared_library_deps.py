#! /usr/bin/python
from __future__ import print_function
import os, sys
from glob import glob

cmake_header = """
macro( add_openeye_libraries )
  foreach ( libname ${ARGN} )
    if ( NOT TARGET ${libname} )
      add_library ( ${libname} SHARED IMPORTED )
      set_target_properties ( ${libname} PROPERTIES IMPORTED_LOCATION 
        ${OE_PYTHON_LIB_DIR}/${CMAKE_SHARED_LIBRARY_PREFIX}${libname}${CMAKE_SHARED_LIBRARY_SUFFIX} )
    endif()
  endforeach ( libname )
endmacro( add_openeye_libraries )
"""

shared_lib_template = """
set ( %(name)s_AND_SHARED_DEP_LIBS %(libraries)s )
add_openeye_libraries ( ${%(name)s_AND_SHARED_DEP_LIBS} )
"""

def main(argv=[__name__]):
    if len(argv) < 3:
        print("%s <shared_libs_dir> <shared_lib_prefix> <shared_lib_suffix>" % argv[0])
        return 1

    libdir    = argv[1]
    libprefix = argv[2]
    libsuffix = argv[3]

    print(cmake_header)

    libexpr = "{}*{}".format(libprefix, libsuffix) 
    for library in glob(os.path.join(libdir, libexpr)):
        libfname = os.path.basename(library)

        fulllibname = libfname.lstrip(libprefix).rstrip(libsuffix)
        libname = fulllibname.split("-")[0]

        params = {"name" : libname,
                  "libraries" : fulllibname}
        
        print(shared_lib_template % params)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
