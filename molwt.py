#!/usr/bin/env python

from openeye.oechem import *
from example import *
 
mol=OEGraphMol()
OEParseSmiles(mol, "c1ccccc1CCCBr")
print ExampleCalcMolWt(mol) 
