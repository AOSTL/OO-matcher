from run import *
from gen import *
import subprocess
from multiprocessing import Pool
import os
from colorama import Fore, Back, init

init(autoreset=True)

if __name__ == '__main__':
    my_jar = '../project2/out/artifacts/project2_jar/project2.jar'
    jars = []
    # for file in os.listdir('./jars'):
    #     if file in []:
    #         continue
    #     jar_name = os.path.join('jars', file)
    #     jars.append(jar_name)
    # jars.append(my_jar)
    jars.append('jars/dhj.jar')
    # print(jars)
    cnt = 0
    while True:
        for jar in jars:
            single_test(jar)
            cnt += SINGLE_TEST_BATCH_NUM
        print(f'{cnt} tests finished.')

