%module example

%typemap(jstype) OEChem::OEMolBase& "openeye.oechem.OEGraphMol";

%typemap(javain) OEChem::OEMolBase& "openeye.oechem.OEGraphMol.getCPtr($javainput)"

%{
#include "molwt.h"

#include <oechem.h>

using namespace OEChem;
%}

// headers of custom extension to wrap
%include "molwt.h"

