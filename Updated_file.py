import time
import datetime

mice_dis = []
daily_times = {}

def generate_data():
	"""
		Logic to return final distance
	"""
	import RP.GPIO as GPIO
	import time

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(false)

	pulse = 0
	distance = 0
	rpm = 0
	speed = 0
	r = 0.12
	wheel_c = 2*pi*r
	multiplier = 0
	hall = 18
	elapse = 0


	GPIO.setup(hall,GPIO.IN,pull_up_down=GPIO.PUD.UP)

	def get_rpm():
		return rpm
	def get_distance():
		return speed
	def get_distance():
		return distance
	def get_elapse():
		return elapse
	def get_multiplier():
		return multiplier
		
		
	def handle_falling_edge():
		start = time.time()
		distance += wheel_c

	def handle_rising_edge():
		pass 
		

	def get_pulse(number):
		start = time.time()
		distance += wheel_c
		
		

	try:
		print('Inializing speedometer')
		time.sleep(1)
		
		start = time.time()	  
		GPIO.add_event_detect(hall,GPIO.FALLING,callback = get_pulse,bouncetime=20)
		
		# For now just set a random val - literally no meaning
		speed = 3
		  
		while True:
			elapse = time.time() - start  
			multiplier = 3600/elapse
			rpm = 1/elapse*60
			speed = (wheel_c*multiplier)/(1000)
			print('rpm{0:.2f} speed{1:.2f} distance{2} elapse{3:.4f} multiplier{4:.2f}'.format(rpm,speed,distance,elapse,multiplier))
				time.sleep(0.1)

			if speed < 1:
	        		def get_distance():
					return distance
	        		print(str.format('{0:.2f}', distance), "Meters")
	        		print("MICE IS NO LONGER RUNNING.")
				break
				
	except KeyboardInterrupt:
		print('End of program')
		GPIO.cleanup()	

def write_to_file(data=None, final_recording=False): 
	with open("/media/pi/VOLE_DATA/Distance.txt", 'a') as file:
		if not final_recording:
			for instance in data:
				file.write("Date: %s, Distance ran in session: %s, Total distance so far: %s" % (data[0], data[1], data[2]))
		else:
				file.write("Final distance for %s is: %s" % (data[0], data[1]))

def main():
	already_recorded = False
	running_sum = 0
	daily_mice_data = [] # Tuple : Time, current distance, total distance for the current day**	

	# Want to be able to read indefinitely
	while True:


		# TODO: Figure out how to trigger "rfid"


		curr_distance = generate_data()
		if curr_distance > 0: 
			mice_dis.append(total_distance)

			# Gather current time and final running sum
			curr_time = datatime.datetime.utcnow()

			# Time, Current distance, running sum

			running_sum += curr_distance
			curr_instance = (curr_time, curr_distance, running_sum)
			daily_mice_data.append(curr_instance)

			write_to_file(curr_instance)



		# Ensure that we are only writing to file once # Reset value once we hit an hour mark that is not 12am
		if curr_time.hour > 0:
			already_recorded = False

		if curr_time.hour == 00 and not already_recorded:
			already_recorded = True

			data = (curr_time, running_sum)
			write_to_file(data, True)
			running_sum = 0


if __name__ == '__main__':
	main()