import openeye.oechem.oechem;
import openeye.oechem.*;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;

public class MolWT {
    static {
        System.loadLibrary("example");
    }

    public static void main(String argv[]) {
      OEGraphMol mol = new OEGraphMol();
      oechem.OESmilesToMol(mol, "c1ccccc1CCCBr");

      System.out.println(example.ExampleCalcMolWt(mol));
      example.UsingAStream("fubar?");

      for(int j=0; j<100; j++) {
        VectorMol mols = new VectorMol();
        for(int i=0; i<50; i++){
          OEGraphMol gm = new OEGraphMol();
          oechem.OESmilesToMol(gm, "c1ccccc1CCCBr");
          mols.add(gm);
        }
        example.VectorTest(mols);
      }
    }
}
