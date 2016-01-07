import openeye.oechem.*;
import example.*;

public class MolWT {
    public static void main(String argv[]) {

        OEGraphMol mol = new OEGraphMol();
        oechem.OESmilesToMol(mol, "c1ccccc1CCCBr");

        System.out.println(example.ExampleCalcMolWt(mol));
    }
}
