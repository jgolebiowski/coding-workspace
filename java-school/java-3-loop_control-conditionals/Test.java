public class Test {

	public static void main(String args[]) 
	{
		//Classic for loop
		for(int x = 10; x < 20; x = x + 1) 
		{
			System.out.print("value of x : " + x );
			System.out.print("\n");
		}

		int[] numbers = {10, 20, 30, 40, 5};
		//For loop with iterators, just as python loop
		for (int i : numbers)
		{
			//Continue statement - skipping an iteration
			if (i == 20)
			{
				continue;
			}

			//Break statement - finish loop
			if (i == 40)
			{
				break;
			}

			// Loop body
			System.out.print( "The value from iterator loop: " + i + "\n");
		}
			/* ############################## */
			//COnditionals
			/* A switch statement allows a variable to be tested for equality 
			against a list of values. Each value is called a case, and the 
			variable being switched on is checked for each case. */

		char grade = 'C';

		switch(grade) 
		{
			case 'A' :
				System.out.println("Excellent!"); 
				break;
			case 'B' :
			case 'C' :
				System.out.println("Well done");
				break;
			case 'D' :
				System.out.println("You passed");
				case 'F' :
			System.out.println("Better try again");
				break;
			default :
				System.out.println("Invalid grade");
		}
		System.out.println("Your grade is " + grade);
	}
}