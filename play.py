from utils.judger import Judger
from run import work
from gen import genData, genId, genPath

with open('data.in', 'w') as f:
    # for i in range(10):
    #     l, r = genPath()
    #     f.write(f'[2]{genId()}-FROM-{l}-TO-{r}\n')
        # print(f'[2]{genId()}-FROM-{l}-TO-{r}')

    for i in range(6):
        f.write(f'[2.1]RESET-Elevator-{i + 1}-6-0.4\n')
        # print(f'[2.1]RESET-Elevator-{i + 1}-6-0.4')

    for i in range(64):
        l, r = genPath()
        f.write(f'[2.1]{genId()}-FROM-{l}-TO-{r}\n')
        # print(f'[2.1]{genId()}-FROM-{l}-TO-{r}')

    # for i in range(8):
    #     l, r = genPath()
    #     f.write(f'[2.2]{genId()}-FROM-{l}-TO-{r}\n')
    #     # print(f'[2.2]{genId()}-FROM-{l}-TO-{r}')

    # for i in range(8):
    #     l, r = genPath()
    #     f.write(f'[2.3]{genId()}-FROM-{l}-TO-{r}\n')
    #     # print(f'[2.3]{genId()}-FROM-{l}-TO-{r}')

    # for i in range(8):
    #     l, r = genPath()
    #     f.write(f'[2.4]{genId()}-FROM-{l}-TO-{r}\n')
    #     # print(f'[2.4]{genId()}-FROM-{l}-TO-{r}')


