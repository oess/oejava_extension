/* 
Example OEChem extension header 
*/

#include <openeye.h>
#include <oechem.h>

float ExampleCalcMolWt(OEChem::OEMolBase &mol);

void VectorTest(std::vector<OEChem::OEGraphMol>& mols);

void UsingAStream(const char *data);
