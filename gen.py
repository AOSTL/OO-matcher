from random import *
from utils.params import *
from utils.person import Person
from utils.judger import Judger

ids = []
def genId():
    while True:
        id = randint(1, 10**9)
        if id not in ids:
            ids.append(id)
            return id

timetable = []
def genTime():
    # global min_input_time, max_input_time
    # print('genTime: ', min_input_time, max_input_time)
    # return randint(min_input_time * 10, max_input_time * 10) / 10
    return choice(timetable)

def genPath():
    l = randint(MIN_FLOOR, MAX_FLOOR)
    r = randint(MIN_FLOOR, MAX_FLOOR)
    while l == r:
        r = randint(MIN_FLOOR, MAX_FLOOR)
    return l, r

def genPerson():
    l, r = genPath()
    return [0, genTime(), genId(), l, r, l]

def init():
    global ids, timetable
    global min_input_time, max_input_time, max_cmd_num, max_reset_num
    ids = []
    min_input_time, max_input_time, max_cmd_num, max_reset_num = rand_params()
    print('Selected parameters: ', min_input_time, max_input_time, max_cmd_num, max_reset_num)
    timetable = sample(range(min_input_time * 10, max_input_time * 10), 10)
    timetable = [x / 10 for x in timetable]
    print('Time table: ', timetable)

def toStr(ls):
    if ls[0] == 0: # person:  [0, time, id, start, end, now]   --->    [时间戳]ID-FROM-起点层-TO-终点层
        return f'[{ls[1]}]{ls[2]}-FROM-{ls[3]}-TO-{ls[4]}'
    else: # elevator: [1, time, id, capacity, move]
        return f'[{ls[1]}]RESET-Elevator-{ls[2]}-{ls[3]}-{ls[4]}'

def sample_with_min_diff(min_val, max_val, num_samples, min_diff):
    samples = []
    while len(samples) < num_samples:
        new_sample = randint(min_val, max_val)
        if all(abs(new_sample - s) >= min_diff for s in samples):
            samples.append(new_sample)
    
    return sorted(samples)

def speGen():
    global timetable
    res = []
    timetable = [50]
    while len(res) < 65:
        res.append(genPerson())
    for i in range(1, ELE_NUMBER):
        ts = 49.9
        res.append([1, ts, i, choice(capacity_list), choice(move_list)])
    res.sort(key=lambda x: x[1])
    return '\n'.join(map(toStr, res))

def genData():
    init()
    if max_reset_num == 3:
        return speGen()
    res = []
    while len(res) < max_cmd_num:
        res.append(genPerson())
    for i in range(1, ELE_NUMBER + 1):
        if len(res) >= max_cmd_num:
            break
        ts = sample_with_min_diff(min_input_time * 10, max_input_time * 10, max_reset_num, 50)
        for t in ts:
            res.append([1, t / 10, i, choice(capacity_list), choice(move_list)])
    res.sort(key=lambda x: x[1])
    return '\n'.join(map(toStr, res))

if __name__ == '__main__':
    # genData()
    print(genData())
    # with open('stdin.txt', 'w') as f:
    #     data = genData()
    #     f.write(data)

