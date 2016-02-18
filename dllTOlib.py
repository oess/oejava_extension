from __future__ import print_function
import sys
import os
import subprocess
import re
import argparse

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def getDLLbitness(filename):
    foundheader = False
    command = 'dumpbin /HEADERS ' + filename
    for line in run_command(command.split()):
        line = line.rstrip()
        if foundheader:
            fields = line.split()
            if "x86" in fields[2]:
                return "X86"
            else:
                return "X64"
        if "FILE HEADER VALUES" in line:
            # next line is bitness
            foundheader = True

progname='dllTOlib.py'

parser = argparse.ArgumentParser(prog=progname, description='Create .LIB file from the specified DLL')
parser.add_argument('-i', '--input',
                    dest='input',   help='input DLL file')
parser.add_argument('-64', '--x64', '--X64',
                    dest='mach64',  action='store_true', help='generate 64bit LIB (default:auto_detect)')
parser.add_argument('-32', '--x86', '--X86',
                    dest='mach32',  action='store_true', help='generate 32bit LIB (default:auto_detect)')
parser.add_argument('-v', '--verbose',
                    dest='verbose', action='store_true', help='dump commands being run')
args = parser.parse_args()

if not args or not args.input:
    parser.print_help()
    quit()

if sys.platform != "win32":
    print('Error: Generating LIB from DLL is only meaningful on win32, not',sys.platform)
    exit(1)

if not os.path.isfile(args.input):
    print('Error: File not found:',args.input)
    exit(1)

fname, fext = os.path.splitext(args.input)

ofs = None
command = 'dumpbin /exports '+args.input
if args.verbose:
    print(command)

header = re.compile('^\s*ordinal\s+hint\s+RVA\s+name\s*$')
summary = re.compile('^\s*Summary\s*$')

foundheader = False
for line in run_command(command.split()):
    line = line.rstrip()
    if not foundheader:
        mheader = header.match(line)
        if not mheader:
            continue
        foundheader = True
        ofs = open(args.input+'.exports','wt')
        ofs.write('EXPORTS\n')
        continue # don't include header in the exports!

    if not line:
        continue

    msummary = summary.match(line)
    if msummary:
        break
    items = line.split()
    if len(items) >= 4:
        ofs.write(items[3]+'\n')

if not ofs:
    print('Warning: No exports found in',args.input)
    exit(1)

ofs.close()

if args.mach64:
    bitness = 'X64'
elif args.mach32:
    bitness = 'X86'
else:
    # auto detect
    bitness = getDLLbitness(args.input)

warningORerror = re.compile('\s(warning|error)\s', re.IGNORECASE)

command = 'lib /MACHINE:' + bitness + ' /def:'+args.input+'.exports /OUT:'+fname+'.lib'
if args.verbose:
    print(command)

for line in run_command(command.split()):
    line = line.rstrip()
    if warningORerror.match(line):
        print(line)

