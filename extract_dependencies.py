#! /usr/bin/env python
import os
import sys
from subprocess import Popen, PIPE

def extract_darwin_deps(argv):
    if len(argv) != 2:
        print("Usage: %s shared_library.jnilib" % argv[0])
        return 1

    args = ["otool", "-L", argv[1]]
    proc = Popen(args, stdout=PIPE)
    output = proc.communicate()[0]

    deps = []
    for line in output.split("\n")[1:]:
        if "liboe" not in line:
            continue

        dep = line.split()[0]
        dname, fname = os.path.split(dep)
        libname = '-'.join(fname.split('-')[:-2])
        libname = libname[3:]
        deps.append(libname)
    print(";".join(deps))





def main(argv=[__name__]):
    if sys.platform.startswith("darwin"):
        return extract_darwin_deps(argv)
    else:
        print("Unsupported platform: %s, edit %s to add support" % (sys.platform, argv[0]))
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
