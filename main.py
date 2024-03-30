import jar_files_search
from colorama import Fore, Back, Style
import sys
import args_process

args = args_process.process(sys.argv, len(sys.argv))
sys.setrecursionlimit(10000)
jar_files = jar_files_search.search(not args["n"])
if (args["m"]):
    import multiprocess
    multiprocess.multi_process(jar_files, not args["n"])
else:
    import singleprocess
    singleprocess.single_process(jar_files, not args["n"])