import java.util.Scanner;

public class BubbleSort {
    static void Sort(int[] array, int size){
        for (int i=0 ; i<size-1 ; i++){
            boolean swap = false;
            for (int j=0 ; j<size-i-1 ; j++){
                if (array[j] > array[j+1]){
                    int temp = array[j];
                    array[j] = array[j+1];
                    array[j+1] = temp;
                    swap = true;
                }
            }
            if (!swap)
                break;
        }
    }
    static void PrintArray(int[] array, int size){
        for (int i=0 ; i<size ; i++)
            System.out.print(array[i]+" ");
        System.out.println();
    }
    public static void main(String[] args) {
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
        Sort(array,size);
        System.out.print("sorted array: ");
        PrintArray(array,size);
        sc.close();
    }
}
