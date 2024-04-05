import random
import json

config = json.load(open('config.json', 'r', encoding='utf-8'))

MAX_INT = 1 << 31 - 1

elevator_pool = [1, 2, 3, 4, 5, 6]
# elevator_pool = [1,3,5]
floor_pool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# floor_pool = [1,2,10,11]
id_dirt = {}

reset_capacity_pool = [3, 4, 5, 6, 7, 8]
reset_speed_pool = [0.2, 0.3, 0.4, 0.5, 0.6]

last_reset_time = 1.0


def get_id():
    id = random.randint(1, MAX_INT) % 100 + 1
    while id_dirt.get(id) == True:
        id = random.randint(1, MAX_INT) % 100 + 1
    id_dirt[id] = True
    return id


def get_time_gap():
    chance = random.randint(0, MAX_INT) % 100
    if chance < 2:
        return 10
    elif chance >= 98:
        return 5
    elif chance >= 5 and chance < 10 or chance >= 90 and chance < 95:
        return random.uniform(1.0, 5.0)
    elif chance >= 10 and chance < 45 or chance >= 55 and chance < 90:
        return 0
    else:
        return random.uniform(0, 1.0)


def get_floor():
    return random.choice(floor_pool)


def get_elevator():
    return random.choice(elevator_pool)


def generate_person(time):
    id = str(get_id())
    from_floor = str(get_floor())
    to_floor = str(get_floor())
    while to_floor == from_floor:
        to_floor = str(get_floor())
    elevator_id = str(get_elevator())
    return '[' + str(format(time, '.1f')) + ']' + id + '-FROM-' + from_floor + '-TO-' + to_floor + '\n'


def generate_reset(time):
    elevator = str(get_elevator())
    capacity = str(random.choice(reset_capacity_pool))
    speed = str(random.choice(reset_speed_pool))
    return '[' + str(format(time, '.1f')) + ']' + 'RESET-Elevator-' + elevator + '-' + capacity + '-' + speed + '\n'


def generate_input():
    global last_reset_time
    realNum = 0
    string = ""
    maxNum = random.randint(1, int(config["command_limit"]))
    time = 1.0
    for _ in range(maxNum):
        time += get_time_gap()
        if (time > float(config["time_limit"])):
            break

        realNum = realNum + 1
        chance = random.randint(0, MAX_INT) % 100
        if chance < 60:
            string += generate_person(time)
        else:
            if time - last_reset_time > 3:
                last_reset_time = time
                string += generate_reset(time)
            else:
                string += generate_person(time)
    return string, realNum


if __name__ == "__main__":
    print(generate_input()[0])
