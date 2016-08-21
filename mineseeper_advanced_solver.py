import cv2
import numpy as np
import pyautogui
import random, time, os

pyautogui.PAUSE = 0
map = np.zeros((16, 30), dtype=object)
flagList = []
numberList = []
bombs = 99


def click(y, x, button):
    global map
    global track
    if 0 <= x <= 29 and 0 <= y <= 15:
        pyautogui.moveTo(11 + 16 * int(x + 1), 94 + 16 * int(y + 1), duration=0.)
        if button == 'r':
            pyautogui.click(button='right', duration=0.05)
        else:
            pyautogui.click(button='left', duration=0.05)
        track = 0


def findObjects(image, object):
    threshold = 0.9
    if object == 'squares':
        template = cv2.imread('templates\square.png', 0)
        threshold = 0.95
    elif object == '1':
        template = cv2.imread(r'templates\1.png', 0)
    elif object == '2':
        template = cv2.imread(r'templates\2.png', 0)
    elif object == '3':
        template = cv2.imread(r'templates\3.png', 0)
    elif object == 'flag':
        template = cv2.imread(r'templates\flag.png', 0)
        threshold = 0.8
    elif object == '4':
        template = cv2.imread(r'templates\4.png', 0)
    elif object == '5':
        template = cv2.imread(r'templates\5.png', 0)
    elif object == '6':
        template = cv2.imread(r'templates\6.png', 0)
    elif object == 'nothing':
        template = cv2.imread(r'templates\nothing.png', 0)
        threshold = 0.95
    elif object == 'smile':
        template = cv2.imread(r'templates\smile.png', 0)
    elif object == 'dead':
        template = cv2.imread(r'templates\dead.png', 0)

    imageG = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(imageG, template, cv2.TM_CCOEFF_NORMED)
    w, h = template.shape[::-1]
    loc = np.where(res >= threshold)
    result = []
    for pt in zip(*loc[::-1]):
        result.append(pt)
        '''cv2.rectangle(image,pt,(pt[0] + w, pt[1] + h), (0,0,255), 1)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    return result


def posToNumber(list, type):
    global map
    for item in list:
        n = round((item[0] - 4) / 16)
        m = round((item[1] - 88) / 16)
        map[m - 1][n - 1] = str(type)


Totalmaps = 0


def makeMap():
    global Totalmaps
    try:
        Totalmaps += 1
        global map, checkList
        expert = (0, 0, 520, 370)
        pyautogui.screenshot('screen1.png', region=expert)
        image = cv2.imread('screen1.png')

        squares = findObjects(image, 'squares')
        ones = findObjects(image, '1')
        twos = findObjects(image, '2')
        threes = findObjects(image, '3')
        flags = findObjects(image, 'flag')
        fours = findObjects(image, '4')
        fives = findObjects(image, '5')
        sixes= findObjects(image,'6')
        nothing = findObjects(image, 'nothing')

        posToNumber(ones, '1')
        posToNumber(twos, '2')
        posToNumber(threes, '3')
        posToNumber(flags, 'f')
        posToNumber(squares, 's')
        posToNumber(fours, '4')
        posToNumber(fives, '5')
        posToNumber(sixes,'6')
        posToNumber(nothing, 0)


    except:
        makeMap()


def doTile(y, x, n):
    global map, flagList, numberList
    fcount = 0
    scount = 0
    spos = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if x + dx >= 0 and x + dx <= 29 and y + dy >= 0 and y + dy <= 15:
                if map[y + dy][x + dx] == 'f':
                    fcount += 1
                if map[y + dy][x + dx] == 's':
                    scount += 1
                    spos.append((y + dy, x + dx))
    if n > 0:
        if fcount == n:
            if spos != []:
                for items in spos:
                    numberList.append(items)
        elif scount + fcount == n:
            for items in spos:
                flagList.append(items)
    return fcount, scount


def clickRandom():
    global map, checkList, track
    maxChance = 0
    maxLocation = ()
    minChance=1
    minLocation=()
    for y in range(0, 15):
        for x in range(0, 29):
            if map[y][x] != '0' and map[y][x] != 's' and map[y][x] != 'f':
                fcount, scount = doTile(y, x, 0)
                if scount > 0:
                    chance = (int(map[y][x]) - fcount) / scount
                    if chance >= maxChance:
                        maxChance = chance
                        maxLocation = (y, x)
                    if chance<=minChance:
                        minChance=chance
                        minLocation=(y,x)

    if maxLocation != ():
        if minChance<1-maxChance:
            y = minLocation[0]
            x = minLocation[1]
            op='l'
        else:
            y=maxLocation[0]
            x=maxLocation[1]
            op='r'
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if x + dx >= 0 and x + dx <= 29 and y + dy >= 0 and y + dy <= 15:
                    if map[y + dy][x + dx] == 's':
                        click(y + dy, x + dx, op)
                        print(y + dy, x + dx, maxChance,minChance, op)
                        track = 0
                        return
    track = 0


def start():
    if os.path.exists(os.getcwd()+'\games')==False:
        os.makedirs(os.getcwd()+'\games')
    global checkList
    pyautogui.click(260, 80, clicks=2, interval=0.5, duration=0.05)
    click(0,0,'l')
    makeMap()


def executeMap():
    global numberList, flagList
    for y in range(0, 16):
        for x in range(0, 30):
            if map[y][x] == '1' or map[y][x] == '2' or map[y][x] == '3' or map[y][x] == '4' or map[y][x] == '5' or map[y][x]=='6':
                if x >= 0 and x <= 29 and y >= 0 and y <= 15:
                    doTile(y, x, int(map[y][x]))
    numberList = list(set(numberList))
    flagList = list(set(flagList))
    for number in numberList:
        click(number[0], number[1], 'l')
    for flag in flagList:
        click(flag[0], flag[1], 'r')
    numberList.clear()
    flagList.clear()


def checkFinish():
    pyautogui.screenshot('screen1.png', region=(0, 0, 285, 105))
    image = cv2.imread('screen1.png')
    found=''
    if findObjects(image, 'smile') != []:
        found='win'
    if findObjects(image, 'dead') != []:
        found = 'los'
    if found=='win' or found=='los':
        print('finish')
        maxi=0
        n=0
        for names in os.listdir(os.getcwd()+'\\games'):
            try:
                n = int(names[:-8])
                if n>maxi:
                    maxi=n
            except:
                pass
        pyautogui.screenshot(os.getcwd()+'\\games\\'+str(maxi+1)+'_'+found+'.png', region=(0, 0, 508, 370))
        return True
    return False

start()
track=0
while True:
    executeMap()
    makeMap()
    if checkFinish() == True:
        start()
    if track>=2:
        clickRandom()
        makeMap()

    track+=1
