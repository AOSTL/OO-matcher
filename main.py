import time
import glob
import os
from colorama import Fore, Back, Style
import error
import generate
import sys
import evaluate
import func_timeout

sys.setrecursionlimit(10000)
os.system('cls' if os.name == 'nt' else 'clear')
print("============ INITIALIZATION ============")
directory = './'
jar_files = glob.glob(os.path.join(directory, '*.jar'))
for jar_file in jar_files:
    print(jar_file)

input("Press Enter to continue...")
os.system('cls' if os.name == 'nt' else 'clear')
test_case = 0
wrong = 0
tle = 0
while True:
    test_case += 1
    print("---->   epoch " + str(test_case) + "   ---   wrong: " + str(wrong) + "   ---   tle: " + str(tle) + "   <----")
    origin, command_number = generate.generate_input()
    input_str = ""
    for i in range(0, command_number):
        input_str += origin[i][1] + "\n"

    print("input lines:" + str(command_number))


    # input_str = "[1.0]73-FROM-1-TO-2-BY-1\n"
    with open ("stdin.txt", "w") as f:
        f.write(input_str)
    for jar_file in jar_files:
        name = os.path.splitext(jar_file)[0].split("\\")[1]
        try:
            res = evaluate.evaluate(input_str, name)
            if (res == False):
                print(str(name) + ": " + Fore.RED + "Wrong or TLE\n" + Fore.WHITE)
                wrong += 1
            else:
                print(str(name) + ": " + Fore.GREEN + "Accepted\n" + Fore.WHITE)
        except func_timeout.exceptions.FunctionTimedOut as e:
            tle += 1
            print(str(os.path.basename(jar_file)) + ": " + Fore.WHITE  + "Prase Time Limit Exceeded" + Fore.WHITE)
        except Exception as e:
            wrong += 1
            print(str(os.path.basename(jar_file)) + ": " + Fore.RED + "Error\n" + Fore.WHITE)
            error.error_output(name, "Unkown Error", input_str, "", e)

    time.sleep(0.75)
    os.system('cls' if os.name == 'nt' else 'clear')