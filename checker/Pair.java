import java.lang.reflect.Method;
import java.util.ArrayList;

public class Pair<T1, T2> {
    private T1 first;
    private T2 second;

    public Pair(T1 first, T2 second) {
        this.first = first;
        this.second = second;
    }

    public T1 first() {
        return first;
    }

    public T2 second() {
        return second;
    }

    public boolean equals(Pair<T1, T2> pair) {
        boolean t1;
        boolean t2;
        if (hasEquals(pair.first())) {
            t1 = pair.first().equals(first);
        } else {
            t1 = pair.first() == first;
        } if (hasEquals(pair.second())) {
            t2 = pair.second().equals(second);
        } else {
            t2 = pair.second() == second;
        } return t1 && t2;
    }

    private Boolean hasEquals(Object object) {
        Method[] methods = object.getClass().getDeclaredMethods();
        for (Method method : methods) {
            if (method.getName().equals("equals")) {
                return true;
            }
        } return false;
    }

    public static ArrayList<Object> makePair(Object... objs) {
        ArrayList<Object> res = new ArrayList<Object>();
        for (Object obj : objs) {
            res.add(obj);
        } return res;
    }

    @Override
    public String toString() {
        return "(" + first.toString() + ", " + second.toString() + ")";
    }
}
