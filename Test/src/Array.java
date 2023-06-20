import java.util.Scanner;
public class Array {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        System.out.print("enter size of array: ");
        int size = 0;
        if (sc.hasNextInt()){
            size = sc.nextInt();
        }
        int[] array = new int[size];
        System.out.println("enter elements of the array: ");
        for (int i=0 ; i<size ; i++){
            if (sc.hasNextInt()){
                array[i] = sc.nextInt();
            }
        }
        System.out.print("the array: ");
        for (int i=0 ; i<size ; i++){
            System.out.print(array[i]+" ");
        }
        sc.close();
    }
}
