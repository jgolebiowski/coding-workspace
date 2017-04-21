import java.util.List; 
import java.util.Arrays;
import java.util.ArrayList;

public class TestList {
    public static void main(String[] args) 
    {
        List<Double> myArrayList = new ArrayList<Double>(Arrays.asList(1.38, 2.56, 4.3));
        System.out.println("MyArrayList: " + myArrayList);
        myArrayList.set(2, 10.0);
        System.out.println("MyArrayList: " + myArrayList);
        myArrayList.set(0, myArrayList.get(0) + 10.0);
        System.out.println("MyArrayList: " + myArrayList);



        Double[] myArray = {1.9, 2.9, 3.4, 3.5};
        List<Double> myList = new ArrayList<Double>(Arrays.asList(myArray));
        // Print all the array elements
        for (int i = 0; i < myList.size(); i++) 
        {
            System.out.println(myList.get(i) + " ");
        }
        
        // Summing all elements
        double total = 0;
        for (int i = 0; i < myList.size(); i++) 
        {
            total += myList.get(i);
        }
        System.out.println("Total is " + total);
        
        // Finding the largest element
        double max = myList.get(0);
        for (int i = 1; i < myList.size(); i++) 
        {
            if (myList.get(i) > max) max = myList.get(i);
        }
        System.out.println("Max is " + max);  
    }
}