import os
import glob

def search(interact):
    os.system('cls' if os.name == 'nt' else 'clear')
    if (interact):
        print("============ INITIALIZATION ============")
    directory = './'
    jar_files = glob.glob(os.path.join(directory, '*.jar'))
    if (interact):
        for jar_file in jar_files:
           print(jar_file)

    if (interact):
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
    
    return jar_files