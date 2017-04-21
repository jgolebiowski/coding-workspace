public class FileExplorerElement
{
	public String name;
    public String type;
    public int imageID;
    public Boolean executable;
    public Boolean link;

    public FileExplorerElement(String lsLine)
    {

        String [] parameters = lsLine.split("\0");

        for (int i = 0; i< parameters.length; i++)
        {
        	System.out.println("ELement " + i + ": " + parameters[i]);
        }

        this.name = parameters[0];
        String information = parameters[1];
        determineType(information);
        determineImage(this.type);
    }

    void determineType(String information)
    {
        // Check for data type
        if (information.contains("text"))
        {
            this.type = "text";
        }
        else if (information.contains("directory"))
        {
            this.type = "directory";
        }
        else if (information.contains("data"))
        {
            this.type = "binary";
        }
        else
        {
            this.type = "unknown";
        }

        //Check if executable
        if (information.contains("executable"))
        {
            this.executable = true;
        }
        else
        {
            this.executable = false;
        }

        // Check if link
        // TODO find a better way of treating links than assigning
        // them as directories
        if (information.contains("link"))
        {
            this.link = true;
            this.type = "directory";
        }
        else
        {
            this.link = false;
        }
    }
    void determineImage(String type)
    {
        if (type == "text")
        {
            this.imageID = 0;
        }
        else if (type == "directory")
        {
            this.imageID = 1;
        }
        else if (type == "binary")
        {
            this.imageID = 2;
        }
        else
        {
            this.imageID = 3;
        }
    }

    public static void main(String []args)
	{
		String output = "2091253.cx1b.ER\0: ASCII text\n" +
                "2091253.cx1b.OU\0: ASCII English text, with very long lines\n" +
                "2091254.cx1b.ER\0: ASCII text\n" +
                "2091254.cx1b.OU\0: ASCII English text, with very long lines\n" +
                "backup\0:          directory\n" +
                "bin\0:             directory\n" +
                "cnt_work\0:        symbolic link to `work/CASTEP_MSC/geometry_optimisation/CNT/'\n" +
                "intel\0:           directory\n" +
                "PhD_CASTEP\0:      symbolic link to `/home/jg2214/work/PhD_CASTEP_runs'\n" +
                "PhD_LAMMPS\0:      symbolic link to `/work/jg2214/LAMMPS_runs/'\n" +
                "test.sh\0:         Bourne-Again shell script text executable\n" +
                "work\0:            symbolic link to `/work/jg2214'\n";

		String [] outputList = output.split("\n");
		int nfiles = outputList.length;
        FileExplorerElement [] fileList = new FileExplorerElement[nfiles];


        for (int i = 0; i < nfiles; ++i)
        {
        	System.out.println(outputList[i]);
            fileList[i] = new FileExplorerElement(outputList[i]);
        }

        for (int i = 0; i < nfiles; ++i)
        {
            System.out.println(i + ": " + fileList[i].name + ", " + fileList[i].type + ", " + fileList[i].imageID);
        }
	}
}