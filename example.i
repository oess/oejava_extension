%module example

%{
#include "molwt.h"

#include <oechem.h>

using namespace OEChem;
%}

// headers of custom extension to wrap
%include "molwt.h"

