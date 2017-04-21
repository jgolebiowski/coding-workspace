public abstract class FileExplorerElement
{
	public String name;
    public String type;
    public String information;
    public int imageID;
    public Boolean executable;
    public Boolean link;

    public FileExplorerElement(String lsLine)
    {

        String [] parameters = lsLine.split("\0");

        this.name = parameters[0];
        this.information = parameters[1];
        determineFlags(this.information);
    }

    public abstract void onCLickAction();

    void determineFlags(String information)
    {
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
        }
        else
        {
            this.link = false;
        }
    }

    static String determineType(String information)
    {
        // Check for data type
        if (information.contains("text"))
        {
            return "text";
        }
        else if ((information.contains("directory")) || information.contains("link"))
        {
            return "directory";
        }
        else if ((information.contains("data")) || (information.contains("binary")))
        {
            return "binary";
        }
        else
        {
            return "unknown";
        }
    }
}

class FileExplorerText extends FileExplorerElement
{
    public FileExplorerText(String lsline)
    {
        super(lsline);
        this.type = "text";
        this.imageID = 0;
    }

    public void onCLickAction()
    {
        System.out.println("less " + this.name);
    }
}

class FileExplorerDirectory extends FileExplorerElement
{
    public FileExplorerDirectory(String lsline)
    {
        super(lsline);
        this.type = "directory";
        this.imageID = 1;
    }

    public void onCLickAction()
    {
        System.out.println("cd " + this.name);
    }
}

class FileExplorerBinary extends FileExplorerElement
{
    public FileExplorerBinary(String lsline)
    {
        super(lsline);
        this.type = "binary";
        this.imageID = 3;
    }

    public void onCLickAction()
    {
        System.out.println("this is binary: " + this.name);
    }
}

class FileExplorerUnknown extends FileExplorerElement
{
    public FileExplorerUnknown(String lsline)
    {
        super(lsline);
        this.type = "unknown";
        this.imageID = 4;
    }

    public void onCLickAction()
    {
        System.out.println("this object is unknown: " + this.name);
    }
}