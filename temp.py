import pyzbar.pyzbar as pyzbar
from gtts import gTTS
import os
import pandas as pd
import cv2
import time
def say(visitor):
    ss2 = gTTS(text=visitor.name.get_values()[0], lang='vi')
    with open('name.mp3', 'wb') as f:
        ss2.write_to_fp(f)
    os.system("mpg321 hello.mp3")
    os.system("mpg321 name.mp3")
    if visitor.gender.get_values()[0] == 'male':
        os.system("mpg321 boy.mp3")
    else:
        os.system("mpg321 girl.mp3")
    os.system("mpg321 welcomes.mp3")

df = pd.read_csv('visitors.csv')
csv_edit_time = os.path.getmtime('visitors.csv')
privious_data = []

if os.path.getmtime('visitors.csv') > csv_edit_time:
    df = pd.read_csv('visitors.csv')
    csv_edit_time = os.path.getmtime('visitors.csv')
frame = cv2.imread('frame.png')
decodedObjects = pyzbar.decode(frame)
if decodedObjects != []:
    for obj in decodedObjects:
        if obj.data != privious_data:
            print('Type : ', obj.type)
            print('Data : ', obj.data, '\n')
            qrid = obj.data.decode('utf8')
            visitor = df.query("qr_id == @qrid")
            print (visitor)
            # ss0 = gTTS(text='hello', lang='en')
            say(visitor)
            privious_data = obj.data