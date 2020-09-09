
# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import lcddriver
import time
from time import sleep 
import RPi.GPIO as GPIO
# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcddriver.lcd()

GPIO.setmode(GPIO.BCM)
redb= 22
red= 19
greenb= 27
green= 13
blue= 6
blueb= 4
white= 17 
GPIO_TRIGGER = 10
GPIO_ECHO = 9

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(white, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(redb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(greenb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(blueb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwmred= GPIO.PWM(red,100)
pwmgreen= GPIO.PWM(green,100)
pwmblue= GPIO.PWM(blue,100)

pwmred.start(0)
pwmgreen.start(0)
pwmblue.start(0)

 
def distance():
  #  set Trigger to HIGH
   GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
   time.sleep(0.0001)
   GPIO.output(GPIO_TRIGGER, False)
   StartTime = time.time()
   StopTime = time.time()
    # save StartTime
   while GPIO.input(GPIO_ECHO) == 0:
      StartTime = time.time()
    # save time of arrival
   while GPIO.input(GPIO_ECHO) == 1:
      StopTime = time.time()
    # time difference between start and arrival
   TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
   distance = (TimeElapsed * 34300) / 2
   return distance

# Main body of code
if __name__ == '__main__':
   R= 0
   G= 0
   B= 0
   a= 0
   b= 0
   c = 0
   reset=True
   sensor=False
   try:
      while True:
	      # Remember that your sentences can only be 16 characters long!
         dist = distance()
         print("Writing to display")
         display.lcd_display_string("Distance = %.1f cm" % dist, 1) # Write line of text to first line of display
         display.lcd_display_string("            ", 2) # Write line of text to second line of display	
         time.sleep(.05)                                    # Give time for the message to be read
         if GPIO.input(redb)==1:
               R=1
               G=0
               B=0
               if a>0 and reset:
                    display.lcd_display_string('Red-- {}'.format(a), 2)
                    a -=8
               if a<100 and not reset:
                    display.lcd_display_string('Red++ {}'.format(a), 2)
                    a +=8                         # Write line of text to second line of display                                                             # Give time for the message to be read
               if sensor:
             	    pwmred.ChangeDutyCycle((dist*1.5,100 )[dist>100] )
               else:
             	    pwmred.ChangeDutyCycle((b,100 )[b>100] )
               time.sleep(.005)                             # Give time for the message to be read 
         if GPIO.input(greenb)==1:
               R=0
               G=1
               B= 0
               if b>0 and reset:
                    display.lcd_display_string('Green-- {}'.format(b), 2)
                    b -=8
               if b<100 and not reset:
                    display.lcd_display_string('Green++ {}'.format(b), 2)
                    b +=8               # Give time for the m>
               if sensor:
              	    pwmgreen.ChangeDutyCycle((dist*1.5,100 )[dist>100] )
               else:
             	    pwmgreen.ChangeDutyCycle((c,100 )[c>100] )
               time.sleep(0.05)                    # Give time for the message >
         if GPIO.input(blueb)==1:
               B=1
               G=0
               R=0
               if c>0 and reset:
                    display.lcd_display_string('Blue-- {}'.format(c), 2)
                    c -=8
               if c<100 and not reset:
                    display.lcd_display_string('Blue++ {}'.format(c), 2)
                    c +=8
               if sensor:
             	    pwmblue.ChangeDutyCycle((dist*1.5,100 )[dist>100] )
               else:
                    pwmblue.ChangeDutyCycle(c)                   # Give time for the m>

               time.sleep(0.05)                    # Give time for the message >
         if GPIO.input(white)==1:
               display.lcd_display_string("Lower color", 2)
                    # Give time for the message 
               reset=not reset

               if GPIO.input(white)==1 and GPIO.input(blue)==1:
                    sensor=not sensor
               time.sleep(1)                    # Give time for the message >
   except KeyboardInterrupt:                                 # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
      print("Cleaning up!")
      display.lcd_clear()
      GPIO.cleanup()
GPIO.cleanup()

