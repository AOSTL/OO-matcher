import time
from subprocess import STDOUT, PIPE
from functools import lru_cache
import glob
import os
from colorama import Fore, Back, Style
import sympy

from generate import preTreatment
from run_java import execute_java
from run_java import execute_py

@lru_cache(maxsize=None)
def calculate(string):
    return sympy.expand(preTreatment(string))

@lru_cache(maxsize=None)
def evaluate(myAns, poly, name):
    x = sympy.Symbol('x')
    out, t = execute_java(poly, name)
    subString = "0\n"
    subString += "("
    subString += myAns
    subString +=  ")"
    subString += "-"
    subString += "("
    subString += out
    subString += ")"
    # print(subString)
    x = sympy.Symbol('x')
    sub, t2 = execute_java(subString, "zyt.jar")
    # print(sub)
    if (sub == "0"):
        print(name + ": " + Fore.GREEN + "Accepted" + Fore.WHITE)
        return True, t
    else:
        # with open('output.txt', 'w') as f:
        #     f.write("Origin Input: " + poly)
        #     f.write(os.path.basename(jar_file) + ": no output or output is illegal")
        print(name + ": " + Fore.RED + "Wrong\n" + Fore.WHITE)
        print("Input:")
        print(poly)
        print("Origin:")
        print(myAns)
        print("User Answer:")
        print(out)
        return False, t

print("============ INITIALIZATION ============")
directory = './'
jar_files = glob.glob(os.path.join(directory, '*.jar'))
for jar_file in jar_files:
    print(jar_file)

# times = {}
# for jar_file in jar_files:
#     times[jar_file] = 0

i = 0
while True:
    i += 1
    print("---->   epoch " + str(i))
    poly = execute_py("", "generate.py")


#     poly = "2\n\
# h(y)=  -exp(y^3)*36		*+14\n\
# g(y,z,x)=+-x^+0+-(-		-	y^+1---39 *-	 9	)^3*y^+1*y^+	1\n\
# -x^+1-+h(x^+1)*h((--+55* x^+0---10*7  +x^3*11))+-exp(0003997827692)*h(h(+2700585534))*(h(+13)+(+	-x^2*x^1)-		(--x^+2+-+85*x^0))"
    # poly = "1\ng(y)=-+y^	 3\n+exp(g(  x^+1))*x^0- g((--40*-6*	 21+-x^+3*x^1-+x^3*-76*x^+3)^1)*x^1--g(g(-2))*(-(-x^1*-59*x^ +0+-+74*41*-4294967296+ x^+3*+87*x^ +0)^1*exp(7)*exp(x^+0))^1"
    print(poly)
    x = sympy.Symbol('x')
    myAns, t = execute_java(poly, "zyt.jar")
    for jar_file in jar_files:
        try:
            res, t = evaluate(myAns, poly, str(os.path.basename(jar_file)))
            if (res == False):
                exit()
            # times[jar_file] += t
            pass
        except Exception as e:
            print("Origin Input: \n" + poly)
            print(os.path.basename(jar_file) + ": no output or output is illegal")

            exit()
