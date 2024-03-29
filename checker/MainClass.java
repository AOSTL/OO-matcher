import java.util.Scanner;

public class MainClass {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Expr expr = new Expr(scanner.nextLine().trim().replace("exp", "e"));
        Pair<Boolean, Integer> result = expr.check();
        System.out.println(result.first());
        if (!result.first()) {
            System.out.println(result.second());
        }
        scanner.close();
    }
}