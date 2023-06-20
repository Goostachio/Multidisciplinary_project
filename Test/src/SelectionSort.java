import java.util.Scanner;
public class SelectionSort {
    void Sort(int[] array, int size){
        for (int i=0 ; i<size-1; i++){
            int min = i;
            for (int j=i+1 ; j<size ; j++){
                if (array[j] < array[min])
                    min=j;
            }
            int temp = array[min];
            array[min] = array[i];
            array[i] = temp;
        }
    }
    void PrintArray(int [] array, int size){
        for (int i=0 ; i<size ; ++i)
            System.out.print(array[i]+" ");
        System.out.println();
    }
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
        SelectionSort ob = new SelectionSort();
        ob.Sort(array,size);
        System.out.print("sorted array: ");
        ob.PrintArray(array,size);
        sc.close();
    }
}

