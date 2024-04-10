MIN_FLOOR = 1
MAX_FLOOR = 11
ELE_NUMBER = 6

ELE_MOVE_COST = 0.4
ELE_OPEN_COST = 0.2
ELE_CLOSE_COST = 0.2
ELE_RESET_COST = 1.2
ELE_RESET_MAX = 5
ELE_CARRYLIMIT = 6

move_list = [0.2, 0.3, 0.4, 0.5, 0.6]
capacity_list = [3, 4, 5, 6, 7, 8]

min_input_time = 1
max_input_time = 50
max_cmd_num = 70
max_ele_num = 30
max_reset_num = 1

ls = [
    [1, 50, 64, 1],
    [1, 5, 64, 1],
    [1, 10, 64, 1],
    [48, 50, 64, 1],
    # [1, 10, 200, 1],
    # [1, 5, 240, 1],
    # [1, 5, 20, 1],
    [49, 50, 65, 3],
    # [1, 30, 1080, 3],
]

ACTION_INIT = 0
ACTION_ARRIVE = 1
ACTION_OPEN = 2
ACTION_CLOSE = 3
ACTION_IN = 4
ACTION_OUT = 5
ACTION_RESET_ACCEPT = 6
ACTION_RESET_BEGIN = 7
ACTION_RESET_END = 8
ACTION_RECEIVE = 9

EPS = 0.02

W_ARRIVE = 4
W_OPEN = 1
W_CLOSE = 1

MUTUAL_TEST_THREAD_NUM = 8
SINGLE_TEST_THREAD_NUM = 5
SINGLE_TEST_BATCH_NUM = 32

from random import choice
def rand_params():
    # global min_input_time, max_input_time, max_cmd_num, max_ele_num
    # v_MIN_INPUT_TIME, v_MAX_INPUT_TIME, v_MAX_CMD_NUM, v_MAX_ELE_NUM = choice(ls)
    # print('Selected parameters: ', v_MIN_INPUT_TIME, v_MAX_INPUT_TIME, v_MAX_CMD_NUM, v_MAX_ELE_NUM)
    return choice(ls)
