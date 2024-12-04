#Simple macros Bot for auto-sending-attacks in mylands
import pyautogui, sys
import keyboard
import time

#Screen variable
#This screen preset for 1920 - 1080 screen res.
x_pos = 1385, 820
y_pos = 1385, 850
go_button = 1450, 815
attack_button = 955, 560
select_all_units_button = 1400, 760
#your_town_pos =
# 1-9 Y = 200, 10-18 Y = 300, 19-27 Y = 375, 28-36 Y = 460, 37-45 Y = 550, 46-54 Y = 640, 55-63 Y = 730
cells = {
    1:450,
    2:585,
    3:700,
    4:835,
    5:960,
    6:1090,
    7:1210,
    8:1340,
    9:1470
}

class Dungeon:
    """
    Saving X, Y, cell, coming time. Maybe soon i add a dungeon lvl and what army i want to send. Right now i send just all army 
    """
    def __init__(self, X,Y,cell,attack_time):
        self.X = X
        self.Y = Y
        self.cell = cell
        self.attack_time = attack_time

def move_and_click_x_y(x,y):
    pyautogui.moveTo(x,y,duration=0.5)
    pyautogui.click(clicks=1,interval=0.5)


def move_and_click(pos):
    pyautogui.moveTo(pos,duration=0.5)
    pyautogui.click(clicks=1,interval=0.5)

def go_to_map(dungeon):
    x = dungeon.X
    y = dungeon.Y
    move_and_click(x_pos) # move to x cordinat
    pyautogui.click(clicks=2)
    pyautogui.write(str(x), interval=1)
    move_and_click(y_pos) # move to y cordinat
    pyautogui.click(clicks=2)
    pyautogui.write(str(y), interval=1)
    move_and_click(go_button) # move and click on go button

def go_to_cell_and_attack(dungeon):
    # 1-9 Y = 200, 10-18 Y = 300, 19-27 Y = 375, 28-36 Y = 460, 37-45 Y = 550, 46-54 Y = 640, 55-63 Y = 730
    number = dungeon.cell
    Y=0
    if 1 <= number <= 9:
        Y = 200
    elif 10 <= number <= 18:
        Y = 300
    elif 19 <= number <= 27:
        Y = 375
    elif 28 <= number <= 36:
        Y = 460
    elif 37 <= number <= 45:
        Y = 550
    elif 46 <= number <= 54:
        Y = 640
    elif 55 <= number <= 63:
        Y = 730
    else:
        Y = "Out of range" 

    X_cell_pos = number%9
    if X_cell_pos == 0:
        X_cell_pos = cells.get(9)
    else:
        X_cell_pos = cells.get(X_cell_pos)
    # print(X_cell_pos) #check pos
    # print(Y) #check pos
    move_and_click_x_y(X_cell_pos,Y) # go to cell with dungeon
    move_and_click_x_y(X_cell_pos, Y-40) # go to attack button
    move_and_click(select_all_units_button) # select all unit and prepare to attack
    move_and_click(attack_button) # start attack


#Main game


dungeons_list = []

#input dungeon data
while True:
    X = input("Enter X coordinate (or type 'stop' to end): ")
    if X.lower() == 'stop':
        break
    Y = input("Enter Y coordinate: ")
    cell = int(input("Enter cell number: "))
    attack_time = input("Enter attack hh:mm:ss ")


    
    dungeon = Dungeon(int(X), int(Y), cell, attack_time)
    dungeons_list.append(dungeon)
    print("dungeon-list:")
    for dungeon in dungeons_list:
        print (f"dungeon at X Y: {dungeon.X}:{dungeon.Y}, Cell: {dungeon.cell}, attack_time {dungeon.attack_time}" ) 

log_file = open("attack_log.txt", "a", encoding="utf-8")
log_file.write("Dungeon list \n")
for dungeon in dungeons_list:
    log_file.write(f"dungeon at X Y: {dungeon.X}:{dungeon.Y}, Cell: {dungeon.cell}, attack_time {dungeon.attack_time} \n"  ) 
print("Starting attacks in 10 seconds...")
time.sleep(10)
log_file.close()

for dungeon in dungeons_list:
    log_file = open("attack_log.txt", "a", encoding="utf-8")
    timetime = time.time()
    actual_time = time.localtime()
    
    go_to_map(dungeon)
    go_to_cell_and_attack(dungeon)
#log
    log_file.write(f"Attack started at: {time.strftime('%Y-%m-%d %H:%M:%S', actual_time)} on Dungeon (X:{dungeon.X}, Y:{dungeon.Y}, Cell:{dungeon.cell})\n")
    print(f"start attacking at X:Y( {dungeon.X}:{dungeon.Y} Cell:{dungeon.cell} ) on (h:{actual_time.tm_hour}:m:{actual_time.tm_min})")
#end log

#calcute time in seconds
    hours, minutes, seconds = map(int, dungeon.attack_time.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    sleep_time = (timetime + int(total_seconds) * 2 + 100) - timetime

    log_file.write(f"Waiting {sleep_time/60} minutes until next action.\n")
    log_file.close()
    print(f"waiting time to next dungeon in seconds - {sleep_time}, its equal {sleep_time / 60} minutes")

    next_action_timer = time.time() + sleep_time
    while time.time() < next_action_timer:
        current_time= time.time()
        print(f"time left to next action: {(next_action_timer-current_time)/60} minutes")
        time.sleep(60)
    move_and_click_x_y(x=1750,y=500)
    # print(f"Attack sent to dungeon at ({dungeon.X}, {dungeon.Y})")