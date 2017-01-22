public class DoggoRun
{
		public static void main(String []args)
	{
		//Construct the doggo object using the constructor
		Doggo dogster = new Doggo("Tommy");
		dogster.set_breed("Terrier");
		dogster.set_age(10);
		dogster.set_color("blue");
		dogster.print_data();
	}
}