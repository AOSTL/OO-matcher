public class Expr {
    private String expr;

    public Expr(String expr) {
        this.expr = expr;
    }

    private Pair<Boolean, Integer> parseTerm(int left) {
        int i = left;
        if (i >= expr.length()) {
            return new Pair<Boolean,Integer>(false, expr.length());
        } else if (expr.charAt(i) == '+' || expr.charAt(i) == '-') {
            i++;
        } for (; i < expr.length();) {
            if (expr.charAt(i) == '+' || expr.charAt(i) == '-') {
                i++;
            } for (; i < expr.length(); i++) {
                char c = expr.charAt(i);
                if (c == '(') {
                    i = Matcher.bracketMatch(expr, i);
                } else if (c == '*') {
                    i++;
                    break;
                } else if (c == '+' || c == '-') {
                    return new Pair<Boolean,Integer>(true, i);
                }
            }
        } return new Pair<Boolean,Integer>(true, i);
    
    }

    public Pair<Boolean, Integer> check() {
        if (preTreat() == false) {
            return new Pair<Boolean, Integer>(false, 0);
        } for (int i = 0; i < this.expr.length();) {
            Pair<Boolean, Integer> res = parseTerm(++i);
            if (!res.first()) {
                return res;
            } Term term = new Term(this.expr.substring(i, res.second()));
            Pair<Boolean, Integer> termRes = term.parse();
            if (!termRes.first()) {
                return new Pair<Boolean,Integer>(false, i + termRes.second());
            }
            i = res.second();
        } return new Pair<Boolean,Integer>(true, 0);
    }

    private boolean preTreat() {
        expr = expr.replaceAll("[\\s\\t]+", " "); /* delete redundant spaces */
        expr = expr.replaceAll("\\^\\s\\+", "^"); /* delete redundant '+' after '^' */
        expr = expr.replaceAll("\\s?\\*\\s?", "*"); /* delete redundant ' * ' */
        expr = expr.replaceAll("\\s?\\^\\s?", "^"); /* delete redundant ' ^ ' */
        expr = expr.replaceAll("\\s?x\\s?", "x"); /* delete redundant ' x ' */
        if (expr.replaceAll("[ex\\d\\+\\-\\^()\\s\\*]", "").length() > 0) {
            return false; /* check illegal character */
        } else if (expr.replaceAll("\\d\\s\\d", "_").contains("_")) {
            return false; /* check illegal spaces */
        } else if (expr.replaceAll("\\^[^\\d]+\\d", "_").contains("_")) {
            return false; /* check illegal spaces between sharp and numbers */
        } else if (Matcher.bracketMatch(this.expr) == false) {
            return false; /* check illegal brackets */
        } else if (expr.replaceAll("\\*[\\+\\-]\\s\\d", "_").contains("_")) {
            return false; /* check illegal spaces between '+' and numbers */
        } else if (expr.charAt(0) != '+' && expr.charAt(0) != '-') {
            expr = "+" + expr; /* add '+' at the beginning */
        } return true;
    }
}
