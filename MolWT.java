import openeye.oechem.*;

public class MolWT {
    static {
        System.loadLibrary("example");
    }

    public static void main(String argv[]) {

        OEGraphMol mol = new OEGraphMol();
        oechem.OESmilesToMol(mol, "c1ccccc1CCCBr");

        System.out.println(example.ExampleCalcMolWt(mol));
    }
}
