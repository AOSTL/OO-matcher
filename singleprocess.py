import run.evaluate
import run.generate
import run.error
import func_timeout
import time
import os
from colorama import Fore, Back, Style

def single_process(jar_files, interact):
    test_case = 0
    wrong = 0
    tle = 0
    while True:
        test_case += 1
        if (interact):
            print("---->   epoch " + str(test_case) + "   ---   wrong: " + str(wrong) + "   ---   tle: " + str(tle) + "   <----")

        input_str, command_number = run.generate.generate_input()
        if (interact):
            print("input lines:" + str(command_number))
        
        with open ("stdin.txt", "w") as f:
            f.write(input_str)
        for jar_file in jar_files:
            if (os.name == 'nt'):
                name = os.path.splitext(jar_file)[0].split("\\")[1]
            else:
                name = os.path.splitext(jar_file)[0].split("/")[1]

            try:
                res, run_time = run.evaluate.evaluate(input_str, name)
                if (interact):
                    if (res == False):
                        print(str(name) + ": " + Fore.RED + "Wrong or TLE" + Fore.WHITE)
                        wrong += 1
                    else:
                        print(str(name) + ": " + Fore.GREEN + "Accepted" + Fore.WHITE + " with " + str(run_time) + "s")
                elif (res == False):
                    wrong += 1
            except func_timeout.exceptions.FunctionTimedOut as e:
                tle += 1
                if (interact):
                    print(str(os.path.basename(jar_file)) + ": " + Fore.WHITE  + "Prase Time Limit Exceeded" + Fore.WHITE)
            except Exception as e:
                wrong += 1
                if (interact):
                    print(str(os.path.basename(jar_file)) + ": " + Fore.RED + "Error" + Fore.WHITE)
                run.error.error_output(name, "Unkown Error", input_str, "", e)

        if (interact):
            time.sleep(0.75)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            with open ("matcher.log", "w") as f:
                f.write("epoch: " + str(test_case) + " Wrong: " + str(wrong) + " TLE: " + str(tle))