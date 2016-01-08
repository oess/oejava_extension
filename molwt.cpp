/* 
  Example OEChem extension 
*/
 
#include "molwt.h"

float ExampleCalcMolWt(OEChem::OEMolBase &mol)
{
  float mw = OEChem::OECalculateMolecularWeight(mol);
  mol.SetFloatData("Molecular Weight", mw);
  return mw;
}
