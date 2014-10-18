/* 
  Example OEChem extension 
*/
 
#include "molwt.h"

float ExampleCalcMolWt(OEChem::OEMolBase &mol)
{
    return OEChem::OECalculateMolecularWeight(mol);
}
