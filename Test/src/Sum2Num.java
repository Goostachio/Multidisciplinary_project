import java.util.Scanner;
import static java.lang.Integer.sum;

public class Sum2Num {
    public static void main(String[] args) {
        int a, b, sum;
        Scanner sc = new Scanner(System.in);
        System.out.print("enter first number: ");
        a = sc.nextInt();
        System.out.print("enter second number: ");
        b = sc.nextInt();
        sum = sum(a, b);
        System.out.print("sum of a and b is: " + sum);
    }
    public static int sum(int x, int y){
        int sum;
        sum = x + y;
        return sum;
    }

}
