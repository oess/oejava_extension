WARNING
========================================================

This is considered as advanced in OpenEye toolkit usage as an end-user
can get. This feature is beta, so any feedback is much
appreciated. Have fun hacking!



Quick start to building and installing the MolWT example
========================================================

The extension directory comes with a simple example of writing a
function to calculate molecular weight in OEChem C++ and then exposing
it to JavaOEChem. The function being wrapped is ExampleCalcMolWt
in molwt.cpp. The function is accessed through the example MolWT.java.

1. install C++ compiler
2. install SWIG 3.0.2
3. untar OpenEye C++ distribution into source tree
4. untar OpenEye Java distribution into source tree
5. unzip OpenEye-Java-xxxx.xxx.x-arch/lib/oejava-xxxx.xxx.x-arch.jar
6. edit OE_JAVA_LIB_DIR variable in CMakeLists.txt for the desire architecture (currently hardcoded to MacOSX-x64)
6. ./configure
7. make
8. ctest -V
9. java -cp . MolWT.java
