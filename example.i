%module example
%include "std_vector.i"

%typemap(jstype) OEChem::OEMolBase& "openeye.oechem.OEGraphMol";
%typemap(javain) OEChem::OEMolBase& "openeye.oechem.OEGraphMol.getCPtr($javainput)"


%typemap(jstype) OEChem::OEGraphMol& "openeye.oechem.OEGraphMol";
%typemap(javain) OEChem::OEGraphMol& "openeye.oechem.OEGraphMol.getCPtr($javainput)"
%typemap(javaout) OEChem::OEGraphMol& {
  return new openeye.oechem.OEGraphMol($jnicall,false);
}

%typemap(in) OEChem::OEGraphMol& %{
  OEGraphMol tmp_mol(*reinterpret_cast<OEMolBase *>($input));
  $1 = &tmp_mol;
%}

%{
#include "molwt.h"

#include <oechem.h>

using namespace OEChem;
%}

%feature("valuewrapper") OEChem::OEGraphMol;

%template(VectorMol) std::vector<OEChem::OEGraphMol>;

// headers of custom extension to wrap
%include "molwt.h"

