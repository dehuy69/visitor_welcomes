import pyzbar.pyzbar as pyzbar
from gtts import gTTS
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
import pandas as pd

def say(text, lang='en'):
    ss2 = gTTS(text=visitor.name.get_values()[0], lang='vi')
    with open('name.mp3', 'wb') as f:
        ss2.write_to_fp(f)
    os.system("mpg321 hello.mp3")
    if visitor.gender.get_values()[0] == 'male':
        os.system("mpg321 boy.mp3")
    else:
        os.system("mpg321 girl.mp3")
    # ss4 = gTTS(text='Nice to meet you, welcomes to G bee english. Please enjoy yourself', lang='en')

    # with open('welcomes.mp3', 'wb') as f:
    #     ss4.write_to_fp(f)
    os.system("mpg321 welcomes.mp3")


df = pd.read_csv('visitors.csv')
csv_edit_time = os.path.getmtime('visitors.csv')
camera = PiCamera()
camera.resolution = (480, 320)
rawCapture = PiRGBArray(camera)
privious_data = []
camera.start_preview(fullscreen=False, window=(100,20,480,320))
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try:
        if os.path.getmtime('visitors.csv') > csv_edit_time:
            df = pd.read_csv('visitors.csv')
            csv_edit_time = os.path.getmtime('visitors.csv')
        frame = rawCapture.array
        decodedObjects = pyzbar.decode(frame)
        if decodedObjects != []:
            for obj in decodedObjects:
                if obj.data != privious_data:
                    print('Type : ', obj.type)
                    print('Data : ', obj.data, '\n')
                    qr_id = obj.data.decode('utf8')
                    visitor = df.query("qr_id == @qr_id")

                    say('hello')
                    say(visitor.name.get_values()[0], lang='vi')
                    if visitor.gender.get_values()[0] == 'male':
                        say("what's a handsome boy")
                    else:
                        say("what's a beautiful girl")
                    say('Nice to meet you, welcomes to G bee english, please enjoy yourself')
                    privious_data = obj.data
        rawCapture.truncate(0)
    except:
        camera.stop_preview()
        break