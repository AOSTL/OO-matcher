public class Matcher {
    public static int bracketMatch(String s, int beginAt) {
        int cntLeft = 0;
        for (int i = beginAt; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                cntLeft++;
            } else if (s.charAt(i) == ')') {
                cntLeft--;
            } if (cntLeft == 0) {
                return i;
            }
        } return -1;
    }

    public static boolean bracketMatch(String s) {
        int cntLeft = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                cntLeft++;
            } else if (s.charAt(i) == ')') {
                cntLeft--;
            } if (cntLeft < 0) {
                return false;
            }
        } return cntLeft == 0;
    }

    public static Integer getSharp(String s) {
        for (int i = s.length() - 1; i >= 0; i--) {
            if (Character.isDigit(s.charAt(i))) {
                continue;
            } else if (s.charAt(i) == '^') {
                return i;
            } else {
                return i;
            }
        } return s.length();
    }
}
