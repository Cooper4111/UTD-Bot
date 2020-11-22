import sys
import os
import win32api, win32con
import time
import keyboard
import numpy as np

##############################################################################
################################### DATA #####################################
##############################################################################

# Tower seq:        0       1       2       3       4       5
# Current setup     Fire    Frost   Cannon  Gun     Nrg     Poison
towerNames = {'Fire':0, 'Frost':1, 'Cannon':2, 'Gun':3, 'Nrg':4, 'Poison':5,
              'fire':0, 'frost':1, 'cannon':2, 'gun':3, 'nrg':4, 'poison':5}

TowerSetup = {  'General': [(0,0,'Fire',    [1,2,2,2,0,0]),     (1,0,'Gun',     [2,2,2,2,0,0]),     (2,0,'Nrg',[1,1,1,1,0,0]),
                            (0,1,'Frost',   [1,2,2,2,0,0]),     (1,1,'Nrg',     [1,1,1,1,0,0]),     (2,1,'Nrg',[1,1,1,1,0,0]),
                            (0,2,'Poison',  [1,2,2,2,0,0])],
                'Snake':   [(0,0,'Gun',     [2,2,2,2,0,0]),     (1,0,'Frost',   [1,2,2,2,0,0]),
                            (0,1,'Fire',    [1,2,2,2,0,0]),     (1,1,'Gun',     [2,2,2,2,0,0]),     (2,1,'Nrg',[1,1,1,1,0,0]),
                                                                (1,2,'Cannon',  [1,1,1,2,0,0]),     (2,2,'Nrg',[1,1,1,1,0,0]),
                                                                (1,3,'Poison',  [1,2,2,2,0,0])],
                'River':   [(0,0,'Nrg',     [1,1,1,1,0,0]),
                            (0,1,'Cannon',  [1,1,1,2,0,0]),
                            (0,2,'Frost',   [1,2,2,2,0,0]),     (1,0,'Poison',  [1,2,2,2,0,0]),
                            (0,3,'Fire',    [1,2,2,2,0,0]),     (1,1,'Nrg',     [1,1,1,1,0,0]),
                            (0,4,'Gun',     [2,2,2,2,0,0]),
                            (0,5,'Gun',     [2,2,2,2,0,0]),
                            (0,6,'Nrg',     [2,2,1,2,0,0])]}

towStdTree = {'Fire':[1,2,2,2,0,0], 'Frost':[1,2,2,2,0,0], 'Cannon':[1,1,1,2,0,0], 'Gun':[2,2,2,2,0,0], 'Nrg':[2,2,1,2,0,0], 'Poison':[1,2,2,2,0,0],
              'fire':[1,2,2,2,0,0], 'frost':[1,2,2,2,0,0], 'cannon':[1,1,1,2,0,0], 'gun':[2,2,2,2,0,0], 'nrg':[2,2,1,2,0,0], 'poison':[1,2,2,2,0,0]}

################################################
################# COORDINATES ##################
################################################
'''
TODO:
- Setup savefiles
- GUI for muouse input of coordinates
'''


CRD = {    
    'Gspots' : [[np.array([386+i,256+j]) for i in range(0,4*136,136)] for j in range(0,3*160,160)],
    'battleSpeed' : np.array([1330, 85]),
    'start' : np.array([680,75]),

    'upgr_op1' : np.array([600,400]),
    'upgr_op1' : np.array([800,400]),
    'upgr_ok' : np.array([625,525]),
    'upgr_ChckBx' : np.array([500,490]),
    
    'tw_4_off' : np.array([-100, -55]),
    'tw_5_off' : np.array([-86, 0]),
    'tw_6_off' : np.array([-60, 55]),

    'tw_1_off' : np.array([100, -55]),
    'tw_2_off' : np.array([86, 0]),
    'tw_3_off' : np.array([60, 55]),

    'upgr' : np.array([-40,60]),
    'sell' : np.array([40,60]),

    'mrn_crd' : np.array([1240, 715])
    }

########    MENU    ########

Chlng       = np.array([67, 430])
Boss        = np.array([866, 400])
LevelChoose = np.array([1149, 241])
LevelScrool = np.array([1155, 375])
LevelClick  = np.array([1100, 364])
Play        = np.array([1050, 700])
CloseScore  = np.array([1072, 91])
tabcross    = np.array([222, 15])
wincross    = np.array([1339, 8])
########    SPOTS   ########
'''
OBSOLETE

Gspots = [[np.array([386+i,256+j]) for j in range(0,3*136,136)] for i in range(0,4*160,160)]   # Cols - x; Rows - y;

Sspots = [[np.array([430,290]),np.array([430,365])],                                           # Cols - x; Rows - y;
          [np.array([600,290]),np.array([600,365]),np.array([600,440]),np.array([600,515])],
          [np.array([770,215]),np.array([770,290]),np.array([770,365]),np.array([770,440])]]

Rspots = [[np.array([472,108+i]) for i in range(0,7*72,72)],                                    # Cols - x; Rows - y;
          [np.array([632,249]), np.array([632,391])]]
'''
########    GAME    ########

battleSpeed = np.array([1330, 85])
battleStart = np.array([680,75])
upgr        = np.array([-40,60])
sell        = np.array([40,60])
upgr_op1    = np.array([600,400])
upgr_op2    = np.array([800,400])
#upgr_ok    = np.array([625,525])
upgr_ok     = np.array([650,525])
upgr_ChckBx = np.array([500,490])
nextwave    = np.array([1200,20])
win_ok      = np.array([683,626])

#np.array([256,386]) + np.array([100,-55]) = 356,331
#np.array([256,386]) + np.array([-55,100]) = 201,486
tw_off      = [np.array([100, -55]),np.array([86, 0]),np.array([60, 55]),np.array([-100, -55]),np.array([-86, 0]),np.array([-60, 55])]

mrn_crd     = np.array([1240, 715])

##############################################################################
################################### CODE #####################################
##############################################################################

act_delay   = .5
click_delay = .05
upgr_delay  = .5
running     = True
started     = False
proceeded   = False

############################### ATOMIC FUNCS #################################

########    KEYS    ########

def stop():
    global running
    running = False
    print('Attempt to stop the app')
keyboard.add_hotkey('Space', stop)

def start():
    global started
    started = True
    print('So it begins...')
keyboard.add_hotkey('Enter', start)

def proceed():
    global proceeded
    proceeded = True
    print('No time to waste!')
keyboard.add_hotkey('Shift', proceed)

def speedUp():
    global act_delay
    act_delay = act_delay / 2
    print('FASTA!', ' delay is ', act_delay)
keyboard.add_hotkey('Up', speedUp)

def speedDown():
    global act_delay
    act_delay = act_delay * 2
    print('slowah...', ' delay is ', act_delay)
keyboard.add_hotkey('Down', speedDown)

########    FUNC    ########

def leftClick(coords):
    x = coords[0]
    y = coords[1]
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y)
    time.sleep(click_delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y)
    time.sleep(act_delay)

def upgrOpt(option):
    if option == 1:
        leftClick(upgr_op1)
        leftClick(upgr_ok)
    elif option == 2:
        leftClick(upgr_op2)
        leftClick(upgr_ok)
    else:
        pass
    
def buildTow(spot, tower = 'frost', delay = True):
    try:
        t_offset = tw_off[tower]
    except:    
        t_offset = tw_off[towerNames[tower]]
    print('build_spot')
    leftClick(spot)
    print('build_offset')
    leftClick(spot+t_offset)
    if delay:
        time.sleep(upgr_delay)
      
def upgrTow(spot, times = 6, options = [1,2,2,2,0,0], choice = True, delay = True):
    for i in range(0, times):
        if not running: return
        leftClick(spot)
        leftClick(spot+upgr)
        if i > 3:
            choice = False
        if choice:
            print('upgrading spot ', spot, ' choise option is ', options[i])
            upgrOpt(options[i])
        if delay:
            time.sleep(upgr_delay)
            
def sellTow(spot, delay = True):
    leftClick(spot)
    leftClick(spot+sell)
    if delay:
        time.sleep(upgr_delay)

def getSpots(mapName):
    if mapName == 'General':
        return   [[np.array([386+i,256+j]) for j in range(0,3*136,136)] for i in range(0,4*160,160)]   # Cols - x; Rows - y;
    elif mapName == 'Snake':
        return   [[np.array([430,290]),np.array([430,365])],                                           # Cols - x; Rows - y;
                  [np.array([600,290]),np.array([600,365]),np.array([600,440]),np.array([600,515])],
                  [np.array([770,215]),np.array([770,290]),np.array([770,365]),np.array([770,440])]]
    elif mapName == 'River':
        return   [[np.array([472,108+i]) for i in range(0,7*71,71)],                                    # Cols - x; Rows - y;
                  [np.array([632,249]), np.array([632,391])]]       
    
############################### COMPLEX FUNCS ################################
    
### BUILDS AND SELLS TOWERS    
    
def goldGen(spotsArr, grade = 1):
    spot = spotsArr[0][0] # Current coordinates
    buildTow(spot, tower = 'Frost')
    upgrTow(spot, options = towStdTree['Frost'])
    sellTow(spot)
    buildTow(spot, tower = 'Cannon')
    upgrTow(spot, options = towStdTree['Cannon'])
    sellTow(spot)    
    buildTow(spot, tower = 'Nrg')
    upgrTow(spot, options = towStdTree['Nrg'])
    sellTow(spot)    
    for i in range(0,grade):
        if not running: return
        buildTow(spot, tower = 'Nrg')
        upgrTow(spot, options = towStdTree['Nrg'])
        sellTow(spot)

### BUILDS AND UPGRADES TOWERS ACCORDING TO SETUP
    
def inhabit(spots, mapName):
    setup = TowerSetup[mapName]
    print('mapName is: ', mapName)
    for twr in setup:
        if not running: return
        print('spot is: ', spots[twr[0]][twr[1]])
        buildTow(spots[twr[0]][twr[1]], twr[2], delay = 0)
    for twr in setup:
        if not running: return
        upgrTow(spots[twr[0]][twr[1]], options = twr[3])

### TESTING TOOL

def clickSpots(spotsArr):
    if not running: return
    for row in spotsArr:
        for elem in row:
            leftClick(elem)
    print('click test succesful')

### INITIATES BATTLE FROM THE MAIN SCREEN OF GAME

def initiateBattle():
    global act_delay
    global click_delay
    foobar1 = act_delay
    foobar2 = click_delay
    act_delay   = 1
    leftClick(Chlng)
    leftClick(Boss)
    leftClick(LevelChoose)
    click_delay = 1
    leftClick(LevelScrool)
    click_delay = foobar2
    leftClick(LevelClick)
    leftClick(Play)
    act_delay = foobar1
    press_f_to_win(t = 35, nwave = False)

### SOULD ANALYZE SCREEN FOR WIN MESSAGE BOX, THEN RETURN IF GOT

def press_f_to_win(t = 90, nwave = True):
    i = t
    global proceeded
    while i > 0:
        if not running: return
        if proceeded:
            proceeded = False
            return
        if nwave:
            leftClick(nextwave)
        time.sleep(1)
        i = i-1
        print(i)
    #   to catch the Blue Screen of Victory
    #   should be iter analyses of blue balance on screen
    #   if BSoV: return else: time.sleep(6)

def botExit(exitPoint = 'window', reboot = False, shutdown = False):
    keyboard.send('Esc')
    time.sleep(5)
    if exitPoint == 'window':
        leftClick(wincross)
        time.sleep(5)
    elif exitPoint == 'tab':
        pass
    if reboot:
        pass
    if shutdown:
        leftClick(27,747)
        time.sleep(1)
        leftClick(300,700)

### BOT ENGINE

def engine(mapName, iters = 4):
    spots = getSpots(mapName)
    for i in range(0,iters):
        if not running: return
        initiateBattle()
        leftClick(battleSpeed)
        goldGen(spots)
        inhabit(spots, mapName)
        leftClick(battleStart)
        press_f_to_win()
        leftClick(win_ok)
        time.sleep(20)
    botExit()

### INITIALIZES BOT TO BE READY TO START ON KEYPRESS

def main(args = ['General', 4]):
    if len(args) == 2:
        if args[1] == '-c':
            pass
        else:
            mapName = args[1]
    if len(args) == 3:
        mapName = args[1]
        iters = int(args[2])
    global running
    while running:
        if started:
            engine(mapName, iters)
            running = False
        time.sleep(0.1)
        
main(sys.argv)

print('Done.')

'''
##############################################################################
############################## DEVELOPER NOTES ###############################
##############################################################################

# TODO

> Parse sys.argv for global flags: 0) Shutdown 1) Reboot 3) Open chest
> Catching chechbox on tower upgrade
> Parallelized upgrade of towers (delay = 0)
> Exit func

CV:
> BSoV (Blue Screen of Victory): take screenshot, analyze central area for ammount of blue. Return True or False
> Recognize chests, open the one with most value

'''