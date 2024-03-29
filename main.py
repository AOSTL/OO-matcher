import time
from subprocess import STDOUT, PIPE
from functools import lru_cache
import glob
import os
from colorama import Fore, Back, Style
import sympy
import datetime
from generate import genDate
from generate import genDeclare
from generate import preTreatment
from run_java import execute_java
import func_timeout
from func_timeout import func_set_timeout
import sys

@lru_cache(maxsize=None)
def calculate(string):
    return sympy.expand(preTreatment(string))

def generate():
    declare = genDeclare()
    poly = genDate(2)
    poly = declare + poly
    origin = execute_java(poly, "parse_func.dll")[0]
    return poly, origin

@lru_cache(maxsize=None)
@func_set_timeout(10)
def evaluate(origin, poly, name):
    out, t = execute_java(poly, name)
    oriSym = sympy.sympify(preTreatment(origin.replace("e", "exp")))
    outSym = sympy.sympify(preTreatment(out))
    check_result = execute_java(out, "checker.dll")[0].split("\n")[0]
    if check_result == "true" and oriSym.equals(outSym):
        outLen = len(out)
        print(name + ": " + Fore.GREEN + "Accepted" + Fore.WHITE + " with length " + str(outLen))
        return True, str(outLen)
    else:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d@%H-%M-%S@" + os.path.splitext(jar_file)[0].split("\\")[1])
        with open ("./errors/" + current_time + ".log", "w") as f:
            f.write(os.path.basename(jar_file) + ": Wrong Answer.\n")
            f.write("Input:\n" + poly + "\n")
            f.write("Origin:\n" + origin + "\n")
            f.write("User Answer:\n")
            f.write(out + "\n")
        
        return False, -1


sys.setrecursionlimit(10000)
os.system('cls' if os.name == 'nt' else 'clear')
print("============ INITIALIZATION ============")
directory = './'
jar_files = glob.glob(os.path.join(directory, '*.jar'))
for jar_file in jar_files:
    print(jar_file)

# input("Press Enter to continue...")
os.system('cls' if os.name == 'nt' else 'clear')
i = 0
wrong = 0
tle = 0
while True:
    i += 1
    print("---->   epoch " + str(i) + "   ---   wrong: " + str(wrong) + "   ---   tle: " + str(tle) + "   <----")
    poly, origin = generate()
    print("Origin Input:\n" + poly)
    length = -1
    for jar_file in jar_files:
        name = os.path.splitext(jar_file)[0].split("\\")[1]
        try:
            res = evaluate(origin, poly, str(os.path.basename(jar_file)))
            if (res[0] == False):
                print(str(name) + ": " + Fore.RED + "Wrong\n" + Fore.WHITE)
                wrong += 1
            else:
                if length == -1:
                    length = res[1]
                elif length != res[1] and length != 0:
                    length = 0
                    with open ("./performance.log", "a") as f:
                        f.write("Input:\n" + poly + "\n")
                        f.write("Origin:\n" + origin + "\n")
                        f.write("\n\n===================================================\n")
            pass
        except func_timeout.exceptions.FunctionTimedOut as e:
            tle += 1
            print(str(os.path.basename(jar_file)) + ": " + Fore.YELLOW  + "Time Limit Exceeded" + Fore.WHITE)
            with open ("./errors/" + "tle.log", "a") as f:
                f.write(os.path.basename(jar_file) + ": Time Limit Exceeded.\n")
                f.write("Input:\n" + poly + "\n")
                f.write("Origin:\n" + origin + "\n")
                f.write("\n\n===================================================\n")
        except Exception as e:
            wrong += 1
            print(str(os.path.basename(jar_file)) + ": " + Fore.RED + "Error\n" + Fore.WHITE)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d@%H-%M-%S@" + name)
            with open ("./errors/" + current_time + ".log", "w") as f:
                f.write(os.path.basename(jar_file) + ": No output or illegal output.\n")
                f.write("Input:\n" + poly + "\n")
                f.write("Origin:\n" + origin + "\n")
                f.write("Error:\n")
                f.write(str(e) + "\n")
    
    time.sleep(0.75)
    os.system('cls' if os.name == 'nt' else 'clear')