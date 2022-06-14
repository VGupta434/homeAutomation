import RPi.GPIO as GPIO;
from gpiozero import MotionSensor;
from time import sleep;

pirPin=7;
relayIn1=11;

def setup():
	GPIO.setmode(GPIO.BOARD);
	GPIO.setwarnings(False);
	GPIO.setup(pirPin,GPIO.IN);
	GPIO.setup(relayIn1,GPIO.OUT);
	GPIO.output(relayIn1,GPIO.HIGH);
def work():
	while True:
		GPIO.output(relayIn1,GPIO.HIGH);
		ipState=GPIO.input(pirPin);
		if(ipState == True):
			print("Motion Detected.....");
			GPIO.output(relayIn1,GPIO.LOW);
			sleep(2);
			GPIO.output(relayIn1,GPIO.HIGH);
			sleep(1);
		elif(ipState == False):
			print("No intruders");
			sleep(0.5);
			
def close():
	GPIO.output(relayIn1,GPIO.LOW);
	GPIO.cleanup();
	

setup();

try:
	work();
except KeyboardInterrupt:
	close();
