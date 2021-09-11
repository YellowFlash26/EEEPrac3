# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
global value = 0
name = None
guess=0
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
LEDVal = 0
btn_submit = 16
btn_increase = 18
buzzer =29 
eeprom = ES2EEPROMUtils.ES2EEPROM()
from time import sleep
from time import time
# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
	pwm.stop()
	Buzzpwm.stop()
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    for x in range(0,3):
	g=raw_data[x][0:1]
	w=raw_data[x][1:]
	print("{} - {} took {} guesses".format(x,w,g))


# Setup Pins
def setup():
    # Setup board mode
	GPIO.setmode(GPIO.BOARD)
	
    # Setup regular GPIO
	for i in LED_value:
                GPIO.setup(i, GPIO.OUT)

	GPIO.setup(LED_accuracy, GPIO.OUT)
	GPIO.setup(btn_increase , GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(btn_submit , GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Setup PWM channels
	global pwm = GPIO.PWM(LED_accuracy,100)
	pwm.start(0)
	global Buzzpwm = GPIO.PWM(buzzer,50)
	Buzzpwm.start(0)

    # Setup debouncing and callbacks
	GPIO.add_event_detect(btn_increase, GPIO.BOTH, callback=btn_increase_pressed, bouncetime=1000)
	GPIO.add_event_detect(btn_submit, GPIO.BOTH, callback=btn_guess_pressed, bouncetime=1000)
    


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    s = eeprom.read_byte(0)
    score_count = s
    scores=[]
    for i in range(0,score_count):
	L1=(i+1)*4
	L2=((i+1)*4)+1
	L3=((i+1)*4)+2
	L4=((i+1)*4)+3
	letter1=chr(read_byte(L1))
	letter2=chr(read_byte(L2))
	letter3=chr(read_byte(L3))
	letter4=read_byte(L4)
	str = letter4+letter1 +letter2 +letter3
	scores.append(str)
    # convert the codes back to ascii
    
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
	 count, scores_eeprom = fetch_scores()
    # include new score
	namestr = guess + name
	scores_eeprom.append(namestr)
    # sort
	scores_eeprom.sort()
    # update total amount of scores
	total=count
	total=total+1
	eeprom.clear((count*4)+4)
	write_byte(0,ord(total))
	
    # write new scores
	for x, word in enumarate(scores_eeprom):
		dataWrite=[]
		val = word[0:1]
		wordVal=word[1:4]
		for letter in wordVal:
			dataWrite.append(ord(letter))
		dataWrite.append(val)
		eeprom.write_block(x+1, dataWrite)
    


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
	 while GPIO.input(btn_increase)==0:
		 pass

	LEDVal=LEDVal+1
	if LEDVal>7:
		LEDVal=0
		for x in LED_value:
			GPIO.output(x, GPIO.LOW)
	elif LEDVal == 1:
		GPIO.output(LED_value[0], GPIO.HIGH)

	elif LEDVal == 2:
                GPIO.output(LED_value[0], GPIO.LOW)
		GPIO.output(LED_value[1], GPIO.HIGH)

	elif LEDVal == 3:
                GPIO.output(LED_value[0], GPIO.HIGH)
                GPIO.output(LED_value[1], GPIO.HIGH)

	elif LEDVal == 4:
                GPIO.output(LED_value[0], GPIO.LOW)
                GPIO.output(LED_value[1], GPIO.LOW)
                GPIO.output(LED_value[2], GPIO.HIGH)

	elif LEDVal == 5:
                GPIO.output(LED_value[0], GPIO.HIGH)
                GPIO.output(LED_value[1], GPIO.LOW)
                GPIO.output(LED_value[2], GPIO.HIGH)

	elif LEDVal == 6:
                GPIO.output(LED_value[0], GPIO.LOW)
                GPIO.output(LED_value[1], GPIO.HIGH)
                GPIO.output(LED_value[2], GPIO.HIGH)

	else LEDVal == 7:
                GPIO.output(LED_value[0], GPIO.HIGH)
                GPIO.output(LED_value[1], GPIO.HIGH)
                GPIO.output(LED_value[2], GPIO.HIGH)
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
	
   


# Guess button
def btn_guess_pressed(channel):
	startT=time()
	while GPIO.input(btn_submit)==0:
		pass
	buttonT = time() - startT
	if buttonT >=2:
		end_of_game = True
	elif LEDVal == value:
		guess=guess+1
		accuracy_leds()
		print("Correct Guess")
		name =input("Input your name (Only 3 Letters)")
		for x in LED_value:
                        GPIO.output(x, GPIO.LOW)
		Buzzpwm.ChangeFrequency(0)
		pwm.ChangeDutyCycle(0)
		save_scores()
		end_of_game = True

	elif LEDVal>value or value>LEDVal:
		guess=guess+1
		accuracy_leds()
		trigger_buzzer()
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
	bright = 0
	if LEDVal < value:
		bright = (LEDval/value)*100
		pwm.ChangeDutyCycle(bright)
	elif LEDVal > value:
		bright =((8-LEDVal)/(8-value))*100
		pwm.ChangeDutyCycle(bright)
	else:
		pwm.ChangeDutyCycle(100)
    

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
	Absval = LEDVal-value
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
	if abs(Absval)>=3:
		Buzzpwm.ChangeFrequency(1)
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
	elif abs(Absval)==2:
		Buzzpwm.ChangeFrequency(2)
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
	else abs(AbsVal)==1:
		Buzzpwm.ChangeFrequency(4)
   


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
