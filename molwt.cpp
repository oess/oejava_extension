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

void VectorTest(std::vector<OEChem::OEGraphMol>& mols){
   for(std::size_t i=0; i<mols.size(); i++){
      std::cout << mols[i].GetTitle() << " ";
      mols[i].SetStringData("myData","works");
   }
   std::cout << std::endl;
}

void UsingAStream(const char *data)
{
  OEPlatform::oeisstream is(data);
}
