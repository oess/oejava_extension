%module example
%include "std_vector.i"

%typemap(jstype) OEChem::OEMolBase& "openeye.oechem.OEGraphMol";

%typemap(javain) OEChem::OEMolBase& "openeye.oechem.OEGraphMol.getCPtr($javainput)"

%typemap(jstype) OEChem::OEMolBase*& "openeye.oechem.OEGraphMol";
%typemap(javain) OEChem::OEMolBase*& "openeye.oechem.OEGraphMol.getCPtr($javainput)"
%typemap(javaout) OEChem::OEMolBase*& {
      return new openeye.oechem.OEGraphMol($jnicall,false);
   }

%{
#include "molwt.h"

#include <oechem.h>

using namespace OEChem;
%}

namespace std {
   %template(VectorMol) vector<OEChem::OEMolBase*>;
}

// headers of custom extension to wrap
%include "molwt.h"

