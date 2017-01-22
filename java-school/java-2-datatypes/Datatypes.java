public class Datatypes{

	// this instance variable is visible for any child class.
   public String name;

   // salary  variable is visible in Employee class only.
   private double salary;

   public Datatypes() {}

   // The name variable is assigned in the constructor.
   public Datatypes (String empName) 
   {
      name = empName;
   }

   // The salary variable is assigned a value.
   public void setSalary(double empSal) 
   {
      salary = empSal;
   }

   //A static variable is one that's associated with a class, not objects of that class
   // It can be accessed without declaring a class object
   // salary  variable is a private static variable
   private static double stat_salary;

   // DEPARTMENT is a constant
   public static final String stat_DEPARTMENT = "Development ";


   // This method prints the employee details.
   public void printEmp() 
	{
      System.out.println("name  : " + name );
      System.out.println("salary :" + salary);
	}


	public static void main(String []args)
	{
		//Using instance variabkes
		Datatypes empOne = new Datatypes("Ransika");
		empOne.setSalary(1000);
		empOne.printEmp();

		//Using static variables
		stat_salary = 1000;
		// Here accessing the static variable stat_DEPARTMENT nornally since we are within the Datatypes class
		// Later, the static variable stat_salary is accessed as a member of the Datatypes class
		// Notice that it is not a variable associated with any Datatyped object but the classs itself
      	System.out.println(stat_DEPARTMENT + "average salary:" + Datatypes.stat_salary);

		int a, b, c;         // Declares three ints, a, b, and c.
		int d = 10, e = 10;  // Example of initialization
		byte B = 22;         // initializes a byte type variable B.
		double pi = 3.14159; // declares and assigns a value of PI.
		char f = 'a';        // the char variable a iis initialized with value 'a'

		//References are created using the keyword new and are used to store objects
		Datatypes test = new Datatypes();
	}
}