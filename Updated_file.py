import time
import datetime

mice_dis = []
daily_times = {}

distance = 0
start = 0


# Logic to read rfid
def handle_tag():
	return None

# Logic to determine if rfid is triggered
def triggered_rfid():
	return None

def generate_data():
	import RPi.GPIO as GPIO
	import time
	import math

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(True)

	pulse = 0
	rpm = 0
	speed = 0
	d = 0.12
	wheel_c = math.pi*d
	multiplier = 0
	hall = 18
	elapse = 0
	curr_distance = 0

	GPIO.setup(hall,GPIO.IN,pull_up_down = GPIO.PUD_UP)

	def get_pulse(number):
		global start
		global distance
		start = time.time()
		print("Before adding the wheel current distance: %s " % distance)
		distance += wheel_c
		
	try:
		global distance
		distance = 0
		print('Inializing speedometer')
		time.sleep(1)
		global start 
		start = time.time()	  
		GPIO.add_event_detect(hall,GPIO.FALLING,callback = get_pulse,bouncetime=20)
		
		# For now just set a random val - literally no meaning
		speed = 5
		  
		while True:
			elapse = time.time() - start  
			multiplier = 3600/elapse
			rpm = 1/elapse*60
			speed = (wheel_c*multiplier)/(1000)
			

			print('rpm{0:.2f} speed{1:.2f} distance{2} elapse{3:.4f} multiplier{4:.2f}'.format(rpm,speed,distance,elapse,multiplier))
			time.sleep(0.1)

			if speed < 1:
				print(str.format('{0:.2f}', distance), "Meters")
				print("MICE IS NO LONGER RUNNING.")
				GPIO.cleanup()
				return distance
			
	except KeyboardInterrupt:
		print('End of program')
		GPIO.cleanup()
		sys.exit()


def write_to_file(data=None, final_recording=False, curr_time=None): 
	file_name = "/media/pi/VOLE_DATA/Distance/Distances_%s_%s_%s.txt" % (curr_time.month, curr_time.day, curr_time.year)
	with open(file_name, 'a') as file:
		if not final_recording:
			file.write("Date: %s, Distance ran in session: %s, Total distance so far: %s \n" % (data[0], data[1], data[2]))
		else:
			file.write("Final distance for %s is: %s \n" % (data[0], data[1]))

def main():
	already_recorded = False
	running_sum = 0
	daily_mice_data = [] # Tuple : Time, current distance, total distance for the current day**	
	global distance

	# Want to be able to read indefinitely
	while True:
		# TODO: Figure out how to trigger "rfid"
		curr_distance = generate_data()
		# Gather current time and final running sum
		curr_time = datetime.datetime.now()

		
		if distance > 0:	
			print("Found a distance")
			curr_distance = distance
			mice_dis.append(curr_distance)


			# Time, Current distance, running sum

			running_sum += curr_distance
			curr_data = (curr_time, curr_distance, running_sum)
			daily_mice_data.append(curr_data)

			write_to_file(curr_data, False, curr_time)
			# Reset the data
			
			print("distance before reset: %s " % distance)
			distance = 0
			curr_distance = 0 
			print("distance has been reset: %s " % distance)


		# Ensure that we are only writing to file once # Reset value once we hit an hour mark that is not 12am
		if curr_time.hour > 0:
			already_recorded = False

		if curr_time.hour == 00 and not already_recorded:
			already_recorded = True

			data = (curr_time, running_sum)
			write_to_file(data, True, curr_time)
			running_sum = 0


if __name__ == '__main__':
	main()
