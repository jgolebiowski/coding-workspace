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