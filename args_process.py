def process(argv, argn):
    info = {}
    info["m"] = info["s"] = info["n"] = False
    for i in range(1, argn):
        if argv[i] == "-h" or argv[i] == "--help":
            print("Usage: python3 main.py [OPTION]...")
            print("Options:")
            print("  -h, --help\t\t\tDisplay this help message")
            print("  -m, --multiprocess\t\t\tUse multiprocessing")
            print("  -s, --single\t\t\tUse single process")
            print("  -n, --nointeract\t\t\tWill not interact with user")
            exit(0)
        elif argv[i] == "-m" or argv[i] == "--multiprocess":
            info["m"] = True
        elif argv[i] == "-s" or argv[i] == "--single":
            info["s"] = True
        elif argv[i] == "-n" or argv[i] == "--nointeract":
            info["n"] = True
    
    return info