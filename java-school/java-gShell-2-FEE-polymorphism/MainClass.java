public class MainClass
{
public static void main(String []args)
    {
        String output = "2091253.cx1b.OU\0: ASCII English text, with very long lines\n" +
                        "2091254.cx1b.ER\0: ASCII text\n" +
                        "2091254.cx1b.OU\0: ASCII English text, with very long lines\n" +
                        "backup\0:          directory\n" +
                        "bin\0:             directory\n" +
                        "cnt_work\0:        symbolic link to `work/CASTEP_MSC/geometry_optimisation/CNT/'\n" +
                        "intel\0:           directory\n" +
                        "PhD_CASTEP\0:      symbolic link to `/home/jg2214/work/PhD_CASTEP_runs'\n" +
                        "PhD_LAMMPS\0:      symbolic link to `/work/jg2214/LAMMPS_runs/'\n" +
                        "test.sh\0:         Bourne-Again shell script text executable\n" +
                        "work\0:            symbolic link to `/work/jg2214'\n" +
                        "binarytest\0:      binary file for testing";

        String [] outputList = output.split("\n");
        int nfiles = outputList.length;
        FileExplorerElement [] fileList = new FileExplorerElement[nfiles];

        // String teststring = outputList[11];
        // String name = FileExplorerElement.determineType(teststring);
        // switch(name)
        // {
        //     case "text":
        //         fileList[0] = new FileExplorerText(teststring);
        //         break;
        //     case "directory":
        //         fileList[0] = new FileExplorerDirectory(teststring);
        //         break;
        //     case "binary":
        //         fileList[0] = new FileExplorerBinary(teststring);
        //         break;
        //     case "unknown":
        //         fileList[0] = new FileExplorerUnknown(teststring);
        //         break;
        // }

        // System.out.println(0 + ": " + fileList[0].name + ", " + fileList[0].type + ", " + fileList[0].imageID);
        // fileList[0].onCLickAction();


        for (int i = 0; i < nfiles; ++i)
        {
            String name = FileExplorerElement.determineType(outputList[i]);
            switch(name)
            {
                case "text":
                    fileList[i] = new FileExplorerText(outputList[i]);
                    break;
                case "directory":
                    fileList[i] = new FileExplorerDirectory(outputList[i]);
                    break;
                case "binary":
                    fileList[i] = new FileExplorerBinary(outputList[i]);
                    break;
                case "unknown":
                    fileList[i] = new FileExplorerUnknown(outputList[i]);
                    break;
            }
        }

        for (int i = 0; i < nfiles; ++i)
        {
            System.out.println(i + ": " + fileList[i].name + ", " + fileList[i].type + ", " + fileList[i].imageID);
            fileList[i].onCLickAction();
        }
    }
}
