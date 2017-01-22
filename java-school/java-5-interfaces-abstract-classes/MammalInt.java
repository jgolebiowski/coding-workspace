/* File name : MammalInt.java */
public class MammalInt implements Animal {

    public void eat() {
        System.out.println("Mammal eats");
    }

    public void travel() {
        System.out.println("Mammal travels");
    } 

    public int noOfLegs() {
        return 0;
    }

    public static void main(String args[]) {
        MammalInt m = new MammalInt();
        m.eat();
        m.travel();
    }
} 

/*
When a class implements an interface, you can think of the class as 
signing a contract, agreeing to perform the specific behaviors of 
the interface. If a class does not perform all the behaviors of the 
interface, the class must declare itself as abstract.

A class uses the implements keyword to implement an interface. 
The implements keyword appears in the class declaration following 
the extends portion of the declaration.
*/

/*
Implementing an interface allows a class to become more formal about 
the behavior it promises to provide. Interfaces form a contract between 
the class and the outside world, and this contract is enforced at build 
time by the compiler. If your class claims to implement an interface, 
all methods defined by that interface must appear in its source code before 
the class will successfully compile.
*/