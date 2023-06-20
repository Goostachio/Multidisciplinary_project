import java.util.Scanner;

public class MaxInArray {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        System.out.print("enter size of array: ");
        int size = 0;
        if (sc.hasNextInt())
            size = sc.nextInt();

        int[] array = new int[size];
        System.out.println("enter elements of the array: ");
        for (int i=0 ; i<size ; i++){

            if (sc.hasNextInt())
                array[i] = sc.nextInt();
        }

        int max = array[0];
        for (int i=0 ; i<size ; i++){
            if (array[i]>max)
                max = array[i];
        }
        System.out.print("the largest element of the array: "+max);
        sc.close();
    }
}
