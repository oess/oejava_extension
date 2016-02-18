#! /usr/bin/env python
import os
import sys
import re
from subprocess import Popen, PIPE

def extract_deps(args):
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

    return 0

def extract_doze_deps(args):
    isDLL = re.compile('\.dll\s*$', re.IGNORECASE)

    proc = Popen(args, stdout=PIPE)
    output = proc.communicate()[0]

    deps = []
    for line in output.split("\n")[1:]:
        if "KERNEL32.dll" in line:
            continue
        if "Dump of file " in line:
            continue
        if ".dll" not in line:
            continue
        #print(line)

        dep = line.split()[0]
        dname, fname = os.path.split(dep)
        # convert .dll->.lib
        libname = fname[:-4]+'.lib'
        deps.append(libname)
    print(";".join(deps))

    return 0


def extract_darwin_deps(argv):
    if len(argv) != 2:
        print("Usage: %s shared_library.jnilib" % argv[0])
        return 1

    args = ["otool", "-L", argv[1]]
    return extract_deps(args)


def extract_linux_deps(argv):
    if len(argv) != 2:
        print("Usage: %s shared_library.jnilib" % argv[0])
        return 1

    args = ["ldd", argv[1]]
    return extract_deps(args)

def extract_windows_deps(argv):
    if len(argv) != 2:
        print("Usage: %s shared_library.jnilib" % argv[0])
        return 1

    args = ["dumpbin" , "/imports", argv[1]]
    return extract_doze_deps(args)


def main(argv=[__name__]):
    if sys.platform.startswith("darwin"):
        return extract_darwin_deps(argv)
    elif sys.platform.startswith("linux"):
        return extract_linux_deps(argv)
    elif sys.platform.startswith("win"):
        return extract_windows_deps(argv)
    else:
        print("Unsupported platform: %s, edit %s to add support" % (sys.platform, argv[0]))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
