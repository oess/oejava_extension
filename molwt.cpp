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

void VectorTest(std::vector<OEChem::OEMolBase*>& mols){
   for(std::size_t i=0; i<mols.size(); i++){
      std::cout << i << " " << mols[i]->GetTitle() << std::endl;
   }
}

void UsingAStream(const char *data)
{
  OEPlatform::oeisstream is(data);
}
