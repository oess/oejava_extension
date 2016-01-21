%module example

%pragma(java) jniclassimports=%{
import openeye.oechem.*;
%}

%include "std_vector.i"

%typemap(jstype) OEChem::OEMolBase& "openeye.oechem.OEGraphMol";
%typemap(javain) OEChem::OEMolBase& "openeye.oechem.OEGraphMol.getCPtr($javainput)"

%typemap(jstype) OEChem::OEGraphMol& "openeye.oechem.OEGraphMol";
%typemap(javain) OEChem::OEGraphMol& "openeye.oechem.OEGraphMol.getCPtr($javainput)"
%typemap(javaout) OEChem::OEGraphMol& {
  openeye.oechem.OEMolBase tmpmol = new openeye.oechem.OEMolBase($jnicall, true);
  return new openeye.oechem.OEGraphMol(tmpmol);
}

%typemap(in) OEChem::OEGraphMol& %{
  OEGraphMol tmp_mol(*reinterpret_cast<OEMolBase *>($input));
  $1 = &tmp_mol;
%}

%typemap(out) OEChem::OEGraphMol& %{
  OEMolBase *tmp_mol = OENewMolBase($1->SCMol());
  *(OEMolBase **)&$result = tmp_mol;
%}

%{
#include "molwt.h"

#include <oechem.h>

using namespace OEChem;
%}

%template(VectorMol) std::vector<OEChem::OEGraphMol>;

// headers of custom extension to wrap
%include "molwt.h"

