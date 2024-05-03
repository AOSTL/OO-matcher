import datetime
import os

def error_output(name, error_type, input, output, error_info, ans, error_path):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d@%H-%M-%S")
    usr_path = error_path + "/" + name + "/"
    if not os.path.exists(usr_path):
        os.makedirs(usr_path)

    usr_path = usr_path + current_time + "/"
    if not os.path.exists(usr_path):
        os.makedirs(usr_path)

    with open (usr_path + 'BUG_INFO.txt', "w") as f:
        f.write(name + ": " + error_type + ".\n")
        f.write("======= Error =======\n")
        f.write(str(error_info) + "\n")

    with open (usr_path + 'INPUT.txt', "w") as f:
        f.write(input)

    with open (usr_path + 'OUTPUT.txt', "w") as f:
        f.write(output)

    with open (usr_path + 'ANS.txt', "w") as f:
        f.write(ans)