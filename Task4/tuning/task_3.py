'''
*****************************************************************************************
*
*				===============================================
*					Nirikshak Bot (NB) Theme (eYRC 2020-21)
*				===============================================
*
*  This script is to implement Task 3 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3.py
# Functions:		init_setup(rec_client_id), control_logic(center_x,center_y), change_setpoint(new_setpoint)
#					[ Comma separated list of functions in this file ]
# Global variables: client_id, setpoint=[]
#					[ List of global variables defined in this file ]


####################### IMPORT MODULES #########################
## You are not allowed to make any changes in this section.	  ##
## You have to implement this task with the six available	  ##
## modules for this task (numpy,opencv,os,sys,traceback,time) ##
################################################################
import numpy as np
import cv2
import os, sys
import traceback
import time
##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
	import sim

except Exception:
	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	print('\n[WARNING] Make sure to have following files in the directory:')
	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	sys.exit()


# Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
# NOTE: DO NOT change the value of this "client_id" variable here
client_id = -1

# Global list "setpoint" for storing target position of ball on the platform/top plate
# The zeroth element stores the x pixel and 1st element stores the y pixel
# NOTE: DO NOT change the value of this "setpoint" list
setpoint = [275,275]

# Global variable "vision_sensor_handle" to store handle for Vision Sensor
# NOTE: DO NOT change the value of this "vision_sensor_handle" variable here
vision_sensor_handle = 0

# You can add your global variables here
##############################################################
global pex,pey,errxsum,errysum,psx,psy,pogx,pogy,pcx,pcy,ppcx,ppcy,s
pex=0
pey=0
errxsum=0
errysum=0
psx=0
psy=0
pogx=0
pogy=0
pcx=0
pcy=0
ppcx=0
ppcy=0
s=0
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.		##
## Please add proper comments to ensure that your code is	##
## readable and easy to understand.							##
##############################################################
def send_handles():
	global vision_sensor_handle
	return vision_sensor_handle

def constrain(angle):
	global modex,modey
	#if np.abs([axis])>30:

	ang = 60*np.pi/180

	if angle>=ang:
		angle =ang


	elif angle<=-ang:
		angle = -ang


	return angle

def pmap(value,in_min,in_max,out_min,out_max):
	return ((value - in_min) * ((out_max - out_min) / (in_max - in_min))) + out_min



##############################################################
def control_servo(targets):
	global posarray

	#returnarray = [-1,-1,-1,-1]
	_=sim.simxSetJointTargetPosition(client_id,handle_arr[0],targets[0],sim.simx_opmode_oneshot)

	_=sim.simxSetJointTargetPosition(client_id,handle_arr[1],targets[1],sim.simx_opmode_oneshot)

	_=sim.simxSetJointTargetPosition(client_id,handle_arr[2],targets[2],sim.simx_opmode_oneshot)

	_=sim.simxSetJointTargetPosition(client_id,handle_arr[3],targets[3],sim.simx_opmode_oneshot)

def controlx(targets):
	global posarray

	#returnarray = [-1,-1,-1,-1]

	_=sim.simxSetJointTargetPosition(client_id,handle_arr[1],targets[0],sim.simx_opmode_oneshot)


	_=sim.simxSetJointTargetPosition(client_id,handle_arr[3],targets[1],sim.simx_opmode_oneshot)


def controly(targets):
	global posarray

	#returnarray = [-1,-1,-1,-1]
	_=sim.simxSetJointTargetPosition(client_id,handle_arr[0],targets[0],sim.simx_opmode_oneshot)


	_=sim.simxSetJointTargetPosition(client_id,handle_arr[2],targets[1],sim.simx_opmode_oneshot)






def init_setup(rec_client_id):
	"""
	Purpose:
	---
	This function should:

	1. Get all the required handles from the CoppeliaSim scene and store them in global variables.
	2. Initialize the vision sensor in 'simx_opmode_streaming' operation mode (if required).
	   Teams are allowed to choose the appropriate the oeration mode depending on their code and logic.

	Input Arguments:
	---
	`rec_client_id`		:  [ integer ]
		the client_id generated from start connection remote API in Task 2A, should be stored in a global variable

	Returns:
	---
	None

	Example call:
	---
	init_setup()

	"""
	global client_id, vision_sensor_handle, handle_arr,return_code,image_resolution,vision_sensor_image

	# since client_id is defined in task_2a.py file, it needs to be assigned here as well.
	client_id = rec_client_id

	##############	ADD YOUR CODE HERE	##############
	errorcode, vision_sensor_handle = sim.simxGetObjectHandle(client_id,"vision_sensor_1",sim.simx_opmode_oneshot_wait)
	return_code, image_resolution, vision_sensor_image = sim.simxGetVisionSensorImage(client_id,vision_sensor_handle,0,sim.simx_opmode_streaming) #getting vision sensor image in non-blocking function call

	errorcode, rev1 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_1",sim.simx_opmode_blocking)
	errorcode, rev2 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_2",sim.simx_opmode_blocking)
	errorcode, rev3 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_3",sim.simx_opmode_blocking)
	errorcode, rev4 = sim.simxGetObjectHandle(client_id,"revolute_joint_ss_4",sim.simx_opmode_blocking)
	handle_arr = [rev1,rev2,rev3,rev4]


	##################################################


def control_logic(center_x,center_y,set_x,set_y):
	"""
	Purpose:
	---
	This function should implement the control logic to balance the ball at a particular setpoint on the table.

	The orientation of the top table should "ONLY" be controlled by the servo motor as we would expect in a
	practical scenario.

	Hence "ONLY" the shaft of the servo motor or in other words the revolute joint between servo and servo fin
	should have 'motor enabled' and 'control loop enabled option' checked. Refer documentation for further understanding of
	these options.

	This function should use the necessary Legacy Python Remote APIs to control the revolute joints.

	NOTE: In real life, a 180 degree servo motor can rotate between -90 to +90 degrees or -1.57 to 1.57 radians only.
		  Hence the command to be sent to servo motor should be between this range only. When the top plate is parallel to
		  base plate, the revolute joint between servo and servo fin should be at 0 degrees orientation. Refer documentation
		  for further understanding.

	NOTE: Since the simulation is dynamic in nature there should not by any bottlenecks in this code due to which the
		  processing may take a lot of time. As a result 'control_logic' function should be called in every iteration of
		  the while loop. Use global variables instead of reinitialising the varibles used in this function.

	Input Arguments:
	---
	`center_x`	:  [ int ]
		the x centroid of the ball

	`center_y`	:  [ int ]
		the y centroid of the ball

	Returns:
	---
	None

	Example call:
	---
	control_logic(center_x,center_y)

	"""
	global setpoint,pogx,pogy,modex,modey,client_id, handle_arr,trigger,pex,pey, errxsum,errysum,ogx,ogy, psx,psy,pcx,pcy,s
	##############	ADD YOUR CODE HERE	##############


	error_x = set_x - center_x
	ogx=error_x
	error_y = set_y - center_y
	ogy=error_y
	ang = 60*np.pi/180
	error_x = pmap(error_x,-1270,1270,-800,800)
	error_x = pmap(error_x,-1270,1270,-ang,ang)
	error_y = pmap(error_y,-1270,1270,-800,800)
	error_y = pmap(error_y,-1270,1270,-ang,ang)

	Kpx1=2.2 #3
	Kpx2=0 #6.5 #3.23 5x 4-4ex234,9,600.0015
	Kdx1=0.01 #40.25 ,150,347,500, 0.005, 0.004
	Kdx2 = 0.0 #0.045 3(1),0.01(2) - good response ,0.010, 0.015
	Kpy1=2.2
	Kpy2=0 #5.5,60,0.0015
	Kix1=0.0 #5
	Kix2 = 0.0 #0.05
	Kdy1=0.01
	Kdy2 = 0.0 #30 x35,55-4,347
	Kiy1 =0.0
	Kiy2 = 0.0

	errxsum = errxsum+(Kix2*error_x)
	errysum=errysum+(Kiy2*error_y)

	dinputx = center_x-pcx
	dinputy = center_y-pcy
	modex = 'auto'
	modey = 'auto'
	#	print('not yet')
	ptermx = Kpx1*error_x
	ptermy = Kpy1*error_y
	if psx!=None:
		if psx!=set_x:
			print('yup')
			#dinputx =  -(set_x - psx - dinputx)
			ptermx = ptermx - Kpx1*(error_x-pex)
			print(dinputx,'psx')
			print(ptermx,'ptermx')

		if psy!=set_y:
			print('yup2')
			#dinputy = -(set_y - psy - dinputy)
			ptermy = ptermy - Kpy1*(error_y-pey)
			print(dinputy,'psy')
			print(ptermy,'ptermy')

	

	if pogx is None:
		PIDx = Kpx1*error_x*0.1

		PIDy = Kpy1*error_y*0.1
		s=s+1
	if s<5:
		PIDx = Kpx1*error_x*0.1

		PIDy = Kpy1*error_y*0.1
		s=s+1
	elif pogx is not None:
		PIDx = ptermx - Kdx1*(dinputx) +Kix1*(errxsum)
		PIDy = ptermy - Kdy1*(dinputy)+Kiy1*(errysum)



	
	PIDx = constrain(PIDx)
	PIDy=constrain(PIDy)
	

	if np.abs([PIDx])>np.abs([PIDy]):
		targets = [PIDx,-PIDx,-PIDx,PIDx]
		print('x')
	else:
		targets = [PIDy,PIDy,-PIDy,-PIDy]
		print('y')

	
	

	if psx!=None:
		if psx!=set_x:
			print('yup')
			modex = 'auto'


		if psy!=set_y:
			print('yup2')
			modey = 'auto'

	if modex!='manual' and modey!='manual':
		control_servo(targets)
	elif modex!='manual' and modey=='manual':
		targets = [-PIDx1,PIDx2]
		controlx(targets)
	elif modey!='manual' and modex=='manual':
		targets = [PIDy1,-PIDy2]
		controly(targets)
	print(modex,modey)
	print(targets)
	pex=error_x
	pey=error_y
	psx = set_x
	psy = set_y
	pogx = ogx
	pogy = ogy
	pcx = center_x
	pcy = center_y
	
	##################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:	change_setpoint
#		 Inputs:	list of new setpoint-
#						new_setpoint=[x_pixel,y_pixel]
#		Outputs:	None
#		Purpose:	The function updates the value of global "setpoint" list after every 15 seconds of simulation time.
#					This will be ONLY called by executable file.
def change_setpoint(new_setpoint):

	global setpoint
	setpoint=new_setpoint[:]


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:	main
#		 Inputs:	None
#		Outputs:	None
#		Purpose:	This part of the code is only for testing your solution. The function does the following:
#						- imports 'task_1b' file as module
#						- imports 'task_1a_part1' file as module
#						- imports 'task_2a' file as module
#						- calls init_remote_api_server() function in 'task_2a' to connect with CoppeliaSim Remote API server
#						- then calls start_simulation() function in 'task_2a' to start the simulation
#						- then calls init_setup() function to store the required handles in respective global variables and complete initializations if required
#						- then calls get_vision_sensor_image() function in 'task_2a' to capture an image from the Vision Sensor in CoppeliaSim scene
#						- If the return code is 'simx_return_ok':
#									- then calls transform_vision_sensor_image() function in 'task_2a' to transform the captured image
#									  to a format compatible with OpenCV.
#									- then the transformed image is given as input and Perspective Transform is applied
#									  by calling applyPerspectiveTransform function	from 'task_1b'
#									- then the output of warped_img is given to 'scan_image' function from 'task_1a_part1'
#						- then calls control_logic() function to command the servo motors

# NOTE: Write your solution ONLY in the space provided in the above functions. Main function should not be edited.

if __name__ == "__main__":

	# Import 'task_1b.py' file as module
	try:
		import task_1b

	except ImportError:
		print('\n[ERROR] task_1b.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1b.py is present in this current directory.\n')
		sys.exit()

	except Exception as e:
		print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	# Import 'task_1a_part1.py' file as module
	try:
		import task_1a_part1

	except ImportError:
		print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1a_part1.py is present in this current directory.\n')
		sys.exit()

	except Exception as e:
		print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	# Import 'task_2a.py' file as module
	try:
		import task_2a

	except ImportError:
		print('\n[ERROR] task_2a.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_2a.py is present in this current directory.\n')
		sys.exit()

	except Exception as e:
		print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	# Initiate the Remote API connection with CoppeliaSim server
	print('\nConnection to CoppeliaSim Remote API Server initiated.')
	print('Trying to connect to Remote API Server...')

	try:
		client_id = task_2a.init_remote_api_server()

		if (client_id != -1):
			print('\nConnected successfully to Remote API Server in CoppeliaSim!')

			# Starting the Simulation
			try:
				return_code = task_2a.start_simulation()

				if (return_code == sim.simx_return_novalue_flag):
					print('\nSimulation started correctly in CoppeliaSim.')

					# Storing the required handles in respective global variables.
					try:
						init_setup(client_id)
					except Exception:
						print('\n[ERROR] Your init_setup() function throwed an Exception. Kindly debug your code!')
						print('Stop the CoppeliaSim simulation manually if started.\n')
						traceback.print_exc(file=sys.stdout)
						print()
						sys.exit()

				else:
					print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
					print('start_simulation function in task_2a.py is not configured correctly, check the code!')
					print()
					sys.exit()

			except Exception:
				print('\n[ERROR] Your start_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		else:
			print('\n[ERROR] Failed connecting to Remote API server!')
			print('[WARNING] Make sure the CoppeliaSim software is running and')
			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
			print('[ERROR] OR init_remote_api_server function in task_2a.py is not configured correctly, check the code!')
			print()
			sys.exit()

	except Exception:
		print('\n[ERROR] Your init_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually if started.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()

	# Initialising the center_x and center_y variable to the current position of the ball
	center_x = 1063
	center_y = 1063

	init_simulation_time = 0
	curr_simulation_time = 0

	# Storing time when the simulation started in variable init_simulation_time
	return_code_signal,init_simulation_time_string=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_streaming)

	if(return_code_signal==0):
		init_simulation_time=float(init_simulation_time_string)

	# Running the coppeliasim simulation for 15 seconds
	while(curr_simulation_time - init_simulation_time <=15):

		return_code_signal,curr_simulation_time_string=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)

		if(return_code_signal == 0):
			curr_simulation_time=float(curr_simulation_time_string)

		try:
			vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(vision_sensor_handle)

			if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
				# print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')

				# Get the transformed vision sensor image captured in correct format
				try:
					transformed_image = task_2a.transform_vision_sensor_image(vision_sensor_image, image_resolution)
					if (type(transformed_image) is np.ndarray):

						# cv2.imshow('transformed image', transformed_image)
						# cv2.waitKey(0)
						# cv2.destroyAllWindows()

						# Get the resultant warped transformed vision sensor image after applying Perspective Transform
						try:
							warped_img = task_1b.applyPerspectiveTransform(transformed_image)
							if (type(warped_img) is np.ndarray):

								# Get the 'shapes' dictionary by passing the 'warped_img' to scan_image function
								try:
									shapes = task_1a_part1.scan_image(warped_img)

									if (type(shapes) is dict and shapes!={}):
										print('\nShapes detected by Vision Sensor are: ')
										print(shapes)

										# Storing the detected x and y centroid in center_x and center_y variable repectively
										center_x = shapes['Circle'][1]
										center_y = shapes['Circle'][2]

									elif(type(shapes) is not dict):
										print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.')
										print('Stop the CoppeliaSim simulation manually.')
										print()
										sys.exit()

								except Exception:
									print('\n[ERROR] Your scan_image function in task_1a_part1.py throwed an Exception. Kindly debug your code!')
									print('Stop the CoppeliaSim simulation manually.\n')
									traceback.print_exc(file=sys.stdout)
									print()
									sys.exit()

							else:
								print('\n[ERROR] applyPerspectiveTransform function is not configured correctly, check the code.')
								print('Stop the CoppeliaSim simulation manually.')
								print()
								sys.exit()

						except Exception:
							print('\n[ERROR] Your applyPerspectiveTransform function in task_1b.py throwed an Exception. Kindly debug your code!')
							print('Stop the CoppeliaSim simulation manually.\n')
							traceback.print_exc(file=sys.stdout)
							print()
							sys.exit()

					else:
						print('\n[ERROR] transform_vision_sensor_image function in task_2a.py is not configured correctly, check the code.')
						print('Stop the CoppeliaSim simulation manually.')
						print()
						sys.exit()

				except Exception:
					print('\n[ERROR] Your transform_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
					print('Stop the CoppeliaSim simulation manually.\n')
					traceback.print_exc(file=sys.stdout)
					print()
					sys.exit()

			try:
				control_logic(center_x,center_y)

			except:
				print('\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		except Exception:
			print('\n[ERROR] Your get_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

	# Ending the Simulation
	try:
		return_code = task_2a.stop_simulation()

		if (return_code == sim.simx_return_novalue_flag):
			print('\nSimulation stopped correctly.')

			# Stop the Remote API connection with CoppeliaSim server
			try:
				task_2a.exit_remote_api_server()

				if (task_2a.start_simulation() == sim.simx_return_initialize_error_flag):
					print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

				else:
					print('\n[ERROR] Failed disconnecting from Remote API server!')
					print('[ERROR] exit_remote_api_server function in task_2a.py is not configured correctly, check the code!')

			except Exception:
				print('\n[ERROR] Your exit_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		else:
			print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
			print('[ERROR] stop_simulation function in task_2a.py is not configured correctly, check the code!')
			print('Stop the CoppeliaSim simulation manually.')

		print()
		sys.exit()

	except Exception:
		print('\n[ERROR] Your stop_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()
