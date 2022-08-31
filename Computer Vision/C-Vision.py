import cv2 as cv2
from cvzone.HandTrackingModule import HandDetector
from math import *
from numpy import *
from playsound import *
import os

class button():
    def __init__(self , pos_start = () , pos_end = ()):
        self.pos_start = pos_start
        self.pos_end = pos_end
        
    def draw(self , frame):
        cv2.rectangle(frame , self.pos_start , self.pos_end , (100,0,0) , thickness=2)

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8 , maxHands=1)

x = [300 , 245 , 200 , 170 , 145 , 130 , 112 , 103 , 93 , 87 , 80 , 75 , 70 , 67 , 62 , 59 , 57]
y = [20 , 25 , 30 , 35 , 40 , 45 , 50 , 55 , 60 , 65 , 70 , 75 , 80 , 85 , 90 , 95 , 100]
coff = polyfit(x,y,2)

bottom_list = []

for x in range(0,600,75):
        but1 = button((xs := 50+x , ys := 25) , (xe := 100+x , ye := 125))
        bottom_list.append(((xs , ys) , (xe , ye)))

sounds = {
    ((50, 25), (100, 125)) : (1 , 500),
    ((125 , 25),(175 , 125)) : (2 , 700),
    ((200 , 25),(250 , 125)) : (3 , 900),
    ((275 , 25),(325 , 125)) : (4 , 1100),
    ((350 , 25),(400 , 125)) : (5 , 1300),
    ((425 , 25),(475 , 125)) : (6 , 1500),
    ((500 , 25),(550 , 125)) : (7 , 1700),
    ((575 , 25),(625 , 125)) : (8 , 1900)
}

def play_sound(bottom):
    
    global index
    index = sounds[bottom][0]
    freq = sounds[bottom][1]
    
    # playsound(f"{index}.mp3")
    # os.system(f"beep -f {index} -l 1000")
    
    duration = 0.2
    os.system(f'play -n synth {duration} sine {freq-100}:{freq+100}')
    # play -n synth 4 sine 200:400 sine 400:200 delay 0 4 remix 1,2 1,2 repeat 999
    # play -nq -t alsa synth {duration} sine {freq}
    

def bot_tuch(x_8 , y_8):
    for bottom in bottom_list:
        xs = bottom[0][0]
        ys = bottom[0][1]
        xe = bottom[1][0]
        ye = bottom[1][1]
        
        if xs < x_8 < xe and ys < y_8 < ye and distanceCM<50:
            play_sound(bottom)
            return True  
            
    return False

while True:
    re , frame = cap.read()
    
    frame = cv2.resize(frame , (675 , 600))
    
    hands = detector.findHands(frame , draw=False)
    
    for x in range(0,600,75):
        but1 = button((50+x,25),(100+x,125))
        but1.draw(frame)
        
    if hands:
        lmList = hands[0]['lmList']
        
        x1,y1,z1 = lmList[5]
        x2,y2,z2 = lmList[17]
        x_main,y_main,z_main = lmList[8]
        
        distance = int(sqrt(pow((y2-y1) , 2) + pow((x2-x1) , 2)))
        
        A,B,C = coff
        
        global distanceCM
        distanceCM = pow((A*distance) , 2) + B*distance + C
        
        cv2.putText(frame , f"{int(distanceCM)}" , (650 , 575) , cv2.FONT_HERSHEY_SIMPLEX , 0.5 , (100,0,0) , 1 , cv2.LINE_AA)
        
        if bot_tuch(x_main , y_main):
            if distanceCM < 50:
                print(f"bottom {index} pressed!. ({int(distanceCM)})")
        
        
    cv2.imshow("frame" , frame)
    
    if cv2.waitKey(1) == ord('q'):
        break