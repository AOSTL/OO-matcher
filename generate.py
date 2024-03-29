import random
import re

expPool = [0, 0, 0, 0, 1, 2, 2, 1, 3, 3]
numPool = [0, 0, 0, 1, 1, 1, 2, 3, 114514, 2147483647, 2147483648, 2147483649, 4294967296, 998244353]
funPool = ["f", "g", "h"]
arguPool = ["x", "y", "z"]

namePool = []
arguNumDict = {}
arguListDict = {}
funNum = 0

def remove_leading_zeros(text):
    return re.sub(r'\b0+(\d+)', r'\1', text)

def preTreatment(string):
    return remove_leading_zeros(string.replace('^','**').replace(" ", "").replace("\t",""))

def genDeclare():
    global funNum
    global arguNumDict
    global arguListDict
    global namePool

    funNum = 0
    arguNumDict.clear()
    arguListDict.clear()
    namePool.clear()

    deepNum = random.randint(0, 1)
    string = ""
    num = random.randint(0, 3)
    funNum = num
    string = string + str(num) + "\n"
    names = random.sample(funPool, num)
    namePool.extend(names)
    for i in range(num):
        name = random.choice(names)
        names.remove(name)
        arguNum = random.randint(1, 3)
        arguList = random.sample(arguPool, arguNum)
        arguNumDict[name] = arguNum
        arguListDict[name] = arguList

        string = string + name + '(' + ','.join(arguList) + ")="
        string = string + getExpr(deepNum, True, name) + "\n"

    return string

def genDate(deepNum):
    string = getExpr(deepNum)
    if (len(string) > 200):
        return genDate(deepNum)
    return string


def getExpr(deepNum, gen=False, name='bug'):
    string = ""
    termNum = random.randint(1,3)
    r = random.uniform(0,1)
    if (r < 0.35):
        string = string + getWhite() + "+" + getWhite() + getTerm(deepNum, gen, name)
    elif (r < 0.7):
        string = string + getWhite() + "-" + getWhite() + getTerm(deepNum, gen, name)
    else:
        string = string + getWhite() + getTerm(deepNum, gen, name)

    for i in range(termNum - 1):
        if (random.randint(0, 1)):
            string = string + getWhite() + "+" + getWhite() + getTerm(deepNum, gen, name)
        else:
            string = string + getWhite() + "-" + getWhite() + getTerm(deepNum, gen, name)

    return string


def getTerm(deepNum, gen=False, name='bug'):
    string = ""
    factorNum = random.randint(1, 3)
    r = random.uniform(0, 1)
    if (r < 0.35):
        string = string + getWhite() + "+" + getWhite() + getFactor(deepNum, gen, name)
    elif (r < 0.7):
        string = string + getWhite() + "-" + getWhite() + getFactor(deepNum, gen, name)
    else:
        string = string + getWhite() + getFactor(deepNum, gen, name)

    for i in range(factorNum - 1):
         string = string + getWhite() + "*" + getWhite() + getFactor(deepNum, gen, name)

    return string


def getFactor(deepNum, gen=False, name='bug'):
    r = random.uniform(0, 1)
    if (gen == False):
        if (deepNum > 0):
            if (r<0.4 and funNum > 0):
                return getFunFactor(deepNum - 1)
            elif (r < 0.5):
                return getConFactor()
            elif (r < 0.6):
                return getPowFactor()
            elif (r < 0.8):
                return getExpFactor(deepNum - 1)
            else:
                return getExprFactor(deepNum - 1)
        else:
            if (r < 0.5):
                return getConFactor()
            else:
                return getPowFactor()
    else:
        if (deepNum > 0):
            if (r < 0.3):
                return getConFactor()
            elif (r < 0.6):
                return getPowFactor(gen, name)
            elif (r < 0.9):
                return getExpFactor(deepNum - 1, gen, name)
            else:
                return getExprFactor(deepNum - 1, gen, name)
        else:
            if (r < 0.5):
                return getConFactor()
            else:
                return getPowFactor(gen, name)


def getConFactor():
    string = ""

    rSign = random.uniform(0,1)
    if (rSign < 0.3):
        string = getWhite() + "+"
    elif (rSign <0.6):
        string = getWhite() + "-"

    rValue = random.uniform(0,1)
    if (rValue < 0.1):
        string = string + getWhite() + getZero() + str(random.choice(numPool))
    elif (rValue < 0.3):
        string = string + getWhite() + getZero() + str(random.randint(0,15))
    elif (rValue < 0.4):
        string = string + getWhite() + getZero() + str(random.randint(2147483647,4147483647))
    else:
        string = string + getWhite() + getZero() + str(random.randint(0, 100))

    return string


def getPowFactor(gen=False, name='bug'):
    string = ""
    if (not gen):
        string = string + getWhite() + "x" + getWhite() + "^"
    else:
        arguList = arguListDict[name]
        var = random.choice(arguList)
        string = string + getWhite() + var + getWhite() + "^"

    if (random.uniform(0,1) < 0.5):
        string = string + getWhite() + "+"
    string = string + getWhite() + str(random.choice(expPool))

    return string


def getExprFactor(deepNum, gen=False, name='bug'):
    # print(deepNum)
    if (random.uniform(0,1) < 0.3):
        return "(" + getExpr(deepNum, gen, name) + ")"
    string = getWhite() + "(" + getWhite() + getExpr(deepNum, gen, name) + getWhite() + ")" + getWhite() + "^" + str(random.choice(expPool))
    return string


def getExpFactor(deepNum, gen=False, name='bug'):
    string = "exp("
    string = string + getFactor(deepNum, gen, name)
    string = string + ")"
    return string

def getFunFactor(deepNum):
    global namePool
    global arguNumDict
    name = random.choice(namePool)
    arguNum = arguNumDict[name]
    arguR = []
    for i in range(arguNum):
        arguR.append(getFactor(deepNum))
    return name + '(' + ','.join(arguR) + ')'

def getWhite():
    string = ""
    r = random.uniform(0,1)
    if (r < 0.9):
        string = ""
    else:
        if (random.uniform(0,1) < 0.9):
            num = random.randint(1,2)
        else:
            num = random.randint(3,5)

        for _ in range(num):
            flag = random.randint(0,1)
            if flag == 0:
                string = string + ' '
            else:
                string = string + '\t'

    return string

def getZero():
    string = ""
    if (random.uniform(0, 1) < 0.8):
        return string

    num = random.randint(1,3)
    for i in range(num):
        string = string + "0"

    return string