%module example

%{
#include "molwt.h"

#include <oechem.h>
#include "oe_carrays.h"

using namespace OEChem;
%}

// import OpenEye specific type information 
%import "oeiter.i"
%import "oe_carrays.i"

// headers of custom extension to wrap
%include "molwt.h"

