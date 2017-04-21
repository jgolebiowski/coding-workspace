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