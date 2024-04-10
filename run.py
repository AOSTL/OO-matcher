from utils.params import *
from utils.judger import Judger
from colorama import Fore, Back, Style, init
from gen import genData
from multiprocessing import Pool
import subprocess
import time
import sys
import os
import argparse
import shutil

parser = argparse.ArgumentParser(description='Run the test')
parser.add_argument('--batch_num', type=int, default=10, help='Number of test cases')
parser.add_argument('--batch_id', type=int, default=1, help='Batch ID')
params = parser.parse_args()

init(autoreset=True)

# dataoutput = 'stdin.txt'

def r(x, min, max, avg):
    p = 0.25
    base_min = p * avg + (1 - p) * min
    base_max = p * avg + (1 - p) * max
    if x <= base_min:
        return 1
    if x >= base_max:
        return 0
    return 1 - 10**(1 - (base_max-base_min)/(x-base_min))


def print_performance(performances):
    # 将performances中结果输出到控制台中，第一行为当前这一列是什么数据
    # 之后每一行为数据，按jar文件名，T_run，MT，W，score的顺序输出
    # score=30r(T_run)+30r(MT)+40r(W)，r函数为r(x, min, max, avg)
    # 其中min，max，avg分别为该列结果中的最小值，最大值，平均值
    print(Fore.BLUE + "Performance:")
    print(Fore.YELLOW + f"{'jar':<20}{'T_run':<10}{'MT':<10}{'W':<10}{'score':<10}")
    T_runs = [performance[1] for performance in performances]
    MTs = [performance[2] for performance in performances]
    Ws = [performance[3][-1] for performance in performances]
    T_run_min, T_run_max, T_run_avg = min(T_runs), max(T_runs), sum(T_runs) / len(T_runs)
    MT_min, MT_max, MT_avg = min(MTs), max(MTs), sum(MTs) / len(MTs)
    W_min, W_max, W_avg = min(Ws), max(Ws), sum(Ws) / len(Ws)
    for performance in performances:
        jar, T_run, MT, W = performance
        score = 30 * r(T_run, T_run_min, T_run_max, T_run_avg) + 30 * r(MT, MT_min, MT_max, MT_avg) + 40 * r(W[-1], W_min, W_max, W_avg)
        print(Fore.YELLOW + f"{jar:<20}{T_run:<10.2f}{MT:<10.2f}{W[-1]:<10.2f}{score:<10.2f}")


def run_jar(jar, data):
    '''
    使用subprocess库，形成管道：
    cat data | python feed.py | java -jar jar
    并返回最终输出与运行时间，忽略标准错误输出
    '''
    print(Fore.BLUE + f"Running {jar}...")
    start = time.time()
    p1 = subprocess.Popen(['python', 'feed.py'],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['java', '-jar', jar],
                            stdin=p1.stdout,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    p1.stdin.write(data.encode())
    p1.stdin.close()
    output = p2.communicate()[0].decode()
    end = time.time()
    print(Fore.BLUE + f"Run {jar} done, cost {end - start} seconds")
    return output, end - start


def work(para):
    jar, data = para
    judger = Judger(data)
    try:
        console_print = []
        output, T_real = run_jar(jar, data)
        output = output.strip().split('\n')
        console_print.append([Fore.GREEN, f"{jar} run successfully"])
        console_print.append([Fore.GREEN, f"output {len(output)} lines"])
        T_final = float(output[-1][1:output[-1].find(']')].strip())
        console_print.append([Fore.GREEN, f"cost {T_real} seconds"])
        T_run = max(T_real, T_final)
        if T_run > 150:
            raise Exception('Time Limit Exceeded')
        MT, W = judger.judge(output)
        console_print.append([Fore.MAGENTA, f"T_run: {T_run}\nMT: {MT}\nW: {W}"])
        return console_print, [jar.split('/')[-1], T_run, MT, W]
    except Exception as e:
        jarname = jar.split('/')[-1]
        print(Fore.RED + f"{jarname} run failed for Error:\n{e}")
        # 将错误数据存放到wrong_data文件夹下新建的
        # 时间YEAR-MONTH-DAY-HH-MM-SS-jar命名的文件中
        os.makedirs('wrong_data', exist_ok=True)
        with open(f'wrong_data/{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}-{jarname}.txt', 'w') as f:
            f.write(f'Error: {e}\n')
            f.write(data)
        with open(f'wrong_data/{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}-{jarname}-output.txt', 'w') as f:
            f.write(''.join(output))
        return None
    except KeyboardInterrupt:
        print(Fore.RED + f"KeyboardInterrupt, exit...")
        raise KeyboardInterrupt


def mutual_test(jars):
    # data = genData()
    # with open("data.in", 'w') as f:
    #     f.write(data)
    #     print(Fore.BLUE + f"Data stored in data.in")
    data = open('data.in', 'r').read().strip()
    performances = []
    # 对每个jar文件进行测试，并使用judger判断输出是否正确
    with Pool(MUTUAL_TEST_THREAD_NUM) as p:
        results = p.map(work, [(jar, data) for jar in jars])
    ret = True
    for result in results:
        if result == None:
            ret = False
            continue
        console_print, performance = result
        for line in console_print:
            print(line[0] + line[1])
        performances.append(performance)
    print_performance(performances)
    return ret


def single_test(jar):
    print(Fore.BLUE + f"Testing {jar}...")
    jars = [jar] * SINGLE_TEST_BATCH_NUM
    with Pool(SINGLE_TEST_THREAD_NUM) as p:
        results = p.map(work, [(jar, genData()) for jar in jars])
    ret = True
    for result in results:
        if result == None:
            ret = False
            continue
        console_print, performance = result
        for line in console_print:
            print(line[0] + line[1])
    return ret


def random_judge(jars):
    print(Back.MAGENTA + '----------Random Test----------')
    print()
    batchnum, batchid = params.batch_num, params.batch_id
    for i in range(batchnum):
        print(Back.CYAN + f'----------Test {batchid}.{i + 1}----------')
        if not mutual_test(jars):
            return False
        print(Fore.GREEN + "Correct!")
        
    print(Back.MAGENTA + '=====================')
    print(Back.GREEN + f'All {batchnum} random cases are correct!')

def judge(jars):
    random_judge(jars)

def main():
    # sys.setrecursionlimit(1000000)
    my_jar = '../project2/out/artifacts/project2_jar/project2.jar'
    shutil.copy(my_jar, './jars/dhj.jar')
    jars = []
    for file in os.listdir('./jars'):
        if not file.endswith('.jar'):
            continue
        if file in ['天玑星.jar', '开阳星.jar', '洞明星.jar']:
            continue
        jar_name = f'./jars/{file}'
        jars.append(jar_name)
    # jars.append(my_jar)
    judge(jars)

if __name__ == '__main__':
    # print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    main()

