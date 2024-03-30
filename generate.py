# generate.py
# [(float x.y)time]id-FROM-(int)fromFloor-TO-(int)toFloor-BY-(int)elevatorId
import random
import json

config=json.load(open('config.json','r',encoding='utf-8'))


MAX_INT = 1 << 31 - 1


elevator_pool = [1, 2, 3, 4, 5, 6]
# elevator_pool = [1,3,5]
floor_pool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# floor_pool = [1,2,10,11]
id_dirt = {}


def get_id():
    id = random.randint(1, MAX_INT)
    while id_dirt.get(id) == True:
        id = random.randint(1, MAX_INT)
    id_dirt[id] = True
    return id


def get_time_gap():
    chance = random.randint(0, MAX_INT) % 100
    if chance < 5:
        return 10
    elif chance >= 95:
        return 5
    elif chance >= 5 and chance < 10 or chance >= 90 and chance < 95:
        return random.uniform(1.0, 5.0)
    elif chance >= 10 and chance < 20 or chance >= 80 and chance < 90:
        return 0
    else:
        return random.uniform(0, 1.0)


def get_floor():
    return random.choice(floor_pool)


def get_elevator():
    return random.choice(elevator_pool)


def generate_input():
    realNum = 0
    string = ""
    maxNum = random.randint(1,int(config["command_limit"]))
    time = 0.0
    for _ in range(maxNum):
        time += get_time_gap()
        if (time > float(config["time_limit"])):
            break

        id = str(get_id())
        from_floor = str(get_floor())
        to_floor = str(get_floor())
        while to_floor == from_floor:
            to_floor = str(get_floor())
        elevator_id = str(get_elevator())

        realNum = realNum + 1
        string = string + '[' + str(format(time, '.1f')) + ']' + id + '-FROM-' + from_floor + '-TO-' + to_floor + '-BY-' + elevator_id + "\n"

    return string, realNum
