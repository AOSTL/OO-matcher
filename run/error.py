import datetime

def error_output(name, error_type, input, output, error_info):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d@%H-%M-%S@" + name)
    with open ("./errors/" + current_time + ".log", "w") as f:
        f.write(name + ": " + error_type + ".\n")
        f.write("======= Input =======\n" + input + "\n")
        f.write("======= Output ======\n" + output + "\n")
        f.write("======= Error =======\n")
        f.write(str(error_info) + "\n")