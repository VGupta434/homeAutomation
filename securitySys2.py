import RPi.GPIO as GPIO
# from gpiozero import MotionSensor
from picamera import PiCamera
from pushbullet import Pushbullet
from time import sleep
import io

pirPin = 7;
relayIn1 = 11;
relayIn2 = 12;
pb = Pushbullet("o.TMxVDlQhdoAFrNWE6HLuLooI2RGMXiD6");  # Enter your pushbullet access token here
# o.TMxVDlQhdoAFrNWE6HLuLooI2RGMXiD6
# o.Bbldwvg7cMRWAWhLM3Y6lPcuvq1CQX0S
camera = PiCamera(resolution=(1920, 1080), framerate=30);

GPIO.setmode(GPIO.BOARD);
GPIO.setup(relayIn1, GPIO.OUT);
GPIO.setup(relayIn2, GPIO.OUT);
# GPIO.setup(17, GPIO.OUT);
GPIO.setup(pirPin, GPIO.IN);
sleep(5);

# pir = MotionSensor(4)
# camera.rotation = 180;

GPIO.output(relayIn1, GPIO.HIGH)

def secSys():
    while True:
        ipState = GPIO.input(pirPin);
        if (ipState == True):  # if motion detected
            print("Motion Detected.....")
            GPIO.output(relayIn1, GPIO.HIGH)  # set relay to high
            sleep(0.2)
            for i in range(2):  # take 2 pictures

                camera.capture('/home/pi/Desktop/image%s.jpg' % i)
                sleep(0.1)
                with io.open('/home/pi/Desktop/image%s.jpg' % i, 'rb') as pic:  # open captured pic as pic
                    file_data = pb.upload_file(pic, 'image%s.jpg' % i)  # upload pic as image%i

                push = pb.push_file(**file_data)  # send file to your phone

        elif (ipState == False):
            print("No intruders")
            pushes = pb.get_pushes()
            if ('body' in pushes[0].keys()):
                message = pushes[0]['body']
                print("You typed : ", message)
                if (message == "Start" or message == "start"):
                    GPIO.output(relayIn1, GPIO.LOW)
            else:
                print("No text message found, probably you sent an image message")
            sleep(0.5)
        sleep(1.5);


