// Important - there can be only one public class per source file
// (Multiple non-public classes are ok)
public class Doggo
{
	String dogname;
	String breed;
	int age;
	String color;

	// COnstructor declaration - has to be a public method named as the class
	// It is not really a method since it does not return anything
	public Doggo(String name)
	{
		// The variable usedi n a function cannot be called the same as class variable
		// Otherwise it is necessary ot use this.name instead of name to differenciate
		dogname = name;
		System.out.println("The name of this dog at creation is: " + name);
	}
	public void bark()
	{
		System.out.println("Woof!");
	}

	public void set_name(String name)
	{
		this.dogname = name;
	}

	public void set_breed(String breed)
	{
		this.breed = breed;
	}

	public void set_age(int age)
	{
		this.age = age;
	}

	public void set_color(String color)
	{
		this.color = color;
	}

	public void print_data()
	{
		System.out.println("The " + color + " " + breed + " is called " + dogname + " and is " + age + " yo");
	}

}