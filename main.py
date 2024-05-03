import jar_files_search
import sys
import args_process
import os
import json

config = json.load(open('config.json'))
args = args_process.process(sys.argv, len(sys.argv))
jar_files = jar_files_search.search(not args["n"])
error_path = config["error_folder_name"]
if not os.path.exists(error_path):
    os.makedirs(error_path)

import multiprocess
multiprocess.run(jar_files, not args["n"])