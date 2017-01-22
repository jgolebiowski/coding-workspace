public class TestArray {
    public static void main(String[] args) 
    {
        String teststring;
        teststring = "Elo elo \n320 023"
        String [] splitString = teststring.split("\n");
        System.out.println(splitString[0]);
        System.out.println(splitString[1]);
        System.out.println("The list is " + splitString.length + " long");
    }
}