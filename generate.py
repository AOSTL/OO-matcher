import json
from random import random,randint,shuffle

config = json.load(open('config.json'))
command_num_max = int(config['command_num_max'])

id = -20

def genOneCommand():
    p = random()
    if p < 0.2:
        return ap()
    elif p < 0.45:
        return ar()
    elif p < 0.55:
        return mr()
    elif p < 0.7:
        return qci()
    elif p < 0.85:
        return qbs()
    else:
        return qts()


def ap():
    global id
    instr = "ap " + str(id) + " " + genName() + " " + str(genAge())
    id = id + 1
    return instr

def ar():
    instr = "ar " + str(genId()) + " " + str(genId()) + " " + str(genValue())
    return instr

def mr():
    instr = "mr " + str(genId()) + " " + str(genId()) + " " + str(genModifyValue())
    return instr

def qv():
    instr = "qv " + str(genId()) + " " + str(genId())
    return instr

def qci():
    instr = "qci " + str(genId()) + " " + str(genId())
    return instr


def qbs():
    instr = "qbs"
    return instr


def qts():
    instr = "qts"
    return instr


def genCommands():
    commands = ""
    if random() < 0.5:
        commands = commands + load_network() + "\n"
    p = random()
    if p < 0.3:
        command_num = randint(0, command_num_max) + 1
    elif p < 0.85 :
        command_num = randint(int(command_num_max / 2), command_num_max) + 1
    else :
        command_num = randint(int(command_num_max / 5 * 4), command_num_max) + 1
    for i in range(command_num):
        commands = commands + genOneCommand() + "\n"
    return commands


def load_network():
    global id
    res, tmp = [], []
    p = random()
    n = 100
    # if p < 0.1:
    #     n = randint(1, 100)
    # elif p < 0.4:
    #     n = randint(100, 200)
    # else:
    #     n = randint(200, 300)

    res.append(f'ln {n}')
    ids = [i for i in range(id, id + n)]
    id = id + n
    shuffle(ids)

    for i in range(n):
        tmp.append(ids[i])
    res.append(' '.join(map(str, tmp)))

    tmp = []
    for i in range(n):
        tmp.append(genName())
    res.append(' '.join(map(str, tmp)))


    tmp = []
    for i in range(n):
        tmp.append(str(genAge()))
    res.append(' '.join(map(str, tmp)))

    for i in range(1, n):
        tmp = []
        for j in range(i):
            if (random() < 0.95):
                tmp.append(str(genValue()))
            else:
                tmp.append(0)
        res.append(' '.join(map(str, tmp)))

    return '\n'.join(res)

def genId():
    global id
    if random() < 0.8:
        return randint(-20, id)
    else:
        return randint(-10, 10)


def genName():
    return "name" + str(randint(0, 1000))

def genAge():
    # return randint(1, 200)
    return 1

def genValue():
    return randint(1, 100)

def genModifyValue():
    p = random()
    if p < 0.6:
        return randint(0, 200)
    elif p < 0.8:
        return randint(-200, 0)
    else:
        return randint(-100, 100)
