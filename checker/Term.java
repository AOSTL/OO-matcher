public class Term {
    private String term;

    public Term(String term) {
        this.term = term;
    }

    public Pair<Boolean, Integer> parse() {
        if (this.term.matches("\\s*")) {
            return new Pair<Boolean,Integer>(false, 0);
        }
        for (int i = 0, j; i < term.length(); i++) {
            for (j = i; i < term.length(); i++) {
                if (term.charAt(i) == '*') {
                    break;
                } else if (term.charAt(i) == '(') {
                    i = Matcher.bracketMatch(term, i) - 1;
                }
            } String factor = term.substring(j, i);
            if (factor.matches("\\s?\\(.*\\)(\\^\\d+)?\\s?")) {
                return new Pair<Boolean,Integer>(false, j);
            } else if (factor.matches("\\s?x(\\^\\d+)?\\s?")) {
                continue;
            } else if (factor.matches("\\s?[\\+\\-]?\\d+\\s?")) {
                continue;
            } else if (factor.matches("\\s?e\\(.*\\)(\\^\\d+)?\\s?")) {
                if (!checkExp(factor.trim())) {
                    return new Pair<Boolean,Integer>(false, j);
                } continue;
            } else {
                return new Pair<Boolean,Integer>(false, j);
            }
        } return new Pair<Boolean,Integer>(true, 0);
    }

    private boolean checkExp(String factor) {
        String exp = factor.substring(2, Matcher.bracketMatch(factor, 1)).trim();
        if (exp.matches("\\s*")) {
            return false;
        } else if (exp.charAt(0) == '(') {
            if (Matcher.bracketMatch(exp, 0) == exp.length() - 1) {
                return new Expr(exp.substring(1, exp.length() - 1)).check().first();
            } else {
                return false;
            }
        } else if (exp.matches("[\\+\\-]?\\d+")) {
            return true;
        } else if (exp.matches("x(\\^\\d+)?")) {
            return true;
        } else if (exp.matches("e\\(.*\\)(\\^\\d+)?")) {
            return new Term(exp).parse().first();
        } else {
            return false;
        }
    }
}
